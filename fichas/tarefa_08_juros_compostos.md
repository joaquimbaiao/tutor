# Tarefa 8: Matemática na Poupança e no Crédito (Juros Compostos)
**Módulo**: P1 - Modelos Matemáticos para a Cidadania  
**ID Ficha**: `tarefa_08`

<div align="justify">

Esta ficha de trabalho destina-se ao estudo e aplicação prática do regime de juros compostos, capitalizações periódicas (anuais, semestrais, trimestrais, mensais e diárias) e à tomada de decisões financeiras fundamentadas no âmbito da literacia para a cidadania.

---

## Secção de Exemplos Guiados

### Exemplo 1: Conceito Fundamental e Evolução do Juro Composto
Supõe que depositavas $650\text{ €}$ numa conta a prazo, num regime de juros compostos, durante três anos, a uma taxa de juro anual de $4\%$.

- **Passo 1.1: Juros no final do 1.º ano**
  - **Instrução ao Aluno**: Calcula o valor dos juros auferidos no termo do primeiro ano de aplicação.
  - **Solução Esperada**: $J_1 = 650 \times 0{,}04 = 26\text{ €}$
  - **Erro Típico**: Errar na conversão da taxa decimal ($0{,}4$ em vez de $0{,}04$).
  - **Pista Pedagógica**: No primeiro ano, o juro calcula-se multiplicando o capital inicial pela taxa anual ($4\% = 0{,}04$).

- **Passo 1.2: Capital acumulado no final do 1.º ano**
  - **Instrução ao Aluno**: Determina o montante total existente na conta no fim do 1.º ano.
  - **Solução Esperada**: $C_1 = 650 + 26 = 676\text{ €}$ (ou $650 \times 1{,}04 = 676\text{ €}$)
  - **Erro Típico**: Não somar os juros ao capital inicial.
  - **Pista Pedagógica**: O capital acumulado é a soma do capital inicial com os juros obtidos: $C_1 = C_0 + J_1$.

- **Passo 1.3: Total de juros acumulados ao fim de 3 anos**
  - **Instrução ao Aluno**: Calcula o valor total de juros acumulados nos 3 anos, tendo em conta a capitalização dos juros ano a ano.
  - **Solução Esperada**:
    - 1.º ano: $26\text{ €} \implies C_1 = 676\text{ €}$
    - 2.º ano: $J_2 = 676 \times 0{,}04 = 27{,}04\text{ €} \implies C_2 = 703{,}04\text{ €}$
    - 3.º ano: $J_3 = 703{,}04 \times 0{,}04 = 28{,}1216 \approx 28{,}12\text{ €}$
    - Total de juros acumulados: $26 + 27{,}04 + 28{,}12 = 81{,}16\text{ €}$
  - **Erro Típico**: Multiplicar $26\text{ €} \times 3 = 78\text{ €}$ (confundindo com regime de juros simples).
  - **Pista Pedagógica**: No regime de juros compostos, os juros de cada ano vencem novos juros nos anos seguintes. Calcula o juro de cada ano com base no capital acumulado no ano imediatamente anterior.

- **Passo 1.4: Capital acumulado no final dos 3 anos**
  - **Instrução ao Aluno**: Indica o capital total acumulado no termo dos 3 anos.
  - **Solução Esperada**: $C_3 = 650 \times (1 + 0{,}04)^3 = 650 \times 1{,}124864 \approx 731{,}16\text{ €}$ (ou $650 + 81{,}16 = 731{,}16\text{ €}$)
  - **Erro Típico**: Omitir os cêntimos ou arredondar prematuramente durante as etapas intermédias.
  - **Pista Pedagógica**: Podes aplicar diretamente a fórmula fundamental dos juros compostos $C_n = C_0(1 + i)^n$ com $n = 3$ ou somar o total de juros acumulados ($81{,}16\text{ €}$) ao capital inicial ($650\text{ €}$).

---

### Exemplo 2: Períodos de Capitalização Subanuais e Resolução de Equações

- **Passo 2.1: Capitalização diária a 11 anos**
  - **Enunciado**: Determina o capital acumulado, ao fim de 11 anos, num regime de capitalização diário de juros compostos, sabendo que o capital inicial foi de $250\,000\text{ €}$ e que a taxa de juro anual é de $2{,}5\%$. (Considera o ano comercial com 360 dias).
  - **Solução Esperada**:
    $$C_a = 250\,000 \times \left(1 + \frac{2{,}5}{100 \times 360}\right)^{11 \times 360} \approx 329\,129{,}53\text{ €}$$
  - **Erro Típico**: Esquecer a multiplicação do número de anos no expoente ($11 \times 360 = 3960$ períodos) ou não dividir a taxa por 360.
  - **Pista Pedagógica**: Quando a capitalização é diária, divide a taxa anual pelo número de dias ($k = 360$) e multiplica os anos pelo mesmo fator no expoente: $n \times k = 11 \times 360$.

- **Passo 2.2: Determinação do número de anos de vigência**
  - **Enunciado**: Num regime de capitalização trimestral de juros compostos, a taxa de juro anual é de $3{,}2\%$. Sabendo que o capital final é de $10\,477{,}02\text{ €}$ e que o inicial foi de $9830\text{ €}$, determina quantos anos o depósito esteve em vigor.
  - **Solução Esperada**:
    $$10\,477{,}02 = 9830 \times \left(1 + \frac{0{,}032}{4}\right)^{4n} \iff \frac{10\,477{,}02}{9830} = (1{,}008)^{4n} \iff 1{,}06582 \approx (1{,}008)^{4n}$$
    Para $n = 1 \implies (1{,}008)^4 \approx 1{,}03239 \neq 1{,}06582$  
    Para $n = 2 \implies (1{,}008)^8 \approx 1{,}06582$ (Verdadeiro)  
    O depósito esteve em vigor durante $2\text{ anos}$.
  - **Erro Típico**: Dividir o expoente por 4 em vez de multiplicar, ou parar a verificação no primeiro ano.
  - **Pista Pedagógica**: Como os juros são trimestrais ($k = 4$), a taxa trimestral é $\frac{0{,}032}{4} = 0{,}008$. Testa os valores inteiros de $n$ na potência $(1{,}008)^{4n}$ até obteres a razão $\frac{10\,477{,}02}{9830} \approx 1{,}06582$.

---

## Secção de Exercícios de Aplicação

### Exercício 1 (Bloco 1)
- **Enunciado**: Tendo em conta o primeiro exercício resolvido no Exemplo 2 (onde $C_i = 250\,000\text{ €}$ e a taxa anual é de $2{,}5\%$), determina o valor do capital acumulado durante um período de $10\text{ anos}$, sabendo que as capitalizações são mensais.
- **Orientações no Caderno**: Regista as variáveis $C_i = 250\,000$, $r = 2{,}5$, $n = 10$, $k = 12$ e desenvolve a fórmula com $120$ períodos mensais de capitalização.
- **Resultado Correto**: $C_a \approx 320\,922{,}89\text{ €}$

### Exercício 2 (Bloco 1)
- **Enunciado**: A Cátia investiu um determinado capital numa conta a prazo, em regime de juros compostos semestrais, a uma taxa de juro anual de $1{,}06\%$. No final dos 10 anos obteve $136\,038\text{ €}$. Qual foi o capital inicial investido?
- **Orientações no Caderno**: Identifica $C_a = 136\,038\text{ €}$, $r = 1{,}06\%$, $n = 10\text{ anos}$ e $k = 2$. Monta a equação $136\,038 = C_i \left(1 + \frac{1{,}06}{200}\right)^{20}$ e isola $C_i$.
- **Resultado Correto**: $C_i \approx 122\,391{,}36\text{ €}$

### Exercício 3 (Bloco 1)
- **Enunciado**: Em agosto de 2023, a Mariana vendeu o seu carro por $12\,500\text{ €}$. Depositou o dinheiro numa conta a prazo, em regime de juros compostos, com uma taxa de juro anual de $1{,}4\%$.
  - **3.1**: Será que ao fim de 4 anos o capital acumulado lhe permite comprar um carro no valor de $13\,500\text{ €}$? Caso não seja possível, determina o valor que deveria ter sido depositado inicialmente para conseguir comprar este carro.
  - **3.2**: Se a capitalização dos juros fosse mensal, em vez de anual, a Mariana teria mais dinheiro acumulado ao fim de 4 anos? Justifica a tua resposta com os respetivos cálculos.
- **Orientações no Caderno**:
  - Em 3.1: Calcula $C_a = 12\,500(1 + 0{,}014)^4 \approx 13\,214{,}84\text{ €} < 13\,500\text{ €}$. Para $C_a = 13\,500\text{ €}$, calcula $C_i = \frac{13\,500}{(1{,}014)^4} \approx 12\,770\text{ €}$.
  - Em 3.2: Calcula a capitalização mensal $C_a = 12\,500\left(1 + \frac{0{,}014}{12}\right)^{48} \approx 13\,219{,}54\text{ €}$ e compara ($13\,219{,}54\text{ €} > 13\,214{,}84\text{ €}$).
- **Resultados Corretos**: $13\,214{,}84\text{ €}$ (insuficiente); $C_i \approx 12\,770\text{ €}$; mensal rende $13\,219{,}54\text{ €}$, logo teria mais $4{,}70\text{ €}$.

### Exercício 4 (Bloco 1)
- **Enunciado**: Ao fim de 7 anos, num regime de capitalização trimestral de juros compostos, obteve-se um capital final de $77\,660{,}84\text{ €}$. Sabendo que a taxa de juro anual foi de $3\%$, determina o valor do capital inicial.
- **Orientações no Caderno**: Substitui os dados $C_a = 77\,660{,}84$, $n = 7$, $r = 3\%$, $k = 4$ na fórmula $77\,660{,}84 = C_i \left(1 + \frac{3}{400}\right)^{28}$ e resolve em ordem a $C_i$.
- **Resultado Correto**: $C_i \approx 63\,000\text{ €}$

### Exercício 5 (Bloco 2)
- **Enunciado**: O Marco vendeu uma casa por $235\,000\text{ €}$ e resolveu investir numa aplicação financeira. Consultou dois bancos:
  - **Banco «Mar»**: Capital inicial: $235\,000\text{ €}$; Taxa de juro anual: $3{,}8\%$; Prazo: $10\text{ anos}$; Regime: Juro simples.
  - **Banco «Montanha»**: Capital inicial: $235\,000\text{ €}$; Taxa de juro anual: $3{,}4\%$; Prazo: $10\text{ anos}$; Regime: Juro composto.
  O que sugeres ao Marco? Fundamenta a tua resposta calculando o capital acumulado em cada banco.
- **Orientações no Caderno**:
  - Banco «Mar» (Juros Simples): $C_a = 235\,000 \times (1 + 0{,}038 \times 10) = 324\,300\text{ €}$.
  - Banco «Montanha» (Juros Compostos): $C_a = 235\,000 \times (1 + 0{,}034)^{10} \approx 328\,301{,}79\text{ €}$.
  - Conclui recomendando o Banco «Montanha», pois proporciona uma mais-valia superior em $4001{,}79\text{ €}$.
- **Resultado Correto**: Banco «Montanha» ($328\,301{,}79\text{ €}$ vs $324\,300\text{ €}$).

### Exercício 6 (Bloco 2)
- **Enunciado**: A Cláudia vendeu um carro por $8300\text{ €}$ e depositou esse dinheiro numa conta a prazo, em regime de juros compostos, por um período de $5\text{ anos}$. A taxa de juro anual foi de $1{,}8\%$.
  - **6.1**: Determina o valor do capital acumulado ao fim dos 5 anos se as capitalizações forem semestrais.
  - **6.2**: Determina o valor do capital acumulado ao fim dos 5 anos se as capitalizações forem mensais. O capital acumulado seria igual ao obtido em 6.1?
- **Orientações no Caderno**:
  - 6.1 (Semestral, $k = 2$): $C_a = 8300 \left(1 + \frac{0{,}018}{2}\right)^{10} = 8300 \times (1{,}009)^{10} \approx 9077{,}63\text{ €}$.
  - 6.2 (Mensal, $k = 12$): $C_a = 8300 \left(1 + \frac{0{,}018}{12}\right)^{60} = 8300 \times (1{,}0015)^{60} \approx 9080{,}63\text{ €}$.
  - Conclui que os capitais não são iguais: a capitalização mensal é ligeiramente superior em $3{,}00\text{ €}$ devido à maior frequência de capitalização.
- **Resultados Corretos**: $6.1: 9077{,}63\text{ €}$; $6.2: 9080{,}63\text{ €}$ (com mais $3{,}00\text{ €}$ no regime mensal).

</div>
