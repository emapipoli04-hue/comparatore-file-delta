import streamlit as st
from io import StringIO

st.set_page_config(page_title="Comparatore File Delta", page_icon="🔍", layout="wide")

st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); border-radius: 0.5rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: white;">🔍 Comparatore File Delta</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Confronta righe di PROD vs FABRIC</p>
    </div>
""", unsafe_allow_html=True)

def leggi_file(file_obj):
    righe_set = set()
    righe_lista = []
    try:
        stringio = StringIO(file_obj.getvalue().decode("utf-8-sig"))
        for riga in stringio:
            riga_pulita = riga.rstrip('\r')
            if riga_pulita.strip():
                righe_set.add(riga_pulita)
                righe_lista.append(riga_pulita)
        return righe_set, righe_lista, len(righe_lista), None
    except Exception as e:
        return None, None, 0, str(e)

def confronta_file(righe_prod_set, righe_prod_lista, righe_fabric_set):
    return [riga for riga in righe_prod_lista if riga not in righe_fabric_set]

with st.sidebar:
    st.info("**Come usare:** 1. Carica PROD 2. Carica FABRIC 3. Clicca Avvia")
    nome_output = st.text_input("Nome file output", value="delta_prod_vs_fabric.txt")
    num_esempi = st.slider("Esempi da mostrare", 1, 20, 5)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📁 File PROD")

    file_prod = st.file_uploader("Seleziona PROD", type=["txt"], key="prod")
    if file_prod:
        st.success(f"✅ {file_prod.name}")

with col2:
    st.markdown("### 📁 File FABRIC")

    file_fabric = st.file_uploader("Seleziona FABRIC", type=["txt"], key="fabric")
    if file_fabric:
        st.success(f"✅ {file_fabric.name}")

st.markdown("---")
avvia_btn = st.button("▶️ Avvia Confronto", use_container_width=True, type="primary")

if avvia_btn:
    if not file_prod or not file_fabric:
        st.error("❌ Carica entrambi i file!")
    else:
        with st.spinner("⏳ Confronto in corso..."):
            righe_prod_set, righe_prod_lista, num_prod, err = leggi_file(file_prod)
            if err:
                st.error(f"❌ Errore PROD: {err}")
            else:
                righe_fabric_set, _, num_fabric, err = leggi_file(file_fabric)
                if err:
                    st.error(f"❌ Errore FABRIC: {err}")
                else:
                    righe_mancanti = confronta_file(righe_prod_set, righe_prod_lista, righe_fabric_set)
                    output_content = "".join(righe_mancanti)
                    
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("PROD", num_prod)
                    col2.metric("FABRIC", num_fabric)
                    col3.metric("Identiche", num_prod - len(righe_mancanti))
                    col4.metric("Mancanti", len(righe_mancanti))
                    
                    if righe_mancanti:
                        st.success(f"✅ Trovate {len(righe_mancanti)} righe mancanti!")
                        st.markdown(f"### 📋 Primi {min(num_esempi, len(righe_mancanti))} esempi")

                        for i, riga in enumerate(righe_mancanti[:num_esempi]):
                            with st.expander(f"Riga {i+1}: {riga[:60]}..."):
                                st.code(riga)
                        st.download_button("📥 Scarica risultato", output_content, nome_output, "text/plain", use_container_width=True)
                    else:
                        st.success("✅ Nessuna riga mancante!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem 0;'><p>🔍 Comparatore File Delta v1.0</p></div>", unsafe_allow_html=True)
