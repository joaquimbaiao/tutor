# Tarefa 6: O Imposto sobre o Rendimento de Pessoas Singulares (IRS)
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**Documento Oficial de Critérios e Resoluções Padronizadas**

<div align="justify">

Este documento reúne todas as resoluções oficiais, passos de decomposição matemática, múltiplos métodos equivalentes e pistas pedagógicas socráticas da Tarefa 6, respeitando a notação em LaTeX e o arredondamento monetário às centésimas.

---

## 1. Exemplo Guiado: Mariana e Afonso (Tributação Conjunta)

### Enunciado e Dados:
- Salários mensais brutos (14 meses): Mariana ($1200{,}00\text{ €}$) e Afonso ($1340{,}00\text{ €}$);
- Situação: Casados, tributação conjunta, sem deduções nesta fase;
- Tabela de IRS (Continente 2023).

### Resolução Passo a Passo:
- **Passo 1.1 (Rendimento Bruto Anual Global)**:
  $$(1200 + 1340) \times 14 = 2540 \times 14 = 35\,560{,}00\text{ €}$$
  - **Pista Pedagógica**: Soma os vencimentos mensais de ambos os cônjuges e multiplica por 14 meses: $(1200 + 1340) \times 14 = 35\,560\text{ €}$.

- **Passo 1.2 (Rendimento Coletável de Referência - Quociente Conjugal)**:
  $$RC = \frac{35\,560}{2} = 17\,780{,}00\text{ €}$$
  - **Pista Pedagógica**: Na tributação conjunta, aplica-se o quociente conjugal dividindo o rendimento global por 2: $35\,560 \div 2 = 17\,780\text{ €}$.

- **Passo 1.3 (Enquadramento e Coleta Individual)**:
  - Enquadramento no 4.º escalão ($15\,992\text{ €}$ a $20\,700\text{ €}$): Taxa de $28{,}5\%$ e Parcela a abater de $1426{,}65\text{ €}$.
  $$\text{Coleta Individual} = 17\,780 \times 0{,}285 - 1426{,}65 = 5067{,}30 - 1426{,}65 = 3640{,}65\text{ €}$$
  - **Pista Pedagógica**: Aplica a fórmula legal da coleta: $\text{Coleta} = RC \times \text{Taxa} - \text{Parcela a abater}$.

- **Passo 1.4 (Coleta Total do Casal)**:
  $$\text{Coleta Total} = 3640{,}65 \times 2 = 7281{,}30\text{ €}$$
  - **Pista Pedagógica**: Como aplicaste o quociente conjugal dividindo por 2, deves agora multiplicar a coleta individual por 2 para obteres o imposto total devido pelo agregado: $3640{,}65 \times 2 = 7281{,}30\text{ €}$.

---

## 2. Exercícios de Aplicação

### Exercício 1: A Rita e o Afonso
- **Dados**: Rita ($1050{,}00\text{ €}$/mês) e Afonso ($1010{,}00\text{ €}$/mês), casados, tributação conjunta, 14 meses, sem deduções.
- **Resolução Oficial**:
  - **1.1 Rendimento Bruto Anual Global**:
    $$(1050 + 1010) \times 14 = 2060 \times 14 = 28\,840{,}00\text{ €}$$
  - **1.2 Rendimento Coletável de Referência**:
    $$RC = \frac{28\,840}{2} = 14\,420{,}00\text{ €}$$
  - **1.3 Parâmetros do Escalão (3.º Escalão)**:
    - Taxa: $26{,}5\%$ ($0{,}265$)
    - Parcela a abater: $1106{,}73\text{ €}$
  - **1.4 Coleta Total de IRS**:
    - Coleta individual:
      $$14\,420 \times 0{,}265 - 1106{,}73 = 3821{,}30 - 1106{,}73 = 2714{,}57\text{ €}$$
    - Coleta total do casal (2 titulares):
      $$2714{,}57 \times 2 = 5429{,}14\text{ €}$$
- **Critérios de Aceitação**: Aceitam-se respostas com indicação da coleta individual ($2714{,}57\text{ €}$) ou da coleta total ($5429{,}14\text{ €}$).

---

### Exercício 2: O Manuel (Solteiro)
- **Dados**: Vencimento mensal bruto de $1300{,}00\text{ €}$ (14 meses), solteiro, sem dependentes nem deduções.
- **Resolução Oficial**:
  - **Rendimento Bruto Anual**:
    $$RB = 1300 \times 14 = 18\,200{,}00\text{ €}$$
  - **Rendimento Coletável**:
    Como o Manuel é solteiro e não apresenta deduções, não se aplica quociente conjugal:
    $$RC = 18\,200{,}00\text{ €}$$
  - **Enquadramento no Escalão (4.º Escalão: $15\,992\text{ €}$ a $20\,700\text{ €}$)**:
    - Taxa: $28{,}5\%$ ($0{,}285$)
    - Parcela a abater: $1426{,}65\text{ €}$
  - **Cálculo da Coleta**:
    $$\text{Coleta} = 18\,200 \times 0{,}285 - 1426{,}65 = 5187{,}00 - 1426{,}65 = 3760{,}35\text{ €}$$
- **Conclusão**: O Manuel suporta uma coleta final de IRS de $3760{,}35\text{ €}$.

---

### Exercício 3: A Joana e o Miguel
- **Dados**: Joana ($1200{,}00\text{ €}$/mês) e Miguel ($1890{,}00\text{ €}$/mês), casados, 14 meses, sem deduções.
- **Resolução Oficial**:
  - **Rendimento Bruto Anual**:
    $$(1200 + 1890) \times 14 = 3090 \times 14 = 43\,260{,}00\text{ €}$$
  - **Rendimento Coletável**:
    $$RC = \frac{43\,260}{2} = 21\,630{,}00\text{ €}$$
  - **Enquadramento no Escalão (5.º Escalão: $20\,700\text{ €}$ a $26\,355\text{ €}$)**:
    - Taxa: $35\%$ ($0{,}35$)
    - Parcela a abater: $2772{,}14\text{ €}$
  - **Coleta Individual e Total**:
    - Coleta individual:
      $$21\,630 \times 0{,}35 - 2772{,}14 = 7570{,}50 - 2772{,}14 = 4798{,}36\text{ €}$$
    - Coleta total do casal (2 titulares):
      $$4798{,}36 \times 2 = 9596{,}72\text{ €}$$
- **Critérios de Aceitação**: Valor individual de $4798{,}36\text{ €}$ e valor total de $9596{,}72\text{ €}$ (aceitando-se tolerância de gralha original de $9596{,}36\text{ €}$).

---

### Exercício 4: Mariana e Afonso (Com Deduções Específicas)
- **Dados**: Rendimento bruto de $35\,560{,}00\text{ €}$; Dedução específica da Categoria A de $4104{,}00\text{ €}$ por cada titular ($2 \times 4104 = 8208{,}00\text{ €}$).
- **Resolução Oficial**:
  - **4.1 Rendimento Coletável com Deduções**:
    - Rendimento global após deduções:
      $$35\,560 - (4104 \times 2) = 35\,560 - 8208 = 27\,352{,}00\text{ €}$$
    - Rendimento coletável de referência por titular:
      $$RC = \frac{27\,352}{2} = 13\,676{,}00\text{ €}$$
  - **4.2 Enquadramento e Nova Coleta Total**:
    - Enquadramento no 3.º escalão ($11\,284\text{ €}$ a $15\,992\text{ €}$): Taxa de $26{,}5\%$ e Parcela a abater de $1106{,}73\text{ €}$.
    - Coleta individual:
      $$13\,676 \times 0{,}265 - 1106{,}73 = 3624{,}14 - 1106{,}73 = 2517{,}41\text{ €}$$
    - Coleta total do casal:
      $$2517{,}41 \times 2 = 5034{,}82\text{ €}$$
    - Poupança obtida:
      $$7281{,}30 - 5034{,}82 = 2246{,}48\text{ €}$$

---

### Exercício 5: Eugénia e Augusto (Região Autónoma dos Açores)
- **Dados**: Eugénia ($2530{,}00\text{ €}$/mês) e Augusto ($2300{,}00\text{ €}$/mês), 14 meses cada, Açores.
- **Resolução Oficial**:
  - **5.1 Sem Deduções**:
    - **5.1.1**:
      $$RB = (2530 + 2300) \times 14 = 4830 \times 14 = 67\,620{,}00\text{ €}$$
      $$RC = \frac{67\,620}{2} = 33\,810{,}00\text{ €}$$
    - **5.1.2**:
      - Taxa de escalão (Açores): $25{,}9\%$ ($0{,}259$)
      - Parcela a abater: $2146{,}76\text{ €}$
    - **5.1.3**:
      $$\text{Coleta individual} = 33\,810 \times 0{,}259 - 2146{,}76 = 8756{,}79 - 2146{,}76 = 6610{,}03\text{ €}$$
      $$\text{Coleta total} = 6610{,}03 \times 2 = 13\,220{,}06\text{ €}$$
  - **5.2 Com Deduções Específicas**:
    - Rendimento global após deduções:
      $$67\,620 - 4104 \times 2 = 67\,620 - 8208 = 59\,412{,}00\text{ €}$$
    - Rendimento coletável individual:
      $$RC = \frac{59\,412}{2} = 29\,706{,}00\text{ €}$$
    - Coleta individual (mesmo escalão dos Açores):
      $$29\,706 \times 0{,}259 - 2146{,}76 = 7693{,}854 - 2146{,}76 = 5547{,}094 \approx 5547{,}09\text{ €}$$
    - Coleta total do casal:
      $$5547{,}094 \times 2 = 11\,094{,}19\text{ €}$$
    - Diferença na fatura fiscal:
      $$13\,220{,}06 - 11\,094{,}19 = 2125{,}87\text{ €}$$

</div>
