import streamlit as st
import pickle
import pandas as pd
from create_model_fin import create_model_fin
from streamlit_option_menu import option_menu

import os

# Cambiar fondo de la aplicación, fondo de la barra lateral y color del texto con CSS
page_bg_img = '''
<style>
/* Fondo de la aplicación y colores de texto */
.stApp {
    background-image: url("https://p4.wallpaperbetter.com/wallpaper/185/696/989/dark-blur-abstract-minimalism-wallpaper-preview.jpg");
    background-size: cover;
    background-attachment: fixed;
    color: white;
}

/* Fondo de la barra lateral */
.stSidebar {
    background-color: #262626; /* Fondo oscuro para la barra lateral */
    background-image: url("https://p4.wallpaperbetter.com/wallpaper/185/696/989/dark-blur-abstract-minimalism-wallpaper-preview.jpg");
    background-size: cover;
    background-attachment: fixed;
    color: #e6e6e6; /* Color del texto de la barra lateral */
}

/* Borde y sombra en la barra lateral */
.stSidebar > div:first-child {
    border: 2px solid #FFFFFF; /* Borde blanco */
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
}

/* Estilo del menú de opciones para eliminar el fondo blanco */
.css-1v0mbdj, .css-1b2axud, .css-1ydp377 {
    background-color: transparent !important; /* Fondo transparente para el menú de opciones */
    color: #e6e6e6 !important; /* Asegura el color del texto */
    border: none !important; /* Sin borde */
    box-shadow: none !important; /* Elimina cualquier sombra */
}

/* Estilos de los títulos y etiquetas */
h1, h2, h3, h4, h5, h6, p, label, .stTextInput, .stButton {
    color: #e6e6e6 !important;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)




ruta = r'C:/Users/juanjo/Downloads/PC2-Ciencia de datos-20241106T165308Z-001/PC2-Ciencia de datos'
os.chdir(ruta)


with st.sidebar:
    selected = option_menu(
        menu_title="Predicción de salud del paciente",
        options=["Inicio", "Predict"],
        icons=["bi bi-house", "bi bi-hospital"],
        menu_icon="bi bi-heart-pulse-fill"
    )



current_directory = os.path.abspath(os.getcwd())
file_path_file  = os.path.join(current_directory, 'net_class_smoker.pkl')
data = pd.read_pickle(file_path_file)

modelo_final = data["model"]
X_train = data["X_train"]
preprocessor = data["preprocessor"]
labels = data["labels"]

if selected == "Inicio":
    st.title("Información sobre Enfermedades Coronarias")
    st.write("""
        Las enfermedades coronarias, también conocidas como enfermedades del corazón, son condiciones en las que el flujo de sangre al corazón se ve restringido, lo que puede provocar ataques cardíacos y otros problemas graves. 
        Los factores de riesgo incluyen la edad, el género, los antecedentes familiares, el tabaquismo, la presión arterial alta, el colesterol alto, la diabetes y la obesidad.
        """)
    
    # Cargar y visualizar el archivo .txt
    try:
        data_txt_path = os.path.join(current_directory, 'Data.txt')  # Asegúrate de que el archivo esté en el mismo directorio o ajusta la ruta según sea necesario
        data_txt = pd.read_csv(data_txt_path, sep='\t')  # Cambia el separador si es necesario
        st.write("Datos:")
        st.dataframe(data_txt)
    except FileNotFoundError:
        st.error("El archivo de datos .txt no se encontró. Por favor, asegúrese de que el archivo esté en la ruta especificada.")




if selected == "Predict":

    st.title("Determinar el riesgo de desarrollar una enfermedad coronaria en el paciente")
    st.write("""### Se necesita la siguiente información""")

    Mapeo = {"Femenino": "Female",
             "Masculino": "Male",
             "Sí": "1",
             "No": "0",
             "Sí fumador": "Yes",
             "No fumador": "No",
             "Primaria completa": "C",
             "Secundaria completa": "HS",
             "Universidad incompleta": "SC",
             "Universidad completa": "SHS"}

    Sexo = ("Femenino", "Masculino")
    Sexo = st.selectbox("Seleccione el sexo", Sexo)
    Sexo = Mapeo.get(Sexo)

    Edad = st.slider("Edad del paciente", 32, 70, 45)
    
    Educacion = ("Primaria completa", "Secundaria incompleta", 
                "Secundaria completa", "Alguna universidad")
    Educacion = st.radio("Nivel de educación", Educacion)
    Educacion = Mapeo.get(Educacion)

    Fumador = ("Sí fumador", "No fumador")
    Fumador = st.selectbox("¿El paciente fuma actualmente?", Fumador)
    Fumador = Mapeo.get(Fumador)

    Cigarros = 0

    if Fumador == "Yes":
        Cigarros = st.slider("Cigarrillos por día", 1, 70, 1)

    Presion_Arterial = ("Sí", "No")
    Presion_Arterial = st.selectbox("¿Usa medicamentos para controlar su presión arterial?", Presion_Arterial)
    Presion_Arterial = Mapeo.get(Presion_Arterial)
    
    Presion_Arterial_Sistolica = st.number_input("Presión arterial sistólica (el número más alto en una lectura de presión arterial)")
    
    Presion_Arterial_Diastolica = st.number_input("Presión arterial diastólica (el número más bajo en una lectura de presión arterial)")

    Cerebrovascular = ("Sí", "No")
    Cerebrovascular = st.selectbox("¿Cuenta con historial de accidentes cerebrovasculares?", Cerebrovascular)
    Cerebrovascular = Mapeo.get(Cerebrovascular)

    Hipertension = ("Sí", "No")
    Hipertension = st.selectbox("¿Presenta hipertensión?", Hipertension)
    Hipertension = Mapeo.get(Hipertension)
    
    Diabetes = ("Sí", "No")
    Diabetes = st.selectbox("¿Presenta diabetes?", Diabetes)
    Diabetes = Mapeo.get(Diabetes)

    Glucosa = st.slider("Nivel de glucosa en sangre", 40, 394, 75)

    Colesterol = st.slider("Colesterol total en la sangre", 107, 696, 150)

    Masa_Corporal = st.number_input('Índice de masa corporal calculado')

    Frecuencia_Cardiaca = st.slider("Frecuencia cardíaca en reposo", 44, 143, 75)

    if st.button("Calcule si el paciente presenta riesgo de enfermedad"):
        dat_X = [[Sexo, Edad, Educacion, Fumador,  Cigarros, Presion_Arterial,
                Cerebrovascular, Hipertension, Diabetes, Colesterol, Presion_Arterial_Sistolica,
                Presion_Arterial_Diastolica, Masa_Corporal, Frecuencia_Cardiaca, Glucosa]]
        input_df = pd.DataFrame(dat_X, columns=['male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds', 'prevalentStroke', 'prevalentHyp',
                                                'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'])
        X_res = preprocessor.transform(input_df)
        X_res_df = pd.DataFrame(X_res, columns=labels).tail(1)
        pred1 = modelo_final.predict(X=X_res_df)
        pred2 = modelo_final.predict_proba(X=X_res_df)
        probabilidades_df = pd.DataFrame({
        "Riesgo": ['No presente', "Presente"],
        "Valor": [pred2[1], pred2[0]]
        })

        # Resultado visual con iconos y colores de alerta
        if pred1 == "NonDisease":
            st.success('Sin riesgo de desarrollar una enfermedad coronaria. :grin:')
        else:
            st.warning('Riesgo presente de desarrollar una enfermedad coronaria. :sweat:')

        st.write("Probabilidades:", probabilidades_df.set_index(probabilidades_df.columns[0]))
