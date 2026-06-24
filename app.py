import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Quiniela FIFA 2026", layout="wide")

URL = "https://script.google.com/macros/s/AKfycbzCQ5FcILnKcosplY2PASwTLeLko9YJRrAC602PkBJ1ojdg_cSEUPJsFAATf5XM0ZRRMw/exec"

GRUPOS = {
    "A": ["México", "Sudáfrica", "Corea del Sur", "Chequia"], "B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"], "D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "E": ["Alemania", "Costa de Marfil", "Ecuador", "Curazao"], "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"], "H": ["España", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "I": ["Francia", "Senegal", "Noruega", "Irak"], "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"], "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

if 'logueado' not in st.session_state:
    st.session_state.update({'logueado': False, 'usuario': "", 'datos': None, 'es_admin': False, 'es_definitiva': False})

st.title("⚽ Quiniela Mundial 2026")

# --- LOGIN / REGISTRO ---
if not st.session_state.logueado:
    tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
    with tab1:
        nombre = st.text_input("Nombre:", key="login_n").strip().title()
        password = st.text_input("Contraseña:", type="password", key="login_p")
        if st.button("Ingresar"):
            res = requests.get(URL, params={"nombre": nombre})
            if res.status_code == 200 and res.json().get("status") == "success":
                datos = res.json().get("datos")
                if datos[1] == password:
                    st.session_state.update({'logueado': True, 'usuario': nombre, 'datos': datos, 'es_admin': res.json().get("es_admin", False), 'es_definitiva': (datos[16] == "Definitiva")})
                    st.rerun()
                else: st.error("Contraseña incorrecta")
            else: st.error("Usuario no encontrado")
    with tab2:
        new_n = st.text_input("Nombre de registro:", key="reg_n").strip().title()
        new_p = st.text_input("Contraseña de registro:", type="password", key="reg_p")
        if st.button("Registrarse"):
            res = requests.post(URL, data={"nombre": new_n, "password": new_p, "estado": "En Edición"})
            if res.status_code == 200: st.success("¡Registro exitoso!")
    st.stop()

# --- ESTRUCTURA DE PESTAÑAS ---
tab_grupos, tab_terceros, tab_final = st.tabs(["1. Grupos", "2. Mejores Terceros", "3. Fases Finales"])

es_def = st.session_state.es_definitiva
datos = st.session_state.datos

# --- PESTAÑA 1: GRUPOS ---
res_g = {}
with tab_grupos:
    for i, (g, eq) in enumerate(GRUPOS.items()):
        val = datos[2 + i] if datos and len(datos) > (2 + i) else ""
        opts = val.split(", ") if ", " in val else [None, None]
        with st.expander(f"Grupo {g}"):
            c1, c2 = st.columns(2)
            o1 = c1.selectbox(f"1ero {g}", eq, index=eq.index(opts[0]) if opts[0] in eq else 0, key=f"g{g}_1", disabled=es_def)
            rest = [e for e in eq if e != o1]
            o2 = c2.selectbox(f"2do {g}", rest, index=rest.index(opts[1]) if opts[1] in rest else 0, key=f"g{g}_2", disabled=es_def)
            res_g[g] = {"1": o1, "2": o2}

# --- PESTAÑA 2: MEJORES TERCEROS ---
with tab_terceros:
    st.write("Selecciona los 8 mejores terceros (excluyendo a los clasificados 1ero y 2do):")
    terceros_posibles = []
    for g, sel in res_g.items():
        terceros_posibles.extend([e for e in GRUPOS[g] if e not in [sel['1'], sel['2']]])
    
    terceros_sel = st.multiselect("Elige 8 equipos:", terceros_posibles, max_selections=8, disabled=es_def)

# --- PESTAÑA 3: FASES FINAL ---
with tab_final:
    st.info("Próximamente: Configuración de cruces para 16avos, Octavos, Cuartos, Semis y Final.")

# --- GUARDADO ---
def enviar_datos(estado):
    payload = {
        "nombre": st.session_state.usuario,
        "password": st.session_state.datos[1],
        "estado": estado,
        "octavos": json.dumps({"terceros": terceros_sel}),
        **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
    }
    requests.post(URL, data=payload)

if not es_def:
    if st.button("💾 Guardar Todo"):
        enviar_datos("En Edición")
        st.success("Guardado correctamente.")
        st.rerun()
