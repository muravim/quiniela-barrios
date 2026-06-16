import streamlit as st
import requests
import json

st.set_page_config(page_title="Quiniela Dinastía Barrios", page_icon="⚽", layout="wide")

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

menu = st.sidebar.radio("Navegación:", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

if menu == "Ver mi quiniela guardada":
    st.title("🔍 Buscar Quiniela")
    nombre_consulta = st.text_input("Ingrese su nombre para buscar:").strip()
    if st.button("Consultar"):
        res = requests.get(URL_CONTROL_HOJA, params={"nombre": nombre_consulta})
        respuesta = res.json()
        if respuesta.get("status") == "success":
            d = respuesta["datos"]
            st.success(f"Quiniela de: {d[0]}")
            # Mostrar Grupos
            st.subheader("📋 Fase de Grupos")
            c1, c2, c3 = st.columns(3)
            for i in range(1, 13):
                [c1, c2, c3][(i-1)%3].write(f"**G{chr(64+i)}:** {d[i]}")
            # Mostrar Fases Finales
            st.subheader("🏆 Fases Finales")
            try:
                camino = json.loads(d[13])
                for etapa, partidos in camino.items():
                    with st.expander(f"Ver {etapa}"):
                        for p, det in partidos.items():
                            st.write(f"**{p}:** {det}")
                st.metric("Campeón", d[14])
            except: st.error("Error al leer fases finales.")
        else: st.error("No encontrado.")

else:
    st.title("⚽ Llenar Quiniela")
    nombre = st.text_input("Nombre y Apellido:").strip().title()
    if nombre:
        respuestas_grupos = {}
        for g, eq in GRUPOS_MUNDIAL.items():
            with st.expander(f"{g}"):
                c1, c2 = st.columns(2)
                o1 = c1.selectbox(f"1ero {g}", ["---"] + eq, key=f"{g}_1")
                o2 = c2.selectbox(f"2do {g}", ["---"] + [e for e in eq if e != o1], key=f"{g}_2")
                if o1 != "---" and o2 != "---": respuestas_grupos[g] = [o1, o2]
        
        if len(respuestas_grupos) == 12:
            st.subheader("🥅 Definir Fases Finales")
            # --- Lógica de llenado de Octavos ---
            octavos_res = {}
            for i in range(1, 9):
                octavos_res[f"O{i}"] = st.text_input(f"Ganador Octavos {i}", key=f"O{i}")
            
            campeon = st.text_input("Nombre del Campeón:")
            
            es_definitiva = st.checkbox("✅ Guardado DEFINITIVO")
            if st.button("🚀 ENVIAR"):
                # Empaquetar todo
                todo = {"Octavos": octavos_res}
                payload = {
                    "nombre": nombre,
                    "estado": "Definitiva" if es_definitiva else "En Edición",
                    "grupo_a": ", ".join(respuestas_grupos["Grupo A"]),
                    "grupo_b": ", ".join(respuestas_grupos["Grupo B"]),
                    "grupo_c": ", ".join(respuestas_grupos["Grupo C"]),
                    "grupo_d": ", ".join(respuestas_grupos["Grupo D"]),
                    "grupo_e": ", ".join(respuestas_grupos["Grupo E"]),
                    "grupo_f": ", ".join(respuestas_grupos["Grupo F"]),
                    "grupo_g": ", ".join(respuestas_grupos["Grupo G"]),
                    "grupo_h": ", ".join(respuestas_grupos["Grupo H"]),
                    "grupo_i": ", ".join(respuestas_grupos["Grupo I"]),
                    "grupo_j": ", ".join(respuestas_grupos["Grupo J"]),
                    "grupo_k": ", ".join(respuestas_grupos["Grupo K"]),
                    "grupo_l": ", ".join(respuestas_grupos["Grupo L"]),
                    "octavos": json.dumps(todo),
                    "campeon": campeon
                }
                res = requests.post(URL_CONTROL_HOJA, data=payload)
                st.success("Guardado con éxito.")
