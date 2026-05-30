import streamlit as st
import pandas as pd
import graphviz as gz
import seaborn as sns
from matplotlib import pyplot as plt
from pickle import dump, load
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import (accuracy_score,
                             recall_score,
                             f1_score,
                             roc_auc_score,                             
                             confusion_matrix, 
                             ConfusionMatrixDisplay, 
                             RocCurveDisplay, 
                             PrecisionRecallDisplay)

# Ruta Raíz en Colab añadimos al final -> / 
#PATH = "/content/drive/MyDrive/SMEC658/"
# Ruta Raíz local
PATH = ""

# Función para el menú lateral
def generarMenu():
    # Barra lateral
    with st.sidebar:
        # Esto es de diseño
        col_1, col_2 = st.columns(spec=2)
        with col_1:
            logo = Image.open(PATH + "media/logo_page.png")
            st.image(image=logo,
                     width=80)
        with col_2:
            st.title("SMEC")    
        
        st.page_link('app.py', label='Inicio', icon='🏠',)
        st.page_link('pages/pronostico.py', label='Diagnóstico y pronóstico', icon='💚')
        st.page_link('pages/arboles.py', label='Árboles del modelo', icon='🌳')
        st.page_link('pages/graficos.py', label='Análisis gráfico', icon='📊')
    
    # vamos y la importamos desde app.py

# Función para cargar los datos 
@st.cache_data
def cargar_datos():    
    PATH = "data/datos_pacientes_2.csv"
    df = pd.read_csv(filepath_or_buffer=PATH,
                     encoding="utf-8")
    return df


# Método para el análisis inicial de los datos 
def eda(df: pd.DataFrame):

    # Expander para no saturar la vista con todos los datos
    with st.expander(label="Datos de los pacientes",
                     icon="📋",
                     expanded=False):      

        # Mostrar los datos
        st.dataframe(data=df,
                     hide_index=True,
                     width="stretch",
                     height="stretch"
                     )
    
    # Correlación de variables con Pearson: 
    # + -> aumenta probabilidad de enfermar
    # - -> reduce probabilidad de enfermar
    # 0 -> poca relación lineal entre variables
    with st.expander(label="Matriz de Correlación",
                     icon="🗺",
                     expanded=False):
        
        # Normalizamos los datos (La edad no es necesario normalizar)
        df_norm = df.copy()
        df_norm["Enfermedad"] = df_norm["Enfermedad"].map({"SI": 1, "NO": 0})
        # Eliminamos Expediente (es solo un registro)
        df_corr = df_norm.drop(columns=["Expediente"])
        corr = df_corr.corr(method="pearson", numeric_only=True)
        
        # Creamos la figura
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(data=corr,
                    annot=True,
                    cmap="coolwarm",
                    fmt=".2f",
                    ax=ax
                    )
        
        st.pyplot(fig=fig)
    
    with st.expander(label="Importancia de Features",
                     icon="📤",
                     expanded=False):
        
        # Mostrar el orden de correlación
        corr_target = corr["Enfermedad"].sort_values(ascending=False)
        st.dataframe(corr_target)


# Método para el análisis estadístico
def estadistico(df: pd.DataFrame):

    # Opcional - parámetros genéricos
    ancho_st = "stretch"
    alto_st = "stretch"
    ancho_co = "content"
    alto_co = "content"
    bordes = True

    with st.expander(label="Datos Generales",
                     icon="⚕️",
                     expanded=False):       
                
        # Total de datos
        total = len(df)

        # Género
        contar_genero = df["Género"].value_counts()
        feme = contar_genero.get(0, 0)
        masc = contar_genero.get(1, 0)
        pr_feme = feme / total
        pr_masc = masc / total

        # Enfermedad
        contar_diagnos = df["Enfermedad"].value_counts()
        diag_si = contar_diagnos.get("SI", 0)
        diag_no = contar_diagnos.get("NO", 0)
        pr_diag_si = diag_si / total
        pr_diag_no = diag_no / total        

        # Enfermedad vs Género
        df_si = df[df["Enfermedad"] == "SI"]
        total_si = len(df_si)
        contar_genero_si = df_si["Género"].value_counts()
        feme_si = contar_genero_si.get(0, 0)
        masc_si = contar_genero_si.get(1, 0)
        pr_feme_si = feme_si / total_si if total_si else 0
        pr_masc_si = masc_si / total_si if total_si else 0

        # Orden espacial
        col_1, col_2, col_3 = st.columns(spec=3,
                                        gap="small",
                                        vertical_alignment="top")

        # Métricas

        with col_1:

            st.metric(label="🚺 Cantidad de Mujeres",
                      value=feme,
                      delta=f"{pr_feme:.2%}",
                      delta_color="violet",
                      delta_arrow="up",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
            
            st.metric(label="🚹 Cantidad de Hombres",
                      value=masc,
                      delta=f"{pr_masc:.2%}",
                      delta_color="blue",
                      delta_arrow="down",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
        
        with col_2:

            st.metric(label="🤒 Diagnósticos Positivos",
                      value=diag_si,
                      delta=f"{pr_diag_si:.2%}",
                      delta_color="red",
                      delta_arrow="up",
                      delta_description="SMEC ➕",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
            
            st.metric(label="🤗 Diagnósticos Negativos",
                      value=diag_no,
                      delta=f"{pr_diag_no:.2%}",
                      delta_color="green",
                      delta_arrow="up",
                      delta_description="SMEC ➖",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
        
        with col_3:

            st.metric(label="🤕 Mujeres / Positivos", 
                    value=f"{pr_feme_si:.2%}",                     
                    delta=f"{feme_si:d}",
                    delta_color="orange", 
                    delta_arrow="up",
                    delta_description="SMEC 🚺",                 
                    border=bordes, 
                    width=ancho_st,
                    height=alto_st
                    )
            
            st.metric(label="😷 Hombres / Positivos", 
                    value=f"{pr_masc_si:.2%}",                     
                    delta=f"{masc_si:d}",
                    delta_color="yellow", 
                    delta_arrow="off",
                    delta_description="SMEC 🚹",                 
                    border=bordes, 
                    width=ancho_st,
                    height=alto_st
                    )

    with st.expander(label="Datos Estadísticos",
                     icon="📈",
                     expanded=False):    

        # Total de datos
        total = len(df)   
                
        # Estadísticas Edad
        edad_media = df["Edad"].mean()
        edad_mediana = df["Edad"].median()
        edad_moda = df["Edad"].mode()[0]  #[0] primera moda si no es unimodal
        
        edad_std = df["Edad"].std()
        edad_var = df["Edad"].var()
        
        edad_min = df["Edad"].min()
        edad_max = df["Edad"].max()

        edad_q1 = df["Edad"].quantile(0.25)
        edad_q3 = df["Edad"].quantile(0.75)
        edad_iqr = edad_q3 - edad_q1

        edad_coef_var = (edad_std / edad_media) * 100

        # Prevalencias        
        prev_ica = (
            df["ICA"].mean()
        )
        prev_hiperten = (
            df["Hipertensión"].mean()
        )
        prev_tabaco = (
            df["Tabaco"].mean()
        )
        prev_alcohol = (
            df["Alcohol"].mean()
        )

        # Edad por enfermedad 
        edad_si = df.loc[df["Enfermedad"] == "SI", "Edad"]
        edad_no = df.loc[df["Enfermedad"] == "NO", "Edad"]
        edad_media_si = edad_si.mean()
        edad_media_no = edad_no.mean()

        # Métricas

        col_1, col_2, col_3 = st.columns(spec=3)

        with col_1:

            st.metric(label="📊 Edad Promedio",
                      value=f"{edad_media:.1f} años",
                      delta=f"Mediana: {edad_mediana:.0f}",
                      delta_color="orange",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
            
            st.metric(label="🎯 Moda de Edad",
                      value=f"{edad_moda} años",
                      delta=f"Rango: {edad_min} - {edad_max}",
                      delta_color="gray",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
        
        with col_2:

            st.metric(label="📉 Desviación Estándar (Edad)",
                      value=f"{edad_std:.2f}",
                      delta=f"Varianza: {edad_var:.2f}",
                      delta_color="blue",
                      delta_description=f"Coef={edad_coef_var:.2f}",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
            
            st.metric(label="📦 Rango Intercuartílico (Edad)",
                      value=f"{edad_iqr:.1f}",
                      delta=f"Q1={edad_q1:.0f} | Q3={edad_q3:.0f}",
                      delta_color="yellow",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
        
        with col_3:

            st.metric(label="📏 Índice de Cintura Alta (ICA)",
                      value=f"{prev_ica:.2%}",
                      delta=f"Alcohol: {prev_alcohol:.2%}",
                      delta_color="inverse",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )

            st.metric(label="🩺 Hipertensión",
                      value=f"{prev_hiperten:.2%}",
                      delta=f"Tabaco: {prev_tabaco:.2%}",
                      delta_color="inverse",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st                
                     )
        
        st.divider()

        col_4, col_5, col_6 = st.columns(spec=3)

        with col_4:

            st.metric(label="🚑 Edad Promedio Positivos",
                      value=f"{edad_media_si:.1f} años",
                      delta=f"Enfermedad -> SI",
                      delta_color="inverse",
                      chart_data=edad_si.tolist(),
                      chart_type="line",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
        
        with col_5:
        
            st.metric(label="❤️‍🩹 Edad Promedio Negativos",
                      value=f"{edad_media_no:.1f} años",
                      delta=f"Enfermedad -> NO",
                      delta_color="normal",
                      chart_data=edad_no.tolist(),
                      chart_type="line",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )
               
        with col_6:

            factores = list(df.drop(columns=["Expediente", "Enfermedad", "Género", "Edad"]))
            df_new = df[factores].copy()
            df_new["Riesgo Total"] = df_new[factores].sum(axis=1)  # Contamos cada enfermedad
            riesgo_media = df_new["Riesgo Total"].mean()
            riesgo_max = df_new["Riesgo Total"].max()
            contar_factores = df_new["Riesgo Total"].value_counts().sort_values(ascending=True)

            st.metric(label="⚰️ Índice de Riesgo Acumulado",
                      value=f"{riesgo_media:.2f}",
                      delta=f"Máximo: {riesgo_max}",
                      delta_color="violet",
                      chart_data=contar_factores.tolist(),
                      chart_type="line",
                      border=bordes,
                      width=ancho_st,
                      height=alto_st
                      )


# Función para cargar modelo si existe
@st.cache_resource
def cargar_modelo():    
    MODEL_PATH = PATH + "data/model.sav"
    try:
        model = load(open(MODEL_PATH, "rb"))
        return model
    except:
        return None

# Función para modelar
def modelar(df: pd.DataFrame, model):

    # Normalizamos
    df["Enfermedad"] = df["Enfermedad"].map({"SI": 1, "NO": 0})

    scaler = MinMaxScaler()
    df["Edad"] = scaler.fit_transform(df[["Edad"]])   

    # Features
    X = df.iloc[:,2:]
    # Target
    y = df.iloc[:,1]

    # Split de Datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creamos el modelo o lo leemos si existe
    if model is None:
        model = RandomForestClassifier(n_estimators=100,
                                    criterion="gini",
                                    max_depth=5,
                                    max_samples=2/3,
                                    max_features="sqrt",
                                    bootstrap=True,
                                    oob_score=True                                   
                                    )
        
        model.fit(X_train, y_train)

        # Guardar modelo
        MODEL_PATH = PATH + "data/model.sav"
        archivo_model = open(MODEL_PATH, "wb")
        dump(model, archivo_model)
        archivo_model.close()

    # Predicción
    y_predict = model.predict(X_test)
    # Probabilidades
    y_prob = model.predict_proba(X_test)[:, 1]

    # Precisión
    accuracy = accuracy_score(y_test, y_predict)
    # recall
    recall = recall_score(y_test, y_predict)
    # f1_
    f1 = f1_score(y_test, y_predict)
    # Roc_curve
    roc = roc_auc_score(y_test, y_prob)

    # Matriz de confusión
    conf_matriz = confusion_matrix(y_test, y_predict)


    # Mostramos el proceso
    with st.expander(label="Datos del Modelo",
                     icon="💊",
                     expanded=False):
        
        st.markdown("**Preparación de las variables para el Modelo**")

        col_1, col_2 = st.columns(spec=[1,0.3])

        with col_1:
            features_text = ", ".join(list(X.columns))
            st.info(f"{features_text}", title="FEATURES")
        
        with col_2:
            target_text = y.name
            st.success(f"{target_text}", title="TARGET")
        
        st.divider()
        
        st.markdown("**Conjuntos de entrenamiento y prueba**")

        col_3, col_4, col_5, col_6 = st.columns(spec=4)

        with col_3:
            st.error(f"{X_train.shape[0]}", title="X_TRAIN:")
        
        with col_4:
            st.warning(f"{X_test.shape[0]}", title="X_TEST:")
        
        with col_5:
            st.error(f"{y_train.shape[0]}", title="y_TRAIN:")
        
        with col_6:
            st.warning(f"{y_test.shape[0]}", title="y_TEST:")
        
        st.divider()
        
        st.markdown("**Resultados del Modelo**")

        col_7, col_8, col_9, col_10 = st.columns(spec=4)

        with col_7:
            st.success(f"{accuracy:.2%}", title="Accuracy")
        
        with col_8:
            st.success(f"{recall:.2%}", title="Recall")
        
        with col_9:
            st.success(f"{f1:.2%}", title="f1 Score")
        
        with col_10:
            st.success(f"{roc:.2%}", title="Roc AUC")
        
        st.divider()

        st.markdown("**Gráficos del Modelo**")

        col_11, col_12, col_13 = st.columns(spec=3)

        with col_11:
    
            st.markdown(f"**Matriz de Confusión**", text_alignment="center")

            fig, ax = plt.subplots(figsize=(8, 6))
            disp = ConfusionMatrixDisplay(confusion_matrix=conf_matriz, 
                                            display_labels=["NO", "SI"])
            disp.plot(ax=ax)            
            st.pyplot(fig)
        
        with col_12:
    
            st.markdown(f"**Área bajo la curva**", text_alignment="center")

            fig, ax = plt.subplots(figsize=(8, 6))
            RocCurveDisplay.from_predictions(
                y_test,
                y_prob,
                ax=ax
            )
            st.pyplot(fig)
        
        with col_13:
    
            st.markdown(f"**Curva de precisión Recall**", text_alignment="center")

            fig, ax = plt.subplots(figsize=(8, 6))
            PrecisionRecallDisplay.from_predictions(
                y_test,
                y_prob,
                ax=ax
            )
            st.pyplot(fig)

# Función para predecir nuevos pacientes
def predecir(df_new: pd.DataFrame):

    model = cargar_modelo()
    df_model = cargar_datos()    

    # Normalizamos
    df_new["Género"] = df_new["Género"].map({"Masculino": 1, "Femenino": 0})

    scaler = MinMaxScaler()
    scaler.fit(df_model[["Edad"]])

    df_new["Edad"] = scaler.transform(df_new[["Edad"]]) 
    
    #st.write(df_model)
    #st.dataframe(df_new)

    predict = model.predict(df_new)
    return predict


# NO MOSTRAR ESTA - ES LA SENCILLA
# Función para dibujar árboles
def arboles(model, columnas, num: int):
    st.caption('**Importante: Los árboles pueden variar, ya que cada ejección permite una predicción diferente.')
    
    dot_data = export_graphviz(model.estimators_[num],
                               feature_names=columnas,
                               max_depth=model.max_depth,
                               filled=True,
                               impurity=True,
                               proportion=True,
                               special_characters=True,
                               rounded=False)
    
    graph = gz.Source(dot_data)
    return graph


# MOSTRAR ESTA - LA INTERACTIVA
# Función para dibujar árboles interactivos
def arboles_interac(model, columnas, num: int):
    st.caption('**Importante: Los árboles pueden variar, ya que cada ejección permite una predicción diferente.')
    
    dot_data = export_graphviz(
        decision_tree=model.estimators_[num],
        feature_names=columnas,
        filled=True,
        impurity=True,
        proportion=True,
        special_characters=True,
        rounded=True
    )

    graph = gz.Source(dot_data)

    # Convertimos a SVG
    svg = graph.pipe(format="svg").decode("utf-8")

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

    #components.html(html, height=500, scrolling=True)
    st.iframe(html, height=500)