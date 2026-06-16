import streamlit as st
import requests
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

st.title("⚽ Quiniela Mundial 2026")
nombre = st.text_input("Ingrese su nombre para cargar/continuar:").strip().title()

# Carga de datos si existen
if nombre:
    res = requests.get(URL, params={"nombre": nombre})
    if res.status_code == 200:
        data = res.json()
        if data.get("status") == "success":
            st.success("Progreso cargado con éxito.")

# 1. Fase de Grupos
res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
        res_g[g] = {"1": o1, "2": o2}

# 2. Selección de mejores terceros
st.subheader("🥉 Selección de los 8 mejores terceros")
ya_clasificados = [res_g[g]["1"] for g in GRUPOS] + [res_g[g]["2"] for g in GRUPOS]
opciones_disponibles = [e for grp in GRUPOS.values() for e in grp if e not in ya_clasificados]

terceros_seleccionados = []
cols = st.columns(4)
for i in range(8):
    elegidos = [terceros_seleccionados[j] for j in range(len(terceros_seleccionados))]
    lista = [e for e in opciones_disponibles if e not in elegidos]
    t = cols[i % 4].selectbox(f"3ro #{i+1}", [None] + lista, key=f"tercero_{i}")
    if t: terceros_seleccionados.append(t)

# 3. Dieciseisavos (Cruces dinámicos)
st.subheader("🥅 Dieciseisavos de Final (Eliminación Directa)")
partidos_resultados = {}
cruces = [
    ("A", "1", "B", "2"), ("B", "1", "A", "2"), ("C", "1", "D", "2"), ("D", "1", "C", "2"),
    ("E", "1", "F", "2"), ("F", "1", "E", "2"), ("G", "1", "H", "2"), ("H", "1", "G", "2"),
    ("I", "1", "J", "2"), ("J", "1", "I", "2"), ("K", "1", "L", "2"), ("L", "1", "K", "2"),
    ("A", "2", "C", "1"), ("B", "2", "D", "1"), ("E", "2", "G", "1"), ("F", "2", "H", "1")
]

for i, (g1, pos1, g2, pos2) in enumerate(cruces):
    eq1, eq2 = res_g[g1][pos1], res_g[g2][pos2]
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**D{i+1}:** {eq1} vs {eq2}")
    g1_val = c2.number_input(f"Goles {eq1}", min_value=0, key=f"g1_{i}")
    g2_val = c3.number_input(f"Goles {eq2}", min_value=0, key=f"g2_{i}")
    
    if g1_val == g2_val:
        ganador = st.radio(f"Ganador penaltis {eq1} vs {eq2}", [eq1, eq2], key=f"pen_{i}", horizontal=True)
        partidos_resultados[f"D{i+1}"] = f"{eq1} {g1_val}-{g2_val} (Gana {ganador})"
    else:
        partidos_resultados[f"D{i+1}"] = f"{eq1} {g1_val}-{g2_val} {eq2}"

# 4. Guardado
def enviar(estado):
    payload = {
        "nombre": nombre, "estado": estado,
        "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}),
        **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
    }
    return requests.post(URL, data=payload)

col1, col2 = st.columns(2)
if col1.button("💾 GUARDAR BORRADOR"):
    if nombre:
        enviar("En Edición")
        st.info("Borrador guardado. Puedes volver más tarde buscando por tu nombre.")
    else: st.error("Ingresa tu nombre.")
if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
    if nombre:
        enviar("Definitiva")
        st.success("¡Enviada!")
    else: st.error("Ingresa tu nombre.")
