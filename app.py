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
nombre = st.text_input("Ingrese su nombre para cargar progreso:").strip().title()

# 1. Fase de Grupos
res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
        res_g[g] = {"1": o1, "2": o2}

# 2. Mejores Terceros
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

# 3. Dieciseisavos (Regla: No puede haber empate)
st.subheader("🥅 Dieciseisavos de Final (No se permiten empates)")
partidos_resultados = {}
# (Listas de cruces igual que antes)
c1_l = [res_g["A"]["1"], res_g["B"]["1"], res_g["C"]["1"], res_g["D"]["1"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"], res_g["I"]["1"], res_g["J"]["1"], res_g["K"]["1"], res_g["L"]["1"], res_g["A"]["2"], res_g["B"]["2"], res_g["C"]["2"], res_g["D"]["2"]]
c2_l = [res_g["B"]["2"], res_g["A"]["2"], res_g["D"]["2"], res_g["C"]["2"], res_g["F"]["2"], res_g["E"]["2"], res_g["H"]["2"], res_g["G"]["2"], res_g["J"]["2"], res_g["I"]["2"], res_g["L"]["2"], res_g["K"]["2"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"]]

for i in range(16):
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**D{i+1}:** {c1_l[i]} vs {c2_l[i]}")
    g1 = c2.number_input(f"Goles {c1_l[i]}", min_value=0, key=f"g1_{i}")
    g2 = c3.number_input(f"Goles {c2_l[i]}", min_value=0, key=f"g2_{i}")
    
    # Validación: Si hay empate, pedir ganador en penaltis
    if g1 == g2:
        c3.warning("¡Empate! Selecciona ganador en penaltis:")
        ganador = st.radio(f"¿Quién gana en penaltis {c1_l[i]}/{c2_l[i]}?", [c1_l[i], c2_l[i]], key=f"pen_{i}")
        partidos_resultados[f"D{i+1}"] = f"{c1_l[i]} {g1}-{g2} (Gana {ganador} en penaltis)"
    else:
        partidos_resultados[f"D{i+1}"] = f"{c1_l[i]} {g1}-{g2}"

# 4. Botones
if st.button("💾 GUARDAR BORRADOR"):
    # (Lógica de guardado igual)
    st.info("Borrador guardado.")
