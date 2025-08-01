import requests
import time

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_PARAMS = {
    "hourly": "temperature_2m,relative_humidity_2m,rain",
    "timezone": "Europe/Madrid",
    "past_days": 0
}

def get_historical_weather(latitude, longitude, date_str, time_str, retries=3, delay=1):
    """
    Consulta la API de Open-Meteo para obtener datos climáticos históricos
    con lógica de reintentos.
    """
    params = {
        **API_PARAMS,
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date_str,
        "end_date": date_str
    }

    for attempt in range(retries):
        try:
            response = requests.get(API_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            target_hour_str = time_str.split(':')[0] + ":00"
            if "hourly" in data and "time" in data["hourly"]:
                for i, api_time in enumerate(data["hourly"]["time"]):
                    if target_hour_str in api_time:
                        temperature = data["hourly"]["temperature_2m"][i]
                        humidity = data["hourly"]["relative_humidity_2m"][i]
                        rain = data["hourly"]["rain"][i]
                        return {
                            "Temperatura": temperature,
                            "Humedad": humidity,
                            "Lluvia": rain
                        }
                print(f"No se encontraron datos para la hora {time_str} en {date_str}. Intento {attempt + 1}/{retries}.")
                time.sleep(delay * (attempt + 1))
            else:
                print(f"Formato de respuesta inesperado. Intento {attempt + 1}/{retries}.")
                time.sleep(delay * (attempt + 1))

        except requests.exceptions.RequestException as e:
            print(f"Error en la consulta de la API (Intento {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                return None
        except Exception as e:
            print(f"Error inesperado al procesar la respuesta: {e}. Intento {attempt + 1}/{retries}.")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                return None
    
    return None
