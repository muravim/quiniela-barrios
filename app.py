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

menu = st.sidebar.radio("Menú", ["Llenar/Editar", "Ver Quiniela"])

# --- LÓGICA DE VISUALIZACIÓN ---
if menu == "Ver Quiniela":
    nombre = st.text_input("Buscar por nombre:").strip()
    if st.button("Consultar"):
        res = requests.get(URL, params={"nombre": nombre})
        data = res.json()
        if data.get("status") == "success":
            d = data["datos"]
            st.subheader(f"Quiniela de {d[0]}")
            c1, c2, c3 = st.columns(3)
            for i in range(12): [c1, c2, c3][i%3].write(f"**G{chr(65+i)}:** {d[i+1]}")
            st.divider()
            fases = json.loads(d[13]) if isinstance(d[13], str) else d[13]
            for etapa, juegos in fases.items():
                with st.expander(f"Ver {etapa}"):
                    for p, det in juegos.items(): st.write(f"**{p}:** {det}")
            st.metric("Campeón", d[14])
        else: st.error("No encontrado.")

# --- LÓGICA DE LLENADO CON CRUCES AUTOMÁTICOS ---
else:
    nombre = st.text_input("Nombre:").strip().title()
    if nombre:
        res_g = {}
        for g, eq in GRUPOS.items():
            with st.expander(f"Grupo {g}"):
                c1, c2 = st.columns(2)
                o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
                o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
                res_g[g] = [o1, o2]
        
        st.subheader("🥅 Definir Fases Finales")
        # El sistema detecta los 1ros y 2dos automáticamente
        octavos = {f"O{i+1}": f"{res_g[cruces[0]][0]} vs {res_g[cruces[1]][1]}" 
                   for i, cruces in enumerate([("A","B"),("C","D"),("E","F"),("G","H"),("I","J"),("K","L"),("B","A"),("D","C")])}
        
        # Selección manual de ganadores de octavos
        ganadores_octavos = {k: st.selectbox(f"Ganador {v}", v.split(" vs "), key=k) for k, v in octavos.items()}
        
        campeon = st.text_input("Campeón:")
        if st.button("🚀 ENVIAR"):
            payload = {
                "nombre": nombre, "estado": "En Edición", "campeon": campeon,
                **{f"grupo_{k.lower()}": ", ".join(v) for k, v in res_g.items()},
                "octavos": json.dumps({"Octavos": ganadores_octavos})
            }
            requests.post(URL, data=payload)
            st.success("Guardado.")
