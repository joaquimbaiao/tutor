# Ficha de Trabalho: Resolução de Equações do 2.º Grau
**ID Ficha**: `mat_equacoes_2grau`

<div align="justify">

## Secção de Exemplos Guiados

### Exemplo 1: Resolução pela Fórmula Resolvente
Determine as soluções da equação:
$$2x^2 - 4x - 6 = 0$$

- **Passo 1: Identificação dos Coeficientes**
  - **Instrução ao Aluno**: Indique os valores dos coeficientes $a$, $b$ e $c$.
  - **Solução Esperada**: $a = 2$, $b = -4$, $c = -6$
  - **Erro Típico**: Esquecer o sinal negativo em $b$ ou $c$ (ex.: $b = 4$).
  - **Pista Pedagógica**: Repare nos sinais que antecedem cada termo na equação $ax^2 + bx + c = 0$.

- **Passo 2: Cálculo do Binómio Discriminante ($\Delta$)**
  - **Instrução ao Aluno**: Calcule o valor do discriminante utilizando a fórmula $\Delta = b^2 - 4ac$.
  - **Solução Esperada**: $\Delta = (-4)^2 - 4 \times 2 \times (-6) = 16 + 48 = 64$
  - **Erro Típico**: Calcular $(-4)^2 = -16$ ou errar na regra de sinais do produto $-4 \times 2 \times (-6)$.
  - **Pista Pedagógica**: Lembre-se de que qualquer número negativo elevado ao quadrado resulta num valor positivo, e o produto de dois números negativos é positivo.

- **Passo 3: Aplicação da Fórmula e Soluções Finais**
  - **Instrução ao Aluno**: Substitua os valores na fórmula $x = \frac{-b \pm \sqrt{\Delta}}{2a}$ e calcule as soluções.
  - **Solução Esperada**: $x = \frac{4 \pm \sqrt{64}}{2 \times 2} = \frac{4 \pm 8}{4} \implies x_1 = 3 \lor x_2 = -1$
  - **Erro Típico**: Esquecer de multiplicar o denominador por $2a$ (deixar apenas 2) ou trocar o sinal de $-b$.
  - **Pista Pedagógica**: O termo $-b$ significa o simétrico de $b$. Se $b = -4$, qual é o seu simétrico?

---

## Secção de Exercícios de Aplicação

### Exercício 1
- **Enunciado**: Resolva a seguinte equação em $\mathbb{R}$:
$$x^2 - 5x + 6 = 0$$
- **Imagem de Apoio**: Nenhuma
- **Critérios de Validação Formativa**:
  - **Identificação**: $a = 1$, $b = -5$, $c = 6$
  - **Discriminante**: $\Delta = (-5)^2 - 4(1)(6) = 25 - 24 = 1$
  - **Soluções**: $x = \frac{5 \pm 1}{2} \implies x \in \{2, 3\}$
  - **Feedback para Erro Típico**: Se o aluno encontrar $x \in \{-2, -3\}$, alertar para a troca de sinais na aplicação de $-b$.

### Exercício 2
- **Enunciado**: Determine as dimensões de um retângulo cuja área é dada por $A = 24\text{ cm}^2$, sabendo que o comprimento excede a largura em $2\text{ cm}$.
- **Imagem de Apoio**: `fichas/imagens/retangulo_exercicio2.png`
- **Critérios de Validação Formativa**:
  - **Equação Formulada**: $x(x + 2) = 24 \iff x^2 + 2x - 24 = 0$
  - **Discriminante**: $\Delta = 2^2 - 4(1)(-24) = 4 + 96 = 100$
  - **Soluções Algébricas**: $x = \frac{-2 \pm 10}{2} \implies x = 4 \lor x = -6$
  - **Interpretação Geométrica**: Rejeitar $x = -6$ por se tratar de uma medida de comprimento, concluindo que a largura é $4\text{ cm}$ e o comprimento é $6\text{ cm}$.
  - **Feedback para Erro Típico**: Se o aluno considerar a solução negativa, questionar se faz sentido físico um comprimento negativo.

</div>
