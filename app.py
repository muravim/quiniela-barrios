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

# Inicialización de estado
if 'logueado' not in st.session_state:
    st.session_state.update({'logueado': False, 'usuario': "", 'datos': None, 'es_definitiva': False, 't_sel': []})

# --- FUNCIONES AUXILIARES ---
def calcular_candidatos_terceros(res_g):
    candidatos = []
    for g, sel in res_g.items():
        if sel['1'] and sel['2']:
            candidatos.extend([e for e in GRUPOS[g] if e != sel['1'] and e != sel['2']])
    return list(set(candidatos))

# --- LOGIN ---
if not st.session_state.logueado:
    st.title("⚽ Iniciar Sesión")
    nombre = st.text_input("Nombre de usuario:").strip().title()
    password = st.text_input("Contraseña:", type="password")
    if st.button("Ingresar"):
        res = requests.get(URL, params={"nombre": nombre})
        if res.status_code == 200 and res.json().get("status") == "success":
            datos = res.json().get("datos")
            if datos[1] == password:
                octavos_data = json.loads(datos[14]) if datos[14] else {}
                st.session_state.update({'logueado': True, 'usuario': nombre, 'datos': datos, 'es_definitiva': (datos[16] == "Definitiva"), 't_sel': octavos_data.get("terceros", [])})
                st.rerun()
    st.stop()

# --- INTERFAZ ---
st.title("⚽ Quiniela Mundial 2026")
tab_grupos, tab_terceros, tab_final = st.tabs(["1. Grupos", "2. Mejores Terceros", "3. Fases Finales"])

# Captura de grupos (siempre activa)
res_g = {}
with tab_grupos:
    for g, eq in GRUPOS.items():
        with st.expander(f"Grupo {g}"):
            c1, c2 = st.columns(2)
            # Nota: Usamos keys fijas y evitamos re-crear selectboxes complejos
            o1 = c1.selectbox(f"1ero {g}", eq, key=f"g{g}_1")
            rest = [e for e in eq if e != o1]
            o2 = c2.selectbox(f"2do {g}", rest, key=f"g{g}_2")
            res_g[g] = {"1": o1, "2": o2}

# Pestaña Mejores Terceros
with tab_terceros:
    st.write("Selecciona los 8 mejores terceros:")
    candidatos = calcular_candidatos_terceros(res_g)
    
    st.session_state.t_sel = st.multiselect(
        "Elige 8 equipos:", 
        options=candidatos, 
        default=[t for t in st.session_state.t_sel if t in candidatos],
        max_selections=8,
        key="t_selector_final"
    )
    st.write(f"Seleccionados: {len(st.session_state.t_sel)} / 8")

# Pestaña Fases Finales
with tab_final:
    st.info("Configuración de cruces lista.")

# Guardado
if st.button("💾 Guardar Todo"):
    payload = {
        "nombre": st.session_state.usuario,
        "password": st.session_state.datos[1],
        "octavos": json.dumps({"terceros": st.session_state.t_sel}),
        **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}
    }
    requests.post(URL, data=payload)
    st.success("Guardado correctamente.")
