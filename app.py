import streamlit as st
import requests
import json

# Configuración de página
st.set_page_config(page_title="Quiniela Dinastía Barrios", page_icon="⚽", layout="centered")

URL_CONTROL_HOJA = "https://script.google.com/macros/s/AKfycbzCQ5FcILnKcosplY2PASwTLeLko9YJRrAC602PkBJ1ojdg_cSEUPJsFAATf5XM0ZRRMw/exec"

GRUPOS_MUNDIAL = {
    "Grupo A": ["México", "Sudáfrica", "Corea del Sur", "Chequia"],
    "Grupo B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "Grupo C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "Grupo D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "Grupo E": ["Alemania", "Costa de Marfil", "Ecuador", "Curazao"],
    "Grupo F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "Grupo G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "Grupo H": ["España", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "Grupo I": ["Francia", "Senegal", "Noruega", "Irak"],
    "Grupo J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "Grupo K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"],
    "Grupo L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

PARTIDOS_OCTAVOS_TEORICOS = [("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"), ("1I", "2J"), ("1K", "2L"), ("1B", "2A"), ("1D", "2C")]
CRUCES_CUARTOS = [(0, 1), (2, 3), (4, 5), (6, 7)]
CRUCES_SEMIS = [(0, 1), (2, 3)]

st.title("🏆 Quiniela FIFA 2026")
menu = st.radio("Acción:", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

if menu == "Ver mi quiniela guardada":
    nombre_consulta = st.text_input("👤 Ingrese su Nombre:").strip().title()
    if st.button("Consultar"):
        res = requests.get(URL_CONTROL_HOJA, params={"nombre": nombre_consulta})
        st.json(res.json())
else:
    nombre = st.text_input("👤 Ingrese su Nombre y Apellido:", placeholder="Ej. Carlos Barrios").strip().title()
    if nombre:
        st.header("📋 Fase de Grupos")
        respuestas_grupos = {}
        for grupo, equipos in GRUPOS_MUNDIAL.items():
            with st.expander(f"⚽ {grupo}"):
                c1, c2 = st.columns(2)
                with c1: op1 = st.selectbox(f"1er Clasificado", ["---"] + equipos, key=f"{grupo}_1")
                with c2: op2 = st.selectbox(f"2do Clasificado", ["---"] + [e for e in equipos if e != op1], key=f"{grupo}_2")
                if op1 != "---" and op2 != "---": respuestas_grupos[grupo] = [op1, op2]

        if len(respuestas_grupos) == 12:
            st.header("🥅 Octavos de Final")
            ganadores_octavos, pronosticos_octavos = [], {}
            for i, (pos1, pos2) in enumerate(PARTIDOS_OCTAVOS_TEORICOS, 1):
                eq1 = respuestas_grupos[f"Grupo {pos1[1]}"][0] if pos1[0] == "1" else respuestas_grupos[f"Grupo {pos1[1]}"][1]
                eq2 = respuestas_grupos[f"Grupo {pos2[1]}"][0] if pos2[0] == "1" else respuestas_grupos[f"Grupo {pos2[1]}"][1]
                st.markdown(f"**Partido {i}:** {eq1} vs {eq2}")
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"O_g1_{i}")
                with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"O_g2_{i}")
                with c3:
                    if g1 > g2: p = eq1
                    elif g2 > g1: p = eq2
                    else: p = st.selectbox(f"¿Avanza?", [eq1, eq2], key=f"O_emp_{i}")
                ganadores_octavos.append(p)
                pronosticos_octavos[f"O{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.header("🏆 Cuartos de Final")
            ganadores_cuartos, pronosticos_cuartos = [], {}
            for i, (idx1, idx2) in enumerate(CRUCES_CUARTOS, 1):
                eq1, eq2 = ganadores_octavos[idx1], ganadores_octavos[idx2]
                st.markdown(f"**Cuartos {i}:** {eq1} vs {eq2}")
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"C_g1_{i}")
                with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"C_g2_{i}")
                with c3:
                    if g1 > g2: p = eq1
                    elif g2 > g1: p = eq2
                    else: p = st.selectbox(f"¿Avanza?", [eq1, eq2], key=f"C_emp_{i}")
                ganadores_cuartos.append(p)
                pronosticos_cuartos[f"C{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.header("🔥 Semifinales")
            ganadores_semis, pronosticos_semis = [], {}
            for i, (idx1, idx2) in enumerate(CRUCES_SEMIS, 1):
                eq1, eq2 = ganadores_cuartos[idx1], ganadores_cuartos[idx2]
                st.markdown(f"**Semis {i}:** {eq1} vs {eq2}")
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"S_g1_{i}")
                with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"S_g2_{i}")
                with c3:
                    if g1 > g2: p = eq1
                    elif g2 > g1: p = eq2
                    else: p = st.selectbox(f"¿Avanza?", [eq1, eq2], key=f"S_emp_{i}")
                ganadores_semis.append(p)
                pronosticos_semis[f"S{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.header("👑 FINAL")
            eq1, eq2 = ganadores_semis[0], ganadores_semis[1]
            c1, c2, c3 = st.columns([2, 2, 3])
            with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key="F_g1")
            with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key="F_g2")
            campeon = eq1 if g1 > g2 else eq2
            st.success(f"🏆 Campeón: {campeon}")

            es_definitiva = st.checkbox("✅ Marcar como GUARDADO DEFINITIVO")
            if st.button("🚀 ENVIAR QUINIELA"):
                todo_el_camino = {"Octavos": pronosticos_octavos, "Cuartos": pronosticos_cuartos, "Semifinales": pronosticos_semis, "Campeon": campeon}
                datos_a_enviar = {
                    "nombre": nombre,
                    "estado": "Definitiva" if es_definitiva else "En Edición",
                    "octavos": json.dumps(todo_el_camino, ensure_ascii=False)
                }
                envio = requests.post(URL_CONTROL_HOJA, data=datos_a_enviar)
                st.success("¡Operación realizada con éxito!")
