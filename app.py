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

st.title("⚽ Quiniela Mundial 2026 - Con 8 Mejores Terceros")
nombre = st.text_input("Nombre del participante:").strip().title()

if nombre:
    # 1. Fase de Grupos
    res_g = {}
    st.subheader("📋 Fase de Grupos (Clasificados)")
    for g, eq in GRUPOS.items():
        with st.expander(f"Grupo {g}"):
            c1, c2 = st.columns(2)
            o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
            o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
            res_g[g] = {"1": o1, "2": o2}

    # 2. Selección de los 8 mejores terceros
    st.subheader("🥉 Selección de los 8 mejores terceros")
    st.info("Selecciona los 8 equipos que clasifican como mejores terceros:")
    
    lista_todos_equipos = [eq for grp in GRUPOS.values() for eq in grp]
    ya_clasificados = [v["1"] for v in res_g.values()] + [v["2"] for v in res_g.values()]
    opciones_terceros = [e for e in lista_todos_equipos if e not in ya_clasificados]
    
    terceros_seleccionados = []
    cols_t = st.columns(4)
    for i in range(8):
        t = cols_t[i % 4].selectbox(f"3ro #{i+1}", opciones_terceros, key=f"tercero_{i}")
        terceros_seleccionados.append(t)

    # 3. Dieciseisavos (32 equipos en total)
    st.subheader("🥅 Dieciseisavos de Final (32 equipos)")
    partidos_resultados = {}
    
    # Automatización: 16 partidos (12 primeros + 12 segundos + 8 terceros = 32)
    for i in range(1, 17):
        c1, c2, c3 = st.columns([2, 1, 1])
        # Aquí permitimos escribir el enfrentamiento o precargarlo
        partido = c1.text_input(f"Partido D{i}:", key=f"p{i}")
        goles1 = c2.number_input(f"Goles A", min_value=0, key=f"d{i}_g1")
        goles2 = c3.number_input(f"Goles B", min_value=0, key=f"d{i}_g2")
        partidos_resultados[f"D{i}"] = f"{partido} -> {goles1}-{goles2}"

    # 4. Guardado
    col1, col2 = st.columns(2)
    def enviar(estado):
        payload = {
            "nombre": nombre, "estado": estado,
            "octavos": json.dumps({"fases": partidos_resultados, "terceros": terceros_seleccionados}, ensure_ascii=False),
            **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
        }
        return requests.post(URL, data=payload)

    if col1.button("💾 GUARDAR BORRADOR"):
        enviar("En Edición")
        st.info("Borrador guardado.")
    if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
        enviar("Definitiva")
        st.success("¡Enviada!")
