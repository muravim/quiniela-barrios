import streamlit as st
import requests
import json

st.set_page_config(page_title="Quiniela FIFA 2026", layout="wide")

# Sustituye con tu URL de Web App de Google Apps Script
URL = "TU_URL_DE_GOOGLE_SCRIPT_AQUI" 

GRUPOS = {
    "A": ["México", "Sudáfrica", "Corea del Sur", "Chequia"], "B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"], "D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "E": ["Alemania", "Costa de Marfil", "Ecuador", "Curazao"], "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"], "H": ["España", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "I": ["Francia", "Senegal", "Noruega", "Irak"], "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"], "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

# --- ESTADO DE SESIÓN ---
if 'logueado' not in st.session_state:
    st.session_state.update({'logueado': False, 'usuario': "", 'datos': None, 'es_admin': False, 'es_definitiva': False})

st.title("⚽ Quiniela Mundial 2026")

# --- LOGIN ---
if not st.session_state.logueado:
    nombre = st.text_input("Nombre:").strip().title()
    password = st.text_input("Contraseña:", type="password")
    if st.button("Ingresar"):
        res = requests.get(URL, params={"nombre": nombre})
        # Lógica simple de validación (el password debe estar en la columna B)
        if res.status_code == 200 and res.json().get("status") == "success":
            datos = res.json().get("datos")
            if datos[1] == password: # Columna B es password
                st.session_state.update({
                    'logueado': True, 
                    'usuario': nombre, 
                    'datos': datos, 
                    'es_admin': res.json().get("es_admin", False),
                    'es_definitiva': (datos[16] == "Definitiva")
                })
                st.rerun()
            else: st.error("Contraseña incorrecta")
        else: st.error("Usuario no encontrado")
    st.stop()

# --- PANEL ADMIN ---
if st.session_state.es_admin:
    with st.expander("🛠️ Panel de Administrador"):
        st.write("Bienvenido, Administrador.")
        if st.button("Desbloquear quinielas globales"):
            st.warning("Función de desbloqueo administrativo activa.")

# --- INTERFAZ ---
es_def = st.session_state.es_definitiva
if es_def: st.warning("🔒 QUINIELA DEFINITIVA: No se permiten cambios.")

res_g = {}
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1", disabled=es_def)
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2", disabled=es_def)
        res_g[g] = {"1": o1, "2": o2}

# --- GUARDADO ---
def enviar_datos(estado):
    payload = {
        "nombre": st.session_state.usuario,
        "estado": estado,
        "octavos": "{}", # Aquí iría tu JSON de partidos
        **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
    }
    requests.post(URL, data=payload)

if not es_def:
    col1, col2 = st.columns(2)
    if col1.button("💾 Guardar Borrador"):
        enviar_datos("En Edición")
        st.info("Borrador guardado.")
    if col2.button("🚀 ENVIAR DEFINITIVA"):
        enviar_datos("Definitiva")
        st.success("¡Quiniela enviada permanentemente!")
        st.rerun()
