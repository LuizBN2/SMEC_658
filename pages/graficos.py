import streamlit as st
import pandas as pd
import plotly.express as px
import utils as ut

# Configuración de la página principal
st.set_page_config(page_title="Gráficos",
                   page_icon="📊",
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

# Opciones múltiples y datos
tipos_de_grafico = [ 
        "Dispersión",
        "Histograma",
        "Cajas y Bigotes",
        "Barras",
        "Violín",
        "Mapa de Calor"
    ]
df = df_inicial.drop(columns=["Expediente"])
columnas_numericas = df.select_dtypes(include="number").columns.tolist()
columnas_categoricas = ["Enfermedad"]
alto = 300
sel_color = px.colors.qualitative.Pastel # importamos





# Barra lateral
with st.sidebar:

    st.divider()

    st.subheader("⚙️ Configuración")    

    tipo_grafico = st.selectbox(label="Tipo de gráfico Datos",
                                options=tipos_de_grafico)

# Contenido de la page

st.header("Síndrome Metabólico de Enfermedad Cardiovascular")
st.caption("Explora relaciones entre variables y métricas del modelo Random Forest")

st.subheader("📈 Visualización Dinámica de los Datos")

with st.container(border=True,
                  width="stretch",
                  height="content",
                  horizontal_alignment="distribute",
                  vertical_alignment="top"):

    if tipo_grafico == "Dispersión":

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:
            x = st.selectbox(label="Variable X",
                             options=columnas_numericas
                             )
        with col_2:
            y = st.selectbox(label="Variable Y",
                             options=columnas_numericas,
                             index=1
                             )        
        
        st.divider()
        st.markdown(f"{tipo_grafico} ⮕ {x} vs {y}", text_alignment="center")
        
        fig = px.scatter(data_frame=df,
                         x=x,
                         y=y,
                         color=columnas_categoricas[0],
                         size="Edad",
                         hover_data=df.columns,
                         color_discrete_sequence=sel_color,
                         template="plotly",  #plotly_white or plotly_black
                         )
        fig.update_layout(height=alto)
        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
    elif tipo_grafico == "Histograma":

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            variable = st.selectbox(label="Variable",
                                    options=columnas_numericas
                                    )
        
        st.divider()
        st.markdown(f"{tipo_grafico} ⮕ {variable}", text_alignment="center")

        fig = px.histogram(data_frame=df,
                           x=variable,                         
                           color=columnas_categoricas[0],
                           marginal="box",
                           barmode="overlay",  
                           color_discrete_sequence=sel_color,                       
                           template="plotly"
                          )
        fig.update_layout(height=alto,
                          bargap=0.2,
                          yaxis_title_text='Pacientes',
                          bargroupgap=0.2
                          )
        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
    elif tipo_grafico == "Cajas y Bigotes":

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            variable = st.selectbox(label="Variable",
                                    options=columnas_numericas
                                    )
        
        st.divider()
        st.markdown(f"{tipo_grafico} ⮕ {variable}", text_alignment="center")

        fig = px.box(data_frame=df,
                     x=variable, 
                     y=columnas_categoricas[0],                                             
                     color=columnas_categoricas[0],
                     points="all",  
                     color_discrete_sequence=sel_color,                                         
                     template="plotly"
                    )
        fig.update_layout(height=alto,
                          yaxis_title_text='Diagnóstico de SMEC',
                          )
        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
    elif tipo_grafico == "Barras":

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            variable = st.selectbox(label="Variable",
                                    options=columnas_numericas
                                    )
            
            conteo = (
                df
                .groupby([variable, columnas_categoricas[0]])
                .size()
                .reset_index(name="Cantidad")
            )
        
        st.divider()
        st.markdown(f"{tipo_grafico} ⮕ {variable}", text_alignment="center")
        
        fig = px.bar(data_frame=conteo,
                     x=variable,
                     y=conteo["Cantidad"],
                     color=columnas_categoricas[0],
                     barmode="group",
                     color_discrete_sequence=sel_color,
                     template="plotly"
                     )
        fig.update_layout(height=alto)

        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
    elif tipo_grafico == "Violín":

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            variable = st.selectbox(label="Variable",
                                    options=columnas_numericas
                                    )
        
        st.divider()
        st.markdown(f"{tipo_grafico} ⮕ {variable}", text_alignment="center")

        fig = px.violin(data_frame=df,
                        x=columnas_categoricas[0],   
                        y=variable,                                                                
                        color=columnas_categoricas[0],
                        box=True,
                        points="all",  
                        color_discrete_sequence=sel_color,                                         
                        template="plotly"
                    )
        fig.update_layout(height=alto,
                          xaxis_title_text='Diagnóstico de SMEC',
                          )
        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
    elif tipo_grafico == "Mapa de Calor":   

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            colores_px = px.colors.named_colorscales()            

            colores = st.selectbox(label="Escalas de color PX",
                                    options=colores_px,
                                    index=colores_px.index("viridis")
                                    )  
                
        st.markdown(f"{tipo_grafico} ⮕ Correlación de Variables", text_alignment="center")

        df_corr = df.copy()
        df_corr["Enfermedad"] = df_corr["Enfermedad"].map({"SI": 1, "NO": 0})
        corr = df_corr.corr(numeric_only=True)

        fig = px.imshow(img=corr,
                        text_auto=True,
                        aspect="auto",
                        color_continuous_scale=colores,
                        template="plotly"
                        )
        fig.update_layout(height=alto)
        st.plotly_chart(figure_or_data=fig,
                        width="stretch"
                        )
    
with st.sidebar:

    tipo_grafico_model = st.selectbox(label="Tipo de gráfico Modelo",
                                options=["Barras", "Distribución 3D"])
    
    if tipo_grafico_model == "Distribución 3D":

        eje_x = st.selectbox("Eje X", columnas_numericas, key="x_3d")
        eje_y = st.selectbox("Eje Y", columnas_numericas, index=1, key="y_3d")
        eje_z = st.selectbox("Eje Z", columnas_numericas, index=2, key="z_3d")



st.subheader("🌲 Visualización Dinámica del Modelo")

with st.container(border=True,
                    width="stretch",
                    height="content",
                    horizontal_alignment="distribute",
                    vertical_alignment="top"):


    col_4, col_5 = st.columns(spec=[0.5, 1])

    with col_4:

        with st.container(border=False,
                        width="stretch",
                        height="content",
                        horizontal_alignment="distribute",
                        vertical_alignment="top"):
            
            importance = pd.DataFrame({
                "Variable": columnas_numericas,
                "Importancia": model.feature_importances_
            })
            importance = importance.sort_values(
                by="Importancia",
                ascending=False
            )

            st.markdown("Importancia de Variables", text_alignment="center")

            fig_imp = px.bar(data_frame=importance,
                            x=importance["Importancia"],
                            y=importance["Variable"],
                            orientation="h",
                            text_auto=".3f",
                            color_discrete_sequence=sel_color,
                            template="plotly"
                            )
            fig_imp.update_layout(height=alto)
            st.plotly_chart(figure_or_data=fig_imp,
                            width="stretch"
                            )

    with col_5:

        with st.container(border=False,
                        width="stretch",
                        height="content",
                        horizontal_alignment="distribute",
                        vertical_alignment="top"):
        
            st.markdown(f"{tipo_grafico_model} ⮕ Probabilidades del Modelo", text_alignment="center")

            if tipo_grafico_model == "Barras":

                X = df[columnas_numericas]
                probs = model.predict_proba(X)[:, 1]
                df_prob = df.copy()
                df_prob["Probabilidad"] = probs

                fig_prob = px.histogram(data_frame=df_prob,
                                        x=df_prob["Probabilidad"],
                                        color=df_prob["Enfermedad"],
                                        nbins=20,
                                        color_discrete_sequence=sel_color,
                                        template="plotly"
                                        )
                fig_prob.update_layout(height=alto,
                                    yaxis_title_text='Pacientes'
                                    )
                st.plotly_chart(figure_or_data=fig_prob,
                                width="stretch"
                                )
            
            elif tipo_grafico_model == "Distribución 3D":                
                
                fig_3d = px.scatter_3d(data_frame=df,
                                    x=eje_x,
                                    y=eje_y,
                                    z=eje_z,
                                    color="Enfermedad",
                                    size="Edad",
                                    opacity=0.7,
                                    color_discrete_sequence=sel_color,
                                    template="plotly"
                                    )

                fig_3d.update_layout(height=alto + 200)

                st.plotly_chart(fig_3d, 
                                width="stretch")


    
  







