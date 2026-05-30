import streamlit as st
import pandas as pd
import utils as ut

# Configuración de la página principal
st.set_page_config(page_title="Dx/Px",
                   page_icon="❤️‍🩹",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={"About": "Bootcamp Talento Tech"}
                   )

# Menú desde utilidades
ut.generarMenu()

# Importamos los datos desde la función
df_inicial = ut.cargar_datos()

# Llamamos la función del análisis inicial
st.header("Análisis Exploratorio")
# usamos un contenedor
with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="distribute"):
    ut.eda(df=df_inicial)

# Llamamos la función del análisis estadístico
st.header("Análisis Estadístico")
# usamos un contenedor
with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="distribute"):
    ut.estadistico(df=df_inicial)

# Modelo

# Cargamos el modelo si ya existe
model = ut.cargar_modelo()

# Llamamos la función del pronóstico
st.header("Diagnóstico y Pronóstico")
# usamos un contenedor
with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="distribute"):
    # Modelo
    ut.modelar(df=df_inicial, model=model)

    # Predicción nuevo paciente

    with st.expander(label="Pronóstico Nuevo Paciente",
                     icon="💉",
                     expanded=True):
        
        st.markdown(f"**Anamnesis**", text_alignment="center")

        
        col_1, col_2, col_3 = st.columns(3)
    
        with col_1:
            
            hipertension = st.checkbox('Hipertensión')
            hiperglucemia = st.checkbox('Hiperglucemia')
            hdl = st.checkbox('HDL Bajo')
            hipertri = st.checkbox('Hipertri/cemia')
            
        with col_2:

            ica = st.checkbox('ICA')
            tabaco = st.checkbox('Tabaco')
            alcohol = st.checkbox('Alcohol')
            poliu = st.checkbox('Poliúrea')
        
        with col_3:
        
            edad = st.number_input('Edad', min_value=18)
            genero = st.selectbox('Género',('Femenino','Masculino'))    

        st.divider()

        btn_pronost = st.button('Pronosticar',type='primary')        

        if btn_pronost:

            datos = [
                hipertension, hiperglucemia, hdl, hipertri, ica, edad, genero, tabaco, alcohol, poliu
            ]
            
            # Convertimos a df
            columnas = list(df_inicial.columns[2:].values)
            df_new = pd.DataFrame([datos], columns=columnas)

            st.markdown(f"**Valoración Clínica**", text_alignment="center")

            st.dataframe(df_new, hide_index=True)

            predict = ut.predecir(df_new=df_new)

            resultado = "NO" if predict[0] == 0 else "SI"

            st.markdown(f"**Diagnóstico**", text_alignment="center")

            if resultado == "NO":
                st.success(f'🎉 La persona evaluada, de acuerdo con los datos ingresados en el modelo, {resultado} padece del Síndrome Metabólico de Enfermedad Cardiovascular - SMEC')
            else:
                st.error(f'🚨 La persona evaluada, de acuerdo con los datos ingresados en el modelo, {resultado} padece del Síndrome Metabólico de Enfermedad Cardiovascular - SMEC')
            
