import requests
import time
from datetime import datetime, timedelta

API_BASE_URL = "https://archive-api.open-meteo.com/v1/era5"
API_PARAMS = {
    "hourly": "temperature_2m,relative_humidity_2m,rain",
    "timezone": "Europe/Madrid",
}

def get_historical_weather(latitude, longitude, start_date_str, end_date_str, retries=3, delay=1):
    """
    Consulta la API de Open-Meteo para obtener datos climáticos históricos
    de un rango de fechas. La API devuelve datos horarios para cada día completo
    en el rango especificado.
    """
    params = {
        **API_PARAMS,
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date_str,
        "end_date": end_date_str
    }

    for attempt in range(retries):
        try:
            response = requests.get(API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()  # Lanza un error si la solicitud no es exitosa
            data = response.json()
            
            if "hourly" in data:
                # Procesar los datos hora a hora y añadirlos a una lista
                all_weather_data = []
                for i in range(len(data["hourly"]["time"])):
                    hourly_data = {
                        "fecha_hora": data["hourly"]["time"][i],
                        "temperatura_2m": data["hourly"]["temperature_2m"][i],
                        "humedad_2m": data["hourly"]["relative_humidity_2m"][i],
                        "lluvia": data["hourly"]["rain"][i]
                    }
                    all_weather_data.append(hourly_data)
                return all_weather_data
            
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