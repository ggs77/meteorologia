import pandas as pd
from pathlib import Path
from src.api.open_meteo import get_historical_weather
from src.utils.excel_handler import load_data_from_excel, save_data_to_excel
import time

# --- Constantes de configuración ---
INPUT_FILE = Path("data/raw/datos_entrada.xlsx")
OUTPUT_FILE = Path("data/processed/datos_salida.xlsx")
REQUIRED_COLS = ["Fecha", "Hora", "Latitud", "Longitud"]
WEATHER_COLS = ["Humedad", "Temperatura", "Lluvia"]

def process_data(df):
    """Procesa el DataFrame para obtener los datos climáticos."""
    
    # Crear las columnas de clima si no existen
    for col in WEATHER_COLS:
        if col not in df.columns:
            df[col] = None

    total_rows = len(df)
    for index, row in df.iterrows():
        print(f"Procesando fila {index + 1}/{total_rows}...")
        
        fecha = row["Fecha"]
        hora = row["Hora"]
        latitud = row["Latitud"]
        longitud = row["Longitud"]

        # Validar y convertir datos
        if pd.isna(latitud) or pd.isna(longitud) or pd.isna(fecha) or pd.isna(hora):
            print(f"Fila {index + 1}: Datos incompletos, saltando.")
            continue
        
        try:
            latitud_f = float(latitud)
            longitud_f = float(longitud)
            date_str = pd.to_datetime(fecha).strftime('%Y-%m-%d')
            
            # Lógica para manejar diferentes formatos de hora
            if isinstance(hora, pd.Timedelta):
                time_str = (pd.Timestamp('1900-01-01') + hora).time().strftime('%H:%M:%S')
            elif isinstance(hora, pd.Timestamp):
                time_str = hora.strftime('%H:%M:%S')
            else: # Asumir string
                time_str = str(hora)
                
        except (ValueError, TypeError) as e:
            print(f"Fila {index + 1}: Error de formato de datos ({e}), saltando.")
            continue
        
        # Llamada a la API
        weather_data = get_historical_weather(latitud_f, longitud_f, date_str, time_str)
        
        if weather_data:
            for col, value in weather_data.items():
                df.loc[index, col] = value
        else:
            print(f"No se pudieron obtener datos climáticos para Lat: {latitud_f}, Lon: {longitud_f} el {date_str} a las {time_str}.")

        # Pausa para no saturar la API
        time.sleep(0.1)

    return df

# --- Ejecutar el programa principal ---
if __name__ == "__main__":
    try:
        # Cargar los datos usando la función del handler
        df_embarques = load_data_from_excel(INPUT_FILE, REQUIRED_COLS)
        
        # Procesar los datos
        df_processed = process_data(df_embarques)
        
        # Guardar los datos procesados usando la función del handler
        save_data_to_excel(df_processed, OUTPUT_FILE)
    except Exception as e:
        print(f"El programa principal falló: {e}")