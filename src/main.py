import pandas as pd
from pathlib import Path
from src.api.open_meteo import get_historical_weather_range
from src.utils.excel_handler import load_data_from_excel, save_data_to_excel
import time

# --- Constantes de configuración ---
INPUT_FILE = Path("data/raw/datos_entrada.xlsx")
OUTPUT_FILE = Path("data/processed/datos_salida.xlsx")

def process_data(df):
    """
    Procesa el DataFrame para obtener los datos climáticos de uno o varios días completos.
    """
    required_cols = {"Latitud", "Longitud", "Inicio"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"El archivo de entrada debe contener las columnas: {', '.join(required_cols)}")
    
    return process_data_range(df)

def process_data_range(df):
    """
    Procesa el DataFrame para obtener los datos climáticos de un rango de fechas por día.
    """
    new_df_data = []
    total_rows = len(df)
    
    for index, row in df.iterrows():
        print(f"Procesando fila {index + 1}/{total_rows}...")
        
        latitud = row.get("Latitud")
        longitud = row.get("Longitud")
        
        if pd.isna(latitud) or pd.isna(longitud):
            print(f"Fila {index + 1}: Latitud o Longitud incompletas, saltando.")
            continue
        
        try:
            latitud_f = float(latitud)
            longitud_f = float(longitud)
            start_date_str = pd.to_datetime(row["Inicio"]).strftime('%Y-%m-%d')
            
            # Si no hay fecha de fin, se procesa solo la fecha de inicio
            end_date_str = start_date_str
            if "Fin" in df.columns and not pd.isna(row["Fin"]):
                end_date_str = pd.to_datetime(row["Fin"]).strftime('%Y-%m-%d')

        except (ValueError, TypeError) as e:
            print(f"Fila {index + 1}: Error de formato de datos ({e}), saltando.")
            continue

        print(f"Solicitando datos para Lat: {latitud_f}, Lon: {longitud_f} desde {start_date_str} hasta {end_date_str}.")
        weather_data = get_historical_weather(latitud_f, longitud_f, start_date_str, end_date_str)
        
        if weather_data:
            for hourly_data in weather_data:
                new_row = {
                    "Fecha": hourly_data["fecha_hora"],
                    "Latitud": latitud_f,
                    "Longitud": longitud_f,
                    "Temperatura": hourly_data["temperatura_2m"],
                    "Humedad": hourly_data["humedad_2m"],
                    "Lluvia": hourly_data["lluvia"]
                }
                new_df_data.append(new_row)
        else:
            print(f"No se pudieron obtener datos climáticos para el rango del {start_date_str} al {end_date_str}.")

        time.sleep(0.1) # Pausa entre cada llamada de rango para no saturar la API
        
    if not new_df_data:
        return pd.DataFrame(columns=["Fecha", "Latitud", "Longitud", "Temperatura", "Humedad", "Lluvia"])
    
    return pd.DataFrame(new_df_data)

# --- Ejecutar el programa principal ---
if __name__ == "__main__":
    try:
        df_entrada = load_data_from_excel(INPUT_FILE)
        
        df_processed = process_data(df_entrada)
        
        save_data_to_excel(df_processed, OUTPUT_FILE)
        print("\nProceso finalizado. El archivo de salida se ha guardado en 'data/processed/datos_salida.xlsx'.")
    except Exception as e:
        print(f"El programa principal falló: {e}")