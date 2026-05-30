import streamlit as st
import utils as ut
from PIL import Image
from utils import PATH

# Configuración de la página principal
st.set_page_config(page_title="Trees",
                   page_icon="🌳",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={"About": "Bootcamp Talento Tech"}
                   )

# Menú desde utilidades
ut.generarMenu()

# Importamos los datos desde la función
df_inicial = ut.cargar_datos()

# Cargamos el modelo si ya existe
model = ut.cargar_modelo()

if model is None:
    ut.modelar(df=df_inicial, model=model)
    st.rerun()

# Llamamos la función de graficar árboles
st.header("Dibujar Árboles")
# usamos un contenedor
with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="distribute"):
    
    columnas = list(df_inicial.columns[2:].values)
    
    num_arbol = st.number_input(label="Número del árbol",
                                min_value=1,
                                max_value=100
                                )
    btn_dibujar = st.button("Dibujar", type="primary")

with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="top"):
    
    if btn_dibujar:
        st.subheader(f'Árbol de Decisión {num_arbol}', text_alignment="center")
        #graph = ut.arboles(model=model, columnas=columnas, num=num_arbol - 1)   
        #st.graphviz_chart(figure_or_dot=graph, width="stretch", height="content")

        ut.arboles_interac(model=model, columnas=columnas, num=num_arbol - 1)


    else:
        st.subheader(f'Árbol de Decisión', text_alignment="center")
        image = Image.open(PATH + 'media/arbol_default.png')
        st.image(image=image, 
                 caption="Árboles de Decisión", 
                 width="stretch"
                 )



