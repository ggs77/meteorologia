import pandas as pd
from pathlib import Path

def load_data_from_excel(file_path: Path):
    """
    Carga los datos de un archivo Excel en un DataFrame y valida las columnas.
    
    Args:
        file_path (Path): La ruta al archivo Excel.

    Returns:
        pd.DataFrame: El DataFrame cargado.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Error: El archivo '{file_path}' no se encontró.")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Archivo '{file_path}' cargado exitosamente. Columnas: {df.columns.tolist()}")

        return df
    except Exception as e:
        raise Exception(f"Error al cargar el archivo Excel: {e}")

def save_data_to_excel(df: pd.DataFrame, file_path: Path):
    """
    Guarda un DataFrame en un archivo Excel.

    Args:
        df (pd.DataFrame): El DataFrame a guardar.
        file_path (Path): La ruta donde guardar el archivo.
    """
    try:
        # Asegurarse de que la carpeta de destino exista
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(file_path, index=False)
        print(f"\nProceso completado. Datos guardados en '{file_path}'")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

