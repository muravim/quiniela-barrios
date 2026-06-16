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

st.title("🏆 Quiniela FIFA 2026")
st.subheader("💥 Dinastía Barrios 💥")

menu = st.radio("Acción:", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

if menu == "Ver mi quiniela guardada":
    nombre_consulta = st.text_input("👤 Ingrese su Nombre:").strip()
    if st.button("Consultar"):
        res = requests.get(URL_CONTROL_HOJA, params={"nombre": nombre_consulta})
        respuesta = res.json()
        
        if respuesta.get("status") == "success":
            d = respuesta["datos"]
            st.success(f"### Quiniela de {d[0]}")
            
            st.subheader("📋 Fase de Grupos")
            cols = st.columns(3)
            for i in range(1, 13):
                cols[(i-1)%3].write(f"**Grupo {chr(64+i)}:** {d[i]}")
            
            st.subheader("🏆 Pronósticos Fase Final")
            try:
                camino = json.loads(d[13])
                with st.expander("Ver detalle de Octavos, Cuartos y Semis"):
                    st.write(camino)
                st.info(f"**Tu Campeón Pronosticado:** {d[14]}")
                st.caption(f"Última actualización: {d[15]} | Estado: {d[16]}")
            except:
                st.warning("No se pudo cargar el detalle de las fases finales.")
        else:
            st.error("Participante no encontrado.")

else:
    nombre = st.text_input("👤 Ingrese su Nombre:", placeholder="Ej. Muravi").strip().title()
    
    if nombre:
        st.header("📋 Fase de Grupos")
        respuestas_grupos = {}
        for grupo, equipos in GRUPOS_MUNDIAL.items():
            with st.expander(f"⚽ {grupo}"):
                c1, c2 = st.columns(2)
                with c1: op1 = st.selectbox(f"1er", ["---"] + equipos, key=f"{grupo}_1")
                with c2: op2 = st.selectbox(f"2do", ["---"] + [e for e in equipos if e != op1], key=f"{grupo}_2")
                if op1 != "---" and op2 != "---": respuestas_grupos[grupo] = [op1, op2]

        if len(respuestas_grupos) == 12:
            st.header("🥅 Fases Finales")
            st.write("*(Nota: Lógica de llenado de partidos omitida para brevedad, asegurar que los datos coincidan con tu estructura)*")
            campeon = st.text_input("Ingrese su Campeón:")
            
            es_definitiva = st.checkbox("✅ Marcar como GUARDADO DEFINITIVO")
            
            if st.button("🚀 ENVIAR QUINIELA"):
                datos_a_enviar = {
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
                    "octavos": "{}", 
                    "campeon": campeon
                }
                envio = requests.post(URL_CONTROL_HOJA, data=datos_a_enviar)
                if envio.status_code == 200:
                    st.success("¡Guardado exitosamente!")
                else:
                    st.error("Error al guardar en el servidor.")
