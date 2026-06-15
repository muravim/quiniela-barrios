import streamlit as st
import requests
import json
import datetime

# Configuración de página
st.set_page_config(page_title="Quiniela Dinastía Barrios", page_icon="⚽", layout="centered")

# --- LÓGICA DE TIEMPO (CORREGIDA) ---
# Usamos hora local del servidor sin librerías externas para evitar errores
ahora = datetime.datetime.now()
# El sistema abre hoy 14 a las 22:00 (10 PM)
# Ajuste: Si el servidor está en UTC, comparamos con la hora actual UTC
inicio_periodo = datetime.datetime(2026, 6, 14, 22, 0)
fin_periodo = datetime.datetime(2026, 6, 15, 14, 0)

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

PARTIDOS_OCTAVOS_TEORICOS = [
    ("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"),
    ("1I", "2J"), ("1K", "2L"), ("1B", "2A"), ("1D", "2C")
]
CRUCES_CUARTOS = [(0, 1), (2, 3), (4, 5), (6, 7)]
CRUCES_SEMIS = [(0, 1), (2, 3)]

st.title("🏆 Quiniela FIFA 2026")
st.subheader("💥 Dinastía Barrios 💥")

# --- LÓGICA DE TIEMPO ---
if ahora < inicio_periodo:
    st.warning("⏳ El sistema aún no está abierto. Podrás ingresar tus datos a partir de hoy a las 10:00 PM.")
elif ahora > fin_periodo:
    st.error("⚠️ El plazo para ingresar quinielas ha finalizado. ¡Gracias por participar!")
else:
    # --- FORMULARIO ORIGINAL ---
    st.write("---")
    nombre = st.text_input("👤 Ingrese su Nombre y Apellido:", placeholder="Ej. Carlos Barrios").strip().title()
    
    if nombre:
        st.success(f"¡Hola {nombre}! Completa tus pronósticos:")
        st.header("📋 Fase de Grupos")
        respuestas_grupos = {}
        
        for grupo, equipos in GRUPOS_MUNDIAL.items():
            with st.expander(f"⚽ {grupo}"):
                c1, c2 = st.columns(2)
                with c1: op1 = st.selectbox(f"1er Clasificado de {grupo}", ["---"] + equipos, key=f"{grupo}_1")
                with c2: op2 = st.selectbox(f"2do Clasificado de {grupo}", ["---"] + [e for e in equipos if e != op1], key=f"{grupo}_2")
                if op1 != "---" and op2 != "---": respuestas_grupos[grupo] = [op1, op2]

        if len(respuestas_grupos) == 12:
            st.write("---")
            st.header("🥅 Octavos de Final")
            ganadores_octavos = []
            pronosticos_octavos = {}
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
                    else: p = st.selectbox(f"Empate en P{i}. ¿Avanza?", [eq1, eq2], key=f"O_emp_{i}")
                ganadores_octavos.append(p)
                pronosticos_octavos[f"O{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.write("---")
            st.header("🏆 Cuartos de Final")
            ganadores_cuartos = []
            pronosticos_cuartos = {}
            for i, (idx1, idx2) in enumerate(CRUCES_CUARTOS, 1):
                eq1 = ganadores_octavos[idx1]
                eq2 = ganadores_octavos[idx2]
                st.markdown(f"**Cuartos {i}:** {eq1} vs {eq2}")
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"C_g1_{i}")
                with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"C_g2_{i}")
                with c3:
                    if g1 > g2: p = eq1
                    elif g2 > g1: p = eq2
                    else: p = st.selectbox(f"Empate en C{i}. ¿Avanza?", [eq1, eq2], key=f"C_emp_{i}")
                ganadores_cuartos.append(p)
                pronosticos_cuartos[f"C{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.write("---")
            st.header("🔥 Semifinales")
            ganadores_semis = []
            pronosticos_semis = {}
            for i, (idx1, idx2) in enumerate(CRUCES_SEMIS, 1):
                eq1 = ganadores_cuartos[idx1]
                eq2 = ganadores_cuartos[idx2]
                st.markdown(f"**Semifinal {i}:** {eq1} vs {eq2}")
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"S_g1_{i}")
                with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"S_g2_{i}")
                with c3:
                    if g1 > g2: p = eq1
                    elif g2 > g1: p = eq2
                    else: p = st.selectbox(f"Empate en S{i}. ¿Avanza?", [eq1, eq2], key=f"S_emp_{i}")
                ganadores_semis.append(p)
                pronosticos_semis[f"S{i}"] = f"{eq1} ({g1}) vs {eq2} ({g2}) -> Pasa: {p}"

            st.write("---")
            st.header("👑 LA GRAN FINAL")
            eq1 = ganadores_semis[0]
            eq2 = ganadores_semis[1]
            st.markdown(f"**FINALÍSIMA:** {eq1} vs {eq2}")
            c1, c2, c3 = st.columns([2, 2, 3])
            with c1: g1 = st.number_input(f"Goles {eq1}", min_value=0, step=1, key=f"F_g1")
            with c2: g2 = st.number_input(f"Goles {eq2}", min_value=0, step=1, key=f"F_g2")
            with c3:
                if g1 > g2: campeon = eq1
                elif g2 > g1: campeon = eq2
                else: campeon = st.selectbox("Empate. ¿Quién es el CAMPEÓN?", [eq1, eq2], key=f"F_emp")
            st.success(f"🏆 Tu Campeón es: **{campeon}**")

            st.write("---")
            if st.button("🚀 ENVIAR QUINIELA A LA BASE
