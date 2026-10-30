"""
Dashboard Docente de Avaliação Formativa (Tutor de Matemática).
Permite acompanhar em tempo real o desempenho da turma e o progresso individual.
Execução via:
- Web Integrada nativa (sem dependências): python3 servidor_simulacao.py
- Streamlit (se instalado): streamlit run dashboard.py
"""

import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dados", "tutor.db")

def formatar_tempo(segundos):
    if segundos is None or segundos <= 0:
        return "—"
    s = int(round(segundos))
    if s < 60:
        return f"{s}s"
    m = s // 60
    resto = s % 60
    return f"{m}m {resto:02d}s"

ITENS_OFICIAIS_T7 = [
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.1", "tipo": "exemplo", "numero": 1, "passo": "1.1"},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.2", "tipo": "exemplo", "numero": 1, "passo": "1.2"},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.3", "tipo": "exemplo", "numero": 1, "passo": "1.3"},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 1 (Francisco)", "tipo": "exercicio", "numero": 1, "passo": None},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 2 (Raquel)", "tipo": "exercicio", "numero": 2, "passo": None},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 3 (Diogo)", "tipo": "exercicio", "numero": 3, "passo": None},
    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 4 (Capital Inicial)", "tipo": "exercicio", "numero": 4, "passo": None},
    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exemplo 2 - Passo 2.1", "tipo": "exemplo", "numero": 2, "passo": "2.1"},
    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exemplo 2 - Passo 2.2", "tipo": "exemplo", "numero": 2, "passo": "2.2"},
    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exercício 5 (Herança)", "tipo": "exercicio", "numero": 5, "passo": None},
    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exercício 6 (Emília e Lino)", "tipo": "exercicio", "numero": 6, "passo": None},
]

ITENS_OFICIAIS_T8 = [
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1", "tipo": "exemplo", "numero": 1, "passo": "1.1"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2", "tipo": "exemplo", "numero": 1, "passo": "1.2"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3", "tipo": "exemplo", "numero": 1, "passo": "1.3"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4", "tipo": "exemplo", "numero": 1, "passo": "1.4"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 2 - Passo 2.1", "tipo": "exemplo", "numero": 2, "passo": "2.1"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 2 - Passo 2.2", "tipo": "exemplo", "numero": 2, "passo": "2.2"},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Depósito Prazo 10 anos)", "tipo": "exercicio", "numero": 1, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Cátia - Depósito 10 anos)", "tipo": "exercicio", "numero": 2, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Mariana - Férias)", "tipo": "exercicio", "numero": 3, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Capital Inicial Composto)", "tipo": "exercicio", "numero": 4, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Marco - Mar vs Montanha)", "tipo": "exercicio", "numero": 5, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 6 (Cláudia - Semestral vs Mensal)", "tipo": "exercicio", "numero": 6, "passo": None},
]

ITENS_OFICIAIS_T4 = [
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (IRS)", "tipo": "exemplo", "numero": 1, "passo": "1.1"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Segurança Social)", "tipo": "exemplo", "numero": 1, "passo": "1.2"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Salário Líquido)", "tipo": "exemplo", "numero": 1, "passo": "1.3"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Subsídio Refeição)", "tipo": "exemplo", "numero": 1, "passo": "1.4"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.5 (Total a Receber)", "tipo": "exemplo", "numero": 1, "passo": "1.5"},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Mateus - Açores)", "tipo": "exercicio", "numero": 1, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Carlos - 2010 vs 2023)", "tipo": "exercicio", "numero": 2, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Mariana - Junta Freguesia)", "tipo": "exercicio", "numero": 3, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Carina - Parcela por Fórmula)", "tipo": "exercicio", "numero": 4, "passo": None},
]

ITENS_OFICIAIS_T5 = [
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (Rendimento Anual)", "tipo": "exemplo", "numero": 1, "passo": "1.1"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Total Horas Anuais)", "tipo": "exemplo", "numero": 1, "passo": "1.2"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Salário Bruto à Hora)", "tipo": "exemplo", "numero": 1, "passo": "1.3"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Horas Extraordinárias)", "tipo": "exemplo", "numero": 1, "passo": "1.4"},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Marco - Mecânico)", "tipo": "exercicio", "numero": 1, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Carlos - Horas Extraordinárias)", "tipo": "exercicio", "numero": 2, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Rosa - 4 Dependentes)", "tipo": "exercicio", "numero": 3, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Maria - 12h Extraordinárias)", "tipo": "exercicio", "numero": 4, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Filipa - 35h Semanais)", "tipo": "exercicio", "numero": 5, "passo": None},
]

ITENS_OFICIAIS_T6 = [
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (Rendimento Anual)", "tipo": "exemplo", "numero": 1, "passo": "1.1"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Rendimento Coletável)", "tipo": "exemplo", "numero": 1, "passo": "1.2"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Coleta Individual)", "tipo": "exemplo", "numero": 1, "passo": "1.3"},
    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Coleta Total Casal)", "tipo": "exemplo", "numero": 1, "passo": "1.4"},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Rita e Afonso)", "tipo": "exercicio", "numero": 1, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Manuel - Solteiro)", "tipo": "exercicio", "numero": 2, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Joana e Miguel)", "tipo": "exercicio", "numero": 3, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Mariana e Afonso - Deduções)", "tipo": "exercicio", "numero": 4, "passo": None},
    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Eugénia e Augusto - Açores)", "tipo": "exercicio", "numero": 5, "passo": None},
]

DICIONARIO_ITENS = {
    "tarefa_04": ITENS_OFICIAIS_T4,
    "tarefa_05": ITENS_OFICIAIS_T5,
    "tarefa_06": ITENS_OFICIAIS_T6,
    "tarefa_07": ITENS_OFICIAIS_T7,
    "tarefa_08": ITENS_OFICIAIS_T8
}

ITENS_OFICIAIS = ITENS_OFICIAIS_T7

NOMES_TAREFAS = {
    "tarefa_04": "Tarefa 4 - Matemática nos Salários",
    "tarefa_05": "Tarefa 5 - Salário Bruto à Hora",
    "tarefa_06": "Tarefa 6 - Imposto sobre o Rendimento (IRS)",
    "tarefa_07": "Tarefa 7 - Juros Simples",
    "tarefa_08": "Tarefa 8 - Juros Compostos"
}

def executar_painel_terminal(ficha_id: str = "tarefa_07"):
    """Exibe um resumo analítico no terminal com métricas completas por aluno e por pergunta."""
    itens_atuais = DICIONARIO_ITENS.get(ficha_id, ITENS_OFICIAIS_T7)
    nome_ficha = NOMES_TAREFAS.get(ficha_id, "Tarefa de Matemática")

    print("=" * 80)
    print(f"📊 PAINEL DOCENTE DE AVALIAÇÃO FORMATIVA - {nome_ficha.upper()}")
    print("=" * 80)
    
    if not os.path.exists(DB_PATH):
        print("Base de dados não encontrada em:", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Assegurar migração de colunas
    try:
        c.execute("ALTER TABLE tentativas_passos ADD COLUMN duracao_segundos REAL DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    try:
        c.execute("ALTER TABLE tentativas_passos ADD COLUMN ficha_id TEXT DEFAULT 'tarefa_07'")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    c.execute("SELECT id, nome, turma FROM alunos ORDER BY turma, nome")
    alunos = c.fetchall()

    c.execute("""
    SELECT COUNT(*), SUM(correto) FROM tentativas_passos
    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL))
    """, (ficha_id, ficha_id))
    res = c.fetchone()
    total_tentativas = res[0] or 0
    total_corretas = res[1] or 0

    c.execute("""
    SELECT COUNT(*) FROM tentativas_passos 
    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND pista_fornecida IS NOT NULL AND pista_fornecida != ''
    """, (ficha_id, ficha_id))
    total_pistas = c.fetchone()[0] or 0

    taxa_sucesso = (total_corretas / total_tentativas * 100) if total_tentativas > 0 else 0

    c.execute("""
    SELECT duracao_segundos FROM tentativas_passos 
    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND correto = 1 AND duracao_segundos > 0
    """, (ficha_id, ficha_id))
    tempos_validos_turma = [r[0] for r in c.fetchall()]
    tempo_medio_turma_num = (sum(tempos_validos_turma) / len(tempos_validos_turma)) if tempos_validos_turma else None

    c.execute("""
    SELECT COUNT(DISTINCT aluno_id || '_' || numero) FROM tentativas_passos 
    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exercicio' AND correto = 1
    """, (ficha_id, ficha_id))
    total_exercicios_validados_turma = c.fetchone()[0] or 0

    print(f"Ficha Selecionada:                     {nome_ficha} ({ficha_id})")
    print(f"Total de Alunos Registados:            {len(alunos)}")
    print(f"Exercícios Validados (Turma):          {total_exercicios_validados_turma} de {len(alunos) * 6}")
    print(f"Pistas Pedagógicas Acionadas:          {total_pistas}")
    print(f"Tempo Médio até Validação (Turma):     {formatar_tempo(tempo_medio_turma_num)}")
    print("-" * 80)

    # 1. PANORAMA DA TURMA POR PERGUNTA
    print("\n📈 1. PANORAMA GLOBAL DA TURMA POR PERGUNTA:")
    print(f"{'Pergunta / Item':<40} | {'Validados':<11} | {'Pistas (Turma)':<15} | {'Tempo Médio':<12}")
    print("-" * 85)

    for it in itens_atuais:
        if it["passo"]:
            c.execute("""
            SELECT COUNT(*), SUM(correto), 
                   COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END),
                   COUNT(DISTINCT CASE WHEN correto = 1 THEN aluno_id END)
            FROM tentativas_passos 
            WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ?
            """, (ficha_id, ficha_id, it["tipo"], it["numero"], it["passo"]))
            r = c.fetchone()
            c.execute("""
            SELECT duracao_segundos FROM tentativas_passos 
            WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ? AND correto = 1 AND duracao_segundos > 0
            """, (ficha_id, ficha_id, it["tipo"], it["numero"], it["passo"]))
            tempos = [t[0] for t in c.fetchall()]
        else:
            c.execute("""
            SELECT COUNT(*), SUM(correto), 
                   COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END),
                   COUNT(DISTINCT CASE WHEN correto = 1 THEN aluno_id END)
            FROM tentativas_passos 
            WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ?
            """, (ficha_id, ficha_id, it["tipo"], it["numero"]))
            r = c.fetchone()
            c.execute("""
            SELECT duracao_segundos FROM tentativas_passos 
            WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND correto = 1 AND duracao_segundos > 0
            """, (ficha_id, ficha_id, it["tipo"], it["numero"]))
            tempos = [t[0] for t in c.fetchall()]

        pists = r[2] or 0
        vals = r[3] or 0
        t_med = (sum(tempos) / len(tempos)) if tempos else None
        pistas_str = f"{pists} (À 1.ª)" if (vals > 0 and pists == 0) else str(pists)
        print(f"{it['item']:<40} | {f'{vals}/{len(alunos)}':<11} | {pistas_str:<15} | {formatar_tempo(t_med):<12}")

    # 2. MÉTRICAS POR ALUNO E POR PERGUNTA
    print("\n🎯 2. DESEMPENHO DETALHADO POR ALUNO E POR PERGUNTA:")
    for al in alunos:
        aid, anome, aturma = al[0], al[1], al[2]
        c.execute("""
        SELECT duracao_segundos FROM tentativas_passos 
        WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND correto = 1 AND duracao_segundos > 0
        """, (aid, ficha_id, ficha_id))
        t_al_list = [r[0] for r in c.fetchall()]
        t_al_med = (sum(t_al_list) / len(t_al_list)) if t_al_list else None

        c.execute("""
        SELECT COUNT(DISTINCT numero) FROM tentativas_passos 
        WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exercicio' AND correto = 1
        """, (aid, ficha_id, ficha_id))
        ex_feitos = c.fetchone()[0] or 0

        print(f"\n👤 Aluno: {anome} ({aturma}) | Exercícios Validados: {ex_feitos}/6 | Tempo Médio Resolução: {formatar_tempo(t_al_med)}")
        print(f"   {'Pergunta / Item':<38} | {'Estado':<14} | {'Pistas Pedidas':<15} | {'Tempo até Validação':<20}")
        print("   " + "-" * 93)

        for it in itens_atuais:
            if it["passo"]:
                c.execute("""
                SELECT COUNT(*), SUM(correto), 
                       COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END)
                FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ?
                """, (aid, ficha_id, ficha_id, it["tipo"], it["numero"], it["passo"]))
                r = c.fetchone()
                c.execute("""
                SELECT duracao_segundos FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ? AND correto = 1 AND duracao_segundos > 0
                ORDER BY id ASC LIMIT 1
                """, (aid, ficha_id, ficha_id, it["tipo"], it["numero"], it["passo"]))
                t_row = c.fetchone()
            else:
                c.execute("""
                SELECT COUNT(*), SUM(correto), 
                       COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END)
                FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ?
                """, (aid, ficha_id, ficha_id, it["tipo"], it["numero"]))
                r = c.fetchone()
                c.execute("""
                SELECT duracao_segundos FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND correto = 1 AND duracao_segundos > 0
                ORDER BY id ASC LIMIT 1
                """, (aid, ficha_id, ficha_id, it["tipo"], it["numero"]))
                t_row = c.fetchone()

            al_tents = r[0] or 0
            al_corrs = r[1] or 0
            al_pists = r[2] or 0
            al_conc = al_corrs > 0
            al_tempo = t_row[0] if (al_conc and t_row) else None
            estado = "✓ Validado" if al_conc else ("⏳ Por Resolver" if al_tents > 0 else "— Não Aberto")
            pistas_str = "0 (À 1.ª)" if (al_conc and al_pists == 0) else str(al_pists)

            print(f"   {it['item']:<38} | {estado:<14} | {pistas_str:<15} | {formatar_tempo(al_tempo):<20}")

    # 3. ÚLTIMAS TENTATIVAS FORMATIVAS
    print("\n📜 3. ÚLTIMAS TENTATIVAS FORMATIVAS DA FICHA:")
    c.execute("""
    SELECT tp.data_hora, a.nome, tp.tipo, tp.numero, tp.passo, tp.correto, tp.duracao_segundos, tp.feedback_dado
    FROM tentativas_passos tp
    JOIN alunos a ON tp.aluno_id = a.id
    WHERE (tp.ficha_id = ? OR (? = 'tarefa_07' AND tp.ficha_id IS NULL))
    ORDER BY tp.id DESC LIMIT 8
    """, (ficha_id, ficha_id))
    linhas = c.fetchall()
    if not linhas:
        print("  (Ainda não existem tentativas registadas para esta ficha)")
    for r in linhas:
        status = "✓ CORRETO" if r[5] else "❌ REVER"
        tempo_str = formatar_tempo(r[6])
        print(f"[{r[0][:19]}] {r[1]} | {r[2].upper()} {r[3]} ({r[4]}) | Tempo: {tempo_str} | {status}")
        fb_limpo = r[7].replace('\n', ' ')
        print(f"   Feedback: {fb_limpo[:90]}...")

    conn.close()
    print("=" * 80)
    print("💡 DICA: Para aceder à interface Web dinâmica e interativa em tempo real:")
    print("   1. Executa: python3 servidor_simulacao.py")
    print("   2. Abre: http://localhost:8000 e clica no separador 'Painel do Professor'!")
    print("=" * 80)

try:
    import pandas as pd
    import streamlit as st
    STREAMLIT_DISPONIVEL = True
except ImportError:
    STREAMLIT_DISPONIVEL = False

if STREAMLIT_DISPONIVEL and "streamlit" in sys.modules and getattr(st, "_is_running_with_streamlit", False):
    st.set_page_config(page_title="Tutor de Matemática - Painel Docente", layout="wide")

    st.markdown("""
    <style>
    div.block-container { padding-top: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Painel de Monitorização Formativa - Tutor de Matemática")
    st.write("Acompanhamento contínuo de resoluções passo a passo, tempos de resposta até validação e pistas pedagógicas.")

    def obter_dados():
        if not os.path.exists(DB_PATH):
            return pd.DataFrame(), pd.DataFrame()
        conn = sqlite3.connect(DB_PATH)
        try:
            df_alunos = pd.read_sql_query("SELECT * FROM alunos", conn)
            df_tentativas = pd.read_sql_query("SELECT * FROM tentativas_passos", conn)
        except Exception:
            df_alunos, df_tentativas = pd.DataFrame(), pd.DataFrame()
        finally:
            conn.close()
        return df_alunos, df_tentativas

    df_alunos, df_tentativas = obter_dados()

    tab_geral, tab_individual, tab_comparativo, tab_fichas = st.tabs([
        "📈 Panorama Global da Turma",
        "👤 Desempenho por Aluno",
        "👥 Comparativo de Alunos",
        "📑 Fichas e Histórico"
    ])

    with tab_geral:
        st.subheader("Métricas Gerais da Turma")
        if df_tentativas.empty:
            st.info("Ainda não existem registos de resoluções na base de dados. Os dados surgirão à medida que os alunos interagirem com o tutor.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            ex_val_total = df_tentativas[(df_tentativas['tipo'] == 'exercicio') & (df_tentativas['correto'] == 1)]['numero'].nunique()
            total_alunos_ativos = df_tentativas['aluno_id'].nunique()
            total_pistas = df_tentativas['pista_fornecida'].notnull().sum()
            
            tempos_corretos = df_tentativas[df_tentativas['correto'] == 1]['duracao_segundos']
            tempo_medio_turma = tempos_corretos.mean() if not tempos_corretos.empty else 0

            col1.metric("Exercícios Validados", f"{ex_val_total} de 6")
            col2.metric("Alunos Ativos", total_alunos_ativos)
            col3.metric("Pistas Pedidas (Turma)", total_pistas)
            col4.metric("Tempo Médio até Validação", formatar_tempo(tempo_medio_turma))
            
            st.write("---")
            st.subheader("Erros Frequentes e Pistas Fornecidas")
            erros_df = df_tentativas[df_tentativas['correto'] == 0][['ficha_id', 'tipo', 'numero', 'passo', 'feedback_dado', 'pista_fornecida', 'data_hora']]
            st.dataframe(erros_df, use_container_width=True)

            if not erros_df.empty:
                st.markdown("#### 🔬 Análise Detalhada dos Erros com Renderização LaTeX:")
                for _, row in erros_df.head(10).iterrows():
                    fb = str(row['feedback_dado']).replace(r'\euro', '€')
                    pista = str(row['pista_fornecida'] or '').replace(r'\euro', '€')
                    with st.expander(f"📍 {str(row['tipo']).upper()} {row['numero']} (Passo {row['passo']}) - {str(row['data_hora'])[:19]}"):
                        st.markdown(f"**Feedback:** {fb}")
                        if pista and pista != 'None':
                            st.markdown(f"💡 **Pista Pedagógica:** {pista}")

    with tab_individual:
        st.subheader("Acompanhamento Individual do Aluno")
        if df_alunos.empty or df_tentativas.empty:
            st.info("Sem registo de alunos para visualização individual.")
        else:
            lista_alunos = dict(zip(df_alunos['id'], df_alunos['nome'] + " (" + df_alunos['turma'] + ")"))
            aluno_sel = st.selectbox("Selecione o Aluno:", options=list(lista_alunos.keys()), format_func=lambda x: lista_alunos[x])
            
            df_aluno_tentativas = df_tentativas[df_tentativas['aluno_id'] == aluno_sel]
            
            # Métricas do Aluno
            c1, c2, c3 = st.columns(3)
            ex_val_aluno = df_aluno_tentativas[(df_aluno_tentativas['tipo'] == 'exercicio') & (df_aluno_tentativas['correto'] == 1)]['numero'].nunique()
            n_pistas = df_aluno_tentativas['pista_fornecida'].notnull().sum()
            tempos_al = df_aluno_tentativas[df_aluno_tentativas['correto'] == 1]['duracao_segundos']
            t_med_al = tempos_al.mean() if not tempos_al.empty else 0

            c1.metric("Exercícios Validados", f"{ex_val_aluno} de 6")
            c2.metric("Pistas Pedidas", n_pistas)
            c3.metric("Tempo Médio até Validação", formatar_tempo(t_med_al))

            st.write(f"Histórico de Resoluções de: **{lista_alunos[aluno_sel]}**")
            st.dataframe(df_aluno_tentativas[['ficha_id', 'tipo', 'numero', 'passo', 'correto', 'duracao_segundos', 'resposta_aluno', 'feedback_dado', 'data_hora']], use_container_width=True)

    with tab_comparativo:
        st.subheader("Desempenho Comparativo entre Alunos")
        if df_alunos.empty or df_tentativas.empty:
            st.info("Sem dados suficientes.")
        else:
            dados_comp = []
            for _, al in df_alunos.iterrows():
                aid = al['id']
                df_a = df_tentativas[df_tentativas['aluno_id'] == aid]
                pistas = df_a['pista_fornecida'].notnull().sum()
                ex_val = df_a[(df_a['tipo'] == 'exercicio') & (df_a['correto'] == 1)]['numero'].nunique()
                t_corr = df_a[df_a['correto'] == 1]['duracao_segundos']
                t_med = formatar_tempo(t_corr.mean()) if not t_corr.empty else "—"
                dados_comp.append({
                    "Aluno": al['nome'],
                    "Turma": al['turma'],
                    "Progresso (Exercícios)": f"{ex_val} de 6",
                    "Pistas Pedidas": pistas,
                    "Tempo Médio / Pergunta": t_med
                })
            st.dataframe(pd.DataFrame(dados_comp), use_container_width=True)

    with tab_fichas:
        st.subheader("Fichas de Trabalho e Recursos Disponíveis")
        fichas_dir = os.path.join(BASE_DIR, "fichas")
        if os.path.exists(fichas_dir):
            fichas = [f for f in os.listdir(fichas_dir) if f.endswith(".md")]
            for f in fichas:
                st.markdown(f"- **{f}**")

elif __name__ == "__main__":
    ficha = "tarefa_07"
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if "4" in arg or "salario" in arg:
            ficha = "tarefa_04"
        elif "5" in arg or "hora" in arg:
            ficha = "tarefa_05"
        elif "6" in arg or "irs" in arg:
            ficha = "tarefa_06"
        elif "8" in arg or "composto" in arg:
            ficha = "tarefa_08"
        elif "7" in arg or "simples" in arg:
            ficha = "tarefa_07"
    executar_painel_terminal(ficha)
