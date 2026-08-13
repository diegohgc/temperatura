import os
import requests
from atproto import Client

# Bluesky credentials from GitHub Secrets
BSKY_HANDLE = os.getenv("BSKY_HANDLE")  # quicktemp.bsky.social
BSKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

# Continents & Reference Cities (Latitude, Longitude)
CONTINENTS = {
    "🇪🇺 Europe": [
        {"nombre": "Seville", "lat": 37.38, "lon": -5.98},
        {"nombre": "Madrid", "lat": 40.41, "lon": -3.70},
        {"nombre": "Barcelona", "lat": 41.38, "lon": 2.17},
        {"nombre": "Paris", "lat": 48.85, "lon": 2.35},
        {"nombre": "London", "lat": 51.50, "lon": -0.12},
        {"nombre": "Berlin", "lat": 52.52, "lon": 13.40},
        {"nombre": "Rome", "lat": 41.90, "lon": 12.49},
        {"nombre": "Athens", "lat": 37.98, "lon": 23.72},
        {"nombre": "Lisbon", "lat": 38.72, "lon": -9.14},
        {"nombre": "Vienna", "lat": 48.20, "lon": 16.37},
        {"nombre": "Amsterdam", "lat": 52.36, "lon": 4.90},
        {"nombre": "Brussels", "lat": 50.85, "lon": 4.35},
        {"nombre": "Prague", "lat": 50.07, "lon": 14.43},
        {"nombre": "Warsaw", "lat": 52.22, "lon": 21.01},
        {"nombre": "Dublin", "lat": 53.34, "lon": -6.26},
        {"nombre": "Copenhagen", "lat": 55.67, "lon": 12.56},
        {"nombre": "Stockholm", "lat": 59.32, "lon": 18.06},
        {"nombre": "Oslo", "lat": 59.91, "lon": 10.75},
        {"nombre": "Helsinki", "lat": 60.16, "lon": 24.93},
        {"nombre": "Reykjavik", "lat": 64.14, "lon": -21.94},
        {"nombre": "Milan", "lat": 45.46, "lon": 9.19},
        {"nombre": "Munich", "lat": 48.13, "lon": 11.58},
        {"nombre": "Zurich", "lat": 47.37, "lon": 8.54},
    ],
    "🌎 Americas": [
        {"nombre": "Phoenix", "lat": 33.44, "lon": -112.07},
        {"nombre": "Miami", "lat": 25.76, "lon": -80.19},
        {"nombre": "New York", "lat": 40.71, "lon": -74.00},
        {"nombre": "Los Angeles", "lat": 34.05, "lon": -118.24},
        {"nombre": "Las Vegas", "lat": 36.16, "lon": -115.13},
        {"nombre": "Houston", "lat": 29.76, "lon": -95.36},
        {"nombre": "Chicago", "lat": 41.87, "lon": -87.62},
        {"nombre": "Seattle", "lat": 47.60, "lon": -122.33},
        {"nombre": "Denver", "lat": 39.73, "lon": -104.99},
        {"nombre": "Montreal", "lat": 45.50, "lon": -73.56},
        {"nombre": "Toronto", "lat": 43.65, "lon": -79.38},
        {"nombre": "Vancouver", "lat": 49.28, "lon": -123.12},
        {"nombre": "Anchorage", "lat": 61.21, "lon": -149.90},
        {"nombre": "Mexico City", "lat": 19.43, "lon": -99.13},
        {"nombre": "Cancun", "lat": 21.16, "lon": -86.85},
        {"nombre": "Bogota", "lat": 4.71, "lon": -74.07},
        {"nombre": "Lima", "lat": -12.04, "lon": -77.04},
        {"nombre": "Santiago", "lat": -33.45, "lon": -70.66},
        {"nombre": "Buenos Aires", "lat": -34.60, "lon": -58.38},
        {"nombre": "Ushuaia", "lat": -54.80, "lon": -68.30},
        {"nombre": "Rio de Janeiro", "lat": -22.90, "lon": -43.17},
        {"nombre": "Sao Paulo", "lat": -23.55, "lon": -46.63},
    ],
    "🌍 Africa": [
        {"nombre": "Cairo", "lat": 30.04, "lon": 31.23},
        {"nombre": "Marrakesh", "lat": 31.62, "lon": -7.98},
        {"nombre": "Casablanca", "lat": 33.57, "lon": -7.58},
        {"nombre": "Tunis", "lat": 36.80, "lon": 10.18},
        {"nombre": "Algiers", "lat": 36.75, "lon": 3.05},
        {"nombre": "Khartoum", "lat": 15.50, "lon": 32.55},
        {"nombre": "Djibouti", "lat": 11.82, "lon": 42.59},
        {"nombre": "Nairobi", "lat": -1.29, "lon": 36.82},
        {"nombre": "Lagos", "lat": 6.52, "lon": 3.37},
        {"nombre": "Johannesburg", "lat": -26.20, "lon": 28.04},
        {"nombre": "Cape Town", "lat": -33.92, "lon": 18.42},
    ],
    "🌏 Asia": [
        {"nombre": "Dubai", "lat": 25.20, "lon": 55.27},
        {"nombre": "Riyadh", "lat": 24.71, "lon": 46.67},
        {"nombre": "Kuwait City", "lat": 29.37, "lon": 47.97},
        {"nombre": "Doha", "lat": 25.28, "lon": 51.53},
        {"nombre": "New Delhi", "lat": 28.61, "lon": 77.20},
        {"nombre": "Bangkok", "lat": 13.75, "lon": 100.50},
        {"nombre": "Singapore", "lat": 1.35, "lon": 103.81},
        {"nombre": "Jakarta", "lat": -6.20, "lon": 106.84},
        {"nombre": "Beijing", "lat": 39.90, "lon": 116.40},
        {"nombre": "Tokyo", "lat": 35.67, "lon": 139.65},
        {"nombre": "Seoul", "lat": 37.56, "lon": 126.97},
        {"nombre": "Astana", "lat": 51.16, "lon": 71.47},
        {"nombre": "Yakutsk", "lat": 62.03, "lon": 129.73},
    ],
    "🇦🇺 Oceania": [
        {"nombre": "Darwin", "lat": -12.46, "lon": 130.84},
        {"nombre": "Alice Springs", "lat": -23.69, "lon": 133.88},
        {"nombre": "Sydney", "lat": -33.86, "lon": 151.20},
        {"nombre": "Melbourne", "lat": -37.81, "lon": 144.96},
        {"nombre": "Perth", "lat": -31.95, "lon": 115.86},
        {"nombre": "Auckland", "lat": -36.84, "lon": 174.76},
        {"nombre": "Wellington", "lat": -41.28, "lon": 174.77},
    ]
}

def consultar_continente(ciudades):
    lats = ",".join([str(c["lat"]) for c in ciudades])
    lons = ",".join([str(c["lon"]) for c in ciudades])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&daily=temperature_2m_max&timezone=auto"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        results = data if isinstance(data, list) else [data]
        resultados = []
        for idx, res in enumerate(results):
            temp = res["daily"]["temperature_2m_max"][0]
            if temp is not None:
                resultados.append((ciudades[idx]["nombre"], round(temp)))
        return resultados
    except Exception:
        return []

def construir_post():
    # Bluesky limit: 300 chars. Keep it tight.
    lineas = ["🌡️ Hottest & coldest highs today:\n"]
    for continente, ciudades in CONTINENTS.items():
        resultados = consultar_continente(ciudades)
        if resultados:
            resultados.sort(key=lambda x: x[1], reverse=True)
            max_alta = resultados[0]
            max_baja = resultados[-1]
            # Short continent label (strip flag emoji text after space)
            icono = continente.split()[0]
            lineas.append(f"{icono} 🔥{max_alta[0]} {max_alta[1]}°C  ❄️{max_baja[0]} {max_baja[1]}°C")
    lineas.append("\n#Weather #QuickTemp")
    return "\n".join(lineas)

def publicar_post():
    texto = construir_post()
    client = Client()
    client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)
    client.send_post(text=texto)
    print("Post publicado en Bluesky:")
    print(texto)

if __name__ == "__main__":
    publicar_post()
