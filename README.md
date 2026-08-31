# 🧮 Calculadora de Preços & Comparador de Concorrência

Esta é uma aplicação interativa desenvolvida em **Python** e **Streamlit** criada para automatizar a precificação de produtos (SKUs), calcular a margem de lucro real sobre os custos operacionais (impostos e carreto) e projetar a competitividade mercadológica frente aos preços praticados na praça.

O projeto foi estruturado para ser dinâmico e flexível, permitindo que a base de SKUs seja atualizada por upload local ou link do Google Drive, sem dependências de sistemas ou códigos de marcas específicas.

---

## 🚀 Funcionalidades Principais

* **Busca Automática de SKUs:** Ao inserir o código do produto (SKU), a aplicação busca na base cadastrada os dados de **EAN/DUN**, **Nome do Produto** e o **Fator Hectolitro**.


* **Preenchimento Flexível:** Se a base não estiver carregada, os campos de EAN, Descrição e Fator Hectolitro podem ser informados e ajustados manualmente.


* **Tratamento Inteligente de Nomes:** Limpeza automática do nome do produto (removendo siglas operacionais como `CX`, `PAL`, `SH`) para isolar as palavras-chave principais e otimizar a visualização.


* **Cálculos Automáticos de Precificação:**
* Custo unitário de compra


* Impostos unitários e totais


* Custo de carreto ($Carreto = Valor\ Uni \times Fator\ Hectolitro$)


* Custo total acumulado da operação


* Faturamento bruto esperado


* Margem líquida em $R\$$ e em $\%$ sobre o custo total




* **Comparação com a Concorrência:** Análise em tempo real do diferencial do seu preço em relação ao valor praticado pelo mercado.


* **Projeções Estatísticas & Otimização:**
* **Elasticidade-Preço Cruzada:** Simulação de ganho/perda de volume de vendas conforme flutuações de preços da concorrência.


* **Otimização de Lucro:** Sugestão de preço focal para maximizar a margem em $R\$$.


* **Matriz de Posicionamento:** Enquadramento estratégico do produto nas categorias *Agressivo/Âncora*, *Equilibrado* ou *Margem/Premium*.





---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Streamlit** (Interface gráfica e dashboards interativos)


* **Pandas** (Processamento de dados e leitura de arquivos CSV/Excel)


* **Regular Expressions (`re`)** (Tratamento de texto e normalização de descrições)



---

## 📋 Estrutura Esperada para a Base de SKUs (CSV / Excel)

Para que a busca automática funcione, o arquivo carregado (CSV ou Excel) pode conter as seguintes colunas (o sistema identifica automaticamente maiúsculas e minúsculas):

| Informação | Nomes Aceitos na Coluna |
| --- | --- |
| **Código do Produto** | `Código`, `Codigo`, `COD`, `SKU` |
| **Nome do Produto** | `Descrição`, `Descricao`, `Nome`, `Produto` |
| **Código EAN/DUN** | `EAN`, `DUN`, `Código de Barras` |
| **Fator Hectolitro** | `Fator Hecto`, `Fator`, `FHL` |

---

## 🔧 Como Executar o Projeto Localmente

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

```


2. **Instale as dependências:**
```bash
pip install streamlit pandas openpyxl

```


3. **Execute a aplicação:**
```bash
streamlit run app.py

```
