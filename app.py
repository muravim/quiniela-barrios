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

menu = st.sidebar.radio("Navegación", ["Llenar/Editar Quiniela", "Ver mi quiniela guardada"])

if menu == "Ver mi quiniela guardada":
    nombre = st.text_input("Ingrese nombre:").strip()
    if st.button("Consultar"):
        res = requests.get(URL, params={"nombre": nombre})
        data = res.json()
        if data.get("status") == "success":
            d = data["datos"]
            st.success(f"### Quiniela de {d[0]}")
            st.subheader("📋 Fase de Grupos")
            c1, c2, c3 = st.columns(3)
            for i in range(12): [c1, c2, c3][i%3].write(f"**G{chr(65+i)}:** {d[i+1]}")
            st.subheader("🏆 Fase Eliminatoria (32 clasificados)")
            fases = json.loads(d[13]) if isinstance(d[13], str) else d[13]
            st.write(fases) # Muestra el JSON de los 32 equipos
            st.metric("Campeón", d[14])
        else: st.error("No encontrado.")

else:
    st.title("⚽ Llenar Quiniela (48 Equipos)")
    nombre = st.text_input("Nombre:").strip().title()
    if nombre:
        # 1. Grupos
        res_g = {}
        for g, eq in GRUPOS.items():
            with st.expander(f"Grupo {g}"):
                c1, c2 = st.columns(2)
                o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
                o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
                res_g[g] = [o1, o2]
        
        # 2. Los 8 mejores terceros
        st.subheader("🥉 Selección de los 8 mejores terceros")
        terceros = []
        for i in range(8):
            terceros.append(st.selectbox(f"Mejor Tercero #{i+1}", [eq for grp in GRUPOS.values() for eq in grp if eq not in [y for x in res_g.values() for y in x]], key=f"t{i}"))

        # 3. Dieciseisavos (32 equipos = 16 partidos)
        st.subheader("🥅 Dieciseisavos de Final (16 partidos)")
        dieciseisavos = {}
        for i in range(1, 17):
            dieciseisavos[f"D{i}"] = st.text_input(f"Partido D{i}:")

        campeon = st.text_input("Campeón Final:")
        
        if st.button("🚀 ENVIAR QUINIELA"):
            payload = {
                "nombre": nombre, "estado": "En Edición", "campeon": campeon,
                "octavos": json.dumps({"Dieciseisavos": dieciseisavos, "Terceros": terceros}, ensure_ascii=False),
                **{f"grupo_{k.lower()}": ", ".join(v) for k, v in res_g.items()}
            }
            requests.post(URL, data=payload)
            st.success("Guardado correctamente.")
