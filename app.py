import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Dashboard de Análisis", layout="wide")
st.title("📊 Sistema de Análisis de Datos Automatizado")
st.markdown("Herramienta interactiva para exploración y visualización de datos")

st.write("Sube un archivo CSV para analizarlo 👇")

archivo = st.file_uploader("Elige un archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo, sep=None, engine='python')
    df = df.dropna()

    st.subheader("Vista previa de los datos")
    st.write(df.head())

    st.subheader("Resumen del dataset")
    col1, col2, col3 = st.columns(3)
    col1.metric("Filas", df.shape[0])
    col2.metric("Columnas", df.shape[1])
    col3.metric("Valores nulos", df.isnull().sum().sum())

    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    st.subheader("Filtros")
    columnas_categoricas = df.select_dtypes(include=['object']).columns
    if len(columnas_categoricas) > 0:
        columna_filtro = st.selectbox("Filtrar por columna", columnas_categoricas)
        valores = df[columna_filtro].unique()
        valor_seleccionado = st.selectbox("Selecciona valor", valores)
        df = df[df[columna_filtro] == valor_seleccionado]
        st.write(f"Datos filtrados por {valor_seleccionado}")
        st.download_button(
            label="Descargar datos filtrados",
            data=df.to_csv(index=False),
            file_name="datos_filtrados.csv",
            mime="text/csv"
            )

    if len(columnas_numericas) > 0:
        columna_seleccionada = st.selectbox(
            "Selecciona una columna numérica",
            columnas_numericas
        )

        promedio = df[columna_seleccionada].mean()
        minimo = df[columna_seleccionada].min()
        maximo = df[columna_seleccionada].max()

        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio", round(promedio, 2))
        col2.metric("Mínimo", minimo)
        col3.metric("Máximo", maximo)
        st.subheader("Visualización automática")
        valores_unicos = df[columna_seleccionada].nunique()
        fig, ax = plt.subplots()
        # Si tiene pocos valores únicos → categórico
        if valores_unicos <= 10:
            conteo = df[columna_seleccionada].value_counts()
            # Si son pocas categorías → pastel
            if len(conteo) <= 5:
                ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%')
                ax.set_title("Gráfica de pastel")
            else:
                ax.bar(conteo.index.astype(str), conteo.values)
                ax.set_title("Gráfica de barras")
        # Si tiene muchos valores → numérico continuo
        else:
            ax.hist(df[columna_seleccionada], bins=20)
            ax.axvline(promedio, linestyle='dashed')
            ax.set_title("Histograma")
            st.pyplot(fig)
        st.subheader("Gráfica de dispersión")
        columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
        if len(columnas_numericas) >= 2:
            col_x = st.selectbox("Selecciona eje X", columnas_numericas, key="x")
            col_y = st.selectbox("Selecciona eje Y", columnas_numericas, key="y")
            fig2, ax2 = plt.subplots()
            ax2.scatter(df[col_x], df[col_y])
            ax2.set_xlabel(col_x)
            ax2.set_ylabel(col_y)
            ax2.set_title("Dispersión")
            st.pyplot(fig2)
    else:
        st.write("No hay columnas numéricas en el archivo.")