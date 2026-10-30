# Tarefa 6: O Imposto sobre o Rendimento de Pessoas Singulares (IRS)
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**ID Ficha**: `tarefa_06`

<div align="justify">

Esta tarefa estuda o funcionamento da liquidação anual do IRS em Portugal: a transição do rendimento bruto para o rendimento coletável (aplicação do quociente conjugal e deduções específicas), o enquadramento na tabela de escalões do IRS, o cálculo da coleta total e o acerto final de contas (reembolso ou pagamento adicional).

---

## 1. Princípios e Mecanismos da Liquidação Anual do IRS

1. **Rendimento Bruto Anual ($RB$)**:
   $$\text{Trabalhador Dependente (14 meses)}: RB = \text{Salário Mensal} \times 14$$
   Para um casal em tributação conjunta, soma-se o rendimento anual de ambos os cônjuges.

2. **Deduções Específicas**:
   No regime geral dos rendimentos de trabalho dependente (Categoria A), a lei concede uma dedução específica de $4104{,}00\text{ €}$ por cada sujeito passivo (ou o valor total das contribuições para a Segurança Social, se superior).

3. **Rendimento Coletável ($RC$) e Quociente Conjugal**:
   - **Solteiros**: $RC = RB - \text{Deduções Específicas}$
   - **Casados (Tributação Conjunta)**: Aplica-se a divisão por 2 (quociente conjugal):
     $$RC = \frac{RB - \text{Deduções Específicas}}{2}$$

4. **Cálculo da Coleta por Titular**:
   Enquadrando o $RC$ no respetivo escalão da Tabela de IRS:
   $$\text{Coleta Individual} = RC \times \text{Taxa Normal} - \text{Parcela a abater}$$

5. **Coleta Total do Agregado Familiar**:
   - **Solteiros**: Coleta Total $= \text{Coleta Individual}$
   - **Casados (Tributação Conjunta)**: Multiplica-se por 2:
     $$\text{Coleta Total} = \text{Coleta Individual} \times 2$$

6. **Acerto Final de IRS (Saldo do Imposto)**:
   $$\text{Saldo} = \text{Coleta Total} - \text{Deduções à Coleta} - \text{Retenções na Fonte já efetuadas ao longo do ano}$$
   - Se o saldo for positivo ($\text{Saldo} > 0$), o contribuinte tem **imposto a pagar**;
   - Se o saldo for negativo ($\text{Saldo} < 0$), o contribuinte tem **imposto a receber (reembolso)**.

---

## Secção de Exemplos Guiados

### Exemplo 1: Apuramento Anual de IRS de um Casal (Mariana e Afonso)
A Mariana e o Afonso são casados, vivem em Lisboa e não têm dependentes. Em 2023, a Mariana auferia mensalmente $1200{,}00\text{ €}$ e o Afonso $1340{,}00\text{ €}$ brutos (14 meses). Resolveram entregar a declaração de IRS conjuntamente.  
*Hipótese 1: Considera que o casal não apresentou deduções específicas nem deduções à coleta.*

- **Passo 1.1: Cálculo do Rendimento Bruto Anual Global do Casal**
  - **Instrução ao Aluno**: Calcula o rendimento bruto anual somando os salários mensais do casal e multiplicando por 14 meses.
  - **Solução Esperada**: $(1200 + 1340) \times 14 = 2540 \times 14 = 35\,560{,}00\text{ €}$
  - **Pista Pedagógica**: Soma as duas remunerações e multiplica por 14: $(1200 + 1340) \times 14 = 35\,560\text{ €}$.

- **Passo 1.2: Determinação do Rendimento Coletável de Referência (Quociente Conjugal)**
  - **Instrução ao Aluno**: Sendo casados em tributação conjunta e sem deduções nesta fase, divide o rendimento bruto por 2.
  - **Solução Esperada**: $RC = \frac{35\,560}{2} = 17\,780{,}00\text{ €}$
  - **Pista Pedagógica**: O quociente conjugal para um casal divide o rendimento coletável por 2: $35\,560 \div 2 = 17\,780\text{ €}$.

- **Passo 1.3: Enquadramento no Escalão de IRS e Cálculo da Coleta Individual**
  - **Instrução ao Aluno**: Na Tabela de Escalões de IRS de 2023, $17\,780\text{ €}$ enquadra-se no 4.º escalão (taxa de $28{,}5\%$ e parcela a abater de $1426{,}65\text{ €}$). Calcula a coleta individual.
  - **Solução Esperada**: $\text{Coleta} = 17\,780 \times 0{,}285 - 1426{,}65 = 5067{,}30 - 1426{,}65 = 3640{,}65\text{ €}$
  - **Pista Pedagógica**: Aplica a fórmula $\text{Coleta} = RC \times \text{Taxa} - \text{Parcela a abater}$.

- **Passo 1.4: Determinação da Coleta Total do Casal**
  - **Instrução ao Aluno**: Multiplica a coleta individual por 2 para obter a coleta total devida pelo casal.
  - **Solução Esperada**: $\text{Coleta Total} = 3640{,}65 \times 2 = 7281{,}30\text{ €}$
  - **Pista Pedagógica**: Em tributação conjunta com quociente conjugal de 2, multiplica a coleta de referência por 2: $3640{,}65 \times 2 = 7281{,}30\text{ €}$.

---

## Secção de Exercícios de Aplicação

Resolve os seguintes exercícios no teu caderno de matemática com apresentação clara de todos os passos:

### Exercício 1
A Rita e o Afonso são casados, residem em Beja e não têm filhos. Em 2023, a Rita auferia um rendimento bruto mensal de $1050{,}00\text{ €}$ e o Afonso de $1010{,}00\text{ €}$ (14 meses). Entregaram a declaração de IRS conjuntamente, sem deduções.  
- **1.1**: Calcula o rendimento bruto anual global do casal;
- **1.2**: Determina o rendimento coletável que servirá de base à aplicação da taxa do escalão;
- **1.3**: Sabendo que o rendimento coletável se situa no 3.º escalão com taxa de $26{,}5\%$ e parcela a abater de $1106{,}73\text{ €}$, determina a coleta individual;
- **1.4**: Calcula a coleta total do casal.

---

### Exercício 2
O Manuel, em 2023, residia em Faro, era solteiro e não tinha filhos. Auferia um rendimento mensal bruto de $1300{,}00\text{ €}$ (14 meses). Supondo que não apresentou deduções específicas nem deduções à coleta:  
- Determina o rendimento bruto anual e coletável;
- Enquadra no escalão respetivo (taxa de $28{,}5\%$ e parcela a abater de $1426{,}65\text{ €}$) e calcula o valor da coleta de IRS.

---

### Exercício 3
A Joana e o Miguel são casados, não têm filhos e residem no Porto. Em 2023, o vencimento bruto mensal da Joana era de $1200{,}00\text{ €}$ e o do Miguel era de $1890{,}00\text{ €}$ (14 meses). Optaram pela tributação conjunta sem deduções.  
- Determina o rendimento bruto anual do casal;
- Determina o rendimento coletável e calcula a coleta total de IRS que o casal terá de suportar.

---

### Exercício 4
Considera novamente a situação da Mariana e do Afonso (do Exemplo 1: rendimento bruto anual conjunto de $35\,560{,}00\text{ €}$).  
Supondo agora que foram tidas em conta as deduções específicas da Categoria A ($4104{,}00\text{ €}$ por cada um dos 2 titulares):
- **4.1**: Determina o novo rendimento coletável individual do casal;
- **4.2**: Enquadra no escalão correspondente e calcula a nova coleta total devida pelo casal, comparando com o valor apurado no Exemplo 1 ($7281{,}30\text{ €}$).

---

### Exercício 5
A Eugénia e o Augusto são casados, têm 2 filhos e moram em Ponta Delgada (Região Autónoma dos Açores). Em 2022, auferiam mensalmente um vencimento bruto de $2530{,}00\text{ €}$ e $2300{,}00\text{ €}$, respetivamente (14 meses cada).  
- **5.1 (Sem Deduções)**:
  - 5.1.1: Determina o rendimento bruto anual conjunto e o rendimento coletável;
  - 5.1.2: Enquadra no escalão (taxa de $25{,}9\%$ e parcela a abater de $2146{,}76\text{ €}$) e indica os parâmetros;
  - 5.1.3: Calcula a coleta total do casal.
- **5.2 (Com Deduções)**:
  - Recalcula o rendimento coletável considerando as deduções específicas da Categoria A para ambos os cônjuges ($2 \times 4104{,}00\text{ €}$) e avalia o impacto na coleta final.

</div>
