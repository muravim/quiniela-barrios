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

# --- LÓGICA DE CARGA DE DATOS ---
def cargar_datos(nombre):
    res = requests.get(URL, params={"nombre": nombre})
    if res.status_code == 200:
        data = res.json()
        if data.get("status") == "success": return data["datos"]
    return None

st.title("⚽ Quiniela Mundial 2026")
nombre = st.text_input("Nombre del participante:").strip().title()

if nombre:
    datos_previos = cargar_datos(nombre)
    
    # --- FORMULARIO ---
    res_g = {}
    for g, eq in GRUPOS.items():
        with st.expander(f"Grupo {g}"):
            c1, c2 = st.columns(2)
            o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
            o2 = c2.selectbox(f"2do {g}", [e for e in eq if e != o1], key=f"g{g}_2")
            res_g[g] = {"1": o1, "2": o2}

    st.subheader("🥅 Dieciseisavos de Final (32 equipos)")
    partidos_resultados = {}
    cruces_auto = [("A","B"), ("C","D"), ("E","F"), ("G","H"), ("I","J"), ("K","L"), ("B","A"), ("D","C"),
                   ("F","E"), ("H","G"), ("J","I"), ("L","K"), ("A","C"), ("B","D"), ("E","G"), ("F","H")]
    
    for i in range(1, 17):
        g1, g2 = cruces_auto[i-1]
        eq1 = res_g[g1]["1"] if i <= 8 else res_g[g1]["2"]
        eq2 = res_g[g2]["2"] if i <= 8 else res_g[g2]["1"]
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"**D{i}: {eq1} vs {eq2}**")
        goles1 = c2.number_input(f"Goles {eq1}", min_value=0, key=f"d{i}_g1")
        goles2 = c3.number_input(f"Goles {eq2}", min_value=0, key=f"d{i}_g2")
        partidos_resultados[f"D{i}"] = f"{eq1} {goles1}-{goles2} {eq2}"

    # --- BOTONES DE GUARDADO ---
    col1, col2 = st.columns(2)
    
    # Función para enviar a Google
    def enviar_a_google(estado):
        payload = {
            "nombre": nombre, "estado": estado,
            "octavos": json.dumps(partidos_resultados, ensure_ascii=False),
            **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
        }
        return requests.post(URL, data=payload)

    if col1.button("💾 GUARDAR BORRADOR"):
        resp = enviar_a_google("En Edición")
        if resp.status_code == 200: st.info("Borrador guardado. Puedes volver más tarde.")
        
    if col2.button("🚀 ENVIAR QUINIELA DEFINITIVA"):
        resp = enviar_a_google("Definitiva")
        if resp.status_code == 200: st.success("¡Quiniela enviada! Ya no se puede modificar.")
