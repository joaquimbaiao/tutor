# Tarefa 7: Matemática na Poupança e no Crédito (Juro Simples)
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**Documento Oficial de Enunciados e Resoluções Padronizadas**

<div align="justify">

Este documento contém os enunciados integrais e todos os percursos de resolução oficiais (com fórmulas explícitas em LaTeX e múltiplos métodos equivalentes aceites) da Tarefa 7.

---

## BLOCO 1: Cálculo de Juros e Capital Acumulado

### Exemplo 1 (Guiado Passo a Passo)
Supõe que depositaste $650\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $4\%$. Qual é o valor:
- **1.1** A receber de juros no final do 1.º ano?
- **1.2** De juros acumulados ao fim de 3 anos?
- **1.3** Do capital acumulado ao fim dos 3 anos?

#### Proposta de Resolução Oficial:
- **Passo 1.1**: $J_1 = 650 \times 0{,}04 = 26\text{ €}$ (ou $650 \times \frac{4}{100} = 26\text{ €}$)
- **Passo 1.2**: $J_3 = 26 \times 3 = 78\text{ €}$ (ou $650 \times 0{,}04 \times 3 = 78\text{ €}$)
- **Passo 1.3**: $C_3 = 650 + 78 = 728\text{ €}$ (ou $650 \times (1 + 0{,}04 \times 3) = 728\text{ €}$)

---

### Exercício 1 (Aplicação - Bloco 1)
O Francisco depositou $1500\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $1{,}2\%$. Qual será o valor do capital acumulado ao fim de $1\text{ ano}$?

#### Critérios e Métodos de Resolução Aceites:
- **Dados**: $C_i = 1500$, $r = 1{,}2$, $n = 1\text{ ano}$.
- **Método A (Fórmula Direta do Capital Acumulado)**:
  $$C_a = C_i \times \left(1 + \frac{r}{100} \times n\right) \iff C_a = 1500 \times \left(1 + \frac{1{,}2}{100} \times 1\right) \iff C_a = 1518\text{ €}$$
- **Método B (Cálculo dos Juros + Adição ao Capital Inicial)**:
  $$J = 1500 \times 0{,}012 \times 1 = 18\text{ €} \implies C_a = 1500 + 18 = 1518\text{ €}$$
- **Conclusão**: Ao fim de um ano, o Francisco acumulou um capital de $1518\text{ €}$.

---

### Exercício 2 (Aplicação - Bloco 1)
Durante as férias de verão, a Raquel trabalhou como nadadora-salvadora e recebeu $3000\text{ €}$. Em setembro, resolveu depositar o dinheiro, numa conta a prazo, num regime de juros simples e durante um período de 7 anos. A taxa de juro anual foi de $1{,}2\%$. Calcula o valor:
- **2.1** Dos juros no final do 1.º ano.
- **2.2** Do capital acumulado ao fim dos 7 anos.

#### Critérios e Métodos de Resolução Aceites:
- **Alínea 2.1 (Juros no final do 1.º ano)**:
  $$J_1 = 3000 \times \frac{1{,}2}{100} = 36\text{ €} \quad \text{ou} \quad 3000 \times 0{,}012 = 36\text{ €}$$
- **Alínea 2.2 (Capital acumulado ao fim dos 7 anos)**:
  - *Opção 1 (Fórmula Direta)*:
    $$C_a = 3000 \times \left(1 + \frac{1{,}2}{100} \times 7\right) \iff C_a = 3252\text{ €}$$
  - *Opção 2 (Soma dos Juros Totais ao Capital)*:
    $$C_a = 3000 + 7 \times 36 \iff C_a = 3252\text{ €}$$
- **Conclusão**: O valor dos juros no 1.º ano é $36\text{ €}$ e o capital acumulado ao fim de 7 anos é $3252\text{ €}$.

---

### Exercício 3 (Aplicação - Bloco 1)
O Diogo quer aplicar parte dos $89\,000\text{ €}$, que recebeu da venda de um imóvel, num depósito a prazo. Consultou dois bancos: o Banco «Mar» e o Banco «Montanha». As propostas apresentadas pelos bancos foram as seguintes:

| Banco «Mar» | Banco «Montanha» |
| :--- | :--- |
| **Capital inicial**: $80\,000\text{ €}$ | **Capital inicial**: $85\,000\text{ €}$ |
| **Taxa de juro anual**: $2{,}3\%$ | **Taxa de juro anual**: $1{,}2\%$ |
| **Período de capitalização**: $5\text{ anos}$ | **Período de capitalização**: $5\text{ anos}$ |
| **Regime**: Juro simples | **Regime**: Juro simples |

Qual será a melhor opção para o Diogo investir o seu dinheiro? Justifica a tua resposta com base no rendimento de juros gerado.

#### Critérios e Métodos de Resolução Aceites:
- **Cálculo da Opção Banco «Mar»**:
  - Capital acumulado: $C_a = 80\,000 \times \left(1 + \frac{2{,}3}{100} \times 5\right) = 89\,200\text{ €}$
  - Juros auferidos: $J = 89\,200 - 80\,000 = 9200\text{ €}$ (ou $80\,000 \times 0{,}023 \times 5 = 9200\text{ €}$)
- **Cálculo da Opção Banco «Montanha»**:
  - Capital acumulado: $C_a = 85\,000 \times \left(1 + \frac{1{,}2}{100} \times 5\right) = 90\,100\text{ €}$
  - Juros auferidos: $J = 90\,100 - 85\,000 = 5100\text{ €}$ (ou $85\,000 \times 0{,}012 \times 5 = 5100\text{ €}$)
- **Justificação e Conclusão Aceite**:
  - A melhor proposta é a do **Banco «Mar»**, pois proporciona $9200\text{ €}$ de juros (rendimento efetivo), contra apenas $5100\text{ €}$ no Banco «Montanha».
  - No mesmo regime e horizonte temporal ($5\text{ anos}$), é mais vantajoso o banco com a taxa de juro anual mais elevada ($2{,}3\%$ vs $1{,}2\%$).

---

### Exercício 4 (Aplicação - Bloco 1)
Determina o capital inicial de um investimento, sabendo que o capital acumulado, ao fim de 4 anos, foi de $15\,600\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $1{,}5\%$.

#### Critérios e Métodos de Resolução Aceites:
- **Dados**: $C_a = 15\,600$, $n = 4\text{ anos}$, $r = 1{,}5$.
- **Método A (Equação Direta com Isolamento da Incógnita)**:
  $$C_a = C_i \times \left(1 + \frac{r}{100} \times n\right) \iff 15\,600 = C_i \times \left(1 + \frac{1{,}5}{100} \times 4\right)$$
  $$15\,600 = C_i \times 1{,}06 \iff C_i = \frac{15\,600}{1{,}06} \iff C_i \approx 14\,717\text{ €} \text{ (ou } 14\,716{,}98\text{ €)}$$
- **Método B (Raciocínio por Fator Acumulador)**:
  Como a taxa total a 4 anos é $1{,}5\% \times 4 = 6\%$, o capital acumulado representa $106\%$ do capital inicial ($1{,}06 \cdot C_i$). Logo, $C_i = 15\,600 / 1{,}06 \approx 14\,717\text{ €}$.
- **Conclusão**: O capital inicial foi de, aproximadamente, $14\,717\text{ €}$ (aceita-se $14\,716{,}98\text{ €}$).

---

## BLOCO 2: Determinação da Taxa de Juro Anual

### Exemplo 2 (Guiado Passo a Passo - Pré-Requisito do Bloco 2)
Um casal investiu $123\,000\text{ €}$ num regime de juros simples. Ao fim de $10\text{ anos}$ tinham $136\,038\text{ €}$. Qual foi a taxa de juro anual?

#### Proposta de Resolução Oficial:
- **Passo 2.1 (Juros Totais)**:
  $$J_{10} = 136\,038 - 123\,000 = 13\,038\text{ €}$$
- **Passo 2.2 (Taxa de Juro Anual $r$)**:
  $$13\,038 = 123\,000 \times \frac{r}{100} \times 10 \iff 13\,038 = 12\,300r \iff r = \frac{13\,038}{12\,300} = 1{,}06\%$$
  A taxa de juro anual foi de $1{,}06\%$.

---

### Exercício 5 (Aplicação - Bloco 2)
Um casal recebeu uma herança no valor de $57\,000\text{ €}$ e depositou o dinheiro numa conta a prazo em regime de juros simples. Ao fim de 5 anos, o capital acumulado foi de $60\,705\text{ €}$. Calcula a taxa de juro anual.

#### Critérios e Métodos de Resolução Aceites:
- **Dados**: $C_i = 57\,000$, $C_a = 60\,705$, $n = 5\text{ anos}$.
- **Método A (Equação do Capital Acumulado)**:
  $$60\,705 = 57\,000 \times \left(1 + \frac{r}{100} \times 5\right) \iff 60\,705 = 57\,000 \times (1 + 0{,}05r)$$
  $$60\,705 = 57\,000 + 2850r \iff 60\,705 - 57\,000 = 2850r \iff 3705 = 2850r \iff r = \frac{3705}{2850} = 1{,}3\%$$
- **Método B (Cálculo dos Juros + Equação Direta da Taxa)**:
  $$J = 60\,705 - 57\,000 = 3705\text{ €} \implies 3705 = 57\,000 \times i \times 5 \iff 3705 = 285\,000i \iff i = 0{,}013 \implies r = 1{,}3\%$$
- **Conclusão**: A taxa de juro anual aplicada a este depósito foi de $1{,}3\%$.

---

### Exercício 6 (Aplicação - Bloco 2)
A Emília e o Lino depositaram $12\,000\text{ €}$ numa conta a prazo, num regime de juro simples. Ao fim de 5 anos, o capital acumulado foi de $13\,200\text{ €}$. Determina a taxa de juro anual.

#### Critérios e Métodos de Resolução Aceites:
- **Dados**: $C_i = 12\,000$, $n = 5\text{ anos}$, $C_a = 13\,200$.
- **Método A (Equação do Capital Acumulado)**:
  $$13\,200 = 12\,000 \times \left(1 + \frac{r}{100} \times 5\right) \iff 13\,200 = 12\,000(1 + 0{,}05r)$$
  $$13\,200 = 12\,000 + 600r \iff 13\,200 - 12\,000 = 600r \iff 1200 = 600r \iff r = \frac{1200}{600} = 2\%$$
- **Método B (Cálculo dos Juros + Equação Direta da Taxa)**:
  $$J = 13\,200 - 12\,000 = 1200\text{ €} \implies 1200 = 12\,000 \times i \times 5 \iff 1200 = 60\,000i \iff i = 0{,}02 \implies r = 2\%$$
- **Conclusão**: A taxa de juro anual aplicada a este depósito foi de $2\%$.

</div>
