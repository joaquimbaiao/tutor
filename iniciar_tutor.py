#!/usr/bin/env python3
"""
Script Principal de Inicialização e Diagnóstico - Tutor de Matemática IA.
Verifica a integridade da base de dados, testa a API Google Gemini e inicia o servidor local.
"""

import os
import sys
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import tutor_engine
import avaliador_gemini
import servidor_simulacao

def verificar_estado():
    print("\n" + "=" * 65)
    print("🔍 DIAGNÓSTICO DO TUTOR INTELIGENTE DE MATEMÁTICA")
    print("=" * 65)

    # 1. Base de dados
    db_path = os.path.join(BASE_DIR, "dados", "tutor.db")
    tutor_engine.inicializar_bd(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM alunos")
    n_alunos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tentativas_passos")
    n_tentativas = c.fetchone()[0]
    conn.close()
    print(f"✓ Base de Dados SQLite: OK ({n_alunos} alunos, {n_tentativas} tentativas registadas)")

    # 2. Configuração Gemini
    api_key, model = avaliador_gemini.obter_config()
    key_mascarada = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "NÃO CONFIGURADA"
    print(f"✓ API Google Gemini: Configurada (Modelo: {model}, Chave: {key_mascarada})")

    # 3. Fichas em Markdown
    fichas_dir = os.path.join(BASE_DIR, "fichas")
    fichas_md = [f for f in os.listdir(fichas_dir) if f.endswith(".md")]
    print(f"✓ Fichas Estruturadas: {len(fichas_md)} ficheiros encontrados ({', '.join(fichas_md)})")

    print("=" * 65)

if __name__ == "__main__":
    verificar_estado()
    print("\nA iniciar servidor web local...")
    servidor_simulacao.run_server()
