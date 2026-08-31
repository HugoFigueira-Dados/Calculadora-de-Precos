import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Calculadora de Preços & Comparador", layout="wide")
st.title("🧮 Calculadora de Preços & Comparador de Concorrência")

# ==========================================
# FUNÇÃO PARA REDUZIR E TRATAR NOME DO PRODUTO
# ==========================================
def simplificar_nome_produto(nome, max_palavras=3):
    """
    Limpa o nome do produto reduzindo para até N palavras-chave.
    Trata siglas de embalagem/palete para padronizar a exibição no portfólio.
    """
    if not nome or pd.isna(nome):
        return ""
    
    texto = str(nome).upper().strip()
    
    # Substituições comuns para padronizar unidades/embalagens antes de fatiar
    texto = re.sub(r'\b1\s*L\b', '1L', texto)
    texto = re.sub(r'\b2\s*L\b', '2L', texto)
    texto = re.sub(r'\b350\s*ML\b', '350ML', texto)
    texto = re.sub(r'\b260\s*ML\b', '260ML', texto)
    texto = re.sub(r'\b473\s*ML\b', '473ML', texto)
    texto = re.sub(r'\b500\s*ML\b', '500ML', texto)
    
    # Remove termos informativos de distribuição
    termos_remover = [
        r'\bSH\b', r'\bC/\d+\b', r'\bCX\b', r'\bCX/\d+\b', r'\bNPAL\b', 
        r'\bPAL\b', r'\bCOQ\.\b', r'\bCOMPOSTO\b', r'\bVIDRO\b', r'\bPET\b'
    ]
    for termo in termos_remover:
        texto = re.sub(termo, '', texto)
    
    # Remove múltiplos espaços
    palavras = [p for p in texto.split() if p.strip()]
    
    # Limita ao número máximo de palavras desejado (padrão: 3)
    return " ".join(palavras[:max_palavras])

# ==========================================
# 1. CARREGAMENTO E CACHE DA BASE GENÉRICA DE SKUs
# ==========================================
@st.cache_data
def carregar_base_produtos(fonte_dados):
    try:
        if isinstance(fonte_dados, str) and "drive.google.com" in fonte_dados:
            if "/file/d/" in fonte_dados:
                file_id = fonte_dados.split("/file/d/")[1].split("/")[0]
                fonte_dados = f"https://drive.google.com/uc?export=download&id={file_id}"
            elif "id=" in fonte_dados:
                file_id = fonte_dados.split("id=")[1].split("&")[0]
                fonte_dados = f"https://drive.google.com/uc?export=download&id={file_id}"

        try:
            df = pd.read_csv(fonte_dados, sep=";", dtype=str, encoding="latin1")
            if len(df.columns) <= 1:
                df = pd.read_csv(fonte_dados, sep="\t", dtype=str, encoding="latin1")
            if len(df.columns) <= 1:
                df = pd.read_csv(fonte_dados, sep=",", dtype=str, encoding="latin1")
        except:
            df = pd.read_excel(fonte_dados, dtype=str)

        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        st.error(f"Erro ao ler a base de dados: {e}")
        return None

# ==========================================
# SIDEBAR: BASE DE DADOS
# ==========================================
st.sidebar.header("⚙️ Configurações & Base de Produtos")

origem_dados = st.sidebar.radio(
    "Como deseja carregar a base de SKUs?",
    ["Upload de Arquivo Local", "Link do Google Drive / URL Direta"]
)

df_base = None

if origem_dados == "Upload de Arquivo Local":
    file = st.sidebar.file_uploader("Carregar base de produtos (CSV ou Excel)", type=["csv", "xlsx", "xls"])
    if file is not None:
        df_base = carregar_base_produtos(file)
        if df_base is not None:
            st.sidebar.success(f"Base carregada! Total de itens: {len(df_base)}")
else:
    url_drive = st.sidebar.text_input("Cole o link público do Google Drive ou URL:")
    if url_drive:
        df_base = carregar_base_produtos(url_drive)
        if df_base is not None:
            st.sidebar.success(f"Base carregada via link! Total de itens: {len(df_base)}")

# ==========================================
# ESTRUTURA DE ABAS PRINCIPAL
# ==========================================
aba1, aba2, aba3 = st.tabs([
    "🧮 Calculadora & Comparador", 
    "📈 Projeções Estatísticas & Otimização", 
    "🏷️ Matriz de Posicionamento"
])

with aba1:
    # ==========================================
    # PAINEL DE ENTRADAS (VERDE) - ZERADO COMO PADRÃO
    # ==========================================
    st.subheader("🟢 Dados de Entrada (Preenchimento Manual)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cod_produto = st.text_input("CÓDIGO DO PRODUTO (SKU):", value="")

    with col2:
        caixas = st.number_input("CAIXAS / Quantidade:", min_value=0, value=0, step=1)
        valor_compra_nf = st.number_input("VALOR DE COMPRA NF (R$):", min_value=0.0, value=0.00, step=10.0)

    with col3:
        impostos_pct = st.number_input("Impostos (%):", min_value=0.0, max_value=100.0, value=0.00, step=0.1)
        preco_venda = st.number_input("Preço Venda (R$):", min_value=0.0, value=0.00, step=1.0)

    with col4:
        preco_concorrencia_manual = st.number_input("PREÇO CONCORRÊNCIA (Manual R$):", min_value=0.0, value=0.00, step=1.0)

    # ==========================================
    # BUSCA DOS DADOS NA BASE DE SKUs (AZUL)
    # ==========================================
    ean_auto = ""
    nome_auto = ""
    fator_hecto_auto = 0.0

    if df_base is not None and cod_produto.strip() != "":
        # Procura coluna de código dinamicamente
        cols_codigo = [c for c in df_base.columns if "CÓDIGO" in c.upper() or "COD" in c.upper() or "SKU" in c.upper()]
        col_codigo = cols_codigo[0] if cols_codigo else df_base.columns[0]
        
        match = df_base[df_base[col_codigo].astype(str).str.strip().str.lstrip('0') == str(cod_produto).strip().lstrip('0')]
        
        if not match.empty:
            row = match.iloc[0]
            
            # Puxa EAN
            col_ean = [c for c in df_base.columns if "EAN" in c.upper() or "DUN" in c.upper() or "BARRAS" in c.upper()]
            if col_ean:
                ean_auto = str(row[col_ean[0]]).strip()
                
            # Puxa Nome/Descrição
            col_nome = [c for c in df_base.columns if "DESCRIÇÃO" in c.upper() or "NOME" in c.upper() or "PRODUTO" in c.upper()]
            if col_nome:
                nome_auto = str(row[col_nome[0]]).strip()
                
            # Puxa Fator Hectolitro
            col_fator = [c for c in df_base.columns if "HECTO" in c.upper() or "FATOR" in c.upper() or "VOLUME" in c.upper()]
            if col_fator:
                try:
                    fator_hecto_auto = float(str(row[col_fator[0]]).replace(",", "."))
                except ValueError:
                    fator_hecto_auto = 0.0

    st.markdown("---")
    st.subheader("🔵 Informações do Produto")

    c1, c2, c3 = st.columns([2, 4, 2])
    ean_input = c1.text_input("EAN / DUN:", value=ean_auto)
    nome_input = c2.text_input("NOME DO PRODUTO:", value=nome_auto)
    fator_hecto = c3.number_input("Fator Hectolitro:", value=fator_hecto_auto, format="%.4f")

    nome_busca_3_palavras = simplificar_nome_produto(nome_input, max_palavras=3)
    if nome_busca_3_palavras:
        st.caption(f"💡 **Nome Simplificado para Exibição:** `{nome_busca_3_palavras}`")

    # ==========================================
    # CÁLCULOS AUTOMÁTICOS (EM BRANCO)
    # ==========================================
    und = caixas
    valor_uni = valor_compra_nf / und if und > 0 else 0.0
    imposto_un = valor_uni * (impostos_pct / 100.0)
    total_imposto = imposto_un * und

    carreto = valor_uni * fator_hecto
    total_carreto = carreto * und
    total_frete = 0.0

    custo_total = valor_compra_nf + total_imposto + total_carreto + total_frete
    faturamento = preco_venda * und
    margem_rs = faturamento - custo_total

    margem_pct = (margem_rs / custo_total * 100.0) if custo_total > 0 else 0.0

    st.markdown("---")
    st.subheader("⚪ Resumo dos Cálculos Automáticos")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Valor Uni", f"R$ {valor_uni:.2f}")
    m2.metric("Imposto Un.", f"R$ {imposto_un:.2f}")
    m3.metric("Total Imposto", f"R$ {total_imposto:.2f}")
    m4.metric("Carreto Un.", f"R$ {carreto:.2f}")

    m5, m6, m7, m8 = st.columns(4)
    m5.metric("Total Carreto", f"R$ {total_carreto:.2f}")
    m6.metric("Custo Total", f"R$ {custo_total:.2f}")
    m7.metric("FATURAMENTO", f"R$ {faturamento:.2f}")
    m8.metric("MARGEM (R$)", f"R$ {margem_rs:.2f}", delta=f"{margem_pct:.2f}% (s/ Custo)")

    # ==========================================
    # ANÁLISE COMPARATIVA DE CONCORRÊNCIA
    # ==========================================
    st.markdown("---")
    st.subheader("📊 Variação vs Preço da Concorrência")

    if preco_concorrencia_manual > 0 and preco_venda > 0:
        pct_vs_manual = ((preco_venda / preco_concorrencia_manual) - 1) * 100.0
        dif_reais = preco_venda - preco_concorrencia_manual
        
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        col_comp1.metric(
            label="Seu Preço de Venda", 
            value=f"R$ {preco_venda:.2f}"
        )
        col_comp2.metric(
            label="Preço Concorrência (Manual)", 
            value=f"R$ {preco_concorrencia_manual:.2f}"
        )
        col_comp3.metric(
            label="Variação vs Concorrência",
            value=f"{pct_vs_manual:+.2f}%",
            delta=f"Dif: R$ {dif_reais:+.2f}",
            delta_color="inverse"
        )
    else:
        st.info("Preencha os campos de **Preço Venda** e **PREÇO CONCORRÊNCIA** para calcular a variação.")

    # ==========================================
    # GUIA INFORMATIVO DA APLICAÇÃO
    # ==========================================
    with st.expander("ℹ️ Entenda as Projeções Avançadas e Análises Estatísticas"):
        st.markdown("""
        * **1. Elasticidade-Preço Cruzada:** Simula a porcentagem de volume de caixas que você **ganha ou perde** quando o concorrente altera a tabela de preços dele.
        * **2. Curva de Otimização de Lucro:** Identifica o **preço ideal de venda** que maximiza o lucro total acumulado em Reais (R$), ponderando volume versus taxa de margem.
        * **3. Matriz de Posicionamento:** Classifica este SKU automaticamente como **Agressivo**, **Equilibrado** ou **Margem/Premium** dependendo da distância do seu valor para o preço de mercado.
        """)

with aba2:
    st.header("📈 Projeções Estatísticas & Otimização")
    st.markdown("Simule como alterações nos preços da concorrência impactam sua demanda e otimize a margem em R$.")
    
    st.info("""
    📖 **Guia dos Parâmetros de Entrada:**
    * **Sensibilidade estimada do cliente (Elasticidade Cruzada):** Define o perfil do comprador. 
      * *Valores > 1.0:* Cliente muito sensível ao preço (troca de fornecedor facilmente por centavos).
      * *Valores próximos de 0.0:* Produto com pouca concorrência ou alta fidelidade (demanda insensível).
    * **Variação esperada no preço do Concorrente (%):** Simula um movimento do mercado local.
      * *Valores Negativos (ex: -4.00%):* O concorrente aplicou desconto ou iniciou guerra de preços.
      * *Valores Positivos (ex: +5.00%):* O concorrente reajustou a tabela para cima.
    * **Impacto Estimado na Demanda (% Volume):** Aponta a oscilação percentual no seu volume de caixas vendidas.
    """)
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        st.subheader("1. Elasticidade-Preço Cruzada")
        elasticidade = st.slider("Sensibilidade estimada do cliente (Elasticidade Cruzada):", -3.0, 3.0, 1.2, step=0.1)
        variacao_conc = st.slider("Variação esperada no preço do Concorrente (%):", -20.0, 20.0, 0.0, step=0.5)
        
        impacto_demanda = variacao_conc * elasticidade
        st.metric("Impacto Estimado na Sua Demanda (Volume)", f"{impacto_demanda:+.2f}%")
        
    with col_sim2:
        st.subheader("2. Curva de Otimização de Lucro")
        st.write("Cálculo do ponto focal que maximiza a Margem Total (R$) combinando Volume x Custo x Margem.")
        if preco_venda > 0 and caixas > 0:
            preco_sugerido_otimo = preco_concorrencia_manual * 0.98 if preco_concorrencia_manual > 0 else preco_venda
            st.success(f"💡 **Preço Recomendado para Maximizar Lucro:** R$ {preco_sugerido_otimo:.2f}")
        else:
            st.info("Preencha o Preço de Venda e Caixas na Aba 1 para gerar a otimização.")

with aba3:
    st.header("🏷️ Matriz de Posicionamento Mercadológico")
    st.markdown("Categorização estratégica de SKUs segundo o nível de competitividade regional.")
    
    st.info("""
    📖 **Critério de Classificação da Matriz:**
    * **🟢 Produto Agressivo / Âncora:** Preço praticado **> 2% abaixo** da concorrência. Utilizado para atrair fluxo e ganhar fatia de mercado.
    * **🟡 Produto Equilibrado:** Preço situado na faixa neutra de **±2%** em relação à concorrência. Alinhado com a média regional.
    * **🔴 Produto Margem / Premium:** Preço praticado **> 2% acima** da concorrência. Focado na captura de margem de lucro.
    """)
    
    if preco_venda > 0 and preco_concorrencia_manual > 0:
        diferenca_pct = ((preco_venda / preco_concorrencia_manual) - 1) * 100
        
        if diferenca_pct < -2.0:
            categoria = "🟢 Produto Agressivo / Âncora (Abaixo da Concorrência)"
            desc = "Ideal para atrair volume e conquistar participação de mercado."
        elif -2.0 <= diferenca_pct <= 2.0:
            categoria = "🟡 Produto Equilibrado (Alinhado ao Mercado)"
            desc = "Precificação neutra. Acompanha diretamente a margem do distribuidor local."
        else:
            categoria = "🔴 Produto Margem / Premium (Acima da Concorrência)"
            desc = "Preço superior. Recomendado para SKUs com restrição de oferta ou diferenciais de frete."
            
        st.subheader(categoria)
        st.write(desc)
    else:
        st.info("Insira o Preço de Venda e o Preço da Concorrência na Aba 1 para classificar este SKU.")
