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
    "K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"], "L": ["Ing ইংল্যান্ড", "Croacia", "Ghana", "Panamá"]
}

st.title("⚽ Quiniela Mundial 2026")
nombre = st.text_input("Ingrese su nombre para cargar progreso:").strip().title()

datos_guardados = None
if nombre:
    res = requests.get(URL, params={"nombre": nombre})
    if res.status_code == 200:
        data = res.json()
        if data.get("status") == "success": datos_guardados = data["datos"]

res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
        res_g[g] = {"1": o1, "2": o2}

st.subheader("🥉 Selección de los 8 mejores terceros")
terceros_seleccionados = []
opciones_base = [None] + [e for grp in GRUPOS.values() for e in grp]
cols = st.columns(4)

for i in range(8):
    t = cols[i % 4].selectbox(f"3ro #{i+1}", opciones_base, key=f"tercero_{i}")
    if t: terceros_seleccionados.append(t)

st.subheader("🥅 Dieciseisavos de Final")
partidos_resultados = {}
# Cruces automáticos
c1_list = [res_g["A"]["1"], res_g["B"]["1"], res_g["C"]["1"], res_g["D"]["1"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"], res_g["I"]["1"], res_g["J"]["1"], res_g["K"]["1"], res_g["L"]["1"], res_g["A"]["2"], res_g["B"]["2"], res_g["C"]["2"], res_g["D"]["2"]]
c2_list = [res_g["B"]["2"], res_g["A"]["2"], res_g["D"]["2"], res_g["C"]["2"], res_g["F"]["2"], res_g["E"]["2"], res_g["H"]["2"], res_g["G"]["2"], res_g["J"]["2"], res_g["I"]["2"], res_g["L"]["2"], res_g["K"]["2"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"]]

for i in range(16):
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**Partido D{i+1}:** {c1_list[i]} vs {c2_list[i]}")
    g1 = c2.number_input(f"Goles A", min_value=0, key=f"g1_{i}")
    g2 = c3.number_input(f"Goles B", min_value=0, key=f"g2_{i}")
    partidos_resultados[f"D{i+1}"] = f"{c1_list[i]} {g1}-{g2} {c2_list[i]}"

col1, col2 = st.columns(2)
def enviar(estado):
    payload = {"nombre": nombre, "estado": estado, "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}), **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}}
    return requests.post(URL, data=payload)

if col1.button("💾 GUARDAR BORRADOR"):
    enviar("En Edición")
    st.info("Borrador guardado.")
if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
    enviar("Definitiva")
    st.success("¡Enviada!")
