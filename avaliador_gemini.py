"""
Módulo de Avaliação Multimodal com Google Gemini API
Processa fotografias de cadernos dos alunos, realiza OCR manuscrito,
compara com o gabarito oficial em LaTeX e gera feedback formativo socrático.
"""

import json
import os
import re
import urllib.request
import urllib.error

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "dados", "config.json")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

RUBRICAS_OFICIAIS = {
    1: """
    Exercício 1: O Francisco depositou 1500 €, juros simples, taxa anual de 1,2%. Capital acumulado ao fim de 1 ano.
    Gabarito Oficial:
    - Método A (Fórmula Direta): $C_a = C_i \\times (1 + \\frac{r}{100} \\times n) = 1500 \\times (1 + \\frac{1{,}2}{100} \\times 1) = 1518\\text{ €}$
    - Método B (Juros + Capital): $J = 1500 \\times 0{,}012 \\times 1 = 18\\text{ €} \\implies C_a = 1500 + 18 = 1518\\text{ €}$
    Resultado Correto: $1518\\text{ €}$.
    Erros típicos: Esquecer de somar o juro ao capital inicial (apresentar apenas 18 €); errar a forma decimal de 1,2% (usar 0,12 em vez de 0,012).
    """,
    2: """
    Exercício 2: Raquel depositou 3000 € a 7 anos, juros simples, taxa anual de 1,2%.
    - 2.1: Juros no final do 1.º ano: $J_1 = 3000 \\times 0{,}012 = 36\\text{ €}$.
    - 2.2: Capital acumulado ao fim de 7 anos: $C_a = 3000 \\times (1 + 0{,}012 \\times 7) = 3252\\text{ €}$ (ou $3000 + 7 \\times 36 = 3252\\text{ €}$).
    Erros típicos: Calcular os juros de 7 anos na alínea 2.1; errar a multiplicação $7 \\times 36 = 252$; esquecer de somar ao capital de 3000 €.
    """,
    3: """
    Exercício 3: Diogo quer aplicar parte dos 89 000 € num depósito a prazo e compara dois bancos.
    - Banco «Mar»: $C_i = 80\\,000\\text{ €}$, $r = 2{,}3\\%$, $5\\text{ anos} \\implies J = 80\\,000 \\times 0{,}023 \\times 5 = 9200\\text{ €}$ (Capital acumulado $89\\,200\\text{ €}$).
    - Banco «Montanha»: $C_i = 85\\,000\\text{ €}$, $r = 1{,}2\\%$, $5\\text{ anos} \\implies J = 85\\,000 \\times 0{,}012 \\times 5 = 5100\\text{ €}$ (Capital acumulado $90\\,100\\text{ €}$).
    Decisão Correta: A melhor opção é o Banco «Mar» porque proporciona um rendimento em juros de $9200\\text{ €}$, superior aos $5100\\text{ €}$ do Banco «Montanha» (diferença favorável de $4100\\text{ €}$), devido à taxa de juro mais alta ($2{,}3\\%$ vs $1{,}2\\%$).
    Erros típicos: Escolher o Banco «Montanha» só porque o montante total aparente na conta é 90 100 €, esquecendo que o investimento inicial também era superior em 5000 € (o rendimento em juros é significativamente inferior).
    """,
    4: """
    Exercício 4: Determinar o capital inicial sabendo que o capital acumulado ao fim de 4 anos foi de 15 600 €, taxa anual de 1,5%.
    Gabarito Oficial:
    - Método A (Equação / Fórmula Direta): $15\\,600 = C_i \\times (1 + \\frac{1{,}5}{100} \\times 4) \\iff 15\\,600 = C_i \\times 1{,}06 \\iff C_i = \\frac{15\\,600}{1{,}06} \\approx 14\\,717\\text{ €}$ (aceita-se $14\\,716{,}98\\text{ €}$).
    - Método B (Taxa Global): Taxa a 4 anos: $1{,}5\\% \\times 4 = 6\\% \\implies 15\\,600$ representa $106\\%$. Logo $C_i = 15\\,600 / 1{,}06 \\approx 14\\,717\\text{ €}$.
    Resultado Correto: $14\\,717\\text{ €}$ (ou $14\\,716{,}98\\text{ €}$).
    Erros típicos: Multiplicar 15 600 por 1,06 em vez de dividir (confundir capital inicial com final); subtrair diretamente 6% a 15 600; esquecer de multiplicar a taxa pelos 4 anos.
    """,
    5: """
    Exercício 5: Herança de 57 000 €, 5 anos em juros simples, capital acumulado de 60 705 €. Determinar taxa anual.
    Gabarito Oficial:
    - Juros auferidos: $J = 60\\,705 - 57\\,000 = 3705\\text{ €}$.
    - Equação: $3705 = 57\\,000 \\times i \\times 5 \\iff 3705 = 285\\,000i \\iff i = \\frac{3705}{285\\,000} = 0{,}013 \\implies r = 1{,}3\\%$.
    - Ou por fórmula direta: $60\\,705 = 57\\,000(1 + 0{,}05r) \\iff 3705 = 2850r \\iff r = 1{,}3\\%$.
    Resultado Correto: Taxa anual de $1{,}3\\%$.
    Erros típicos: Esquecer de dividir por 5 anos; não converter a taxa decimal $0{,}013$ em percentagem ($1{,}3\\%$).
    """,
    6: """
    Exercício 6: Emília e Lino depositaram 12 000 €, 5 anos em juros simples, capital acumulado de 13 200 €. Determinar taxa anual.
    Gabarito Oficial:
    - Juros auferidos: $J = 13\\,200 - 12\\,000 = 1200\\text{ €}$.
    - Equação: $1200 = 12\\,000 \\times i \\times 5 \\iff 1200 = 60\\,000i \\iff i = \\frac{1200}{60\\,000} = 0{,}02 \\implies r = 2\\%$.
    - Ou por fórmula direta: $13\\,200 = 12\\,000(1 + 0{,}05r) \\iff 1200 = 600r \\iff r = 2\\%$.
    Resultado Correto: Taxa anual de $2\\%$.
    Erros típicos: Dividir 1200 por 12 000 esquecendo os 5 anos (obtendo erradamente 10%); erro na divisão.
    """
}

RUBRICAS_OFICIAIS_T4 = {
    1: """
    Exercício 1 (Tarefa 4 - O Mateus nos Açores):
    Dados: Salário base de 1956,40 €, solteiro, taxa de IRS de 14,6%, Segurança Social de 11%, subsídio de refeição de 5,80 €/dia (22 dias úteis).
    Gabarito Oficial:
    - Desconto Segurança Social (11%): $1956{,}40 \\times 0{,}11 = 215{,}204 \\approx 215{,}20\\text{ €}$.
    - Retenção de IRS (14,6%): $1956{,}40 \\times 0{,}146 = 285{,}6344 \\approx 285{,}63\\text{ €}$.
    - Salário líquido: $1956{,}40 - 215{,}20 - 285{,}63 = 1455{,}57\\text{ €}$.
    - Subsídio de refeição: $22 \\times 5{,}80 = 127{,}60\\text{ €}$.
    - Valor líquido total a receber: $1455{,}57 + 127{,}60 = 1583{,}17\\text{ €}$ (aceita-se entre 1583,16 € e 1583,18 €).
    Resultado Correto: $1583{,}17\\text{ €}$.
    """,
    2: """
    Exercício 2 (Tarefa 4 - O Carlos 2010 vs 2023):
    Gabarito Oficial:
    - Fevereiro de 2010: $SL = 845 - 92{,}95 - 47{,}91 = 704{,}14\\text{ €}$; $SR = 21 \\times 5{,}20 = 109{,}20\\text{ €}$; Total = $813{,}34\\text{ €}$.
    - Fevereiro de 2023: $SL = 975 - 107{,}25 - 48{,}75 = 819{,}00\\text{ €}$; $SR = 20 \\times 5{,}90 = 118{,}00\\text{ €}$; Total = $937{,}00\\text{ €}$.
    - Diferença: Mais $123{,}66\\text{ €}$ em 2023 (aumento de aproximadamente $15{,}2\\%$).
    Resultado Correto: Fevereiro de 2023: $937{,}00\\text{ €}$ (diferença de $123{,}66\\text{ €}$).
    """,
    3: """
    Exercício 3 (Tarefa 4 - Mariana na Junta de Freguesia):
    Dados: Salário base de 1700,00 €, solteira, Continente 2.º semestre 2023 (taxa marginal 28,5%, parcela 191,23 €), SS 11%, 22 dias úteis com SR de 5,20 €/dia.
    Gabarito Oficial:
    - 3.1 Retenção de IRS: $1700 \\times 0{,}285 - 191{,}23 = 484{,}50 - 191{,}23 = 293{,}27\\text{ €}$.
    - 3.2 Desconto Segurança Social: $1700 \\times 0{,}11 = 187{,}00\\text{ €}$.
    - 3.3 Total líquido: $SL = 1700 - 293{,}27 - 187{,}00 = 1219{,}73\\text{ €}$; $SR = 22 \\times 5{,}20 = 114{,}40\\text{ €}$; Total = $1219{,}73 + 114{,}40 = 1334{,}13\\text{ €}$.
    Resultado Correto: 3.1: $293{,}27\\text{ €}$; 3.2: $187{,}00\\text{ €}$; 3.3: $1334{,}13\\text{ €}$.
    """,
    4: """
    Exercício 4 (Tarefa 4 - Carina com Parcela por Fórmula):
    Dados: Salário base de 800,00 €, solteira, 21 dias úteis (SR 5,50 €/dia). Fórmula da parcela: $14{,}5\\% \\times 2{,}3 \\times (1093{,}31 - 800) = 97{,}82\\text{ €}$.
    Gabarito Oficial:
    - Retenção de IRS: $800 \\times 0{,}145 - 97{,}82 = 116{,}00 - 97{,}82 = 18{,}18\\text{ €}$.
    - Desconto SS (11%): $800 \\times 0{,}11 = 88{,}00\\text{ €}$.
    - Salário líquido: $800 - 18{,}18 - 88{,}00 = 693{,}82\\text{ €}$.
    - Subsídio de refeição: $21 \\times 5{,}50 = 115{,}50\\text{ €}$.
    - Total líquido a receber: $693{,}82 + 115{,}50 = 809{,}32\\text{ €}$.
    Resultado Correto: $809{,}32\\text{ €}$ (salário líquido de $693{,}82\\text{ €}$ e IRS de $18{,}18\\text{ €}$).
    """
}

RUBRICAS_OFICIAIS_T5 = {
    1: """
    Exercício 1 (Tarefa 5 - O Marco mecânico):
    Dados: Salário base de 1800,00 €, 40 horas semanais, 9 horas extraordinárias.
    Gabarito Oficial:
    - 1.1 Salário bruto à hora: $V_h = \\frac{1800 \\times 12}{52 \\times 40} = \\frac{21\\,600}{2080} \\approx 10{,}3846 \\approx 10{,}38\\text{ €/h}$.
    - 1.2 Horas extraordinárias: $10{,}38 \\times 9 = 93{,}42\\text{ €}$.
    Resultado Correto: 1.1: $10{,}38\\text{ €/h}$; 1.2: $93{,}42\\text{ €}$.
    """,
    2: """
    Exercício 2 (Tarefa 5 - O Carlos):
    Dados: Salário base de 760,00 €, 40 horas semanais ($V_h \\approx 4{,}38\\text{ €/h}$), 14 horas extraordinárias.
    Gabarito Oficial:
    - 2.1 Salário bruto à hora: $V_h = \\frac{760 \\times 12}{52 \\times 40} \\approx 4{,}38\\text{ €/h}$.
    - 2.2 Retribuição bruta total: $760 + (14 \\times 4{,}38) = 760 + 61{,}32 = 821{,}32\\text{ €}$.
    Resultado Correto: 2.1: $4{,}38\\text{ €/h}$; 2.2: $821{,}32\\text{ €}$.
    """,
    3: """
    Exercício 3 (Tarefa 5 - A Rosa):
    Dados: Salário base de 2789,43 €, 40 horas semanais, 8 horas extraordinárias.
    Gabarito Oficial:
    - 3.2 Salário bruto à hora: $V_h = \\frac{2789{,}43 \\times 12}{52 \\times 40} \\approx 16{,}09\\text{ €/h}$.
    - Valor das horas extraordinárias: $16{,}09 \\times 8 = 128{,}72\\text{ €}$.
    - Salário bruto total de agosto: $2789{,}43 + 128{,}72 = 2918{,}15\\text{ €}$.
    Resultado Correto: $V_h \\approx 16{,}09\\text{ €/h}$ e remuneração total de $2918{,}15\\text{ €}$.
    """,
    4: """
    Exercício 4 (Tarefa 5 - A Maria 40h):
    Dados: Salário base de 902,00 €, 40 horas semanais, 12 horas extraordinárias.
    Gabarito Oficial:
    - Salário bruto à hora: $V_h = \\frac{902 \\times 12}{52 \\times 40} = \\frac{10\\,824}{2080} = 5{,}20\\text{ €/h}$.
    - Valor das horas extraordinárias: $5{,}20 \\times 12 = 62{,}40\\text{ €}$.
    Resultado Correto: $V_h = 5{,}20\\text{ €/h}$ e valor de horas de $62{,}40\\text{ €}$.
    """,
    5: """
    Exercício 5 (Tarefa 5 - A Filipa 35h):
    Dados: Salário base de 1000,00 €, 35 horas semanais, 8 horas extraordinárias.
    Gabarito Oficial:
    - Salário bruto à hora: $V_h = \\frac{1000 \\times 12}{52 \\times 35} = \\frac{12\\,000}{1820} \\approx 6{,}5934 \\approx 6{,}59\\text{ €/h}$.
    - Valor das horas extraordinárias: $6{,}59 \\times 8 = 52{,}72\\text{ €}$.
    Resultado Correto: $V_h = 6{,}59\\text{ €/h}$ e valor das horas de $52{,}72\\text{ €}$.
    """
}

RUBRICAS_OFICIAIS_T6 = {
    1: """
    Exercício 1 (Tarefa 6 - Rita e Afonso):
    Dados: Salários de 1050,00 € e 1010,00 € (14 meses), casados sem deduções. Taxa 3.º escalão: 26,5%, parcela: 1106,73 €.
    Gabarito Oficial:
    - 1.1 Rendimento bruto anual: $(1050 + 1010) \\times 14 = 28\\,840{,}00\\text{ €}$.
    - 1.2 Rendimento coletável de referência: $28\\,840 \\div 2 = 14\\,420{,}00\\text{ €}$.
    - 1.4 Coleta individual: $14\\,420 \\times 0{,}265 - 1106{,}73 = 2714{,}57\\text{ €}$.
    - Coleta total do casal (2 titulares): $2714{,}57 \\times 2 = 5429{,}14\\text{ €}$.
    Resultado Correto: Coleta total do casal de $5429{,}14\\text{ €}$ (ou coleta individual de $2714{,}57\\text{ €}$).
    """,
    2: """
    Exercício 2 (Tarefa 6 - Manuel Solteiro):
    Dados: Salário bruto mensal de 1300,00 € (14 meses), solteiro sem deduções. 4.º escalão: taxa 28,5%, parcela 1426,65 €.
    Gabarito Oficial:
    - Rendimento bruto e coletável: $RB = RC = 1300 \\times 14 = 18\\,200{,}00\\text{ €}$.
    - Coleta final de IRS: $18\\,200 \\times 0{,}285 - 1426{,}65 = 5187{,}00 - 1426{,}65 = 3760{,}35\\text{ €}$.
    Resultado Correto: $3760{,}35\\text{ €}$.
    """,
    3: """
    Exercício 3 (Tarefa 6 - Joana e Miguel):
    Dados: Vencimentos de 1200,00 € e 1890,00 € (14 meses), casados sem deduções. 5.º escalão: taxa 35%, parcela 2772,14 €.
    Gabarito Oficial:
    - Rendimento bruto anual: $(1200 + 1890) \\times 14 = 43\\,260{,}00\\text{ €}$.
    - Rendimento coletável de referência: $43\\,260 \\div 2 = 21\\,630{,}00\\text{ €}$.
    - Coleta individual: $21\\,630 \\times 0{,}35 - 2772{,}14 = 4798{,}36\\text{ €}$.
    - Coleta total do casal: $4798{,}36 \\times 2 = 9596{,}72\\text{ €}$ (aceita-se $9596{,}36\\text{ €}$).
    Resultado Correto: Coleta total de $9596{,}72\\text{ €}$ (ou individual de $4798{,}36\\text{ €}$).
    """,
    4: """
    Exercício 4 (Tarefa 6 - Mariana e Afonso com Deduções):
    Dados: Rendimento bruto de 35 560,00 €, deduções específicas de $4104\\text{ €} \\times 2 = 8208\\text{ €}$. Taxa 26,5%, parcela 1106,73 €.
    Gabarito Oficial:
    - Rendimento após deduções: $35\\,560 - 8208 = 27\\,352{,}00\\text{ €}$.
    - Rendimento coletável de referência: $27\\,352 \\div 2 = 13\\,676{,}00\\text{ €}$.
    - Coleta individual: $13\\,676 \\times 0{,}265 - 1106{,}73 = 2517{,}41\\text{ €}$.
    - Coleta total do casal: $2517{,}41 \\times 2 = 5034{,}82\\text{ €}$.
    - Poupança obtida: $7281{,}30 - 5034{,}82 = 2246{,}48\\text{ €}$.
    Resultado Correto: Nova coleta total de $5034{,}82\\text{ €}$ (poupança de $2246{,}48\\text{ €}$).
    """,
    5: """
    Exercício 5 (Tarefa 6 - Eugénia e Augusto nos Açores):
    Dados: Salários de 2530,00 € e 2300,00 € (14 meses).
    Gabarito Oficial:
    - 5.1 Sem deduções: $RB = 67\\,620{,}00\\text{ €}$, $RC = 33\\,810{,}00\\text{ €}$. Coleta indiv: $33\\,810 \\times 0{,}259 - 2146{,}76 = 6610{,}03\\text{ €}$. Coleta total: $13\\,220{,}06\\text{ €}$.
    - 5.2 Com deduções ($4104\\text{ €} \\times 2 = 8208\\text{ €}$): Rendimento líquido de deduções: $59\\,412{,}00\\text{ €}$, $RC = 29\\,706{,}00\\text{ €}$. Coleta indiv: $29\\,706 \\times 0{,}259 - 2146{,}76 \\approx 5547{,}09\\text{ €}$. Coleta total: $11\\,094{,}19\\text{ €}$.
    - Diferença: $13\\,220{,}06 - 11\\,094{,}19 = 2125{,}87\\text{ €}$.
    Resultado Correto: Coleta final de $11\\,094{,}19\\text{ €}$ (poupança de $2125{,}87\\text{ €}$).
    """
}

RUBRICAS_OFICIAIS_T8 = {
    1: """
    Exercício 1 (Tarefa 8): Depósito de 250 000 €, taxa anual de 2,5%, capitalizações mensais (k=12), durante 10 anos.
    Gabarito Oficial:
    - Fórmula: $C_a = 250\\,000 \\times (1 + \\frac{2{,}5}{100 \\times 12})^{12 \\times 10} = 250\\,000 \\times (1 + \\frac{0{,}025}{12})^{120} \\approx 320\\,922{,}89\\text{ €}$
    Resultado Correto Exato: $320\\,922{,}89\\text{ €}$ (exigir valor exato arredondado aos cêntimos; NÃO aceitar aproximações a inteiros como $320\\,922\\text{ €}$ ou $320\\,923\\text{ €}$).
    Erros típicos: Esquecer de multiplicar por 12 no expoente (usar apenas 10); esquecer de dividir a taxa por 12; truncar ou ignorar os cêntimos.
    """,
    2: """
    Exercício 2 (Tarefa 8): Cátia obteve 136 038 € ao fim de 10 anos, taxa anual de 1,06%, capitalização semestral (k=2). Determinar capital inicial.
    Gabarito Oficial:
    - Fórmula: $136\\,038 = C_i \\times (1 + \\frac{1{,}06}{100 \\times 2})^{10 \\times 2} \\iff 136\\,038 = C_i \\times (1{,}0053)^{20} \\iff 136\\,038 = C_i \\times 1{,}111504$
    - $C_i = \\frac{136\\,038}{1{,}111504} \\approx 122\\,391{,}36\\text{ €}$.
    Resultado Correto Exato: $122\\,391{,}36\\text{ €}$ (exigir rigor aos cêntimos; NÃO aceitar número inteiro $122\\,391\\text{ €}$).
    Erros típicos: Usar k=1 em vez de k=2; multiplicar em vez de dividir no isolamento de C_i; ignorar os cêntimos no resultado final.
    """,
    3: """
    Exercício 3 (Tarefa 8): Mariana depositou 12 500 € a 4 anos com taxa anual de 1,4%. Carro custa 13 500 €.
    - 3.1: $C_a = 12\\,500 \\times (1 + 0{,}014)^4 \\approx 13\\,214{,}84\\text{ €} < 13\\,500\\text{ €}$. Logo não permite comprar o carro.
      Para comprar o carro: $C_i = \\frac{13\\,500}{(1{,}014)^4} \\approx 12\\,770{,}38\\text{ €}$ (ou $12\\,770\\text{ €}$).
    - 3.2: Capitalização mensal ($k=12$): $C_a = 12\\,500 \\times (1 + \\frac{0{,}014}{12})^{48} \\approx 13\\,219{,}54\\text{ €}$.
      Como $13\\,219{,}54\\text{ €} > 13\\,214{,}84\\text{ €}$, teria mais dinheiro (mais $4{,}70\\text{ €}$).
    Resultado Correto: Não é possível comprar o carro ($13\\,214{,}84\\text{ €}$); precisava de $12\\,770{,}38\\text{ €}$; no regime mensal acumula mais dinheiro ($13\\,219{,}54\\text{ €}$).
    """,
    4: """
    Exercício 4 (Tarefa 8): Capital acumulado de 77 660,84 € ao fim de 7 anos, capitalização trimestral (k=4), taxa anual de 3%.
    Gabarito Oficial:
    - Fórmula: $77\\,660{,}84 = C_i \\times (1 + \\frac{3}{100 \\times 4})^{7 \\times 4} = C_i \\times (1{,}0075)^{28} = C_i \\times 1{,}232712$
    - $C_i = \\frac{77\\,660{,}84}{1{,}232712} = 63\\,000\\text{ €}$.
    Resultado Correto: $63\\,000\\text{ €}$ (ou $63\\,000{,}00\\text{ €}$).
    Erros típicos: Usar expoente 7 em vez de 28; erro ao dividir por 4 na taxa trimestral.
    """,
    5: """
    Exercício 5 (Tarefa 8): Marco tem 235 000 € a 10 anos. Banco Mar (juro simples, 3,8%) vs Banco Montanha (juro composto, 3,4%).
    Gabarito Oficial:
    - Banco «Mar»: $C_a = 235\\,000 \\times (1 + 0{,}038 \\times 10) = 324\\,300\\text{ €}$.
    - Banco «Montanha»: $C_a = 235\\,000 \\times (1 + 0{,}034)^{10} \\approx 328\\,301{,}79\\text{ €}$.
    Decisão Correta: Deve optar pelo Banco «Montanha» porque gera maior capital acumulado ($328\\,301{,}79\\text{ €}$ vs $324\\,300\\text{ €}$, mais $4001{,}79\\text{ €}$ de rendimento).
    Erros típicos: Escolher o Banco Mar por ter taxa percentual nominal maior (3,8% vs 3,4%), sem calcular o efeito multiplicador dos juros compostos.
    """,
    6: """
    Exercício 6 (Tarefa 8): Cláudia depositou 8300 € a 5 anos com taxa anual de 1,8%.
    Gabarito Oficial:
    - 6.1 (Semestral, k=2): $C_a = 8300 \\times (1 + \\frac{0{,}018}{2})^{10} = 8300 \\times (1{,}009)^{10} \\approx 9077{,}63\\text{ €}$.
    - 6.2 (Mensal, k=12): $C_a = 8300 \\times (1 + \\frac{0{,}018}{12})^{60} = 8300 \\times (1{,}0015)^{60} \\approx 9080{,}63\\text{ €}$.
    Comparação: Não são iguais; o regime mensal gera mais $3{,}00\\text{ €}$ ($9080{,}63\\text{ €}$ vs $9077{,}63\\text{ €}$).
    Resultado Correto: 6.1: $9077{,}63\\text{ €}$; 6.2: $9080{,}63\\text{ €}$, sendo o mensal mais rentável.
    """
}

DICIONARIO_RUBRICAS = {
    "tarefa_04": RUBRICAS_OFICIAIS_T4,
    "tarefa_05": RUBRICAS_OFICIAIS_T5,
    "tarefa_06": RUBRICAS_OFICIAIS_T6,
    "tarefa_07": RUBRICAS_OFICIAIS,
    "tarefa_08": RUBRICAS_OFICIAIS_T8
}

def obter_config():
    api_key = DEFAULT_API_KEY
    model = DEFAULT_MODEL
    
    # 1. Tentar ler do ficheiro .env se presente
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha.startswith("GEMINI_API_KEY="):
                        val = linha.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            api_key = val
                    elif linha.startswith("GEMINI_MODEL="):
                        val = linha.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            model = val
        except Exception:
            pass

    # 2. Ficheiro config.json tem prioridade se existir
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                dados = json.load(f)
                api_key = dados.get("gemini_api_key", api_key).strip()
                model = dados.get("gemini_model", model).strip()
        except Exception:
            pass
            
    return api_key, model

def harmonizar_segunda_pessoa(texto):
    if not texto or not isinstance(texto, str):
        return texto
    substituicoes = [
        (r'\b[Oo] aluno calculou\b', 'Calculaste'),
        (r'\b[Oo] aluno obteve\b', 'Obtiveste'),
        (r'\b[Oo] aluno cometeu\b', 'Cometeste'),
        (r'\b[Oo] aluno aplicou\b', 'Aplicaste'),
        (r'\b[Oo] aluno utilizou\b', 'Utilizaste'),
        (r'\b[Oo] aluno escreveu\b', 'Escreveste'),
        (r'\b[Oo] aluno indicou\b', 'Indicaste'),
        (r'\b[Oo] aluno deve\b', 'Deves'),
        (r'\b[Oo] aluno precisa\b', 'Precisas'),
        (r'\b[Oo] aluno pode\b', 'Podes'),
        (r'\bno caderno do aluno\b', 'no teu caderno'),
        (r'\bno caderno da aluna\b', 'no teu caderno'),
        (r'\bdo aluno\b', 'teu'),
        (r'\bda aluna\b', 'tua'),
        (r'\bao aluno\b', 'a ti'),
        (r'\b[Oo] aluno\b', 'tu'),
        (r'\b[Aa] aluna\b', 'tu'),
        (r'\b[Oo] estudante\b', 'tu')
    ]
    res = texto
    for padrao, subst in substituicoes:
        res = re.sub(padrao, subst, res)
    return res

def reparar_escapes_latex(texto):
    if not texto or not isinstance(texto, str):
        return texto
    # Converter qualquer ocorrência de \euro, \text{\euro}, \textyen para símbolo € ou \text{ €}
    texto = re.sub(r'\\text\{\s*\\euro\s*\}', r'\\text{ €}', texto)
    texto = re.sub(r'\\text\{\s*€\s*\}', r'\\text{ €}', texto)
    texto = re.sub(r'\\textyen\b', r'\\text{ €}', texto)
    texto = re.sub(r'\\euro\b', r'\\text{ €}', texto)
    # Reparar caracteres de controlo ou perdas de barra invertida em comandos LaTeX
    texto = re.sub(r'[\t\x09]imes\b', r'\\times', texto)
    texto = re.sub(r'(\d+)\s*imes\s*(\d+)', r'\1 \\times \2', texto)
    texto = re.sub(r'\bimes\b', r'\\times', texto)
    texto = re.sub(r'[\x0c\f]rac\b', r'\\frac', texto)
    texto = re.sub(r'[\t\x09]ext\b', r'\\text', texto)
    texto = re.sub(r'[\x08\b]egin\b', r'\\begin', texto)
    texto = re.sub(r'[\r\x0d]ight\b', r'\\right', texto)
    texto = re.sub(r'[\n\x0a]eq\b', r'\\neq', texto)
    return texto

def assegurar_delimitadores_latex(texto):
    if not texto or not isinstance(texto, str):
        return texto
    t = texto.strip()
    if "$" in t or "$$" in t:
        return t
    if "\\" in t or re.search(r'\d+\s*[\+\-\*\/=]\s*\d+', t):
        if not re.search(r'\b(no teu caderno|escreveste|calculaste|fizeste|resolveste)\b', t, re.I):
            return f"${t}$"
        else:
            return re.sub(r'([0-9\\][0-9a-zA-Z\\_{}\s\+\-\*\/\,\.\=]+[0-9])', r'$\1$', t)
    return t

def decodificar_json_com_latex(texto):
    if not texto:
        return {}

    # Extrair bloco JSON limpo se houver código markdown ou texto livre circundante
    match_bloco = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', texto)
    if match_bloco:
        texto = match_bloco.group(1).strip()
    else:
        match_obj = re.search(r'(\{[\s\S]*\})', texto)
        if match_obj:
            texto = match_obj.group(1).strip()

    # 1. Proteger barras invertidas de LaTeX ANTES de json.loads:
    # Qualquer barra invertida não escapada que não seja \" nem \\ deve ser duplicada para \\\\
    # Isso impede que \times seja interpretado pelo JSON como tabulação ('\t' + 'imes')
    pat_escape = re.compile(r'(?<!\\)\\(?![\"\\])')
    texto_seguro = pat_escape.sub(r'\\\\', texto)

    dados = None
    try:
        dados = json.loads(texto_seguro, strict=False)
    except Exception:
        try:
            dados = json.loads(texto, strict=False)
        except Exception:
            pass

    if not dados:
        correto = bool(re.search(r'"correto"\s*:\s*true', texto, re.I))
        fb_match = re.search(r'"feedback"\s*:\s*"(.*?)(?:"\s*,\s*"pista"|"\s*\})', texto, re.DOTALL)
        pista_match = re.search(r'"pista"\s*:\s*"(.*?)"\s*\}', texto, re.DOTALL)
        transc_match = re.search(r'"transcricao_caderno"\s*:\s*"(.*?)"\s*,', texto, re.DOTALL)
        dados = {
            "correto": correto,
            "transcricao_caderno": transc_match.group(1) if transc_match else "",
            "feedback": fb_match.group(1).replace('\\"', '"') if fb_match else texto,
            "pista": pista_match.group(1).replace('\\"', '"') if pista_match else None
        }

    for k in ["feedback", "pista", "transcricao_caderno", "metodo_identificado"]:
        if k in dados and isinstance(dados[k], str):
            dados[k] = reparar_escapes_latex(dados[k])

    if "transcricao_caderno" in dados:
        dados["transcricao_caderno"] = assegurar_delimitadores_latex(dados["transcricao_caderno"])

    return dados

def avaliar_com_gemini(imagem_b64, mime_type, exercicio_id, ficha_id="tarefa_07", nota_aluno=""):
    api_key, model = obter_config()
    rubricas_tarefa = DICIONARIO_RUBRICAS.get(ficha_id, RUBRICAS_OFICIAIS)
    rubrica = rubricas_tarefa.get(int(exercicio_id), f"Exercício {exercicio_id} da {ficha_id}.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    instrucoes = f"""
És um Tutor de Matemática e Avaliador Pedagógico Formativo em Portugal.
Analisa a fotografia da resolução manuscrita no caderno para o Exercício {exercicio_id}.

Gabarito Oficial e Critérios de Validação:
{rubrica}

Anotação ou resultado complementar indicado na submissão:
{nota_aluno if nota_aluno else 'Nenhuma anotação adicional, basear a análise na fotografia do caderno.'}

REGRA DE OURO DE TRATAMENTO:
1. TRATAMENTO ESTRITAMENTE NA SEGUNDA PESSOA DO SINGULAR («TU»):
   - Dirige-te SEMPRE à pessoa que está a resolver por «tu».
   - Usa verbos e pronomes como: «calculaste», «fizeste», «escreveste», «o teu caderno», «a tua resolução», «deves rever», «repara», «obtiveste», «aplicaste».
   - É TERMINANTEMENTE PROIBIDO utilizar a expressão «o aluno», «a aluna», «o estudante» ou qualquer formulação na terceira pessoa em qualquer campo (nem em feedback, nem em pista, nem em transcricao_caderno, nem em metodo_identificado).

2. REGRA DE RIGOR NUMÉRICO EM VALORES MONETÁRIOS:
   - Em todos os valores em euros (€), exige o valor EXATO arredondado aos cêntimos (2 casas decimais / centésimas).
   - É ESTRITAMENTE PROIBIDO aceitar valores que estejam apenas "próximos" ou aproximações a números inteiros quando o cálculo envolve cêntimos (por exemplo, se o resultado correto for $320\\,922{{,}}89\\text{{ €}}$, NÃO aceites $320\\,922\\text{{ €}}$ nem $320\\,923\\text{{ €}}$; se for $122\\,391{{,}}36\\text{{ €}}$, NÃO aceites $122\\,391\\text{{ €}}$; se for $9077{{,}}63\\text{{ €}}$, NÃO aceites $9078\\text{{ €}}$).
   - Aceita notações matematicamente equivalentes para o mesmo valor exato de cêntimos, tais como $7{{,}}2\\text{{ €}}$ para $7{{,}}20\\text{{ €}}$ (omissão do zero final de centésimas) ou «7 euros e 20 cêntimos», mas os cêntimos têm de coincidir rigorosamente com o gabarito.

3. Norma Linguística: Responde rigorosamente em Português de Portugal (Português Europeu), sem translineação de palavras.

4. Notação Matemática e LaTeX em JSON:
   - Usa OBRIGATORIAMENTE LaTeX ($...$ para inline e $$...$$ para bloco) para todas as fórmulas, variáveis e valores em euros (exemplo: $1518\\text{{ €}}$).
   - NUNCA uses o comando \\euro nem \\textyen; escreve SEMPRE o símbolo direto do euro € ou \\\\text{{ €}}.
   - Em formato JSON, deves SEMPRE escrever comandos LaTeX com barra invertida dupla (exemplo: \\\\times, \\\\frac, \\\\text, \\\\approx, etc.) para que não ocorra a perda da barra ou conversão para tabulação (que geraria 'imes' em vez de '\\times').
   - No campo "transcricao_caderno", coloca sempre a expressão manuscrita identificada envolvida em delimitadores LaTeX $...$ (exemplo: "$1500 \\times 1,012 = 1518\\text{{ €}}$").

5. Leitura Visual do Caderno (OCR Manuscrito): Lê a tua escrita no caderno, fórmulas montadas, operações aritméticas intermédias e o valor final.
6. Flexibilidade de Métodos: Se aplicaste um método matematicamente correto (fórmula direta ou por etapas), valida a resolução com reforço positivo desde que o resultado numérico aos cêntimos esteja correto.
7. Se a resolução estiver CORRETA:
   - "correto": true
   - "feedback": Elogia diretamente («Fizeste um excelente trabalho!...»), descreve resumidamente o que fizeste bem no teu caderno e valida o resultado.
   - "pista": null
8. Se a resolução estiver INCORRETA, INCOMPLETA ou com ERRO DE CÁLCULO / APROXIMAÇÃO INDEVIDA:
   - "correto": false
   - "feedback": Explica de forma construtiva e pedagógica por «tu» onde erraste no teu cálculo (seja na fórmula, nos períodos ou na precisão dos cêntimos), sem dar a resposta final direta.
   - "pista": Fornece uma pergunta ou pista orientadora em LaTeX dirigida diretamente a ti («Como podes combinar o teu capital inicial com...?») para te guiar.

Responde ESTRITAMENTE em formato JSON com as seguintes chaves:
{{
  "transcricao_caderno": "expressão do caderno em LaTeX $...$ (ex.: $1500 \\times 1,012 = 1518\\text{{ €}}$)",
  "metodo_identificado": "método que aplicaste (ex.: Utilizaste a fórmula direta de capital acumulado)",
  "correto": true ou false,
  "feedback": "texto explicativo em Português de Portugal dirigido estritamente por tu",
  "pista": "pista orientadora dirigida por tu se incorreto, ou null se correto"
}}
"""

    payload = {
        "contents": [{
            "parts": [
                {"text": instrucoes},
                {
                    "inline_data": {
                        "mime_type": mime_type or "image/jpeg",
                        "data": imagem_b64
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            corpo = json.loads(resp.read().decode("utf-8"))
            candidatos = corpo.get("candidates", [])
            if not candidatos:
                return {
                    "correto": False,
                    "feedback": "Não foi possível obter resposta do modelo Gemini.",
                    "pista": "Verifica a ligação à Internet ou tenta submeter novamente a fotografia."
                }
            parts = candidatos[0].get("content", {}).get("parts", [])
            textos = [p.get("text", "") for p in parts if not p.get("thought", False) and "text" in p]
            if not textos:
                textos = [p.get("text", "") for p in parts if "text" in p]
            texto = "\n".join(textos).strip()
            
            res_dict = decodificar_json_com_latex(texto)
            res_dict["feedback"] = harmonizar_segunda_pessoa(res_dict.get("feedback", ""))
            res_dict["pista"] = harmonizar_segunda_pessoa(res_dict.get("pista", ""))
            res_dict["transcricao_caderno"] = harmonizar_segunda_pessoa(res_dict.get("transcricao_caderno", ""))
            res_dict["metodo_identificado"] = harmonizar_segunda_pessoa(res_dict.get("metodo_identificado", ""))
            return res_dict

    except urllib.error.HTTPError as e:
        erro_msg = e.read().decode('utf-8', errors='ignore')
        return {
            "correto": False,
            "feedback": f"Erro de comunicação com a API Google Gemini (HTTP {e.code}): {erro_msg[:200]}",
            "pista": "Tenta novamente dentro de momentos."
        }
    except Exception as e:
        return {
            "correto": False,
            "feedback": f"Erro ao processar a avaliação com o modelo Gemini: {str(e)}",
            "pista": "Verifica se a fotografia está nítida e tenta novamente."
        }
