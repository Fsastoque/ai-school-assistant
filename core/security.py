import streamlit as st
import hashlib

def hash_codigo(codigo):
    return hashlib.sha256(codigo.encode()).hexdigest()


def validar_usuario():

    if "validado" not in st.session_state:
        st.session_state.validado = False

    if not st.session_state.validado:

        st.warning("Ley 1581 de 2012 - Protección de datos")

        codigo = st.text_input("Código estudiantil")
        acepta = st.checkbox("Acepto términos")

        if st.button("Ingresar"):

            if not codigo or not acepta:
                st.error("Completa los datos")
                return False

            # 🔐 AQUÍ se usa el hash
            codigo_hash = hash_codigo(codigo)

            st.session_state.codigo_estudiante = codigo_hash
            st.session_state.validado = True

            st.success("Acceso autorizado")
            st.rerun()

    return True