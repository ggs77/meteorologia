



# Script de Extracción de Datos Climáticos

### Propósito

Este proyecto es un script de Python que utiliza la API de **Open-Meteo** para obtener datos climáticos históricos (temperatura, humedad y lluvia) y los añade a un archivo de Excel. Sirve como una herramienta genérica y versátil para cualquier proyecto que necesite enriquecer datos de ubicación con información meteorológica de un momento y lugar específico.

El código está diseñado para ser modular y fácil de mantener, con la lógica de la API, el manejo de archivos y el flujo principal del programa separados en distintos módulos.

### Estructura del Proyecto

El proyecto sigue una estructura de carpetas estándar para aplicaciones de Python, lo que facilita su organización y escalabilidad:

```
mi_proyecto_clima/
├── src/
│   ├── api/
│   │   └── open_meteo.py       # Lógica para interactuar con la API del clima.
│   ├── utils/
│   │   └── excel_handler.py    # Funciones para leer y escribir archivos Excel.
│   └── main.py                 # Script principal que orquesta el proceso.
├── data/
│   ├── raw/
│   │   └── datos_entrada.xlsx    # Archivo de entrada con los datos de ubicación.
│   └── processed/
│       └── datos_salida.xlsx    # Archivo de salida con los datos climáticos.
└── requirements.txt             # Dependencias del proyecto.
```

### Uso

1. **Clona el repositorio:**

   ```
   git clone https://github.com/tu-usuario/mi_proyecto_clima.git
   cd mi_proyecto_clima
   ```

2. **Instala las dependencias:** Asegúrate de tener Python 3.6 o superior. Las bibliotecas necesarias están listadas en `requirements.txt`.

   ```
   pip install -r requirements.txt
   ```

3. **Prepara el archivo de entrada:** Coloca tu archivo de Excel en la carpeta `data/raw/` y renómbralo a **`datos_entrada.xlsx`**.

4. **Ejecuta el script:** Desde la raíz del proyecto, ejecuta el script principal.

   ```
   python src/main.py
   ```

El script leerá tu archivo de entrada, consultará la API para cada fila y guardará los resultados en un nuevo archivo llamado **`datos_salida.xlsx`** dentro de la carpeta `data/processed/`.

### Formato del Archivo de Entrada (`datos_entrada.xlsx`)

El script requiere que el archivo de Excel de entrada tenga una hoja de cálculo con las siguientes columnas y nombres exactos para poder procesar los datos correctamente:

| Columna      | Tipo de Dato | Descripción                                                  |
| ------------ | ------------ | ------------------------------------------------------------ |
| **Fecha**    | `Fecha`      | La fecha del evento en cualquier formato reconocido por pandas (ej. `DD-MM-AAAA` o `YYYY-MM-DD`). |
| **Hora**     | `Hora`       | La hora del evento (ej. `10:00`, `14:30:00`).                |
| **Latitud**  | `Numérico`   | La latitud de la ubicación.                                  |
| **Longitud** | `Numérico`   | La longitud de la ubicación.                                 |

El script añadirá automáticamente las columnas **"Humedad"**, **"Temperatura"** y **"Lluvia"** al DataFrame. Si ya existen, las rellenará con los datos de la API.