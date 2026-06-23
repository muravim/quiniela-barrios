import streamlit as st
import requests
import json

st.set_page_config(page_title="Quiniela FIFA 2026", layout="wide")

# URL de tu script de Google Apps
URL = "https://script.google.com/macros/s/AKfycbzCQ5FcILnKcosplY2PASwTLeLko9YJRrAC602PkBJ1ojdg_cSEUPJsFAATf5XM0ZRRMw/exec"

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
    st.session_state.update({'logueado': False, 'usuario': "", 'datos': None, 'es_definitiva': False})

st.title("⚽ Quiniela Mundial 2026")

# --- LOGIN ---
if not st.session_state.logueado:
    nombre = st.text_input("Nombre:").strip().title()
    password = st.text_input("Contraseña:", type="password")
    if st.button("Ingresar"):
        res = requests.get(URL, params={"nombre": nombre, "pass": password})
        if res.status_code == 200 and res.json().get("status") == "success":
            st.session_state.update({'logueado': True, 'usuario': nombre, 'datos': res.json().get("datos"), 'es_definitiva': (res.json().get("datos")[16] == "Definitiva")})
            st.rerun()
        else: st.error("Usuario o contraseña incorrectos")
    st.stop()

# --- INTERFAZ PRINCIPAL ---
es_def = st.session_state.es_definitiva
if es_def: st.warning("🔒 QUINIELA DEFINITIVA: Solo visualización.")

# 1. Fase de Grupos
res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1", disabled=es_def)
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2", disabled=es_def)
        res_g[g] = {"1": o1, "2": o2}

# 2. Terceros
st.subheader("🥉 Mejores 8 Terceros")
terceros_seleccionados = []
cols = st.columns(4)
for i in range(8):
    t = cols[i % 4].selectbox(f"3ro #{i+1}", [None] + [e for grp in GRUPOS.values() for e in grp], key=f"tercero_{i}", disabled=es_def)
    if t: terceros_seleccionados.append(t)

# 3. Dieciseisavos
st.subheader("🥅 Dieciseisavos de Final")
partidos_resultados = {}
cruces = [("A", "1", "B", "2"), ("B", "1", "A", "2"), ("C", "1", "D", "2"), ("D", "1", "C", "2"),
          ("E", "1", "F", "2"), ("F", "1", "E", "2"), ("G", "1", "H", "2"), ("H", "1", "G", "2"),
          ("I", "1", "J", "2"), ("J", "1", "I", "2"), ("K", "1", "L", "2"), ("L", "1", "K", "2"),
          ("A", "2", "C", "1"), ("B", "2", "D", "1"), ("E", "2", "G", "1"), ("F", "2", "H", "1")]

for i, (g1, pos1, g2, pos2) in enumerate(cruces):
    eq1, eq2 = res_g[g1][pos1], res_g[g2][pos2]
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**D{i+1}:** {eq1} vs {eq2}")
    g1_v = c2.number_input(f"Goles {eq1}", min_value=0, key=f"g1_{i}", disabled=es_def)
    g2_v = c3.number_input(f"Goles {eq2}", min_value=0, key=f"g2_{i}", disabled=es_def)
    if g1_v == g2_v:
        gan = st.radio(f"Ganador penaltis {eq1} vs {eq2}", [eq1, eq2], key=f"pen_{i}", horizontal=True, disabled=es_def)
        partidos_resultados[f"D{i+1}"] = f"{eq1} {g1_v}-{g2_v} (Gana {gan})"
    else: partidos_resultados[f"D{i+1}"] = f"{eq1} {g1_v}-{g2_v} {eq2}"

# 4. Acciones
if not es_def:
    c1, c2 = st.columns(2)
    if c1.button("💾 GUARDAR BORRADOR"):
        requests.post(URL, data={"nombre": st.session_state.usuario, "estado": "En Edición", "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}), **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}})
        st.info("Guardado.")
    if c2.button("🚀 ENVIAR DEFINITIVA"):
        requests.post(URL, data={"nombre": st.session_state.usuario, "estado": "Definitiva", "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}), **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}})
        st.success("¡Enviada!")
        st.rerun()
