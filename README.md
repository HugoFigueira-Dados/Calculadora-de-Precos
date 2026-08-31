# Calculadora-de-Preços
  O repositório **Calculadora de preços** é uma aplicação web interativa desenvolvida em Python com o framework Streamlit. Seu objetivo principal é apoiar a precificação estratégica de produtos, integrando a gestão de custos operacionais (com foco em frete/carreto) a análises comparativas de preços de concorrência e projeções estatísticas de mercado.

---

  **Visão Geral da Arquitetura e Recursos**
  
  **Entrada Manual & Gestão de Custos:**
  
* Painel para inclusão manual de dados de compra: código EAN do produto, quantidade de caixas, valor da nota fiscal de compra, alíquota de impostos e preço de venda sugerido.

* Cálculo automático do custo unitário, total de impostos, faturamento e margem financeira/percentual.

   **Integração com a Base Interna de SKUs:**

* Suporte ao carregamento da base de dados via upload local (CSV/Excel) ou link público do Google Drive.

* Preenchimento e cruzamento automático de campos a partir do código: recuperação de código EAN, descrição completa do produto e o *Fator Hecto*.

* Cálculo do valor de carreto unitário e total por meio da regra: $\text{Carreto} = \text{Valor Unitário} \times \text{Fator Hecto}$.

   **Tratamento de Dados de Produto:**
  
* Função de limpeza e simplificação de nomes (`simplificar_nome_produto`), que remove siglas operacionais e de paletização (ex.: `SH`, `NPAL`, `VIDRO`, `PET`) para padronizar exibições e facilitar identificações.

   **Comparativo de Mercado & Projeções Estatísticas:**

* Acompanhamento e cálculo da diferença percentual em relação ao preço do concorrente praticado na praça: $\left(\frac{\text{Preço Venda}}{\text{Preço Concorrência}} - 1\right) \times 100$.

* Módulo de simulação de **Elasticidade-Preço Cruzada da Demanda**, estimando o impacto no volume de vendas em resposta a alterações na tabela da concorrência.

* Módulo de **Otimização do Preço Ótimo** para balanceamento entre margem em R$ e volume de vendas.

* **Matriz de Posicionamento Mercadológico**, que classifica automaticamente o SKU em categorias (Agressivo/Âncora, Equilibrado ou Margem/Premium) de acordo com a variação frente à concorrência.
