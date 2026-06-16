import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Quiniela Dinastía Barrios", page_icon="⚽", layout="wide")
URL = "https://script.google.com/macros/s/AKfycbzCQ5FcILnKcosplY2PASwTLeLko9YJRrAC602PkBJ1ojdg_cSEUPJsFAATf5XM0ZRRMw/exec"

GRUPOS = {
    "A": ["México", "Sudáfrica", "Corea del Sur", "Chequia"], "B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"], "D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "E": ["Alemania", "Costa de Marfil", "Ecuador", "Curazao"], "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"], "H": ["España", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "I": ["Francia", "Senegal", "Noruega", "Irak"], "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"], "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

menu = st.sidebar.radio("Navegación", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

# --- LÓGICA DE VISUALIZACIÓN ---
if menu == "Ver mi quiniela guardada":
    st.title("🔍 Buscar Quiniela")
    nombre_busqueda = st.text_input("Ingrese nombre:").strip()
    if st.button("Consultar"):
        res = requests.get(URL, params={"nombre": nombre_busqueda})
        data = res.json()
        if data.get("status") == "success":
            d = data["datos"]
            st.success(f"### Quiniela de {d[0]}")
            st.subheader("📋 Fase de Grupos")
            c1, c2, c3 = st.columns(3)
            for i in range(12):
                [c1, c2, c3][i%3].write(f"**Grupo {chr(65+i)}:** {d[i+1]}")
            st.subheader("🏆 Fases Finales")
            st.info(f"**Octavos:** {d[13]}")
            st.metric("Campeón", d[14])
        else: st.error("Participante no encontrado.")

# --- LÓGICA DE LLENADO ---
else:
    st.title("⚽ Llenar Quiniela")
    nombre = st.text_input("Nombre:").strip().title()
    if nombre:
        res_g = {}
        for g, eq in GRUPOS.items():
            with st.expander(f"Grupo {g}"):
                c1, c2 = st.columns(2)
                o1 = c1.selectbox(f"1ero {g}", ["---"] + eq, key=f"g{g}_1")
                o2 = c2.selectbox(f"2do {g}", ["---"] + [e for e in eq if e != o1], key=f"g{g}_2")
                if o1 != "---" and o2 != "---": res_g[f"Grupo {g}"] = f"{o1}, {o2}"
        
        if len(res_g) == 12:
            st.subheader("🥅 Fases Finales")
            octavos = st.text_area("Resultados Octavos (Formato libre):")
            campeon = st.text_input("Campeón Final:")
            
            if st.button("🚀 ENVIAR QUINIELA"):
                payload = {
                    "nombre": nombre, "estado": "En Edición", "campeon": campeon,
                    "octavos": octavos,
                    **{f"grupo_{k.lower().replace(' ','_')}": v for k, v in res_g.items()}
                }
                requests.post(URL, data=payload)
                st.success("Guardado exitosamente.")
