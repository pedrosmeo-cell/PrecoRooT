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

            st.success(f"🎉 Localização detetada: {cidade}, {pais}!")

            # 2. Se o utilizador enviou um LINK
            if link_produto:
                st.info("🔍 A ler os dados do link fornecido...")
                resultado_link = extrair_dados_da_url(link_produto)

                if resultado_link.get("sucesso"):
                    st.subheader(f"📦 {resultado_link.get('produto')}")
                    st.caption(f"Detetado via: {resultado_link.get('loja')}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Melhor Opção na Raiz 🎯", value="Preço Excelente")
                        st.button("Comprar Mais Barato 🛒", key="btn_raiz")
                    with col2:
                        st.metric(label="Preço no Link Original", value=resultado_link.get("preco"))
                        st.button("Ver Link Original 🛒", key="btn_original")
                else:
                    st.error("⚠️ Não conseguimos extrair os dados deste link.")

            # 3. Se o utilizador enviou uma FOTO
            elif foto_produto:
                st.info("📸 A processar a imagem com Inteligência Artificial...")
                resultado_imagem = analisar_imagem_produto(foto_produto)

                if resultado_imagem.get("sucesso"):
                    st.subheader(f"🔍 {resultado_imagem.get('produto')}")
                    st.caption(f"Identificado via: Busca Visual PreçoRoot")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label=f"Preço na Raiz (Lojas em {pais})",
                                  value=resultado_imagem.get("preco_estimado"))
                        st.button("Comprar Agora 🛒", key="btn_img_1")
                    with col2:
                        st.metric(label="Média de Mercado", value=f"89,90 {moeda}")
                        st.button("Ver Outras Lojas 🛒", key="btn_img_2")
                else:
                    st.error("⚠️ Erro ao processar a imagem.")
    else:
        st.warning("⚠️ Por favor, introduza uma foto ou um link para o PreçoRoot começar a procurar.")

# --- RODAPÉ LEGAL ADICIONADO ---
st.markdown("---")

with st.expander("🔒 Informações Legais e Política de Privacidade (RGPD)"):
    st.markdown("""
    ### 1. Recolha e Processamento de Dados
    O **PreçoRoot** respeita a privacidade dos seus utilizadores em conformidade com o RGPD. 
    * **Geolocalização:** O site analisa o seu endereço IP de forma automatizada e estritamente para identificar o seu país e moeda, garantindo a exibição dos preços corretos da sua região. Nenhum histórico de localização é guardado.
    * **Imagens e Links:** As imagens e links de produtos enviados para análise são processados em tempo real na memória do servidor para extração de dados e identificação comercial. Estes ficheiros não são armazenados nos nossos servidores após a conclusão da pesquisa.

    ### 2. Isenção de Responsabilidade
    O PreçoRoot é uma ferramenta de busca e comparação de preços em fase de testes (MVP). Os valores, produtos e lojas apresentados são simulações ou estimativas informativas. Não garantimos o stock, a precisão dos preços ou a segurança das transações nas lojas externas integradas.

    ### 3. Contacto
    Para questões sobre os seus direitos de dados, contacte: suporte@precoroot.com
    """)

st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>© 2026 PreçoRoot • Todos os direitos reservados.</p>", unsafe_allow_html=True)
