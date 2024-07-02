import streamlit as st
from comandos import LeitorDataFrame, Graficos
import inspect

# Função para carregar dados usando cache do Streamlit

def carregar_dados():
    caminho_arquivo = "dados_5.csv"
    df = LeitorDataFrame(caminho_arquivo).df
    return df

# Função para verificar se um parâmetro existe em um método específico de Graficos
def verificar(string, tipo):
    if string in inspect.getfullargspec(Graficos(carregar_dados()).methods[tipo])[0]:
        return True
    else:
        return False

# Função para plotar gráficos com opções dinâmicas
def plotar(tipo_grafico, eixo_x=None, eixo_y=None, plot=None, col=None, hue=None, size=None):
    if plot:
        if col:
            st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, col), use_container_width=True)
        elif hue:
            if size:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, size), use_container_width=True)
            else:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue), use_container_width=True)
        else:
            if eixo_y:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y), use_container_width=True)
            else:
                st.pyplot(Graficos(carregar_dados()).plot(tipo_grafico, eixo_x), use_container_width=True)

# Função para salvar gráficos com opções dinâmicas
def salvar(tipo_grafico, eixo_x=None, eixo_y=None, col=None, hue=None, size=None, save=None):
    if col:
        Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, col, save)
    elif hue:
        if size:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, size, save)
        else:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, hue, save)
    else:
        if eixo_y:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, eixo_y, save)
        else:
            Graficos(carregar_dados()).plot(tipo_grafico, eixo_x, save)

# Função para definir o layout da aplicação Streamlit
def layout(opcao):
    match opcao:
        case 'Dados vitais':
            layout_dados_vitais()
        case 'Dashboard':
            layout_dashboard()
        case 'Plotar Gráfico':
            layout_plotar_grafico()

# Layout específico para a opção 'Dashboard'
def layout_dashboard():
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        st.pyplot(Graficos(carregar_dados()).plot("linear com tipagem", "TIME", "RPM", "Marcha"), use_container_width=True)
    with col2:
        st.pyplot(Graficos(carregar_dados()).plot("dispersão", "Pressão_de_Óleo", "RPM", "Marcha"), use_container_width=True)
    with col3:
        st.pyplot(Graficos(carregar_dados()).plot("barra", "Marcha", "RPM"), use_container_width=True)
    with col4:
        st.pyplot(Graficos(carregar_dados()).plot("dispersão", "Força_G_lateral", "Força_G_aceleração","Marcha"), use_container_width=True)
    with col5:
        st.pyplot(Graficos(carregar_dados()).plot("barra com contagem", "RPM"), use_container_width=True)
    with col6:
        st.pyplot(Graficos(carregar_dados()).plot("dispersão 3D", "RPM", "Marcha", "Velocidade_de_tração"), use_container_width=True)
# Layout específico para a opção 'Plotar Gráfico'
def layout_plotar_grafico():
    eixo_x = None
    eixo_y = None
    hue = None
    size = None
    col = None
    save = st.session_state.get("save", None)
    col1 = st.empty()
    col2, col3 = st.columns(2)
    col4, col5 = st.columns(2)
    col6 = st.empty()
    with col1:
        tipo_grafico = st.selectbox("Selecione o Gráfico", options=Graficos(carregar_dados()).get_method_names())
    with col2:
        eixo_x = st.selectbox("Eixo X", options=list(carregar_dados().columns))
        if verificar("hue", tipo_grafico):
            hue = st.selectbox("hue", options=list(carregar_dados().columns))
    with col3:
        if verificar("y", tipo_grafico):
            eixo_y = st.selectbox("Eixo Y", options=list(carregar_dados().columns))
        if verificar("col", tipo_grafico):
            col = st.selectbox("Colunas", options=list(carregar_dados().columns))
        if verificar("size", tipo_grafico):
            size = st.selectbox("size", options=list(carregar_dados().columns))
    with col4:
        if verificar("z", tipo_grafico):
            eixo_z = st.selectbox("Eixo Z", options=list(carregar_dados().columns))
        plot = st.button("Plotar Gráfico")
    with col5:
        save = st.text_input("Nome do arquivo para salvar", value=save, key="save_input")
        save_button = st.button("Salvar")
        if save_button:
            st.session_state.save = save  # Atualiza o valor em session_state
            salvar(tipo_grafico, eixo_x, eixo_y, col, hue, size, save)
    with col6:
        plotar(tipo_grafico, eixo_x, eixo_y, plot, col, hue, size)

def layout_dados_vitais():
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        st.pyplot(Graficos(carregar_dados()).plot("linear", "TIME", "Tensão_da_Bateria"), use_container_width=True)
    with col2:
        st.pyplot(Graficos(carregar_dados()).plot("linear com tipagem", "TIME", "Temp._do_motor","Eletroventilador_1"), use_container_width=True)
    with col3:
        st.pyplot(Graficos(carregar_dados()).plot("linear", "TIME", "Eletroventilador_1"), use_container_width=True)
    with col4:
        st.pyplot(Graficos(carregar_dados()).plot("dispersão", "RPM", "Pressão_de_Óleo","Marcha"), use_container_width=True)
    with col5:
        st.pyplot(Graficos(carregar_dados()).plot("linear", "TIME", "Velocidade_de_tração"), use_container_width=True)
    with col6:
        st.pyplot(Graficos(carregar_dados()).plot("linear", "TIME", "Bomba_Combustível"), use_container_width=True)
        #colored_container("#006400", verificação_bateria())
        
# Layout específico para a opção 'Plotar Gráfico'
def colored_container(color, text):

    container_style = f"background-color: {color}; padding: 20px; border-radius: 20px;"
    st.markdown(f'<div style="{container_style}">{text}</div>', unsafe_allow_html=True)

def verificação_bateria():
    if any(value < 8 for value in carregar_dados()["Tensão_da_Bateria"]):
        return "Tensão da bateria baixa"
    
    elif any(value > 15 for value in carregar_dados()["Tensão_da_Bateria"]):
        return "Tensão da bateria alta"
    return "Tensão da bateria normal"

