import streamlit as st
import requests

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

if 'logueado' not in st.session_state:
    st.session_state.update({'logueado': False, 'usuario': "", 'datos': None, 'es_admin': False, 'es_definitiva': False})

st.title("⚽ Quiniela Mundial 2026")

# --- LOGIN / REGISTRO ---
if not st.session_state.logueado:
    tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
    
    with tab1:
        nombre = st.text_input("Nombre de usuario:", key="login_n").strip().title()
        password = st.text_input("Contraseña:", type="password", key="login_p")
        if st.button("Ingresar"):
            res = requests.get(URL, params={"nombre": nombre})
            if res.status_code == 200 and res.json().get("status") == "success":
                datos = res.json().get("datos")
                if datos[1] == password:
                    st.session_state.update({'logueado': True, 'usuario': nombre, 'datos': datos, 'es_admin': res.json().get("es_admin", False), 'es_definitiva': (datos[16] == "Definitiva")})
                    st.rerun()
                else: st.error("Contraseña incorrecta")
            else: st.error("Usuario no encontrado")

    with tab2:
        new_n = st.text_input("Elige tu nombre:").strip().title()
        new_p = st.text_input("Elige una contraseña:", type="password")
        if st.button("Registrarse"):
            res = requests.post(URL, data={"nombre": new_n, "password": new_p, "estado": "En Edición"})
            if res.status_code == 200: st.success("¡Registro exitoso! Ya puedes ingresar en la pestaña de Ingreso.")
            else: st.error("Error al registrar.")
    st.stop()

# --- PANEL ADMIN ---
if st.session_state.es_admin:
    with st.expander("🛠️ Panel de Administrador"):
        st.write("Bienvenido, Administrador.")
        st.button("Desbloquear quinielas globales")

# --- INTERFAZ ---
es_def = st.session_state.es_definitiva
if es_def: st.warning("🔒 QUINIELA DEFINITIVA: No se permiten cambios.")

res_g = {}
datos = st.session_state.datos
for i, (g, eq) in enumerate(GRUPOS.items()):
    val = datos[2 + i] if datos and len(datos) > (2 + i) else ""
    opts = val.split(", ") if ", " in val else [None, None]
    with st.expander(f"Grupo {g}"):
        c1, c2 = st.columns(2)
        o1 = c1.selectbox(f"1ero {g}", eq, index=eq.index(opts[0]) if opts[0] in eq else 0, key=f"g{g}_1", disabled=es_def)
        rest = [e for e in eq if e != o1]
        o2 = c2.selectbox(f"2do {g}", rest, index=rest.index(opts[1]) if opts[1] in rest else 0, key=f"g{g}_2", disabled=es_def)
        res_g[g] = {"1": o1, "2": o2}

def enviar_datos(estado):
    payload = {"nombre": st.session_state.usuario, "password": st.session_state.datos[1], "estado": estado, "octavos": "{}", **{f"grupo_{k.lower()}": f"{v['1']}, {v['2']}" for k, v in res_g.items()}}
    requests.post(URL, data=payload)

if not es_def:
    col1, col2 = st.columns(2)
    if col1.button("💾 Guardar Borrador"):
        enviar_datos("En Edición")
        st.info("Borrador guardado.")
    if col2.button("🚀 ENVIAR DEFINITIVA"):
        enviar_datos("Definitiva")
        st.success("¡Quiniela enviada!")
        st.rerun()
