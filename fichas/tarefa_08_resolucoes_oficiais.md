# Critérios Oficiais de Resolução e Gabaritos: Tarefa 8
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**Unidade Temática**: Matemática na Poupança e no Crédito (Juros Compostos)  
**ID Ficha**: `tarefa_08`

<div align="justify">

Este documento estabelece os critérios pedagógicos oficiais, fórmulas em notação LaTeX e resoluções integrais dos exercícios da Tarefa 8 para avaliação formativa presencial e via IA multimodal (Google Gemini).

---

### Exemplo 1: Evolução Ano a Ano de Juros Compostos
- **Passo 1.1 (Juros 1.º ano)**:
  $$J_1 = 650 \times 0{,}04 = 26\text{ €}$$
- **Passo 1.2 (Capital 1.º ano)**:
  $$C_1 = 650 + 26 = 676\text{ €}$$
- **Passo 1.3 (Total de Juros em 3 anos)**:
  - 1.º ano: $26\text{ €} \implies C_1 = 676\text{ €}$
  - 2.º ano: $J_2 = 676 \times 0{,}04 = 27{,}04\text{ €} \implies C_2 = 703{,}04\text{ €}$
  - 3.º ano: $J_3 = 703{,}04 \times 0{,}04 = 28{,}12\text{ €} \implies C_3 = 731{,}16\text{ €}$
  - Soma dos juros: $26 + 27{,}04 + 28{,}12 = 81{,}16\text{ €}$
- **Passo 1.4 (Capital acumulado 3 anos)**:
  $$C_3 = 650 + 81{,}16 = 731{,}16\text{ €} \quad \text{ou} \quad C_3 = 650 \times (1{,}04)^3 \approx 731{,}16\text{ €}$$

---

### Exemplo 2: Capitalização Fracionada e Determinação de Prazo
- **Passo 2.1 (Capitalização diária, $k = 360$, $n = 11$, $C_0 = 250\,000\text{ €}$, $r = 2{,}5\%$)**:
  $$C_a = 250\,000 \times \left(1 + \frac{2{,}5}{100 \times 360}\right)^{11 \times 360} \approx 329\,129{,}53\text{ €}$$
- **Passo 2.2 (Trimestral, $k = 4$, $r = 3{,}2\%$, $C_0 = 9830\text{ €}$, $C_a = 10\,477{,}02\text{ €}$)**:
  $$\frac{10\,477{,}02}{9830} = \left(1 + \frac{0{,}032}{4}\right)^{4n} \iff 1{,}06582 = (1{,}008)^{4n}$$
  Para $n = 2 \implies (1{,}008)^8 \approx 1{,}06582$. O depósito esteve ativo durante $2\text{ anos}$.

---

### Exercício 1: Aplicação com Capitalização Mensal
- **Dados**: $C_i = 250\,000\text{ €}$, $r = 2{,}5\%$, $n = 10\text{ anos}$, $k = 12$ (mensal).
- **Resolução Oficial**:
  $$C_a = 250\,000 \times \left(1 + \frac{2{,}5}{100 \times 12}\right)^{12 \times 10} = 250\,000 \times \left(1 + \frac{0{,}025}{12}\right)^{120} \approx 320\,922{,}89\text{ €}$$
- **Critérios de Validação**:
  - Identificação correta das variáveis: $C_i = 250\,000$, $r = 2{,}5$, $n = 10$, $k = 12$.
  - Cálculo do expoente total de períodos: $12 \times 10 = 120$.
  - Resultado final rigoroso: $320\,922{,}89\text{ €}$ (aceitando aproximações entre $320\,922\text{ €}$ e $320\,923\text{ €}$).

---

### Exercício 2: Determinação de Capital Inicial com Capitalização Semestral
- **Dados**: $C_a = 136\,038\text{ €}$, $r = 1{,}06\%$, $n = 10\text{ anos}$, $k = 2$ (semestral).
- **Resolução Oficial**:
  $$136\,038 = C_i \times \left(1 + \frac{1{,}06}{100 \times 2}\right)^{10 \times 2} \iff 136\,038 = C_i \times (1{,}0053)^{20} \iff 136\,038 = C_i \times 1{,}111504$$
  $$C_i = \frac{136\,038}{1{,}111504} \approx 122\,391{,}36\text{ €}$$
- **Critérios de Validação**:
  - Identificação correta da fórmula de juro composto semestral ($k = 2$).
  - Isolamento algébrico de $C_i$.
  - Resultado final: aproximadamente $122\,391{,}36\text{ €}$ (ou arredondado a $122\,391\text{ €}$).

---

### Exercício 3: Decisão Financeira e Comparação de Frequências (Mariana)
- **Dados**: $C_i = 12\,500\text{ €}$, $r = 1{,}4\%$, $n = 4\text{ anos}$.
- **Alínea 3.1 (Capitalização Anual e Capital Inicial Necessário)**:
  - Capital acumulado ao fim de 4 anos:
    $$C_a = 12\,500 \times (1 + 0{,}014)^4 = 12\,500 \times 1{,}057187 \approx 13\,214{,}84\text{ €}$$
  - Comparação: $13\,214{,}84\text{ €} < 13\,500\text{ €}$, logo o montante acumulado não permite comprar o carro.
  - Capital inicial necessário para atingir $13\,500\text{ €}$:
    $$13\,500 = C_i \times (1{,}014)^4 \iff C_i = \frac{13\,500}{1{,}057187} \approx 12\,769{,}73\text{ €} \approx 12\,770\text{ €}$$
- **Alínea 3.2 (Capitalização Mensal vs Anual)**:
  - Capital com capitalização mensal ($k = 12$):
    $$C_a = 12\,500 \times \left(1 + \frac{0{,}014}{12}\right)^{48} \approx 13\,219{,}54\text{ €}$$
  - Conclusão: Sim, a Mariana teria mais dinheiro se as capitalizações fossem mensais ($13\,219{,}54\text{ €} > 13\,214{,}84\text{ €}$, auferindo mais $4{,}70\text{ €}$).

---

### Exercício 4: Capital Inicial com Capitalização Trimestral
- **Dados**: $C_a = 77\,660{,}84\text{ €}$, $r = 3\%$, $n = 7\text{ anos}$, $k = 4$ (trimestral).
- **Resolução Oficial**:
  $$77\,660{,}84 = C_i \times \left(1 + \frac{3}{100 \times 4}\right)^{7 \times 4} \iff 77\,660{,}84 = C_i \times (1{,}0075)^{28} \iff 77\,660{,}84 = C_i \times 1{,}232712$$
  $$C_i = \frac{77\,660{,}84}{1{,}232712} \approx 63\,000\text{ €}$$
- **Critérios de Validação**:
  - Aplicação de $k = 4$ e período total de $28$ trimestres.
  - Resultado final exato: $C_i = 63\,000\text{ €}$.

---

### Exercício 5: Estudo Comparativo Banco «Mar» vs Banco «Montanha» (Marco)
- **Dados**: $C_i = 235\,000\text{ €}$, $n = 10\text{ anos}$.
- **Banco «Mar» (Juro Simples, $r = 3{,}8\%$)**:
  $$C_a = 235\,000 \times (1 + 0{,}038 \times 10) = 235\,000 \times 1{,}38 = 324\,300\text{ €}$$
- **Banco «Montanha» (Juro Composto, $r = 3{,}4\%$)**:
  $$C_a = 235\,000 \times (1 + 0{,}034)^{10} = 235\,000 \times 1{,}397029 \approx 328\,301{,}79\text{ €}$$
- **Decisão e Parecer**:
  - Recomendação ao Marco: Deve optar pelo Banco «Montanha».
  - Justificação: Embora a taxa aparente seja ligeiramente menor ($3{,}4\%$ vs $3{,}8\%$), o efeito capitalizador dos juros compostos gera um capital final de $328\,301{,}79\text{ €}$, superando o Banco «Mar» em $4001{,}79\text{ €}$.

---

### Exercício 6: Comparação de Regimes Semestral e Mensal (Cláudia)
- **Dados**: $C_i = 8300\text{ €}$, $n = 5\text{ anos}$, $r = 1{,}8\%$.
- **Alínea 6.1 (Capitalização Semestral, $k = 2$)**:
  $$C_a = 8300 \times \left(1 + \frac{0{,}018}{2}\right)^{10} = 8300 \times (1{,}009)^{10} \approx 9077{,}63\text{ €}$$
- **Alínea 6.2 (Capitalização Mensal, $k = 12$)**:
  $$C_a = 8300 \times \left(1 + \frac{0{,}018}{12}\right)^{60} = 8300 \times (1{,}0015)^{60} \approx 9080{,}63\text{ €}$$
  - O capital acumulado não seria igual: no regime mensal o valor acumulado é superior em $3{,}00\text{ €}$ ($9080{,}63\text{ €} > 9077{,}63\text{ €}$).

</div>
