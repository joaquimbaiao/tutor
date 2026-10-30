#!/usr/bin/env python3
"""
Script de Gestão e Importação de Alunos para o Tutor de Matemática.
Permite importar pautas para os cursos 10.º TPE/TOE e 10.º TCR com credenciais padronizadas.
"""

import sys
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import tutor_engine

DB_PATH = os.path.join(BASE_DIR, "dados", "tutor.db")

def listar_alunos():
    """Apresenta a lista atual de alunos organizada por curso."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, turma, username FROM alunos ORDER BY turma, nome")
    linhas = c.fetchall()
    conn.close()

    if not linhas:
        print("\n⚠️ Nenhum aluno registado na base de dados.")
        return

    print(f"\n{'='*75}")
    print("📋 LISTA DE ALUNOS REGISTADOS NO TUTOR INTELIGENTE")
    print(f"{'='*75}")
    print(f"{'ID':<4} | {'Turma / Curso':<16} | {'Nome do Aluno':<30} | {'Username':<15}")
    print(f"{'-'*75}")
    turma_anterior = None
    for r in linhas:
        if turma_anterior != r[2]:
            turma_anterior = r[2]
            print(f"--- {turma_anterior} ---")
        print(f"{r[0]:<4} | {r[2]:<16} | {r[1]:<30} | {r[3]:<15}")
    print(f"{'='*75}\nTotal de Alunos: {len(linhas)}\n")

def importar_lista(turma: str, nomes: list, senha_padrao: str = "1234"):
    """Importa uma lista de nomes para uma determinada turma."""
    if not nomes:
        print("⚠️ Nenhum nome fornecido para importação.")
        return

    inseridos = tutor_engine.importar_alunos_lote(nomes, turma=turma, senha_padrao=senha_padrao, db_path=DB_PATH)
    print(f"\n✅ {len(inseridos)} alunos importados com sucesso para a turma '{turma}'!")
    print(f"🔒 Palavra-passe inicial atribuída: {senha_padrao}")
    for a in inseridos:
        print(f"   👤 {a['nome']:<28} -> Username: {a['username']}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        listar_alunos()
        print("Para importar alunos via ficheiro:")
        print("   python3 tutor/importar_alunos.py '10.º TPE/TOE' ficheiro_alunos.txt")
        print("   python3 tutor/importar_alunos.py '10.º TCR' ficheiro_alunos.txt")
        print("\nPara listar alunos:")
        print("   python3 tutor/importar_alunos.py --listar")
    elif sys.argv[1] in ["--listar", "-l", "listar"]:
        listar_alunos()
    elif len(sys.argv) >= 3:
        turma = sys.argv[1]
        caminho_ficheiro = sys.argv[2]
        senha_padrao = sys.argv[3] if len(sys.argv) > 3 else "1234"
        if os.path.exists(caminho_ficheiro):
            with open(caminho_ficheiro, "r", encoding="utf-8") as f:
                nomes = [linha.strip() for linha in f if linha.strip()]
            importar_lista(turma, nomes, senha_padrao)
        else:
            print(f"❌ Ficheiro não encontrado: {caminho_ficheiro}")
    else:
        print("Uso: python3 tutor/importar_alunos.py <turma> <caminho_ficheiro> [senha_padrao]")
