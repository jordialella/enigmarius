import streamlit as st
import subprocess
import os
from playwright.sync_api import sync_playwright

# Funció màgica per instal·lar els binaris de Playwright al servidor
def install_playwright():
    try:
        # Intentem comprovar si ja està instal·lat, si no, l'instal·lem
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Error instal·lant el navegador: {e}")

st.title("🤖 El meu Agent de Navegació Web")

url_usuari = st.text_input("URL de la pàgina:", "https://www.wikipedia.org")

if st.button("Llançar Agent 🚀"):
    # Pas 1: Instal·lar el navegador (només triga uns segons la primera vegada)
    with st.spinner("Preparant el navegador al servidor..."):
        install_playwright()

    # Pas 2: Executar l'agent
    with st.spinner("L'agent està navegant..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url_usuari, wait_until="networkidle")
                
                titol = page.title()
                st.success(f"✅ Connectat! El títol és: **{titol}**")
                
                browser.close()
        except Exception as e:
            st.error(f"S'ha produït un error en la navegació: {e}")
            st.error(f"S'ha produït un error: {e}")
