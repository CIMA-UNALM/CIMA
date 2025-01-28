# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:36:51 2024

@author: USUARIO

"""

# -*- coding: utf-8 -*-
"""
Creado el miércoles 3 de junlo

Integrantes:



"""

import streamlit as st
import pickle
import pandas as pd
from create_model_fin import create_model_fin
from streamlit_option_menu import option_menu

import os
ruta = r'C:/Users/juanjo/Downloads/PC2-Ciencia de datos-20241106T165308Z-001/PC2-Ciencia de datos'
os.chdir(ruta)

st.sidebar.image("Descarga.png", use_column_width=True)

with st.sidebar:
    selected = option_menu(
        menu_title="Predicción de salud del paciente",
        options=["Predict"],
        icons=["bi bi-hospital"],
        menu_icon="bi bi-heart-pulse-fill"
    )

current_directory = os.path.abspath(os.getcwd())
file_path_file  = os.path.join(current_directory, 'net_class_smoker.pkl')
data = pd.read_pickle(file_path_file)

modelo_final = data["model"]
X_train = data["X_train"]
preprocessor = data["preprocessor"]
labels = data["labels"]

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