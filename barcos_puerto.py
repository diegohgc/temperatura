# -*- coding: utf-8 -*-
"""
Conector a Aisstream.io para contar barcos atracados (status=5, "Moored")
y fondeados/esperando (status=1, "At anchor") en los puertos de España.

Se ejecuta periodicamente via GitHub Actions (ver
.github/workflows/barcos.yml), genera barcos.json en la raiz del repo, y
el propio workflow hace commit+push si el contenido cambio -- GitHub
Pages lo sirve automaticamente en la misma URL de siempre.

La API key se lee de la variable de entorno AISSTREAM_API_KEY (secreto
de GitHub Actions), nunca hardcodeada aqui -- Aisstream.io exige
explicitamente que esta key solo se use desde el lado del servidor.
"""
import asyncio
import json
import math
import os
import time

import websockets

API_KEY = os.environ["AISSTREAM_API_KEY"]

# Cajas geograficas que cubren la costa espanola (peninsula+Baleares, y
# Canarias aparte por estar lejos).
BOUNDING_BOXES = [
    [[35.0, -10.5], [44.0, 4.5]],    # peninsula + Baleares
    [[27.3, -18.5], [29.6, -13.0]],  # Canarias
]

LISTEN_SECONDS = 210  # ~3.5 min: los barcos fondeados/amarrados transmiten
                       # AIS con poca frecuencia, hace falta escuchar un
                       # rato para no perdérselos.

PUERTOS_PATH = "puertos_espana.json"
OUT_PATH = "barcos.json"

RADIO_FONDEO_NM = 4.0
RADIO_ATRAQUE_NM = 0.6


def haversine_nm(lat1, lon1, lat2, lon2):
    R_km = 6371.0
    r = math.pi / 180
    dlat = (lat2 - lat1) * r
    dlon = (lon2 - lon1) * r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1 * r) * math.cos(lat2 * r) * math.sin(dlon / 2) ** 2
    km = R_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return km / 1.852


async def main():
    with open(PUERTOS_PATH, encoding="utf-8") as f:
        puertos = json.load(f)
    print(f"Puertos cargados: {len(puertos)}")

    vistos = {}

    async with websockets.connect("wss://stream.aisstream.io/v0/stream", max_size=None) as ws:
        sub = {
            "APIKey": API_KEY,
            "BoundingBoxes": BOUNDING_BOXES,
            "FilterMessageTypes": ["PositionReport"],
        }
        await ws.send(json.dumps(sub))
        print("Suscripcion enviada, escuchando", LISTEN_SECONDS, "segundos...")

        t0 = time.time()
        n_msgs = 0
        try:
            while time.time() - t0 < LISTEN_SECONDS:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=5)
                except asyncio.TimeoutError:
                    continue
                n_msgs += 1
                try:
                    data = json.loads(raw)
                except Exception:
                    continue
                if data.get("MessageType") != "PositionReport":
                    continue
                msg = data.get("Message", {}).get("PositionReport", {})
                meta = data.get("MetaData", {})
                mmsi = meta.get("MMSI") or msg.get("UserID")
                lat = msg.get("Latitude")
                lon = msg.get("Longitude")
                status = msg.get("NavigationalStatus")
                nombre = (meta.get("ShipName") or "").strip()
                if mmsi is None or lat is None or lon is None:
                    continue
                vistos[mmsi] = {"lat": lat, "lon": lon, "status": status, "nombre": nombre}
                if n_msgs % 100 == 0:
                    print(f"  ...{n_msgs} mensajes, {len(vistos)} barcos distintos")
        except Exception as e:
            print("Error durante la escucha:", e)

    print(f"Total mensajes: {n_msgs}, barcos distintos vistos: {len(vistos)}")

    resultado = [
        {"nombre": p["nombre"], "lat": p["lat"], "lon": p["lon"], "atracados": 0, "fondeados": 0, "barcos": []}
        for p in puertos
    ]

    for mmsi, v in vistos.items():
        mejor_idx, mejor_dist = None, None
        for i, p in enumerate(puertos):
            d = haversine_nm(v["lat"], v["lon"], p["lat"], p["lon"])
            if mejor_dist is None or d < mejor_dist:
                mejor_dist, mejor_idx = d, i
        if mejor_idx is None:
            continue
        r = resultado[mejor_idx]
        if v["status"] == 5 and mejor_dist <= RADIO_ATRAQUE_NM:
            r["atracados"] += 1
            r["barcos"].append({"mmsi": mmsi, "nombre": v["nombre"], "lat": v["lat"], "lon": v["lon"], "estado": "atracado"})
        elif v["status"] == 1 and mejor_dist <= RADIO_FONDEO_NM:
            r["fondeados"] += 1
            r["barcos"].append({"mmsi": mmsi, "nombre": v["nombre"], "lat": v["lat"], "lon": v["lon"], "estado": "fondeado"})

    resultado = [r for r in resultado if r["atracados"] > 0 or r["fondeados"] > 0]
    salida = {"puertos": resultado, "actualizado": int(time.time())}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print(f"Guardado {OUT_PATH} con {len(resultado)} puertos con actividad.")


if __name__ == "__main__":
    asyncio.run(main())
