import streamlit as st
import subprocess
import time
from playwright.sync_api import sync_playwright

def install_playwright():
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(page_title="Agent Enigmàrius", page_icon="🏆")
st.title("🏆 Buscador de Classificació Enigmàrius")

# Buscador de text
nom_a_buscar = st.text_input("Escriu el nom exacte de la persona que vols buscar:", "")

if st.button("Buscar a la Classificació 🚀"):
    estat = st.empty()
    
    try:
        estat.info("🚀 Preparant l'agent buscador...")
        install_playwright()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Finestra extremadament gran per veure la taula sencera
            context = browser.new_context(viewport={'width': 1000, 'height': 5000})
            page = context.new_page()
            
            estat.info("🌐 Connectant amb 3Cat i Classificació...")
            page.goto("https://www.3cat.cat/catradio/mon-enigmarius/", wait_until="networkidle")
            
            # Neteja de cookies ràpida
            page.evaluate("document.querySelector('#onetrust-consent-sdk')?.remove()")
            
            # Busquem el botó de classificació clicant per text
            try:
                page.click("text='Veure tota la classificació', text='Classificació'", timeout=15000)
                time.sleep(5) # Temps perquè la taula carregui
            except:
                st.warning("No he trobat el botó directe, intentant captura general.")

            # BUCLE DE CERCA AMB PAGINACIÓ
            trobat = False
            pàgines_maximes = 10 # Limitem la cerca a 10 pàgines per seguretat
            pàgina_actual = 1
            
            while nom_a_buscar and not trobat and pàgina_actual <= pàgines_maximes:
                estat.info(f"🕵️ Buscant '{nom_a_buscar}' a la pàgina {pàgina_actual}...")
                
                # Intentem trobar el text i moure la pantalla
                try:
                    target = page.get_by_text(nom_a_buscar, exact=False).first
                    # Si el text és visible, ho hem trobat
                    if target.is_visible():
                        target.scroll_into_view_if_needed()
                        time.sleep(2)
                        trobat = True
                        estat.success(f"✅ Trobat a '{nom_a_buscar}' a la pàgina {pàgina_actual}!")
                except:
                    pass
                
                # Si no l'hem trobat, intentem clicar "Següent"
                if not trobat:
                    estat.info("⏭️ No trobat a la primera vista, intentant clicar 'Següent'...")
                    # Busquem el botó de "Següent" o ">"
                    try:
                        # Selector flexible per buscar botons de següent
                        next_btn = page.locator("text='Següent', text='>', text='Next'").first
                        if next_btn.is_visible():
                            next_btn.click()
                            time.sleep(4) # Esperem que la nova pàgina carregui
                            pàgina_actual += 1
                        else:
                            # Si no hi ha botó de següent, s'ha acabat la llista
                            pàgina_actual = pàgines_maximes + 1
                    except:
                        # Si no troba el botó, s'ha acabat la llista
                        pàgina_actual = pàgines_maximes + 1

            # CAPTURA FINAL
            foto = page.screenshot(full_page=False)
            browser.close()
            
            # Mostrar resultat
            if nom_a_buscar and not trobat:
                st.error(f"❌ No he pogut trobar a '{nom_a_buscar}' a les primeres {pàgines_maximes} pàgines.")
            
            st.image(foto)
            
    except Exception as e:
        st.error(f"❌ L'agent s'ha encallat: {e}")
