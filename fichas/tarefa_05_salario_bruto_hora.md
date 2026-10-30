# Tarefa 5: Salário Bruto à Hora e Horas Extraordinárias
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**ID Ficha**: `tarefa_05`

<div align="justify">

Esta tarefa incide sobre o cálculo do valor da retribuição horária de um trabalhador em Portugal, com base no Código do Trabalho, e a aplicação prática desse valor no apuramento da remuneração de trabalho suplementar (horas extraordinárias) e retenção na fonte.

---

## 1. Princípios e Fórmulas Legais

1. **Fórmula Legal do Salário Bruto à Hora ($V_h$)**:
   De acordo com a legislação laboral portuguesa, o valor da hora normal de trabalho calcula-se através da fórmula:
   $$V_h = \frac{SB \times 12}{52 \times n}$$
   onde:
   - $SB$ representa a remuneração base mensal (salário bruto em euros);
   - $12$ é o número de meses do ano civil;
   - $52$ é o número de semanas do ano;
   - $n$ é o período normal de trabalho semanal em número de horas (geralmente $35\text{ h}$ ou $40\text{ h}$).
   
2. **Remuneração de Horas Extraordinárias ($HE$)**:
   $$\text{Valor Total de } HE = \text{Número de Horas Suplementares} \times V_h \times \text{Fator de Acréscimo}$$
   (quando calculadas à tarifa base simples ou multiplicadas pelos coeficientes aplicáveis).

3. **Remuneração Bruta Total Mensal com Horas Extraordinárias**:
   $$SB_{\text{total}} = SB_{\text{base}} + \text{Valor das } HE$$

---

## Secção de Exemplos Guiados

### Exemplo 1: Determinação do Salário à Hora da Maria
A Maria trabalha como animadora num hotel e recebe à hora. Cumpre um horário de $8\text{ horas}$ por dia e $5\text{ dias}$ por semana ($n = 40\text{ horas semanais}$). A sua remuneração bruta mensal base é de $760{,}00\text{ €}$ (ordenado mínimo nacional da época de referência).

- **Passo 1.1: Cálculo do Rendimento Bruto Anual de Referência**
  - **Instrução ao Aluno**: Calcula o produto da remuneração mensal base por $12\text{ meses}$.
  - **Solução Esperada**: $760 \times 12 = 9120{,}00\text{ €}$
  - **Pista Pedagógica**: Multiplica o salário mensal pelos $12$ meses do ano para encontrar o rendimento base anual.

- **Passo 1.2: Cálculo do Total de Horas de Trabalho Anuais**
  - **Instrução ao Aluno**: Calcula o número de horas anuais multiplicando as $52\text{ semanas}$ pelo número de horas semanais ($40\text{ h}$).
  - **Solução Esperada**: $52 \times 40 = 2080\text{ horas}$
  - **Pista Pedagógica**: O ano civil de trabalho considera $52$ semanas completas: $52 \times 40 = 2080$.

- **Passo 1.3: Apuramento do Salário Bruto à Hora ($V_h$)**
  - **Instrução ao Aluno**: Aplica a fórmula legal $V_h = \frac{9120}{2080}$ e arredonda o resultado às centésimas.
  - **Solução Esperada**: $V_h = \frac{9120}{2080} \approx 4{,}38\text{ €/h}$
  - **Pista Pedagógica**: Divide $9120$ por $2080$. Obténs $4{,}3846\dots$, que arredondado a duas casas decimais dá $4{,}38\text{ €}$.

- **Passo 1.4: Cálculo de Trabalho Suplementar Realizado**
  - **Instrução ao Aluno**: Se a Maria realizar $10\text{ horas extraordinárias}$ no mês com a tarifa de $4{,}38\text{ €/h}$, quanto receberá a mais?
  - **Solução Esperada**: $10 \times 4{,}38 = 43{,}80\text{ €}$
  - **Pista Pedagógica**: Multiplica a quantidade de horas pelo valor à hora: $10 \times 4{,}38 = 43{,}80\text{ €}$.

---

## Secção de Exercícios de Aplicação

Resolve os seguintes exercícios no teu caderno diário, registando todos os passos de cálculo:

### Exercício 1
O Marco é mecânico, trabalha $40\text{ horas semanais}$ e aufere mensalmente um salário bruto de $1800{,}00\text{ €}$. Acordou com a gerência da oficina que realizaria trabalho suplementar aos fins de semana.
- **1.1**: Determina o valor do seu salário bruto à hora;
- **1.2**: Sabendo que em julho trabalhou $9\text{ horas extraordinárias}$, determina o valor bruto suplementar que recebeu no final desse mês.

---

### Exercício 2
O Carlos foi admitido como operador de armazém, cumprindo $40\text{ horas semanais}$ de trabalho com uma remuneração base de $760{,}00\text{ €}$.
- **2.1**: Calcula o seu salário bruto à hora;
- **2.2**: Se no primeiro mês de laboração realizar $14\text{ horas extraordinárias}$, qual será a retribuição bruta total que auferirá (vencimento base mais trabalho suplementar)?

---

### Exercício 3
Em 2023, a Rosa recebia um salário base mensal de $2789{,}43\text{ €}$. É divorciada (1 titular), reside no Porto (Continente) e tem 4 filhos a seu cargo. Trabalha 5 dias por semana, num total de $40\text{ horas semanais}$.
- **3.1**: Consulta a Tabela II do IRS (Não casado, com 4 dependentes, $2.^{\circ}$ semestre de 2023) e identifica a taxa marginal máxima de retenção na fonte correspondente;
- **3.2**: Determina o seu salário bruto à hora e o valor que deve receber a título de horas extraordinárias, sabendo que no mês de agosto prestou $8\text{ horas}$ suplementares. Qual foi a sua remuneração bruta global nesse mês?

---

### Exercício 4
Uma amiga da Maria trabalha como rececionista de hotel e aufere mensalmente $1000{,}00\text{ €}$, cumprindo um horário semanal de $35\text{ horas}$. No mês de agosto de 2023, o seu supervisor propôs-lhe que realizasse $2\text{ horas extraordinárias}$ por semana (num total de $8\text{ horas}$ no mês).  
Sabendo que a Maria (do Exemplo 1) também realizou $8\text{ horas extraordinárias}$ em agosto, qual das duas trabalhadoras recebeu um montante superior relativo a horas suplementares? Justifica calculando o valor auferido por cada uma.

---

### Exercício 5
Um técnico eletricista aufere um vencimento base de $902{,}00\text{ €}$ por um horário de $40\text{ horas semanais}$. No mês anterior cumpriu $12\text{ horas extraordinárias}$ para concluir a instalação de uma infraestrutura agropecuária.
- Determina o valor do salário bruto à hora e a quantia que o técnico auferiu pelas 12 horas suplementares realizadas.

</div>
