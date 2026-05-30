# 📊 Dashboard SMEC: Síndrome Metabólico de Enfermedad Cardiovascular

> **Talento Tech 2:** Universidad de Antioquia  
> **Autor:** Mg. Luis Felipe Bustamante Narváez  
> **Bootcamp:** Análisis de Datos Explorador - 658

<br>

# Herramientas

Python, Streamlit, Google Colab, VS Code, Ngrok

<br>

# Crear proyecto

1. Crear carpeta

2. Crear archivo **_app.py_** en la raíz del proyecto

   'app' es un nombre sugerido, pero es el más común.

3. Crear archivo **_utils.py_** en la raíz del proyecto

   'utils' es un nombre sugerido, pero es el más común para manejar las funciones comunes a todo el tablero.

<br>

# Estructura del proyecto

    SMEC658
    ├─ .streamlit
    │  └─ config.toml
    ├─ data
    │  ├─ Datos_Pacientes.csv
    │  ├─ Datos_Pacientes_Nuevos.csv
    │  └─ model.sav
    ├─ media
    │  ├─ arbol_default.png
    │  ├─ imagen_1.jpeg
    │  └─ logo_pag.png
    ├─ pages
    │  ├─ arboles.py
    │  ├─ graficos.py
    │  └─ pronostico.py
    ├─ app.py
    ├─ requirements.txt
    └─ utils.py

<br>

# Configuración del proyecto

1.  Crear la carpeta **_.streamlit_** en la raíz del proyecto

2.  Crear el archivo **_config.toml_** dentro de la carpeta .streamlit

3.  Dentro de config.toml agregamos:

        [client]
        showSidebarNavigation = false

        [server]
        runOnSave = true

        [theme]

        # Opciones base compartidas

        base = "light"
        font = "sans-serif"
        baseFontSize = 16
        baseRadius = "0.5rem"

        # Tema Claro

        [theme.light]

        primaryColor = "#4CAF50"
        backgroundColor = "#F7F9FB"
        secondaryBackgroundColor = "#FFFFFF"
        textColor = "#1F2937"

        blueColor = "#2563EB"
        greenColor = "#16A34A"
        redColor = "#DC2626"

        # Tema oscuro

        [theme.dark]

        primaryColor = "#22C55E"
        backgroundColor = "#0E1117"
        secondaryBackgroundColor = "#1A1F2B"
        textColor = "#E5E7EB"

        blueColor = "#3B82F6"
        greenColor = "#22C55E"
        redColor = "#EF4444"

    Nota: Los parámetros de **_theme_** son solo un ejemplo.

4.  Crear la carpeta **_data_** en la raíz del proyecto

5.  Crear la carpeta **_media_** en la raíz del proyecto

6.  Crear la carpeta **_pages_** en la raíz del proyecto

7.  Dentro de la carpeta **_pages_** crear los siguientes archivos:
    - arboles.py
    - graficos.py
    - pronostico.py

<br>

# Entorno Virtual (solo local)

Nota 1: Sigue estos pasos si vas a trabajar en un ambiente local, por ejemplo en **VS Code**, u otros.  
Nota 2: Un **_entorno virtual_** te permite aislar cualquier proyecto, no saturar tu **_entorno global_** con librerías y mejorar el rendimiento del equipo en tiempo de ejecución.

En la terminal del proyecto:

1.  Crear entorno virtual

        python -m venv env

    **_env_** es el nombre del entorno. Puedes usar cualquier nombre, aunque este es uno de los más comunes.

2.  Activar entorno virtual

        .\env\Scripts\activate

3.  Desactivar entorno virtual

        deactivate

4.  Instalar librerías

    Nota: Pueden hacer falta algunas librerías.

         pip install streamlit
         pip install scikit-learn
         pip install matplotlib
         pip install seaborn
         pip install graphviz
         pip install plotly

         # Nuestro módulo

         pip install utils

5.  Guardar las librerías utilizadas

        pip freeze > requirements.txt

    - **_requirements_** es el nombre estricto que debemos usar.

    - La extensión debe ser estrictamente **_.txt_** ya que almacena los nombres de las librerías y sus versiones.

    - Al inspeccionar el archivo, encontrarás más liberías de las que instalaste, ya que son requisito de estas.

6.  Instalar las librerías desde los requerimientos en caso de migrar de entorno o equipo de cómputo.

        pip install -r requirements.txt

<br>

# Varios

En la terminal del proyecto:

1.  Revisar versiones

        python --version
        pip --version

2.  Identificar librerías instaladas

        pip list

3.  Actualizar PIP (solo local)

        python.exe -m pip install --upgrade pip

4.  Problemas de versiones del entorno Global vs Virtual (Si los presenta)

        pip install isort

<br>

# Recursos del proyecto SMEC

1.  Texto introductorio (para usar en el código - Opcional)

        """
        Determinar si un paciente al cual se le realizan diferentes estudios clínicos para hallar enfermedades como: Hipertensión, Hiperglusemia, Colesterol HDL bajo, Hipertriglidicemia, Trastorno de cintura-altura y poliúrea. Además, se le preguntan datos como: Edad, Género, si fuma y si consume licor.

        Todo esto con la finalidad de diagnosticar si la persona posee un síndrome metabólico asociado a enfermedad cardiovascular (SMEC), a la cual llamaremos enferdedad, una variable categórica que vamos a predecir a través del modelo de Bosques Aleatorios (Random Forest).

        Los datos se encuentran en la carpeta:\n\n https://drive.google.com/drive/folders/1IynJDozf6bXvoPjegsGMstVvijMhvpaf?usp=drive_link
        """

2.  Texto conceptual (para usar en el código - Opcional)

        """
        - KPI: Identificar a través de los parámetros de las enfermedades de base de cada paciente, y sus datos médicos generales como el género, la edad, si consume o no, tabaco y alcohol, para determinar si el paciente puede padecer SMEC.
        """

3.  Imágenes

    Guardar en la carpeta **_media_** los archivos de imágenes sin cambiar los nombres ni la extensión. Te recomendamos hacerlo desde el Drive.
    - arbol_default.png
    - logo_pag.png
    - imagen_1.jpeg

4.  Datos

    Guardar en la carpeta **_data_** el archivo **datos_pacientes.csv** compartido.

5.  Script para renderizar gráficos de árboles

        html = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        </head>

        <body style="margin:0; overflow:hidden;">

            <div id="container" style="width:100%; height:500px; border:0px solid #ddd;">
                {svg}
            </div>

            <script>
                const svgElement = document.querySelector('svg');

                svgElement.removeAttribute('width');
                svgElement.removeAttribute('height');

                svgElement.style.width = '100%';
                svgElement.style.height = '100%';

                svgPanZoom(svgElement, {{
                    zoomEnabled: true,
                    controlIconsEnabled: true,
                    fit: true,
                    center: true,
                    minZoom: 0.5,
                    maxZoom: 20
                }});
            </script>

        </body>
        </html>
        """

# Emojis 🧸

Para enriquecer el texto, streamlit permite el uso de emojis. En este enlace se encuentran los códigos de todos lo emojis permitidos, aunque es más eficiente copiar el emoji directamente y pegarlo en el código de python.

Enlace: [Emojis para Streamlit](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)

A continuación, encontrarás los emojis que usaremos como base en la aplicación para ahorrar el tiempo de búsqueda. Están ordenados por página:

1. app.py

   ❤️‍🩹

2. utils.py

   ❤️‍🩹

   🏠💚🌳📊

   📋🗺📤

   ⚕️🚺🚹🤒➕🤗➖🤕😷📈📊🎯📉📦📏🩺🚑⚰️

   ⚰️

3. pronostico.py

   ❤️‍🩹💉🎉🚨

4. arboles.py

   🌳

5. graficos.py

   📊⚙️📈
