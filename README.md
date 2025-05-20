# Dashboard de Mortalidad en Colombia

## Tabla de Contenidos
- [Objetivo](#objetivo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Prerrequisitos](#prerrequisitos)
- [Metodología](#metodología)
  - [Instalación de Git](#instalación-de-git)
  - [Desarrollar la Aplicación Web con Dash](#desarrollar-la-aplicación-web-con-dash)
  - [Validar Git](#validar-git)
  - [Configurar la Estructura del Proyecto con Dash Tools](#configurar-la-estructura-del-proyecto-con-dash-tools)
  - [Despliegue en Render](#despliegue-en-render)
- [Software](#software)
- [Instalación](#instalación)

## Objetivo
El objetivo de este proyecto es desarrollar un dashboard interactivo que visualiza datos de mortalidad en Colombia para el año 2019. La aplicación presenta diferentes visualizaciones que permiten analizar patrones de mortalidad por departamento, ciudad, causa de muerte, distribución por edad y género. Se utiliza **Dash** para crear una interfaz web interactiva y **Plotly** para generar gráficos dinámicos. El código se gestiona con **Git** y se almacena en **GitHub**, mientras que el despliegue se realiza en la plataforma **Render**.

## Estructura del proyecto
```bash
dashboard/
├── data/                      # Datos utilizados por la aplicación
│   ├── Codigos_de_muerte.csv  # Códigos CIE-10 y descripciones
│   ├── Colombia.geo.json      # Datos geográficos de Colombia
│   ├── datos_mortalidad.csv   # Datos principales de mortalidad
│   └── Division_politico_administrativa.csv  # Información de municipios y departamentos
├── src/                       # Código fuente
│   ├── assets/                # Recursos estáticos (CSS)
│   ├── data/                  # Datos procesados
│   ├── modulos/               # Módulos de la aplicación
│   │   ├── cargar_datos.py    # Funciones para cargar datos
│   │   ├── generar_graficos.py # Funciones para crear visualizaciones
│   │   └── procesar_datos.py  # Funciones para procesar datos
│   └── app.py                 # Aplicación principal Dash (server = app.server)
├── Procfile                   # Configuración para despliegue
├── README.md                  # Documentación del proyecto
├── render.yaml                # Configuración para Render
└── requirements.txt           # Dependencias del proyecto
```

## Prerrequisitos
- Python 3.10 o superior
- Una cuenta en **GitHub** para almacenar el código fuente
- Una cuenta en **Render** para desplegar la aplicación web (puedes crearla gratuitamente en [render.com](https://render.com/))
- Conocimientos básicos de Python, Dash y Plotly

## Metodología

### Instalación de Git
Antes de iniciar el desarrollo, es necesario tener instalado **Git** para el control de versiones:

1. Descarga Git desde la página oficial: [git-scm.com](https://git-scm.com/)
2. Instala siguiendo las instrucciones proporcionadas en el sitio web
3. Configura tu nombre de usuario y correo electrónico:
```bash
git config --global user.name "brayanmoyano"
git config --global user.email "brayanmoyano53@gmail.com"
```

### Desarrollar la Aplicación Web con Dash
Para desarrollar el dashboard con Dash, se siguieron estas convenciones:

1. **Estructura modular**: Se organizó el código en módulos separados para facilitar el mantenimiento:
   - `cargar_datos.py`: Funciones para leer archivos CSV y JSON
   - `procesar_datos.py`: Funciones para transformar y analizar los datos
   - `generar_graficos.py`: Funciones para crear visualizaciones con Plotly

2. **Archivo principal (`app.py`)**: Contiene la definición de la aplicación Dash, las rutas y el diseño de la interfaz.

3. **Exposición del servidor**: Se definió `server = app.server` para exponer la instancia Flask subyacente, necesario para el despliegue en Render.

### Validar Git
Para verificar que Git está correctamente instalado:

```bash
git --version
```

Una vez confirmada la instalación, inicializa el repositorio:

```bash
git init
git add .
git commit -m "Versión inicial del dashboard"
```

### Configurar la Estructura del Proyecto con Dash Tools
**Dash Tools** facilita la preparación del proyecto para su despliegue en Render:

1. **Instalación de Dash Tools**:
```bash
pip install dash-tools
```

2. **Abrir la interfaz gráfica**:
```bash
dashtools gui
```

3. **Validación del proyecto**:
   - Verificar la existencia de `src/app.py`
   - Confirmar que existe la definición `server = app.server`

4. **Generación de archivos de configuración**:
   - `render.yaml`: Configuración para el despliegue en Render
   - `requirements.txt`: Lista de dependencias del proyecto

### Despliegue en Render
Para desplegar la aplicación en Render:

1. **Subir el proyecto a GitHub**:
```bash
git remote add origin <URL-de-tu-repositorio>
git push -u origin main
```

2. **Configurar el despliegue en Render**:
   - Inicia sesión en [render.com](https://render.com/)
   - Crea un nuevo servicio web
   - Conecta con tu repositorio de GitHub
   - Configura el comando de inicio: `gunicorn src.app:server`
   - Especifica la versión de Python: 3.10.0

3. **Verificar el despliegue**:
   - Render proporcionará una URL para acceder a la aplicación
   - Comprueba que todas las visualizaciones funcionan correctamente

## Software
**Requisitos**:
1. Python 3.10 o superior
2. Editor de código (recomendado: Visual Studio Code)
3. Bibliotecas principales:
   - `dash` (3.0.4): Framework para aplicaciones web analíticas
   - `plotly` (6.0.1): Biblioteca para gráficos interactivos
   - `pandas` (2.2.3): Manipulación y análisis de datos
   - `numpy` (2.2.5): Operaciones numéricas
   - `gunicorn` (23.0.0): Servidor WSGI para producción
   - `Flask` (2.3.2): Framework web ligero
   - `Unidecode` (1.4.0): Normalización de texto

## Instalación
Para instalar y ejecutar el proyecto localmente:

1. **Clonar el repositorio**:
```bash
git clone <URL-del-repositorio>
cd dashboard
```

2. **Crear y activar un entorno virtual**:
```bash
# En Windows
python -m venv dashboard
venv\Scripts\activate

# En macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python src/app.py
```

La aplicación estará disponible en `localhost:8050`