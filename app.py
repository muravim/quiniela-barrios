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
nombre = st.text_input("Ingrese su nombre para cargar su progreso:").strip().title()

# Lógica de carga de datos previos
datos_guardados = None
if nombre:
    res = requests.get(URL, params={"nombre": nombre})
    if res.status_code == 200:
        data = res.json()
        if data.get("status") == "success":
            datos_guardados = data["datos"]
            st.success(f"¡Hola {nombre}! Hemos cargado tu borrador.")

# 1. Fase de Grupos
res_g = {}
st.subheader("📋 Fase de Grupos")
for g, eq in GRUPOS.items():
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        # Si hay datos, buscamos la selección previa en la columna correspondiente
        idx = ord(g) - 65 + 1 # Asumiendo grupos en columnas 1 a 12
        valor_previo = datos_guardados[idx].split(", ") if datos_guardados else [None, None]
        
        o1 = c1.selectbox(f"1ero {g}", eq, index=eq.index(valor_previo[0]) if valor_previo[0] in eq else 0, key=f"g{g}_1")
        o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], index=[e for e in eq if e != o1].index(valor_previo[1]) if valor_previo[1] in eq else 0, key=f"g{g}_2")
        res_g[g] = {"1": o1, "2": o2}

# 2. Mejores Terceros
st.subheader("🥉 Selección de los 8 mejores terceros")
terceros_seleccionados = []
cols = st.columns(4)
for i in range(8):
    # Intentamos cargar si existe, si no, None
    valor_t = None
    if datos_guardados:
        fases_json = json.loads(datos_guardados[13])
        if "terceros" in fases_json and i < len(fases_json["terceros"]):
            valor_t = fases_json["terceros"][i]
            
    t = cols[i % 4].selectbox(f"3ro #{i+1}", [None] + [e for grp in GRUPOS.values() for e in grp], index=[None] + [e for grp in GRUPOS.values() for e in grp].index(valor_t) if valor_t else 0, key=f"tercero_{i}")
    if t: terceros_seleccionados.append(t)

# 3. Dieciseisavos (Automatizados)
st.subheader("🥅 Dieciseisavos de Final (16 partidos)")
partidos_resultados = {}
c1_list = [res_g["A"]["1"], res_g["B"]["1"], res_g["C"]["1"], res_g["D"]["1"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"], res_g["I"]["1"], res_g["J"]["1"], res_g["K"]["1"], res_g["L"]["1"], res_g["A"]["2"], res_g["B"]["2"], res_g["C"]["2"], res_g["D"]["2"]]
c2_list = [res_g["B"]["2"], res_g["A"]["2"], res_g["D"]["2"], res_g["C"]["2"], res_g["F"]["2"], res_g["E"]["2"], res_g["H"]["2"], res_g["G"]["2"], res_g["J"]["2"], res_g["I"]["2"], res_g["L"]["2"], res_g["K"]["2"], res_g["E"]["1"], res_g["F"]["1"], res_g["G"]["1"], res_g["H"]["1"]]

for i in range(16):
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**Partido D{i+1}:** {c1_list[i]} vs {c2_list[i]}")
    g1 = c2.number_input(f"Goles A", min_value=0, key=f"g1_{i}")
    g2 = c3.number_input(f"Goles B", min_value=0, key=f"g2_{i}")
    partidos_resultados[f"D{i+1}"] = f"{c1_list[i]} {g1}-{g2} {c2_list[i]}"

# 4. Botones
col1, col2 = st.columns(2)
def enviar(estado):
    payload = {"nombre": nombre, "estado": estado, "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}, ensure_ascii=False), **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}}
    return requests.post(URL, data=payload)

if col1.button("💾 GUARDAR BORRADOR"):
    enviar("En Edición")
    st.info("Borrador guardado.")
if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
    enviar("Definitiva")
    st.success("¡Enviada!")
