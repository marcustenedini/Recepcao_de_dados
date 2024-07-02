import streamlit as st
from funções import layout

# Configurações da página do Streamlit
st.set_page_config(page_title="Apuama Racing Dashboard", layout="wide")

# Layout principal usando containers
with st.container():
    # Barra lateral com imagem, subtítulo e opção selecionável
    with st.sidebar:
        st.image("apuama_logo.png")  # Exibe a imagem do logo
        st.subheader("Análise de Dados")  # Título na barra lateral
        opção = st.selectbox("Opção desejada", options=["Dados vitais","Dashboard", "Plotar Gráfico"])  # Opção selecionável

    # Container principal para o layout
    with st.container():
        layout(opção)  # Chama a função layout com a opção selecionada
