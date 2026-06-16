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
nombre = st.text_input("Ingrese su nombre:").strip().title()

# 1. Fase de Grupos
res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
        res_g[g] = {"1": o1, "2": o2}

# 2. Selección de mejores terceros (Lógica estricta de exclusión)
st.subheader("🥉 Selección de los 8 mejores terceros")
# Obtenemos la lista de los que ya son 1ros y 2dos
ya_clasificados = [res_g[g]["1"] for g in GRUPOS] + [res_g[g]["2"] for g in GRUPOS]
# Filtramos la lista de todos los equipos disponibles quitando los clasificados
opciones_disponibles = [e for grp in GRUPOS.values() for e in grp if e not in ya_clasificados]

terceros_seleccionados = []
cols = st.columns(4)
for i in range(8):
    # En cada casilla, quitamos los que ya se eligieron en las casillas anteriores de terceros
    ya_elegidos_en_terceros = [terceros_seleccionados[j] for j in range(len(terceros_seleccionados))]
    lista_actual = [e for e in opciones_disponibles if e not in ya_elegidos_en_terceros]
    
    t = cols[i % 4].selectbox(f"3ro #{i+1}", [None] + lista_actual, key=f"tercero_{i}")
    if t: terceros_seleccionados.append(t)

# 3. Dieciseisavos
st.subheader("🥅 Dieciseisavos de Final (32 equipos)")
partidos_resultados = {}
for i in range(1, 17):
    c1, c2, c3 = st.columns([2, 1, 1])
    p = c1.text_input(f"Partido D{i}:", key=f"p{i}")
    g1 = c2.number_input(f"Goles A", min_value=0, key=f"g1_{i}")
    g2 = c3.number_input(f"Goles B", min_value=0, key=f"g2_{i}")
    partidos_resultados[f"D{i}"] = f"{p} {g1}-{g2}"

# 4. Botones
col1, col2 = st.columns(2)
def enviar(estado):
    payload = {
        "nombre": nombre, "estado": estado,
        "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}, ensure_ascii=False),
        **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
    }
    return requests.post(URL, data=payload)

if col1.button("💾 GUARDAR BORRADOR"):
    if not nombre: st.error("Ingresa tu nombre primero")
    else: 
        enviar("En Edición")
        st.info("Borrador guardado.")

if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
    if not nombre: st.error("Ingresa tu nombre primero")
    elif len(terceros_seleccionados) < 8: st.error("Selecciona los 8 terceros.")
    else:
        enviar("Definitiva")
        st.success("¡Enviada!")
