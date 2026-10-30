# Tarefa 4: Matemática nos Salários
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**ID Ficha**: `tarefa_04`

<div align="justify">

Esta tarefa foca o cálculo dos vencimentos em Portugal: a relação entre o salário bruto (remuneração base), os descontos obrigatórios para a Segurança Social e a retenção na fonte para o IRS (Imposto sobre o Rendimento de Pessoas Singulares), bem como o processamento do subsídio de refeição para a obtenção do salário líquido e do valor total líquido a receber.

---

## 1. Princípios e Regras de Cálculo Salarial

1. **Remuneração Base / Salário Bruto ($SB$)**: Quantia acordada antes de quaisquer retenções ou deduções legais.
2. **Contribuição para a Segurança Social ($SS$)**: Desconto obrigatório do trabalhador dependente fixado legalmente em $11\%$ sobre o salário base:
   $$SS = SB \times 0{,}11$$
3. **Retenção na Fonte de IRS**: Adiantamento mensal por conta do imposto devido no final do ano fiscal. Obtém-se consultando as tabelas oficiais de retenção em vigor ou aplicando a taxa marginal máxima subtraída da respetiva parcela a abater:
   $$\text{Retenção IRS} = SB \times \text{Taxa de IRS} \quad \text{ou} \quad SB \times \text{Taxa Marginal} - \text{Parcela a abater}$$
4. **Subsídio de Refeição ($SR$)**: Compensação por cada dia de trabalho efetivo realizado no mês. O valor até $6{,}00\text{ €}$ por dia (em numerário) está isento de tributação:
   $$SR = \text{Dias de Trabalho} \times \text{Valor Diário}$$
5. **Salário Líquido ($SL$)**: Rendimento do trabalhador após a dedução dos descontos fiscais e sociais:
   $$SL = SB - SS - \text{Retenção IRS}$$
6. **Valor Total Líquido a Receber**: Quantia final depositada na conta bancária do trabalhador no fim do mês:
   $$\text{Total a Receber} = SL + SR$$

---

## Secção de Exemplos Guiados

### Exemplo 1: Processamento de Vencimento Mensal com Consulta de Tabelas
A Catarina é casada (2 titulares), tem 1 filho (1 dependente), reside em Braga (Continente) e aufere mensalmente uma remuneração base de $1256{,}20\text{ €}$. Desconta $11\%$ para a Segurança Social e aufere $5{,}20\text{ €}$ diários de subsídio de refeição. Em abril de 2023 trabalhou 20 dias úteis (de segunda a sexta-feira).

- **Passo 1.1: Identificação da Taxa de Retenção de IRS e Cálculo do Desconto**
  - **Instrução ao Aluno**: Consulta a Tabela III (Casado, dois titulares, 1 dependente) do 1.º semestre de 2023. Na linha da remuneração até $1280{,}00\text{ €}$, a taxa aplicável é de $12{,}3\%$. Calcula o valor retido na fonte para o IRS.
  - **Solução Esperada**: $\text{IRS} = 1256{,}20 \times 0{,}123 = 154{,}51\text{ €}$
  - **Pista Pedagógica**: Multiplica a remuneração base ($1256{,}20\text{ €}$) pela taxa decimal $0{,}123$ e arredonda o resultado às centésimas.

- **Passo 1.2: Cálculo da Contribuição para a Segurança Social**
  - **Instrução ao Aluno**: Calcula o valor descontado para a Segurança Social ($11\%$).
  - **Solução Esperada**: $SS = 1256{,}20 \times 0{,}11 = 138{,}18\text{ €}$
  - **Pista Pedagógica**: O desconto para a Segurança Social é de $11\%$ sobre o salário base: $1256{,}20 \times 0{,}11 = 138{,}182 \approx 138{,}18\text{ €}$.

- **Passo 1.3: Cálculo do Salário Líquido**
  - **Instrução ao Aluno**: Determina o salário líquido da Catarina deduzindo à remuneração base os descontos do IRS e da Segurança Social.
  - **Solução Esperada**: $SL = 1256{,}20 - 154{,}51 - 138{,}18 = 963{,}51\text{ €}$
  - **Pista Pedagógica**: O salário líquido resulta de subtrair ao salário bruto a soma dos dois descontos: $1256{,}20 - (154{,}51 + 138{,}18) = 963{,}51\text{ €}$.

- **Passo 1.4: Cálculo do Subsídio de Refeição**
  - **Instrução ao Aluno**: Calcula o valor total do subsídio de refeição relativo aos 20 dias de trabalho realizados.
  - **Solução Esperada**: $SR = 20 \times 5{,}20 = 104{,}00\text{ €}$
  - **Pista Pedagógica**: Multiplica o número de dias úteis trabalhados ($20$) pelo valor diário estipulado ($5{,}20\text{ €}$).

- **Passo 1.5: Cálculo do Valor Total a Receber no Final do Mês**
  - **Instrução ao Aluno**: Calcula o montante total líquido transferido para a conta da Catarina no fim do mês.
  - **Solução Esperada**: $\text{Total a Receber} = 963{,}51 + 104{,}00 = 1067{,}51\text{ €}$
  - **Pista Pedagógica**: Adiciona o subsídio de refeição isento ao salário líquido previamente apurado: $963{,}51 + 104{,}00 = 1067{,}51\text{ €}$.

---

## Secção de Exercícios de Aplicação

Resolve os seguintes exercícios no teu caderno diário com todo o rigor matemático e apresenta os cálculos detalhados.

### Exercício 1
O Mateus é solteiro e não tem filhos, reside nos Açores e aufere mensalmente uma remuneração base de $1956{,}40\text{ €}$. Desconta $11\%$ para a Segurança Social e recebe $5{,}80\text{ €}$ por dia de subsídio de refeição. Em setembro de 2022 trabalhou 22 dias úteis de segunda a sexta-feira, sendo a sua taxa de retenção de IRS de $14{,}6\%$.  
Calcula o valor líquido total que o Mateus recebeu no final do mês de setembro de 2022.

---

### Exercício 2
Compara os valores líquidos recebidos pelo Carlos em fevereiro de 2010 e em fevereiro de 2023, tendo em conta os seguintes dados constantes do seu registo profissional:

| Indicador | Fevereiro de 2010 | Fevereiro de 2023 |
| :--- | :--- | :--- |
| **Estado Civil e Família** | Solteiro, sem filhos | Casado (2 titulares), 3 filhos |
| **Residência** | Região Autónoma da Madeira | Lisboa (Continente) |
| **Salário Bruto** | $845{,}00\text{ €}$ | $975{,}00\text{ €}$ |
| **Segurança Social** | $11\%$ | $11\%$ |
| **Taxa de IRS** | $5{,}67\%$ | $5{,}00\%$ |
| **Subsídio de Alimentação** | $5{,}20\text{ €}$ por dia | $5{,}90\text{ €}$ por dia |
| **Dias Úteis Trabalhados** | 21 dias | 20 dias |

Calcula o total auferido em cada um dos meses e indica a diferença percentual e absoluta entre eles.

---

### Exercício 3
A Mariana é funcionária na Junta de Freguesia de Avelares e, após ter sido promovida, passou a auferir um salário bruto mensal de $1700{,}00\text{ €}$. É solteira, não tem dependentes a cargo e reside no Continente. Trabalhou 22 dias úteis no mês, recebendo $5{,}20\text{ €}$ por dia de subsídio de alimentação.  
No 2.º semestre de 2023, segundo a Tabela I de retenção na fonte para o Continente, a sua remuneração enquadra-se no escalão com taxa marginal máxima de $28{,}50\%$ e parcela a abater de $191{,}23\text{ €}$, calculando-se o imposto retido por:
$$\text{Retenção IRS} = \text{Salário Bruto} \times \text{Taxa Marginal} - \text{Parcela a abater}$$
Determina:
- **3.1**: O valor retido na fonte relativo ao IRS;
- **3.2**: O desconto para a Segurança Social;
- **3.3**: O valor total líquido que a Mariana recebeu no final do mês.

---

### Exercício 4
A Carina aufere um salário bruto de $800{,}00\text{ €}$ mensais. É solteira, sem filhos e reside no Continente. No mês de setembro de 2023 trabalhou 21 dias úteis, auferindo um subsídio de refeição de $5{,}50\text{ €}$ diários.  
De acordo com a Tabela I do 2.º semestre de 2023 para trabalhadores não casados sem dependentes com remuneração até $886{,}57\text{ €}$, a taxa marginal máxima é de $14{,}50\%$ e a fórmula da parcela a abater é dada por:
$$\text{Parcela a abater} = 14{,}5\% \times 2{,}3 \times (1093{,}31 - R)$$
onde $R$ representa a remuneração mensal bruta ($800{,}00\text{ €}$).  
Determina o valor da parcela a abater, a retenção na fonte de IRS, o salário líquido e o montante global recebido pela Carina em setembro de 2023.

</div>
