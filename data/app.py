import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt

# Cargar datos
archivo_estudiantes = "estudiantes 1 1.csv"
archivo_preguntas = "preguntas 1 1.csv"

estudiantes = pd.read_csv(archivo_estudiantes, encoding="latin1")
preguntas = pd.read_csv(archivo_preguntas, encoding="latin1")

# Crear carpeta para respuestas si no existe
if not os.path.exists("data"):
    os.makedirs("data")

# Título de la aplicación
st.title("Evaluación de Estudiantes")

# Menú de opciones
menu = ["Evaluar estudiantes", "Ver reportes"]
opcion = st.sidebar.selectbox("Menú", menu)

if opcion == "Evaluar estudiantes":
    maestro = st.sidebar.text_input("Nombre del maestro")

    if maestro:
        curso = st.selectbox("Selecciona un curso", estudiantes["curso"].unique())

        if curso:
            estudiantes_curso = estudiantes[estudiantes["curso"] == curso]
            estudiante = st.selectbox("Selecciona un estudiante", estudiantes_curso["nombre"].unique())
            materia = st.selectbox("Selecciona una materia", preguntas["materia"].unique())
            preguntas_materia = preguntas[preguntas["materia"] == materia]

            respuestas = []
            for _, row in preguntas_materia.iterrows():
                pregunta = row["texto"]
                respuesta = st.radio(pregunta, [
                    "Incumplimiento",
                    "Incumplimiento parcial",
                    "Cumplimiento",
                    "Excede cumplimiento"
                ], key=pregunta)
                respuestas.append({
                    "maestro": maestro,
                    "curso": curso,
                    "estudiante": estudiante,
                    "materia": materia,
                    "pregunta": pregunta,
                    "respuesta": respuesta
                })

            if st.button("Guardar respuestas"):
                archivo_respuestas = f"data/respuestas_{maestro.replace(' ', '_')}.csv"
                if os.path.exists(archivo_respuestas):
                    df_respuestas = pd.read_csv(archivo_respuestas, encoding="latin1")
                    ya_existe = not df_respuestas[
                        (df_respuestas["estudiante"] == estudiante) &
                        (df_respuestas["materia"] == materia)
                    ].empty
                else:
                    df_respuestas = pd.DataFrame(columns=["maestro", "curso", "estudiante", "materia", "pregunta", "respuesta"])
                    ya_existe = False

                if ya_existe:
                    st.error("Ya has evaluado a este estudiante para esta materia.")
                else:
                    df_nuevas = pd.DataFrame(respuestas)
                    df_respuestas = pd.concat([df_respuestas, df_nuevas], ignore_index=True)
                    df_respuestas.to_csv(archivo_respuestas, index=False, encoding="latin1")
                    st.success("Respuestas guardadas exitosamente.")

elif opcion == "Ver reportes":
    maestro = st.sidebar.text_input("Nombre del maestro para ver reportes")
    if maestro:
        archivo_respuestas = f"data/respuestas_{maestro.replace(' ', '_')}.csv"
        if os.path.exists(archivo_respuestas):
            df = pd.read_csv(archivo_respuestas, encoding="latin1")
            estudiante = st.selectbox("Selecciona un estudiante", df["estudiante"].unique())
            materia = st.selectbox("Selecciona una materia", df["materia"].unique())

            if estudiante and materia:
                df_filtrado = df[(df["estudiante"] == estudiante) & (df["materia"] == materia)]
                conteo_respuestas = df_filtrado["respuesta"].value_counts()

                fig, ax = plt.subplots()
                ax.pie(conteo_respuestas, labels=conteo_respuestas.index, autopct='%1.1f%%')
                ax.axis('equal')
                st.pyplot(fig)
        else:
            st.warning("No hay respuestas guardadas para este maestro.")

# Pie de página con el nombre del autor
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: gray;
        }
    </style>
    <div class="footer">
        <p>Steven Nehemias Polanco Rojas, IT SUPPORT</p>
    </div>
""", unsafe_allow_html=True)
