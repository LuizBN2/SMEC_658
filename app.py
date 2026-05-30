# Librerías
import streamlit as st
from PIL import Image
import utils
from utils import PATH

# Configuración de la página principal
st.set_page_config(page_title="SMEC",
                   page_icon="❤️‍🩹",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={"About": "Bootcamp Talento Tech"}
                   )

# Menú desde utilidades --- llamamos luego de crear todo app.py line 67
utils.generarMenu()

# Manejo del espacio de trabajo
col_1, col_2, col_3 = st.columns(spec=[0.2,1,0.2],
                                 gap="large",
                                 vertical_alignment="center",
                                 border=False,
                                 width="stretch")

# Solo usaremos la columna del medio como ejemplo
with col_2:
    # Título
    st.title("Síndrome Metabólico de Enfermedad Cardiovascular")

    # Introducción
    st.write("""
    Determinar si un paciente al cual se le realizan diferentes estudios clínicos para hallar enfermedades como: Hipertensión, Hiperglusemia, Colesterol HDL bajo, Hipertriglidicemia, Trastorno de cintura-altura y poliúrea. Además, se le preguntan datos como: Edad, Género, si fuma y si consume licor.

    Todo esto con la finalidad de diagnosticar si la persona posee un síndrome metabólico asociado a enfermedad cardiovascular (SMEC), a la cual llamaremos enferdedad, una variable categórica que vamos a predecir a través del modelo de Bosques Aleatorios (Random Forest).

    Los datos se encuentran en la carpeta:\n\n https://drive.google.com/drive/folders/1IynJDozf6bXvoPjegsGMstVvijMhvpaf?usp=drive_link

    """)

    # Imagen
    imagen = Image.open(PATH + "media/imagen_fondo.jpeg")
    st.image(image=imagen,
             caption="Enfermedad Cardiovascular",
             width=700)
    
    # Subtítulo
    st.header("Key Performance Indicators (KPIs)")

    # Texto de conceptualización
    st.write("""
    - KPI: Identificar a través de los parámetros de las enfermedades de base de cada paciente, y sus datos médicos generales como el género, la edad, si consume o no, tabaco y alcohol, para determinar si el paciente puede padecer SMEC.

    """)

# Ahora sí vamos a crear utils



