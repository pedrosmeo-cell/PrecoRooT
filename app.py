import streamlit as st
import time
import sys
import os

# Garante que o frontend consegue ler a pasta backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.localizador import obter_dados_localizacao
from backend.buscador_link import extrair_dados_da_url
from backend.buscador_imagem import analisar_imagem_produto

# Configuração da identidade visual do PreçoRoot
st.set_page_config(
    page_title="PreçoRoot - O preço mais barato na sua região",
    page_icon="🎯",
    layout="centered"
)

# Inicializa as variáveis de memória (session_state) para os resultados não sumirem
if "busca_realizada" not in st.session_state:
    st.session_state.busca_realizada = False
if "dados_busca" not in st.session_state:
    st.session_state.dados_busca = {}

# Cabeçalho do Site
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🎯 PreçoRoot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #4B5563;'>Encontre o menor preço direto na raiz, na sua zona!</h4>",
            unsafe_allow_html=True)
st.write("")

# Área de Entrada do Cliente
link_produto = st.text_input("🔗 Cole aqui o link de um produto (ex: Amazon):")
foto_produto = st.file_uploader("📸 Ou faça upload/tire uma foto do produto:", type=["jpg", "jpeg", "png"])

st.markdown("---")

# Botão de Ação Principal
if st.button("Buscar no PreçoRoot 🚀", use_container_width=True):
    if link_produto or foto_produto:
        with st.spinner("🎯 O PreçoRoot está a identificar a sua localização e a analisar os preços locais..."):

            # 1. Ativa o Motor de Localização
            dados_loc = obter_dados_localizacao()
            pais = dados_loc.get("pais_nome", "Portugal")
            moeda = dados_loc.get("moeda", "EUR")
            cidade = dados_loc.get("cidade", "Desconhecida")

            # Salva o estado na memória do site
            st.session_state.busca_realizada = True
            st.session_state.dados_busca = {
                "pais": pais,
                "moeda": moeda,
                "cidade": city_nome if 'city_nome' in locals() else cidade,
                "tipo": "link" if link_produto else "foto",
                "link_original": link_produto if link_produto else "https://amazon.es"
            }

            if link_produto:
                st.session_state.dados_busca["resultado"] = extrair_dados_da_url(link_produto)
            elif foto_produto:
                st.session_state.dados_busca["resultado"] = analisar_imagem_produto(foto_produto)
    else:
        st.warning("⚠️ Por favor, introduza uma foto ou um link para o PreçoRoot começar a procurar.")

# --- EXIBIÇÃO DOS RESULTADOS FIXOS ---
if st.session_state.busca_realizada:
    info = st.session_state.dados_busca
    res = info["resultado"]

    st.success(f"🎉 Localização detetada: {info['cidade']}, {info['pais']}!")

    if res.get("sucesso"):
        st.subheader(f"📦 {res.get('produto')}")

        if info["tipo"] == "link":
            st.caption(f"Detetado via: {res.get('loja')}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Melhor Opção na Raiz 🎯", value="Preço Excelente")
                # Botão de Link Real: Abre o site de afiliados numa nova aba sem resetar o Streamlit
                st.link_button("Comprar Mais Barato 🛒", url="https://amazon.es/-/pt/?tag=precoroot-21",
                               use_container_width=True)
            with col2:
                st.metric(label="Preço no Link Original", value=res.get("preco"))
                st.link_button("Ver Link Original 🛒", url=info["link_original"], use_container_width=True)

        elif info["tipo"] == "foto":
            st.caption(f"Identificado via: Busca Visual PreçoRoot")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"Preço na Raiz (Lojas em {info['pais']})", value=res.get("preco_estimado"))
                st.link_button("Comprar Agora 🛒", url="https://amazon.es/-/pt/?tag=precoroot-21",
                               use_container_width=True)
            with col2:
                st.metric(label="Média de Mercado", value=f"89,90 {info['moeda']}")
                st.link_button("Ver Outras Lojas 🛒", url="https://google.com", use_container_width=True)
    else:
        st.error(f"⚠️ Erro: {res.get('erro', 'Não foi possível processar.')}")

# --- RODAPÉ LEGAL ---
st.markdown("---")
with st.expander("🔒 Informações Legais e Política de Privacidade (RGPD)"):
    st.markdown("""
    ### 1. Recolha e Processamento de Dados
    O **PreçoRoot** respeita a privacidade dos seus utilizadores em conformidade com o RGPD. 
    * **Geolocalização:** O site analisa o seu endereço IP de forma automatizada e estritamente para identificar o seu país e moeda.
    * **Imagens e Links:** As imagens e links de produtos enviados para análise são processados em tempo real na memória do servidor.
    ### 2. Isenção de Responsabilidade
    O PreçoRoot é uma ferramenta de busca e comparação de preços em fase de testes (MVP).
    ### 3. Contacto
    Para questões sobre os seus direitos de dados, contacte: suporte@precoroot.com
    """)

st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>© 2026 PreçoRoot • Todos os direitos reservados.</p>",
    unsafe_allow_html=True)
