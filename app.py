import streamlit as st
import requests
import json

st.set_page_config(page_title="Quiniela Dinastía Barrios", page_icon="⚽", layout="wide")

URL_CONTROL_HOJA = "https://script.google.com/macros/s/AKfycbzCQ5FcILnKcosplY2PASwTLeLko9YJRrAC602PkBJ1ojdg_cSEUPJsFAATf5XM0ZRRMw/exec"

GRUPOS = {
    "A": ["México", "Sudáfrica", "Corea del Sur", "Chequia"], "B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"], "D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "E": ["Alemania", "Costa de Marfil", "Ecuador", "Curazao"], "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"], "H": ["España", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "I": ["Francia", "Senegal", "Noruega", "Irak"], "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "Colombia", "Uzbekistán", "RD Congo"], "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
}

menu = st.sidebar.radio("Navegación", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

if menu == "Ver mi quiniela guardada":
    nombre_busqueda = st.text_input("Ingrese su nombre:").strip()
    if st.button("Consultar"):
        res = requests.get(URL_CONTROL_HOJA, params={"nombre": nombre_busqueda})
        data = res.json()
        if data.get("status") == "success":
            d = data["datos"]
            st.success(f"Quiniela de {d[0]}")
            st.subheader("📋 Fase de Grupos")
            c1, c2, c3 = st.columns(3)
            for i in range(1, 13):
                [c1, c2, c3][(i-1)%3].write(f"**G{chr(64+i)}:** {d[i]}")
            st.subheader("🏆 Fases Finales")
            try:
                fases = json.loads(d[13]) if isinstance(d[13], str) else d[13]
                for etapa, juegos in fases.items():
                    with st.expander(f"Ver {etapa}"):
                        for p, det in juegos.items(): st.write(f"**{p}:** {det}")
                st.metric("Campeón", d[14])
            except: st.error("Error al cargar fases finales.")
else:
    nombre = st.text_input("Nombre del participante:").strip().title()
    if nombre:
        res_g = {}
        for g, eq in GRUPOS.items():
            with st.expander(f"Grupo {g}"):
                c1, c2 = st.columns(2)
                o1 = c1.selectbox(f"1ero {g}", ["---"] + eq, key=f"g{g}_1")
                o2 = c2.selectbox(f"2do {g}", ["---"] + [e for e in eq if e != o1], key=f"g{g}_2")
                if o1 != "---" and o2 != "---": res_g[f"Grupo {g}"] = [o1, o2]
        
        if len(res_g) == 12:
            st.subheader("🥅 Definición de Octavos")
            # Cruces automáticos (Ejemplo: 1A vs 2B)
            cruces = [("Grupo A", "Grupo B"), ("Grupo C", "Grupo D"), ("Grupo E", "Grupo F"), ("Grupo G", "Grupo H"), 
                      ("Grupo I", "Grupo J"), ("Grupo K", "Grupo L"), ("Grupo B", "Grupo A"), ("Grupo D", "Grupo C")]
            octavos_res = {}
            for i, (g1, g2) in enumerate(cruces, 1):
                p1, p2 = res_g[g1][0], res_g[g2][1]
                octavos_res[f"O{i}"] = st.text_input(f"Ganador {p1} vs {p2}:", key=f"O{i}")
            
            campeon = st.text_input("Campeón Final:")
            if st.button("🚀 ENVIAR QUINIELA"):
                payload = {
                    "nombre": nombre, "estado": "En Edición", "campeon": campeon,
                    **{f"grupo_{g.lower().replace(' ','_')}": ", ".join(res_g[g]) for g in res_g},
                    "octavos": json.dumps({"Octavos": octavos_res}, ensure_ascii=False)
                }
                requests.post(URL_CONTROL_HOJA, data=payload)
                st.success("Guardado correctamente.")
