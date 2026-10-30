#!/usr/bin/env python3
"""
Servidor Web de Simulação Local - Tutor de Matemática (Avaliação Formativa).
Versão Didática por Blocos e Pré-Requisitos:
- Bloco 1: Exemplo 1 (Passos 1.1 a 1.3) desbloqueia Exercícios 1, 2, 3 e 4;
- Bloco 2: Exemplo 2 (Passos 2.1 e 2.2) desbloqueia Exercícios 5 e 6;
- Impedimento pedagógico estrito: Exercícios 5 e 6 bloqueados (🔒) até conclusão do Exemplo 2;
- Barra superior interativa: [📘 Ex. 1] [Ex. 1..4] [📘 Ex. 2] [🔒 Ex. 5..6];
- Submissão obrigatória de fotografia nos exercícios de aplicação;
- Alinhamento à esquerda em interfaces web e suporte LaTeX total;
- Painel Docente com Quadro Consolidado em tempo real e botão de reinício de testes.
"""

import json
import os
import re
import sys
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def obter_docente_senha():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha.startswith("DOCENTE_SENHA="):
                        val = linha.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
        except Exception:
            pass
    cfg_path = os.path.join(BASE_DIR, "dados", "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                dados = json.load(f)
                val = dados.get("docente_senha", "").strip()
                if val:
                    return val
        except Exception:
            pass
    return "profmat2026"

PORT = 8000
DB_PATH = os.path.join(BASE_DIR, "dados", "tutor.db")

# Assegurar base de dados inicializada
import tutor_engine
tutor_engine.inicializar_bd(DB_PATH)

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutor de Matemática - Avaliação Formativa</title>
    <!-- MathJax para suporte a fórmulas LaTeX -->
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        macros: {
          euro: "{\\\\text{€}}",
          textyen: "{\\\\text{€}}"
        }
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea']
      },
      svg: { fontCache: 'global' }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {
            --primary: #1a56db;
            --primary-hover: #1e429f;
            --success: #057a55;
            --success-light: #def7ec;
            --warning: #d97706;
            --error: #e02424;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --border: #cbd5e1;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            text-align: left; /* Regra estrita: alinhamento à esquerda em interfaces web */
        }
        .container {
            max-width: 980px;
            margin: 0 auto;
            padding: 24px;
            text-align: left;
        }
        header {
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-align: left;
        }
        .header-title h1 {
            margin: 0;
            font-size: 20px;
            color: var(--primary);
            text-align: left;
        }
        .header-title p {
            margin: 2px 0 0 0;
            font-size: 13px;
            color: #64748b;
            text-align: left;
        }
        .aluno-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        .aluno-selector select {
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 14px;
            background: white;
        }
        .tabs {
            display: flex;
            gap: 12px;
            margin-top: 16px;
        }
        .tab-btn {
            background: #e2e8f0;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }
        .tab-btn.active {
            background: var(--primary);
            color: #ffffff;
        }
        .card {
            background: var(--card);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid var(--border);
            margin-bottom: 20px;
            text-align: left;
        }
        /* Barra de Navegação Superior Clicável */
        .nav-bar-container {
            margin-bottom: 18px;
        }
        .nav-bar-label {
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .nav-pill {
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid var(--border);
            background: #f1f5f9;
            color: #475569;
            transition: all 0.15s ease-in-out;
            user-select: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .nav-pill:hover:not(.locked) {
            border-color: #94a3b8;
            background: #e2e8f0;
        }
        .nav-pill.locked {
            cursor: not-allowed;
            background: #f8fafc;
            color: #94a3b8;
            border: 1px dashed #cbd5e1;
        }
        .nav-pill.active {
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary-hover);
            box-shadow: 0 2px 4px rgba(26, 86, 219, 0.25);
        }
        .nav-pill.completed {
            background: var(--success-light);
            color: #03543f;
            border-color: #31c48d;
        }
        .nav-pill.completed.active {
            background: var(--success);
            color: #ffffff;
            border-color: #046c4e;
            box-shadow: 0 2px 4px rgba(5, 122, 85, 0.3);
        }
        .celebration-box {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border: 2px solid #34d399;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: left;
        }
        .feedback-box {
            border-radius: 8px;
            padding: 16px;
            margin-top: 16px;
            text-align: left;
            font-size: 14px;
        }
        .feedback-error {
            background-color: #fef2f2;
            border-left: 4px solid var(--error);
            color: #991b1b;
        }
        .feedback-success {
            background-color: #f0fdf4;
            border-left: 4px solid var(--success);
            color: #166534;
        }
        .feedback-locked {
            background-color: #fffbeb;
            border-left: 4px solid var(--warning);
            color: #92400e;
        }
        .pista-box {
            background-color: #fffbeb;
            border-left: 4px solid var(--warning);
            padding: 12px 16px;
            border-radius: 6px;
            margin-top: 10px;
            color: #92400e;
            text-align: left;
        }
        .instrucao-calculo {
            background: #f1f5f9;
            border-left: 4px solid #64748b;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 13px;
            color: #334155;
            margin: 14px 0;
            text-align: left;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 15px;
            box-sizing: border-box;
            margin-top: 6px;
            text-align: left;
        }
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.15);
        }
        .input-error {
            border-color: var(--error) !important;
            background-color: #fff5f5;
        }
        .btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 22px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            margin-top: 12px;
            transition: background 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn:hover { background-color: var(--primary-hover); }
        .btn-success { background-color: var(--success); }
        .btn-success:hover { background-color: #046c4e; }
        .btn-warning { background-color: var(--warning); }
        .btn-warning:hover { background-color: #b45309; }
        .btn-secondary { background-color: #64748b; }
        .btn-secondary:hover { background-color: #475569; }
        .btn-danger { background-color: #dc2626; }
        .btn-danger:hover { background-color: #b91c1c; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 14px;
            text-align: left;
        }
        th, td {
            border: 1px solid var(--border);
            padding: 10px 12px;
            text-align: left;
        }
        th { background: #f1f5f9; font-weight: 600; }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: white;
            border: 1px solid var(--border);
            padding: 16px;
            border-radius: 8px;
            text-align: left;
        }
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--primary);
        }
        .stat-label {
            font-size: 13px;
            color: #64748b;
        }
        .badge-status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 12px;
        }
        .badge-ok { background: #def7ec; color: #03543f; }
        .badge-pista { background: #fef3c7; color: #92400e; }
        .badge-pendente { background: #f1f5f9; color: #64748b; }

        /* Modal de Autenticação */
        #modal-auth-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(4px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        .auth-card {
            background: white;
            border-radius: 16px;
            max-width: 440px;
            width: 100%;
            padding: 28px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border: 1px solid #cbd5e1;
            text-align: left;
        }
        .auth-tabs {
            display: flex;
            background: #f1f5f9;
            padding: 4px;
            border-radius: 10px;
            margin-bottom: 20px;
            gap: 4px;
        }
        .auth-tab-btn {
            flex: 1;
            padding: 8px 12px;
            border: none;
            background: transparent;
            font-size: 13px;
            font-weight: 600;
            color: #64748b;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .auth-tab-btn.active {
            background: white;
            color: var(--primary);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 14px;
            text-align: left;
        }
        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: #334155;
            margin-bottom: 5px;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            font-size: 14px;
            box-sizing: border-box;
            background: #f8fafc;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: var(--primary);
            background: #ffffff;
        }
        .btn-block {
            width: 100%;
            padding: 11px;
            font-size: 15px;
            font-weight: 600;
            margin-top: 10px;
        }

    </style>
</head>
<body>

<!-- MODAL DE AUTENTICAÇÃO OBRIGATÓRIA -->
<div id="modal-auth-overlay" style="display: none;">
    <div class="auth-card" style="position: relative;">
        <button onclick="fecharModalLogin()" title="Fechar" style="position: absolute; top: 12px; right: 14px; background: none; border: none; font-size: 20px; color: #64748b; cursor: pointer; padding: 4px; line-height: 1;">✕</button>
        <div style="text-align: center; margin-bottom: 18px;">
            <div style="font-size: 32px; margin-bottom: 4px;">📐</div>
            <h2 style="margin: 0; color: var(--primary); font-size: 20px;">Tutor de Matemática IA</h2>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #64748b;">Avaliação Formativa Contínua | Módulo P1</p>
        </div>

        <div class="auth-tabs">
            <button class="auth-tab-btn active" id="btn-tab-auth-aluno" onclick="mudarAbaAuth('aluno')">👨‍🎓 Sou Aluno</button>
            <button class="auth-tab-btn" id="btn-tab-auth-docente" onclick="mudarAbaAuth('docente')">👨‍🏫 Área do Professor</button>
        </div>

        <!-- FORMULÁRIO DO ALUNO -->
        <div id="form-auth-aluno">
            <div class="form-group">
                <label for="input-auth-usuario">Nome de Utilizador ou Nome Completo:</label>
                <select id="sel-rapido-aluno" onchange="selecionarAlunoRapido(this.value)" style="margin-bottom: 8px;">
                    <option value="">-- Escolhe o teu nome da turma --</option>
                </select>
                <input type="text" id="input-auth-usuario" placeholder="Ou digita o teu utilizador (ex: duarte)...">
            </div>
            <div class="form-group">
                <label for="input-auth-senha">Palavra-passe Pessoal:</label>
                <input type="password" id="input-auth-senha" placeholder="Digita a tua palavra-passe (padrão: 1234)" onkeydown="if(event.key==='Enter') submeterLoginAluno()">
            </div>
            <div id="msg-erro-login-aluno" style="display: none; color: #dc2626; font-size: 13px; margin-bottom: 10px; background: #fef2f2; padding: 8px; border-radius: 6px; border: 1px solid #fecaca;"></div>
            <button class="btn btn-primary btn-block" onclick="submeterLoginAluno()">
                🚀 Entrar e Recuperar o Meu Trabalho
            </button>
            <p style="font-size: 11px; color: #64748b; margin-top: 12px; text-align: center;">
                🔒 O teu progresso e exercícios validados a verde são guardados de forma segura e recuperados em qualquer telemóvel ou computador.
            </p>
        </div>

        <!-- FORMULÁRIO DO PROFESSOR -->
        <div id="form-auth-docente" style="display: none;">
            <div class="form-group">
                <label for="input-auth-senha-docente">Palavra-passe de Professor:</label>
                <input type="password" id="input-auth-senha-docente" placeholder="Digita a palavra-passe docente..." onkeydown="if(event.key==='Enter') submeterLoginDocente()">
            </div>
            <div id="msg-erro-login-docente" style="display: none; color: #dc2626; font-size: 13px; margin-bottom: 10px; background: #fef2f2; padding: 8px; border-radius: 6px; border: 1px solid #fecaca;"></div>
            <button class="btn btn-primary btn-block" onclick="submeterLoginDocente()">
                🔐 Aceder ao Painel da Turma
            </button>
            <p style="font-size: 11px; color: #64748b; margin-top: 12px; text-align: center;">
                Painel reservado ao docente: acompanhamento em tempo real, métricas individuais, redefinição de senhas e relatórios.
            </p>
        </div>
    </div>
</div>

<!-- MODAL DE IMPORTAÇÃO DE ALUNOS PELO PROFESSOR -->
<div id="modal-importar-alunos-overlay" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(4px); z-index: 10000; align-items: center; justify-content: center;">
    <div class="auth-card" style="max-width: 480px; text-align: left;">
        <h3 style="margin-top: 0; color: #166534;">📥 Importar Lista de Alunos</h3>
        <p style="font-size: 13px; color: #64748b; margin-bottom: 14px;">
            Cola os nomes dos alunos (um por linha). O sistema gerará automaticamente os nomes de utilizador (*usernames*) únicos e atribuirá a palavra-passe inicial.
        </p>
        <div class="form-group">
            <label for="import-turma">Curso / Turma de Destino:</label>
            <select id="import-turma" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-weight: 600;">
                <option value="10.º TPE/TOE">10.º TPE/TOE</option>
                <option value="10.º TCR">10.º TCR</option>
            </select>
        </div>
        <div class="form-group">
            <label for="import-senha-padrao">Palavra-passe Inicial:</label>
            <input type="text" id="import-senha-padrao" value="1234" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1;">
        </div>
        <div class="form-group">
            <label for="import-nomes">Nomes dos Alunos (um por linha):</label>
            <textarea id="import-nomes" rows="6" placeholder="Gonçalo Silva&#10;Inês Martins&#10;Rodrigo Santos..." style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-family: inherit; font-size: 13px;"></textarea>
        </div>
        <div id="msg-import-status" style="display: none; font-size: 13px; margin-bottom: 10px; padding: 8px; border-radius: 6px;"></div>
        <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <button class="btn btn-secondary" style="margin: 0;" onclick="fecharModalImportarAlunos()">Cancelar</button>
            <button class="btn btn-primary" style="margin: 0; background: #166534;" onclick="submeterImportacaoAlunos()">✅ Importar para a Turma</button>
        </div>
    </div>
</div>

<header>
    <div class="header-title">
        <h1>Tutor de Matemática Inteligente</h1>
        <p>Avaliação Formativa Contínua | Módulo P1: Modelos Matemáticos para a Cidadania</p>
    </div>
    <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
        <div class="aluno-selector">
            <label for="sel-tarefa"><strong>Tarefa:</strong></label>
            <select id="sel-tarefa" onchange="trocarTarefa(this.value)" style="font-weight: 600; color: var(--primary);">
                <option value="tarefa_04">Tarefa 4: Matemática nos Salários</option>
                <option value="tarefa_05">Tarefa 5: Salário Bruto à Hora</option>
                <option value="tarefa_06">Tarefa 6: IRS (Liquidação Anual)</option>
                <option value="tarefa_07" selected>Tarefa 7: Juros Simples</option>
                <option value="tarefa_08">Tarefa 8: Juros Compostos</option>
            </select>
        </div>
        <div id="badge-sessao-usuario" style="display: flex; align-items: center; gap: 8px;">
            <!-- Preenchido dinamicamente com o nome do aluno ou professor e botão Sair -->
        </div>
    </div>
</header>

<div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
        <div class="tabs" style="margin: 0;">
            <button class="tab-btn active" id="tab-aluno-btn" onclick="mostrarAba('aluno')">✍️ Resolução do Aluno</button>
            <button class="tab-btn" id="tab-docente-btn" onclick="mostrarAba('docente')">📊 Painel do Professor (Tempo Real)</button>
        </div>
    </div>

    <!-- ÁREA DO ALUNO -->
    <div id="aba-aluno" style="margin-top: 20px;">

        <!-- Mensagem de Conclusão Global se toda a ficha estiver a verde -->
        <div id="caixa-celebracao-global" style="display: none;" class="celebration-box">
            <h3 style="margin: 0 0 6px 0; color: #065f46; font-size: 18px;">🏆 Parabéns! Todos os exercícios estão validados a verde!</h3>
            <p style="margin: 0; font-size: 14px; color: #047857;">
                Completaste os dois exemplos e todos os 6 exercícios de aplicação da Tarefa 7 com sucesso.
            </p>
        </div>

        <div class="card">
            <!-- Barra de Navegação Superior Interativa -->
            <div class="nav-bar-container">
                <div class="nav-bar-label">
                    <span>Navegação Rápida (Bloco 1: Ex. 1 a 4 | Bloco 2: Ex. 5 e 6)</span>
                    <span id="badge-contador-concluidos" style="font-weight: 600; color: #057a55;">0 de 6 Exercícios Validados</span>
                </div>
                <div class="nav-pills" id="nav-pills-bar">
                    <!-- Gerado dinamicamente -->
                </div>
            </div>

            <div id="conteudo-enunciado">
                <!-- Enunciado e questões dinâmicas -->
            </div>

            <div id="area-resposta" style="margin-top: 14px;">
                <!-- Formulário de inserção de resposta -->
            </div>

            <div id="feedback-area"></div>
        </div>
    </div>

    <!-- ÁREA DOCENTE -->
    <div id="aba-docente" style="display: none; margin-top: 20px;">
        <div class="card" style="background: #f0fdf4; border: 1px solid #86efac; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <h4 style="margin: 0; color: #166534; font-size: 15px;">🤖 Google Gemini Vision & Painel Analítico Docente</h4>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #15803d;">
                        Modelo: <strong>gemini-3.5-flash-lite</strong> | Avaliação formativa, tempos de resposta até validação, tentativas e pistas pedagógicas por pergunta.
                    </p>
                </div>
                <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <label for="sel-turma-docente" style="font-size: 13px; font-weight: 600; color: #166534;">Turma / Curso:</label>
                        <select id="sel-turma-docente" onchange="selecionarTurmaDocente(this.value)" style="padding: 6px 10px; border-radius: 6px; border: 1px solid #86efac; font-size: 13px; font-weight: 600; background: white; color: #166534;">
                            <option value="todas">Todas as Turmas</option>
                            <option value="10.º TPE/TOE">10.º TPE/TOE</option>
                            <option value="10.º TCR">10.º TCR</option>
                        </select>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <label for="sel-tarefa-docente" style="font-size: 13px; font-weight: 600; color: #166534;">Ficha / Tarefa:</label>
                        <select id="sel-tarefa-docente" onchange="selecionarTarefaDocente(this.value)" style="padding: 6px 10px; border-radius: 6px; border: 1px solid #86efac; font-size: 13px; font-weight: 600; background: white; color: #166534;">
                            <option value="tarefa_04">Tarefa 4: Matemática nos Salários</option>
                            <option value="tarefa_05">Tarefa 5: Salário Bruto à Hora</option>
                            <option value="tarefa_06">Tarefa 6: IRS (Liquidação Anual)</option>
                            <option value="tarefa_07" selected>Tarefa 7: Juros Simples</option>
                            <option value="tarefa_08">Tarefa 8: Juros Compostos</option>
                        </select>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <label for="sel-aluno-docente" style="font-size: 13px; font-weight: 600; color: #166534;">Aluno em Análise:</label>
                        <select id="sel-aluno-docente" onchange="selecionarAlunoDocente(this.value)" style="padding: 6px 12px; border-radius: 6px; border: 1px solid #86efac; font-size: 13px; font-weight: 600; background: white; color: #166534;">
                            <option value="">A carregar alunos...</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" style="margin: 0; padding: 6px 12px; font-size: 12px; background: #166534;" onclick="abrirModalImportarAlunos()">
                        ➕ Importar Alunos
                    </button>
                </div>
            </div>
        </div>

        <div class="stat-grid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));">
            <div class="stat-card" style="border-left: 4px solid var(--success);">
                <div class="stat-value" id="stat-exercicios-aluno" style="color: var(--success);">0 / 6</div>
                <div class="stat-label">Exercícios Validados (<span id="stat-label-nome-progresso">Aluno</span>)</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #f59e0b;">
                <div class="stat-value" id="stat-pistas-aluno" style="color: #d97706;">0</div>
                <div class="stat-label">Total Pistas Pedidas (<span id="stat-label-nome-pistas">Aluno</span>)</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid var(--primary);">
                <div class="stat-value" id="stat-tempo-aluno" style="color: var(--primary);">—</div>
                <div class="stat-label">Tempo Médio / Pergunta (<span id="stat-label-nome-aluno">Aluno</span>)</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #64748b;">
                <div class="stat-value" id="stat-tempo-turma" style="color: #475569;">—</div>
                <div class="stat-label">Tempo Médio / Pergunta (Turma)</div>
            </div>
        </div>

        <!-- 1. MATRIZ ANALÍTICA DE DESEMPENHO POR PERGUNTA DO ALUNO -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h3 style="margin: 0;">🎯 Desempenho por Pergunta: <span id="nome-aluno-analise" style="color: var(--primary);">Duarte Ferreira</span></h3>
                    <p style="font-size: 13px; color: #64748b; margin: 4px 0 0 0;">
                        Estado de resolução, pistas pedagógicas necessárias e tempo total decorrido até à validação correta.
                    </p>
                </div>
                <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                    <div style="display: inline-flex; background: #e2e8f0; padding: 3px; border-radius: 8px; gap: 3px;">
                        <button id="btn-filtro-exercicios" style="margin: 0; padding: 5px 12px; font-size: 12px; font-weight: 600; border-radius: 6px; border: none; background: var(--primary); color: white; cursor: pointer;" onclick="mudarFiltroItensDocente('exercicio')">
                            ⭐ Apenas Exercícios (1 a 6)
                        </button>
                        <button id="btn-filtro-todos" style="margin: 0; padding: 5px 12px; font-size: 12px; font-weight: 600; border-radius: 6px; border: none; background: transparent; color: #475569; cursor: pointer;" onclick="mudarFiltroItensDocente('todos')">
                            📋 Todos (com Passos dos Exemplos)
                        </button>
                    </div>
                </div>
            </div>
            <div style="overflow-x: auto; margin-top: 14px;">
                <table>
                    <thead>
                        <tr>
                            <th>Bloco Pedagógico</th>
                            <th>Pergunta / Etapa</th>
                            <th>Estado</th>
                            <th style="text-align: center;">Pistas Pedidas</th>
                            <th style="text-align: center;">Tempo até Validação</th>
                            <th style="text-align: center;">Média da Turma (Tempo)</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-progresso-consolidado">
                        <!-- Carregamento dinâmico -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 2. PANORAMA COMPARATIVO DA TURMA POR PERGUNTA -->
        <div class="card">
            <h3 style="margin: 0;">📊 Panorama Global da Turma por Pergunta</h3>
            <p style="font-size: 13px; color: #64748b; margin: 4px 0 14px 0;">
                Métricas agregadas da turma por exercício de aplicação para deteção imediata de pontos de bloqueio pedagógico.
            </p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Pergunta / Exercício</th>
                            <th style="text-align: center;">Alunos Validados</th>
                            <th style="text-align: center;">Total Pistas Pedidas (Turma)</th>
                            <th style="text-align: center;">Tempo Médio até Validação</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-turma-perguntas">
                        <!-- Carregamento dinâmico -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 3. QUADRO RESUMO COMPARATIVO ENTRE ALUNOS -->
        <div class="card">
            <h3 style="margin: 0;">👥 Desempenho Comparativo entre Alunos</h3>
            <p style="font-size: 13px; color: #64748b; margin: 4px 0 14px 0;">
                Visão consolidada por estudante: progresso na ficha, pistas pedidas e tempo médio por pergunta resolvida.
            </p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Turma</th>
                            <th style="text-align: center;">Exercícios Validados</th>
                            <th style="text-align: center;">Total Pistas Pedidas</th>
                            <th style="text-align: center;">Tempo Médio / Pergunta</th>
                            <th style="text-align: center;">Ação</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-resumo-alunos">
                        <!-- Carregamento dinâmico -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 4. REGISTO DETALHADO FORMATIVO -->
        <div class="card">
            <h3 style="margin-top: 0;">📜 Histórico Formativo de Tentativas</h3>
            <p style="font-size: 13px; color: #64748b; margin: 4px 0 16px 0;">
                Registo de apoio pedagógico. Tentativas que geraram pistas indicam momentos de aprendizagem guiada (*scaffolding*).
            </p>
            <div style="overflow-x: auto;">
                <table id="tabela-tentativas">
                    <thead>
                        <tr>
                            <th>Hora</th>
                            <th>Item</th>
                            <th>Passo / Etapa</th>
                            <th>Tempo Resposta</th>
                            <th>Resposta Submetida</th>
                            <th>Avaliação Formativa</th>
                            <th>Feedback e Pista Fornecida</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-tentativas">
                        <!-- Carregamento dinâmico -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
let alunoAtivoId = 1;
let alunoDocenteId = 1;
let fichaAtivaId = 'tarefa_07';
let fichaDocenteId = 'tarefa_07';
let filtroDocenteTipo = 'exercicio';
let timestampInicioPergunta = Date.now();

let estadoAtual = {
    fase: 'exemplo', // 'exemplo' ou 'exercicio'
    exemploId: 1,
    passoIndex: 0,
    passosLista: ['1.1', '1.2', '1.3'],
    exercicioId: 1
};

// Progresso do aluno ativo
let exerciciosValidados = new Set();
let passosValidados = new Set();
let exemplo1Concluido = false;
let exemplo2Concluido = false;

const dadosTarefas = {
    tarefa_04: {
        id: "tarefa_04",
        nome: "Tarefa 4: Matemática nos Salários",
        exemplos: {
            1: {
                id: 1,
                titulo: "Exemplo 1: Processamento de Vencimento Mensal com Consulta de Tabelas",
                enunciadoGeral: "A Catarina é casada (2 titulares), tem 1 filho (1 dependente), reside em Braga e aufere mensalmente uma remuneração base de $1256{,}20\\\\text{ €}$. Desconta $11\\\\%$ para a Segurança Social e recebe $5{,}20\\\\text{ €}$/dia de subsídio de refeição ($20$ dias úteis trabalhados em abril de 2023). A taxa de IRS na Tabela III é de $12{,}3\\\\%$.",
                passosLista: ['1.1', '1.2', '1.3', '1.4', '1.5'],
                passos: {
                    '1.1': {
                        numero: 'Passo 1.1',
                        pergunta: "Qual é o valor retido na fonte para o IRS à taxa de $12{,}3\\\\%$?",
                        orientacaoCalculo: "Calcula $\\\\text{IRS} = 1256{,}20 \\\\times 0{,}123$ e arredonda aos cêntimos:",
                        valoresCorretos: [154.51],
                        termosValidos: ["154.51", "154,51", "154.51€", "154,51€"],
                        feedbackErro: "Multiplica $1256{,}20$ por $0{,}123$: $1256{,}20 \\\\times 0{,}123 \\\\approx 154{,}51\\\\text{ €}$.",
                        pista: "A retenção na fonte é de $154{,}51\\\\text{ €}$.",
                        sucesso: "Muito bem! O valor retido para o IRS é de $154{,}51\\\\text{ €}$."
                    },
                    '1.2': {
                        numero: 'Passo 1.2',
                        pergunta: "Qual é o valor descontado para a Segurança Social ($11\\\\%$)?",
                        orientacaoCalculo: "Calcula $SS = 1256{,}20 \\\\times 0{,}11$:",
                        valoresCorretos: [138.18],
                        termosValidos: ["138.18", "138,18", "138.18€", "138,18€"],
                        feedbackErro: "Calcula $11\\\\%$ de $1256{,}20$: $1256{,}20 \\\\times 0{,}11 \\\\approx 138{,}18\\\\text{ €}$.",
                        pista: "O desconto para a Segurança Social é de $138{,}18\\\\text{ €}$.",
                        sucesso: "Excelente! O desconto para a Segurança Social é de $138{,}18\\\\text{ €}$."
                    },
                    '1.3': {
                        numero: 'Passo 1.3',
                        pergunta: "Qual é o valor do salário líquido da Catarina?",
                        orientacaoCalculo: "Subtrai os dois descontos ao salário bruto ($1256{,}20 - 154{,}51 - 138{,}18$):",
                        valoresCorretos: [963.51],
                        termosValidos: ["963.51", "963,51", "963.51€", "963,51€"],
                        feedbackErro: "Subtrai $154{,}51$ e $138{,}18$ ao salário bruto: $1256{,}20 - 154{,}51 - 138{,}18 = 963{,}51\\\\text{ €}$.",
                        pista: "O salário líquido é de $963{,}51\\\\text{ €}$.",
                        sucesso: "Correto! O salário líquido é de $963{,}51\\\\text{ €}$."
                    },
                    '1.4': {
                        numero: 'Passo 1.4',
                        pergunta: "Qual é o valor total do subsídio de refeição relativo aos 20 dias úteis?",
                        orientacaoCalculo: "Multiplica os 20 dias por $5{,}20\\\\text{ €}$:",
                        valoresCorretos: [104],
                        termosValidos: ["104", "104.00", "104,00", "104€", "104 €"],
                        feedbackErro: "Multiplica $20 \\\\times 5{,}20 = 104{,}00\\\\text{ €}$.",
                        pista: "O subsídio de refeição é $20 \\\\times 5{,}20 = 104\\\\text{ €}$.",
                        sucesso: "Muito bem! O subsídio de alimentação totaliza $104{,}00\\\\text{ €}$."
                    },
                    '1.5': {
                        numero: 'Passo 1.5',
                        pergunta: "Qual é o montante total líquido transferido para a conta da Catarina?",
                        orientacaoCalculo: "Soma o salário líquido com o subsídio de refeição ($963{,}51 + 104{,}00$):",
                        valoresCorretos: [1067.51],
                        termosValidos: ["1067.51", "1067,51", "1067.51€", "1067,51€"],
                        feedbackErro: "Soma $963{,}51 + 104{,}00 = 1067{,}51\\\\text{ €}$.",
                        pista: "O total líquido a receber é de $1067{,}51\\\\text{ €}$.",
                        sucesso: "Parabéns! Concluíste o Exemplo 1 da Tarefa 4 com sucesso ($1067{,}51\\\\text{ €}$)!"
                    }
                }
            }
        },
        exercicios: {
            1: {
                numero: 1,
                bloco: 1,
                enunciado: "O Mateus é solteiro e não tem filhos, reside nos Açores e aufere mensalmente um salário base de $1956{,}40\\\\text{ €}$. Desconta $11\\\\%$ para a Segurança Social e recebe $5{,}80\\\\text{ €}$ por dia de subsídio de refeição. Em setembro de 2022 trabalhou 22 dias úteis, sendo a sua taxa de retenção de IRS de $14{,}6\\\\%$. Calcula o valor líquido total que o Mateus recebeu no final do mês.",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o salário líquido e soma o subsídio de alimentação no teu caderno:",
                valoresCorretos: [1583.17, 1583.16, 1583.18],
                termosValidos: ["1583.17", "1583,17", "1583.16", "1583,16", "1583.18", "1583,18"],
                feedbackErro: "Desconto SS ($11\\\\%$): $215{,}20\\\\text{ €}$. Retenção IRS ($14{,}6\\\\%$): $285{,}63\\\\text{ €}$. Salário Líquido: $1455{,}57\\\\text{ €}$. Subsídio refeição ($22 \\\\times 5{,}80$): $127{,}60\\\\text{ €}$. Total: $1455{,}57 + 127{,}60 = 1583{,}17\\\\text{ €}$.",
                pista: "O valor total líquido recebido pelo Mateus é de $1583{,}17\\\\text{ €}$.",
                sucesso: "Excelente! O Mateus recebeu um valor total de $1583{,}17\\\\text{ €}$."
            },
            2: {
                numero: 2,
                bloco: 1,
                enunciado: "Compara os valores líquidos recebidos pelo Carlos em fevereiro de 2010 ($SB = 845\\\\text{ €}$, SS $11\\\\%$, IRS $5{,}67\\\\%$, $SR = 5{,}20\\\\text{ €}$/dia $\\\\times 21$ dias) e fevereiro de 2023 ($SB = 975\\\\text{ €}$, SS $11\\\\%$, IRS $5\\\\%$, $SR = 5{,}90\\\\text{ €}$/dia $\\\\times 20$ dias). Qual é o total líquido auferido em fevereiro de 2023?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o total auferido em fevereiro de 2023 no teu caderno:",
                valoresCorretos: [937, 937.00, 813.34],
                termosValidos: ["937", "937.00", "937,00", "937€", "813.34", "813,34"],
                feedbackErro: "Em fev/2023: $SL = 975 - 107{,}25 - 48{,}75 = 819{,}00\\\\text{ €}$. $SR = 20 \\\\times 5{,}90 = 118{,}00\\\\text{ €}$. Total em 2023: $819 + 118 = 937{,}00\\\\text{ €}$ (em 2010 recebeu $813{,}34\\\\text{ €}$).",
                pista: "O total auferido pelo Carlos em fevereiro de 2023 foi de $937{,}00\\\\text{ €}$.",
                sucesso: "Muito bem! O Carlos auferiu $937{,}00\\\\text{ €}$ em fevereiro de 2023 (mais $123{,}66\\\\text{ €}$ do que em 2010)."
            },
            3: {
                numero: 3,
                bloco: 1,
                enunciado: "A Mariana aufere um salário bruto mensal de $1700{,}00\\\\text{ €}$, reside no Continente e trabalhou 22 dias úteis ($SR = 5{,}20\\\\text{ €}$/dia). No 2.º semestre de 2023 a taxa marginal máxima é de $28{,}50\\\\%$ e a parcela a abater é de $191{,}23\\\\text{ €}$. Qual é o valor líquido total recebido pela Mariana?",
                tabela: null,
                imagem: null,
                orientacao: "Aplica $\\\\text{IRS} = 1700 \\\\times 0{,}285 - 191{,}23$, desconta $11\\\\%$ da Segurança Social e adiciona o subsídio de refeição:",
                valoresCorretos: [1334.13],
                termosValidos: ["1334.13", "1334,13"],
                feedbackErro: "Retenção IRS: $1700 \\\\times 0{,}285 - 191{,}23 = 293{,}27\\\\text{ €}$. SS: $187{,}00\\\\text{ €}$. $SL = 1219{,}73\\\\text{ €}$. $SR = 22 \\\\times 5{,}20 = 114{,}40\\\\text{ €}$. Total: $1219{,}73 + 114{,}40 = 1334{,}13\\\\text{ €}$.",
                pista: "O total líquido final que a Mariana recebe é de $1334{,}13\\\\text{ €}$.",
                sucesso: "Excelente! A Mariana recebeu um valor total líquido de $1334{,}13\\\\text{ €}$."
            },
            4: {
                numero: 4,
                bloco: 1,
                enunciado: "A Carina aufere $800{,}00\\\\text{ €}$ de salário bruto, trabalhou 21 dias úteis ($SR = 5{,}50\\\\text{ €}$/dia). Pela Tabela I do 2.º semestre de 2023, a taxa marginal é de $14{,}5\\\\%$ e a parcela a abater é dada por $14{,}5\\\\% \\\\times 2{,}3 \\\\times (1093{,}31 - 800) = 97{,}82\\\\text{ €}$. Determina o total líquido que a Carina auferiu no mês.",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o IRS retido ($800 \\\\times 0{,}145 - 97{,}82 = 18{,}18\\\\text{ €}$), desconta $11\\\\%$ da Segurança Social e soma a refeição:",
                valoresCorretos: [809.32],
                termosValidos: ["809.32", "809,32"],
                feedbackErro: "Retenção IRS: $116 - 97{,}82 = 18{,}18\\\\text{ €}$. Desconto SS ($11\\\\%$): $88{,}00\\\\text{ €}$. $SL = 800 - 18{,}18 - 88 = 693{,}82\\\\text{ €}$. $SR = 21 \\\\times 5{,}50 = 115{,}50\\\\text{ €}$. Total: $693{,}82 + 115{,}50 = 809{,}32\\\\text{ €}$.",
                pista: "O montante líquido total auferido pela Carina é de $809{,}32\\\\text{ €}$.",
                sucesso: "Parabéns! Concluíste com sucesso todos os exercícios da Tarefa 4! O valor recebido foi de $809{,}32\\\\text{ €}$."
            }
        }
    },
    tarefa_05: {
        id: "tarefa_05",
        nome: "Tarefa 5: Salário Bruto à Hora",
        exemplos: {
            1: {
                id: 1,
                titulo: "Exemplo 1: Determinação do Salário Bruto à Hora e Horas Extraordinárias",
                enunciadoGeral: "A Maria trabalha como animadora num hotel e recebe à hora ($8\\\\text{ horas}$/dia, $5\\\\text{ dias}$/semana, $n = 40\\\\text{ horas semanais}$). A remuneração base é de $760{,}00\\\\text{ €}$. Aplica-se a fórmula legal $V_h = \\\\frac{SB \\\\times 12}{52 \\\\times n}$.",
                passosLista: ['1.1', '1.2', '1.3', '1.4'],
                passos: {
                    '1.1': {
                        numero: 'Passo 1.1',
                        pergunta: "Qual é o valor do rendimento bruto anual de referência ($760 \\\\times 12$)?",
                        orientacaoCalculo: "Calcula o produto de $760$ por $12$:",
                        valoresCorretos: [9120],
                        termosValidos: ["9120", "9120€", "9 120", "9120,00"],
                        feedbackErro: "Calcula $760 \\\\times 12 = 9120\\\\text{ €}$.",
                        pista: "O rendimento anual de referência é $9120\\\\text{ €}$.",
                        sucesso: "Correto! O rendimento anual é $9120\\\\text{ €}$."
                    },
                    '1.2': {
                        numero: 'Passo 1.2',
                        pergunta: "Qual é o total anual de horas de trabalho ($52 \\\\times 40$)?",
                        orientacaoCalculo: "Multiplica as 52 semanas pelas 40 horas semanais:",
                        valoresCorretos: [2080],
                        termosValidos: ["2080", "2080h", "2 080"],
                        feedbackErro: "Multiplica $52 \\\\times 40 = 2080$ horas.",
                        pista: "O divisor anual de horas é de $2080$ horas.",
                        sucesso: "Muito bem! O total anual de horas é de $2080\\\\text{ h}$."
                    },
                    '1.3': {
                        numero: 'Passo 1.3',
                        pergunta: "Qual é o valor do salário bruto à hora ($V_h$) arredondado aos cêntimos?",
                        orientacaoCalculo: "Divide $9120$ por $2080$ e arredonda o resultado às centésimas:",
                        valoresCorretos: [4.38],
                        termosValidos: ["4.38", "4,38", "4.38€", "4,38€"],
                        feedbackErro: "Divide $\\\\frac{9120}{2080} \\\\approx 4{,}3846 \\\\approx 4{,}38\\\\text{ €/h}$.",
                        pista: "O valor da hora normal de trabalho é de $4{,}38\\\\text{ €}$.",
                        sucesso: "Exato! O salário bruto à hora da Maria é de $4{,}38\\\\text{ €}$."
                    },
                    '1.4': {
                        numero: 'Passo 1.4',
                        pergunta: "Se a Maria realizar 10 horas extraordinárias à tarifa simples ($10 \\\\times 4{,}38$), quanto receberá?",
                        orientacaoCalculo: "Multiplica as 10 horas pelo valor horário de $4{,}38\\\\text{ €}$:",
                        valoresCorretos: [43.8, 43.80],
                        termosValidos: ["43.8", "43.80", "43,8", "43,80"],
                        feedbackErro: "Calcula $10 \\\\times 4{,}38 = 43{,}80\\\\text{ €}$.",
                        pista: "O valor a receber pelas 10 horas é $43{,}80\\\\text{ €}$.",
                        sucesso: "Parabéns! Concluíste o Exemplo 1 da Tarefa 5 com sucesso ($43{,}80\\\\text{ €}$)!"
                    }
                }
            }
        },
        exercicios: {
            1: {
                numero: 1,
                bloco: 1,
                enunciado: "O Marco é mecânico, trabalha 40 horas semanais e aufere um salário bruto de $1800{,}00\\\\text{ €}$. Em julho realizou 9 horas extraordinárias. Determina o valor bruto total que o Marco deve receber por essas 9 horas suplementares.",
                tabela: null,
                imagem: null,
                orientacao: "Calcula $V_h = \\\\frac{1800 \\\\times 12}{52 \\\\times 40} \\\\approx 10{,}38\\\\text{ €/h}$ e multiplica por 9 horas:",
                valoresCorretos: [93.42, 10.38],
                termosValidos: ["93.42", "93,42", "10.38", "10,38"],
                feedbackErro: "$V_h = \\\\frac{21\\\\,600}{2080} \\\\approx 10{,}38\\\\text{ €/h}$. Em 9 horas extraordinárias: $10{,}38 \\\\times 9 = 93{,}42\\\\text{ €}$.",
                pista: "O valor auferido pelo Marco nas 9 horas suplementares é de $93{,}42\\\\text{ €}$.",
                sucesso: "Muito bem! O Marco aufere $93{,}42\\\\text{ €}$ pelas 9 horas de trabalho extraordinário."
            },
            2: {
                numero: 2,
                bloco: 1,
                enunciado: "O Carlos trabalha 40 horas semanais e tem um salário base de $760{,}00\\\\text{ €}$ ($V_h \\\\approx 4{,}38\\\\text{ €/h}$). No mês passado realizou 14 horas extraordinárias. Qual é a retribuição bruta total do Carlos nesse mês (salário base + horas extraordinárias)?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula $760 + (14 \\\\times 4{,}38)$ no teu caderno:",
                valoresCorretos: [821.32, 61.32],
                termosValidos: ["821.32", "821,32", "61.32", "61,32"],
                feedbackErro: "Valor das horas: $14 \\\\times 4{,}38 = 61{,}32\\\\text{ €}$. Salário bruto total: $760 + 61{,}32 = 821{,}32\\\\text{ €}$.",
                pista: "A retribuição bruta total do Carlos é de $821{,}32\\\\text{ €}$.",
                sucesso: "Excelente! A retribuição bruta total com as 14 horas extraordinárias é de $821{,}32\\\\text{ €}$."
            },
            3: {
                numero: 3,
                bloco: 1,
                enunciado: "A Rosa aufere um salário base de $2789{,}43\\\\text{ €}$ por um horário de 40 horas semanais. Em agosto de 2023 realizou 8 horas extraordinárias. Sabendo que o seu valor horário é $V_h \\\\approx 16{,}09\\\\text{ €/h}$, qual foi o seu salário bruto total nesse mês?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula as horas suplementares ($8 \\\\times 16{,}09 = 128{,}72\\\\text{ €}$) e soma ao vencimento base:",
                valoresCorretos: [2918.15, 128.72, 16.09],
                termosValidos: ["2918.15", "2918,15", "128.72", "128,72", "16.09", "16,09"],
                feedbackErro: "Horas extraordinárias: $16{,}09 \\\\times 8 = 128{,}72\\\\text{ €}$. Salário bruto de agosto: $2789{,}43 + 128{,}72 = 2918{,}15\\\\text{ €}$.",
                pista: "O salário bruto total da Rosa em agosto foi de $2918{,}15\\\\text{ €}$.",
                sucesso: "Muito bem! O salário bruto total da Rosa em agosto foi de $2918{,}15\\\\text{ €}$."
            },
            4: {
                numero: 4,
                bloco: 1,
                enunciado: "A Maria trabalha 40 horas semanais com um vencimento de $902{,}00\\\\text{ €}$. Em maio realizou 12 horas extraordinárias. Quanto recebeu em horas extraordinárias nesse mês?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula $V_h = \\\\frac{902 \\\\times 12}{52 \\\\times 40} = 5{,}20\\\\text{ €/h}$ e multiplica pelas 12 horas:",
                valoresCorretos: [62.4, 62.40, 5.20],
                termosValidos: ["62.4", "62.40", "62,4", "62,40", "5.20", "5,20"],
                feedbackErro: "$V_h = \\\\frac{10\\\\,824}{2080} = 5{,}20\\\\text{ €/h}$. Horas extraordinárias: $5{,}20 \\\\times 12 = 62{,}40\\\\text{ €}$.",
                pista: "A Maria recebeu $62{,}40\\\\text{ €}$ pelas 12 horas extraordinárias.",
                sucesso: "Correto! O montante recebido pelas 12 horas extraordinárias foi de $62{,}40\\\\text{ €}$."
            },
            5: {
                numero: 5,
                bloco: 1,
                enunciado: "A Filipa aufere $1000{,}00\\\\text{ €}$ por um horário de 35 horas semanais e realizou 8 horas extraordinárias. Determina o montante recebido por essas 8 horas suplementares.",
                tabela: null,
                imagem: null,
                orientacao: "Calcula $V_h = \\\\frac{1000 \\\\times 12}{52 \\\\times 35} \\\\approx 6{,}59\\\\text{ €/h}$ e multiplica por 8 horas:",
                valoresCorretos: [52.72, 6.59],
                termosValidos: ["52.72", "52,72", "6.59", "6,59"],
                feedbackErro: "$V_h = \\\\frac{12\\\\,000}{1820} \\\\approx 6{,}5934 \\\\approx 6{,}59\\\\text{ €/h}$. Horas suplementares: $6{,}59 \\\\times 8 = 52{,}72\\\\text{ €}$.",
                pista: "Pelas 8 horas extraordinárias recebeu $52{,}72\\\\text{ €}$.",
                sucesso: "Parabéns! Concluíste com sucesso todos os exercícios da Tarefa 5! O valor apurado foi de $52{,}72\\\\text{ €}$."
            }
        }
    },
    tarefa_06: {
        id: "tarefa_06",
        nome: "Tarefa 6: Imposto sobre o Rendimento (IRS)",
        exemplos: {
            1: {
                id: 1,
                titulo: "Exemplo 1: Apuramento Anual de IRS de um Casal (Mariana e Afonso)",
                enunciadoGeral: "A Mariana ($1200\\\\text{ €}$) e o Afonso ($1340\\\\text{ €}$) são casados (14 meses brutos cada). Entregam a declaração de IRS conjuntamente em 2023 sem deduções.",
                passosLista: ['1.1', '1.2', '1.3', '1.4'],
                passos: {
                    '1.1': {
                        numero: 'Passo 1.1',
                        pergunta: "Qual é o rendimento bruto anual conjunto do casal ($(1200 + 1340) \\\\times 14$)?",
                        orientacaoCalculo: "Soma as duas remunerações e multiplica por 14:",
                        valoresCorretos: [35560],
                        termosValidos: ["35560", "35 560", "35560€"],
                        feedbackErro: "$(1200 + 1340) \\\\times 14 = 2540 \\\\times 14 = 35\\\\,560\\\\text{ €}$.",
                        pista: "O rendimento bruto anual conjunto é de $35\\\\,560\\\\text{ €}$.",
                        sucesso: "Muito bem! O rendimento bruto anual global é de $35\\\\,560\\\\text{ €}$."
                    },
                    '1.2': {
                        numero: 'Passo 1.2',
                        pergunta: "Qual é o rendimento coletável de referência por titular (quociente conjugal de 2)?",
                        orientacaoCalculo: "Divide o rendimento bruto por 2 ($35\\\\,560 \\\\div 2$):",
                        valoresCorretos: [17780],
                        termosValidos: ["17780", "17 780", "17780€"],
                        feedbackErro: "Divide $35\\\\,560$ por $2$: $RC = 17\\\\,780\\\\text{ €}$.",
                        pista: "O rendimento coletável por titular é de $17\\\\,780\\\\text{ €}$.",
                        sucesso: "Correto! O rendimento coletável de referência é de $17\\\\,780\\\\text{ €}$."
                    },
                    '1.3': {
                        numero: 'Passo 1.3',
                        pergunta: "No 4.º escalão (taxa de $28{,}5\\\\%$ e parcela de $1426{,}65\\\\text{ €}$), qual é a coleta individual?",
                        orientacaoCalculo: "Calcula $17\\\\,780 \\\\times 0{,}285 - 1426{,}65$:",
                        valoresCorretos: [3640.65],
                        termosValidos: ["3640.65", "3640,65", "3640.65€"],
                        feedbackErro: "$17\\\\,780 \\\\times 0{,}285 - 1426{,}65 = 5067{,}30 - 1426{,}65 = 3640{,}65\\\\text{ €}$.",
                        pista: "A coleta individual é de $3640{,}65\\\\text{ €}$.",
                        sucesso: "Exato! A coleta individual de cada cônjuge é de $3640{,}65\\\\text{ €}$."
                    },
                    '1.4': {
                        numero: 'Passo 1.4',
                        pergunta: "Qual é a coleta total de IRS devida pelo casal ($3640{,}65 \\\\times 2$)?",
                        orientacaoCalculo: "Multiplica a coleta individual por 2:",
                        valoresCorretos: [7281.3, 7281.30],
                        termosValidos: ["7281.3", "7281.30", "7281,3", "7281,30"],
                        feedbackErro: "Multiplica $3640{,}65 \\\\times 2 = 7281{,}30\\\\text{ €}$.",
                        pista: "A coleta total a suportar pelo casal é de $7281{,}30\\\\text{ €}$.",
                        sucesso: "Parabéns! Concluíste o Exemplo 1 da Tarefa 6 com sucesso ($7281{,}30\\\\text{ €}$)!"
                    }
                }
            }
        },
        exercicios: {
            1: {
                numero: 1,
                bloco: 1,
                enunciado: "A Rita e o Afonso auferem $1050\\\\text{ €}$ e $1010\\\\text{ €}$ brutos mensais (14 meses) e entregam IRS conjunto sem deduções. No 3.º escalão a taxa é de $26{,}5\\\\%$ e a parcela a abater é de $1106{,}73\\\\text{ €}$. Qual é a coleta total de IRS do casal?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o rendimento bruto anual ($28\\\\,840\\\\text{ €}$), o $RC = 14\\\\,420\\\\text{ €}$ e a coleta total ($2 \\\\times (14\\\\,420 \\\\times 0{,}265 - 1106{,}73)$):",
                valoresCorretos: [5429.14, 2714.57],
                termosValidos: ["5429.14", "5429,14", "2714.57", "2714,57"],
                feedbackErro: "$RB = 28\\\\,840\\\\text{ €}$, $RC = 14\\\\,420\\\\text{ €}$. Coleta individual: $14\\\\,420 \\\\times 0{,}265 - 1106{,}73 = 2714{,}57\\\\text{ €}$. Coleta total (2 titulares): $2714{,}57 \\\\times 2 = 5429{,}14\\\\text{ €}$.",
                pista: "A coleta total de IRS devida pelo casal é de $5429{,}14\\\\text{ €}$.",
                sucesso: "Muito bem! A coleta total devida pelo casal é de $5429{,}14\\\\text{ €}$."
            },
            2: {
                numero: 2,
                bloco: 1,
                enunciado: "O Manuel é solteiro e não tem dependentes nem deduções, auferindo um salário mensal de $1300\\\\text{ €}$ (14 meses). No 4.º escalão a taxa é de $28{,}5\\\\%$ e a parcela a abater é de $1426{,}65\\\\text{ €}$. Determina a coleta de IRS suportada pelo Manuel.",
                tabela: null,
                imagem: null,
                orientacao: "Como é solteiro, $RC = RB = 1300 \\\\times 14 = 18\\\\,200\\\\text{ €}$. Calcula a coleta no teu caderno:",
                valoresCorretos: [3760.35],
                termosValidos: ["3760.35", "3760,35"],
                feedbackErro: "$RB = RC = 18\\\\,200\\\\text{ €}$. Coleta: $18\\\\,200 \\\\times 0{,}285 - 1426{,}65 = 3760{,}35\\\\text{ €}$.",
                pista: "A coleta de IRS apurada é de $3760{,}35\\\\text{ €}$.",
                sucesso: "Excelente! O Manuel suporta uma coleta de IRS de $3760{,}35\\\\text{ €}$."
            },
            3: {
                numero: 3,
                bloco: 1,
                enunciado: "A Joana e o Miguel têm vencimentos mensais de $1200\\\\text{ €}$ e $1890\\\\text{ €}$ (14 meses), casados sem deduções. No 5.º escalão a taxa é de $35\\\\%$ e a parcela a abater é de $2772{,}14\\\\text{ €}$. Qual é a coleta total de IRS do casal?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula $RB = 43\\\\,260\\\\text{ €}$, $RC = 21\\\\,630\\\\text{ €}$ e multiplica a coleta individual por 2:",
                valoresCorretos: [9596.72, 4798.36, 9596.36],
                termosValidos: ["9596.72", "9596,72", "4798.36", "4798,36", "9596.36", "9596,36"],
                feedbackErro: "Coleta individual: $21\\\\,630 \\\\times 0{,}35 - 2772{,}14 = 4798{,}36\\\\text{ €}$. Coleta total: $4798{,}36 \\\\times 2 = 9596{,}72\\\\text{ €}$.",
                pista: "A coleta total devida pelo casal é de $9596{,}72\\\\text{ €}$.",
                sucesso: "Muito bem! O imposto total liquidado para o casal é de $9596{,}72\\\\text{ €}$."
            },
            4: {
                numero: 4,
                bloco: 1,
                enunciado: "Considera a Mariana e o Afonso com rendimento bruto conjunto de $35\\\\,560\\\\text{ €}$, considerando agora as deduções específicas da Categoria A ($4104\\\\text{ €}$ por cada titular). Qual é a nova coleta total devida pelo casal (taxa $26{,}5\\\\%$, parcela $1106{,}73\\\\text{ €}$)?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o rendimento com deduções ($35\\\\,560 - 8208 = 27\\\\,352\\\\text{ €}$), $RC = 13\\\\,676\\\\text{ €}$ e apura a coleta total:",
                valoresCorretos: [5034.82, 2517.41, 2246.48],
                termosValidos: ["5034.82", "5034,82", "2517.41", "2517,41", "2246.48", "2246,48"],
                feedbackErro: "$RC = (35\\\\,560 - 8208) \\\\div 2 = 13\\\\,676\\\\text{ €}$. Coleta individual: $13\\\\,676 \\\\times 0{,}265 - 1106{,}73 = 2517{,}41\\\\text{ €}$. Coleta total: $2517{,}41 \\\\times 2 = 5034{,}82\\\\text{ €}$ (poupança de $2246{,}48\\\\text{ €}$).",
                pista: "Com as deduções específicas, a coleta total desce para $5034{,}82\\\\text{ €}$.",
                sucesso: "Exato! Com as deduções específicas, a coleta total é de $5034{,}82\\\\text{ €}$."
            },
            5: {
                numero: 5,
                bloco: 1,
                enunciado: "A Eugénia e o Augusto nos Açores auferem $2530\\\\text{ €}$ e $2300\\\\text{ €}$ mensais (14 meses). Com deduções específicas de $4104\\\\text{ €}$ por titular, $RC = 29\\\\,706\\\\text{ €}$, taxa de $25{,}9\\\\%$ e parcela de $2146{,}76\\\\text{ €}$. Qual é a coleta total de IRS final do casal?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula a coleta individual ($29\\\\,706 \\\\times 0{,}259 - 2146{,}76 \\\\approx 5547{,}09\\\\text{ €}$) e multiplica por 2:",
                valoresCorretos: [11094.19, 5547.09, 2125.87],
                termosValidos: ["11094.19", "11094,19", "5547.09", "5547,09", "2125.87", "2125,87"],
                feedbackErro: "Coleta individual: $29\\\\,706 \\\\times 0{,}259 - 2146{,}76 \\\\approx 5547{,}09\\\\text{ €}$. Coleta total: $5547{,}094 \\\\times 2 = 11\\\\,094{,}19\\\\text{ €}$.",
                pista: "A coleta final do casal com as deduções é de $11\\\\,094{,}19\\\\text{ €}$.",
                sucesso: "Parabéns! Concluíste com sucesso todos os exercícios da Tarefa 6! A coleta total foi de $11\\\\,094{,}19\\\\text{ €}$."
            }
        }
    },
    tarefa_07: {
        id: "tarefa_07",
        nome: "Tarefa 7: Juros Simples",
        exemplos: {
            1: {
                id: 1,
                titulo: "Exemplo 1: Cálculo de Juros Simples e Capital Acumulado",
                enunciadoGeral: "Supõe que depositaste $650\\\\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $4\\\\%$.",
                passosLista: ['1.1', '1.2', '1.3'],
                passos: {
                    '1.1': {
                        numero: 'Passo 1.1',
                        pergunta: "Qual é o valor a receber de juros no final do 1.º ano?",
                        orientacaoCalculo: "Efetua o cálculo no teu rascunho com a fórmula $J = C_0 \\\\times i$ (onde $i = 4\\\\% = 0{,}04$) e introduz apenas o valor numérico final no espaço abaixo:",
                        valoresCorretos: [26],
                        termosValidos: [
                            "26", "26€", "26 €", "26 euros", "26,00", "26.00", "26,00€", "26,00 €", "26.00€", "26.00 €", "26,0", "26.0", "26 eur", "26 EUR", "26eur", "26EUR",
                            "650*0,04", "650 * 0,04", "650*0.04", "650 * 0.04",
                            "650x0,04", "650 x 0,04", "650x0.04", "650 x 0.04",
                            "650*4%", "650 * 4%", "650x4%", "650 x 4%",
                            "650*4/100", "650 * 4 / 100",
                            "j=26", "j = 26", "j1=26", "j1 = 26", "j_1=26", "j_1 = 26",
                            "vinte e seis", "vinte e seis euros"
                        ],
                        feedbackErro: "Atenção: uma taxa de $4\\\\%$ na forma decimal corresponde a $\\\\frac{4}{100} = 0{,}04$.",
                        pista: "Multiplica o capital inicial ($650\\\\text{ €}$) pela taxa decimal $0{,}04$ para obter o juro de 1 ano.",
                        sucesso: "Excelente! No final do 1.º ano recebes $J_1 = 650 \\\\times 0{,}04 = 26\\\\text{ €}$."
                    },
                    '1.2': {
                        numero: 'Passo 1.2',
                        pergunta: "Qual é o valor de juros acumulados ao fim de 3 anos?",
                        orientacaoCalculo: "No regime de juros simples, o valor do juro é rigorosamente igual em cada ano. Calcula os juros acumulados nos 3 anos completos:",
                        valoresCorretos: [78],
                        termosValidos: ["78", "78€", "78 €", "78 euros", "78,00", "78.00", "78,00€", "78,00 €", "26*3", "26 * 3", "26x3", "26 x 3", "650*0,04*3", "650 * 0,04 * 3", "j3=78", "j=78", "setenta e oito"],
                        feedbackErro: "No regime de juros simples o juro anual de $26\\\\text{ €}$ repete-se em cada ano.",
                        pista: "Multiplica o juro obtido no 1.º ano ($26\\\\text{ €}$) pelo número de anos decorridos ($3\\\\text{ anos}$).",
                        sucesso: "Muito bem! Ao fim de 3 anos tens $J_3 = 26 \\\\times 3 = 78\\\\text{ €}$ de juros acumulados."
                    },
                    '1.3': {
                        numero: 'Passo 1.3',
                        pergunta: "Qual é o valor do capital acumulado ao fim dos 3 anos?",
                        orientacaoCalculo: "O capital acumulado ($C_3$) é a quantia total na conta ao fim do prazo. Calcula a soma do capital inicial com todos os juros acumulados:",
                        valoresCorretos: [728],
                        termosValidos: ["728", "728€", "728 €", "728 euros", "728,00", "728.00", "728,00€", "728,00 €", "650+78", "650 + 78", "c3=728", "c=728", "setecentos e vinte e oito"],
                        feedbackErro: "Tem atenção à soma: o capital inicial é de $650\\\\text{ €}$ e os juros acumulados são de $78\\\\text{ €}$.",
                        pista: "Soma o capital inicial com o total de juros obtidos: $C_3 = C_0 + J_3 = 650 + 78$.",
                        sucesso: "Parabéns! O capital acumulado é $C_3 = 650 + 78 = 728\\\\text{ €}$. Concluíste o Exemplo 1 com sucesso e desbloqueaste os Exercícios 1 a 4!"
                    }
                }
            },
            2: {
                id: 2,
                titulo: "Exemplo 2: Determinação da Taxa de Juro Anual",
                enunciadoGeral: "Um casal investiu $123\\\\,000\\\\text{ €}$ num regime de juros simples. Ao fim de $10\\\\text{ anos}$ tinham $136\\\\,038\\\\text{ €}$. Qual foi a taxa de juro anual?",
                passosLista: ['2.1', '2.2'],
                passos: {
                    '2.1': {
                        numero: 'Passo 2.1',
                        pergunta: "Determina em primeiro lugar o montante total de juros gerados ao longo dos 10 anos:",
                        orientacaoCalculo: "Calcula a diferença entre o capital acumulado final ($136\\\\,038\\\\text{ €}$) e o capital inicialmente investido ($123\\\\,000\\\\text{ €}$):",
                        valoresCorretos: [13038],
                        termosValidos: ["13038", "13 038", "13038€", "13 038€", "13038 euros", "13 038 euros"],
                        feedbackErro: "Atenção: os juros correspondem ao excedente ganho, ou seja, $J_{10} = C_{10} - C_0$.",
                        pista: "Subtrai $123\\\\,000$ a $136\\\\,038$ para determinar os juros totais auferidos.",
                        sucesso: "Muito bem! Os juros totais ao fim de 10 anos foram $J_{10} = 136\\\\,038 - 123\\\\,000 = 13\\\\,038\\\\text{ €}$."
                    },
                    '2.2': {
                        numero: 'Passo 2.2',
                        pergunta: "Qual foi a taxa de juro anual expressa em percentagem ($r$)?",
                        orientacaoCalculo: "Aplica a fórmula dos juros simples $J = C_0 \\\\times i \\\\times n$, isola a taxa decimal $i$ e multiplica por 100 para obter a taxa em percentagem:",
                        valoresCorretos: [1.06, 0.0106],
                        termosValidos: ["1.06", "1,06", "1.06%", "1,06%", "0.0106", "0,0106"],
                        feedbackErro: "Confere os cálculos: $13\\\\,038 = 123\\\\,000 \\\\times i \\\\times 10 \\\\iff 13\\\\,038 = 1\\\\,230\\\\,000 \\\\times i$.",
                        pista: "Divide $13\\\\,038$ por $1\\\\,230\\\\,000$, obtendo $i = 0{,}0106$. Multiplica por $100$ para converter em percentagem ($r = 1{,}06\\\\%$).",
                        sucesso: "Perfeito! A taxa de juro anual foi de $1{,}06\\\\%$. Concluíste o Exemplo 2 com sucesso e desbloqueaste os Exercícios 5 e 6!"
                    }
                }
            }
        },
        exercicios: {
            1: {
                numero: 1,
                bloco: 1,
                enunciado: "O Francisco depositou $1500\\\\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $1{,}2\\\\%$. Qual será o valor do capital acumulado ao fim de $1\\\\text{ ano}$?",
                tabela: null,
                imagem: null,
                orientacao: "Efetua a resolução no teu caderno (pela fórmula direta $C_a = C_i(1 + \\\\frac{r}{100} \\\\times n)$ ou calculando os juros e somando ao capital inicial) com todo o desenvolvimento:",
                valoresCorretos: [1518],
                termosValidos: ["1518", "1518€", "1518 €", "1518 euros"],
                feedbackErro: "Confere os cálculos: o juro auferido é $1500 \\\\times 0{,}012 = 18\\\\text{ €}$. Somando ao capital inicial obtém-se $C_a = 1500 + 18 = 1518\\\\text{ €}$.",
                pista: "Aplica $C_a = 1500 \\\\times (1 + 0{,}012) = 1518\\\\text{ €}$ ou soma o juro ($18\\\\text{ €}$) ao capital inicial.",
                sucesso: "Excelente resolução! Ao fim de um ano, o Francisco acumulou um capital de $1518\\\\text{ €}$."
            },
            2: {
                numero: 2,
                bloco: 1,
                enunciado: "Durante as férias de verão, a Raquel trabalhou como nadadora-salvadora e recebeu $3000\\\\text{ €}$. Em setembro, resolveu depositar o dinheiro, numa conta a prazo, num regime de juros simples durante $7\\\\text{ anos}$ à taxa anual de $1{,}2\\\\%$. Calcula o valor:<br><strong>2.1</strong> Dos juros no final do 1.º ano.<br><strong>2.2</strong> Do capital acumulado ao fim dos 7 anos.",
                tabela: null,
                imagem: null,
                orientacao: "Calcula o juro do 1.º ano ($J_1$) e o capital acumulado final ($C_a$) no teu caderno:",
                valoresCorretos: [36, 3252],
                termosValidos: ["36", "3252"],
                feedbackErro: "Para o 1.º ano: $J_1 = 3000 \\\\times 0{,}012 = 36\\\\text{ €}$. Para os 7 anos: $C_a = 3000 \\\\times (1 + 0{,}012 \\\\times 7) = 3252\\\\text{ €}$ (ou $3000 + 7 \\\\times 36 = 3252\\\\text{ €}$).",
                pista: "No 1.º ano os juros são $36\\\\text{ €}$; ao fim de 7 anos o capital acumulado é $3252\\\\text{ €}$.",
                sucesso: "Muito bem! Juros no final do 1.º ano: $36\\\\text{ €}$; Capital acumulado ao fim de 7 anos: $3252\\\\text{ €}$."
            },
            3: {
                numero: 3,
                bloco: 1,
                enunciado: "O Diogo quer aplicar parte dos $89\\\\,000\\\\text{ €}$, que recebeu da venda de um imóvel, num depósito a prazo. Consultou dois bancos:",
                tabela: `
                <table>
                    <thead>
                        <tr><th>Banco «Mar»</th><th>Banco «Montanha»</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <strong>Capital inicial:</strong> $80\\\\,000\\\\text{ €}$<br>
                                <strong>Taxa de juro anual:</strong> $2{,}3\\\\%$<br>
                                <strong>Período de capitalização:</strong> $5\\\\text{ anos}$<br>
                                <strong>Regime:</strong> Juro simples
                            </td>
                            <td>
                                <strong>Capital inicial:</strong> $85\\\\,000\\\\text{ €}$<br>
                                <strong>Taxa de juro anual:</strong> $1{,}2\\\\%$<br>
                                <strong>Período de capitalização:</strong> $5\\\\text{ anos}$<br>
                                <strong>Regime:</strong> Juro simples
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p><strong>Questão:</strong> Qual será a melhor opção para o Diogo investir o seu dinheiro? Justifica a tua resposta com base no rendimento de juros gerado.</p>
                `,
                imagem: null,
                orientacao: "Compara o ganho em juros nos dois bancos e indica qual é a melhor proposta:",
                valoresCorretos: [9200],
                termosValidos: ["mar", "banco mar", "9200"],
                feedbackErro: "No Banco «Mar» os juros são $80\\\\,000 \\\\times 0{,}023 \\\\times 5 = 9200\\\\text{ €}$, enquanto no Banco «Montanha» são apenas $85\\\\,000 \\\\times 0{,}012 \\\\times 5 = 5100\\\\text{ €}$.",
                pista: "A proposta mais vantajosa é a do Banco «Mar» porque oferece a taxa mais elevada e maior retorno de juros ($9200\\\\text{ €}$ vs $5100\\\\text{ €}$).",
                sucesso: "Excelente análise! A melhor proposta é a do Banco «Mar», pois gera $9200\\\\text{ €}$ de juros contra $5100\\\\text{ €}$ do Banco «Montanha»."
            },
            4: {
                numero: 4,
                bloco: 1,
                enunciado: "Determina o capital inicial de um investimento, sabendo que o capital acumulado, ao fim de 4 anos, foi de $15\\\\,600\\\\text{ €}$, num regime de juros simples, com uma taxa de juro anual de $1{,}5\\\\%$.",
                tabela: null,
                imagem: null,
                orientacao: "Substitui os dados na fórmula $C_a = C_i \\\\times (1 + \\\\frac{r}{100} \\\\times n)$ e isola a incógnita $C_i$:",
                valoresCorretos: [14717, 14716.98, 14716],
                termosValidos: ["14717", "14716", "14716.98", "14716,98", "14 717"],
                feedbackErro: "Atenção: o fator acumulador a 4 anos é $1 + (\\\\frac{1{,}5}{100} \\\\times 4) = 1{,}06$. Deves dividir $15\\\\,600$ por $1{,}06$.",
                pista: "Calcula $C_i = \\\\frac{15\\\\,600}{1{,}06} \\\\approx 14\\\\,717\\\\text{ €}$.",
                sucesso: "Exato! O capital inicial foi de, aproximadamente, $14\\\\,717\\\\text{ €}$ (ou $14\\\\,716{,}98\\\\text{ €}$)."
            },
            5: {
                numero: 5,
                bloco: 2,
                enunciado: "Um casal recebeu uma herança no valor de $57\\\\,000\\\\text{ €}$ e depositou o dinheiro numa conta a prazo em regime de juros simples. Ao fim de $5\\\\text{ anos}$, o capital acumulado foi de $60\\\\,705\\\\text{ €}$. Calcula a taxa de juro anual.",
                tabela: null,
                imagem: null,
                orientacao: "Monta a equação $60\\\\,705 = 57\\\\,000(1 + \\\\frac{r}{100} \\\\times 5)$ ou calcula os juros e determina a taxa $r$:",
                valoresCorretos: [1.3],
                termosValidos: ["1.3", "1,3", "1.3%", "1,3%"],
                feedbackErro: "Os juros gerados são $60\\\\,705 - 57\\\\,000 = 3705\\\\text{ €}$. Na equação: $3705 = 57\\\\,000 \\\\times \\\\frac{r}{100} \\\\times 5 \\\\iff 3705 = 2850r \\\\iff r = \\\\frac{3705}{2850} = 1{,}3\\\\%$.",
                pista: "Divide os juros totais ($3705$) por $2850$ para encontrar a taxa percentual anual.",
                sucesso: "Perfeito! A taxa de juro anual aplicada a este depósito foi de $1{,}3\\\\%$."
            },
            6: {
                numero: 6,
                bloco: 2,
                enunciado: "A Emília e o Lino depositaram $12\\\\,000\\\\text{ €}$ numa conta a prazo, num regime de juro simples. Ao fim de $5\\\\text{ anos}$, o capital acumulado foi de $13\\\\,200\\\\text{ €}$. Determina a taxa de juro anual.",
                tabela: null,
                imagem: null,
                orientacao: "Substitui os dados $C_i = 12\\\\,000$, $C_a = 13\\\\,200$ e $n = 5$ na fórmula e determina o valor de $r$:",
                valoresCorretos: [2],
                termosValidos: ["2", "2%", "2,0", "2.0", "2,0%", "2.0%"],
                feedbackErro: "Os juros totais são $13\\\\,200 - 12\\\\,000 = 1200\\\\text{ €}$. Na equação: $1200 = 12\\\\,000 \\\\times \\\\frac{r}{100} \\\\times 5 \\\\iff 1200 = 600r \\\\iff r = \\\\frac{1200}{600} = 2\\\\%$.",
                pista: "Divide $1200$ por $600$ para obter a taxa percentual de juro anual.",
                sucesso: "Parabéns! Concluíste com sucesso todos os exercícios da Tarefa 7! A taxa de juro anual foi de $2\\\\%$."
            }
        }
    },
    tarefa_08: {
        id: "tarefa_08",
        nome: "Tarefa 8: Juros Compostos",
        exemplos: {
            1: {
                id: 1,
                titulo: "Exemplo 1: Evolução Ano a Ano de Juros Compostos",
                enunciadoGeral: "Supõe que depositavas $650\\\\text{ €}$ numa conta a prazo, num regime de juros compostos, durante três anos. A taxa de juro anual é de $4\\\\%$.",
                passosLista: ['1.1', '1.2', '1.3', '1.4'],
                passos: {
                    '1.1': {
                        numero: 'Passo 1.1',
                        pergunta: "Qual é o valor dos juros no final do 1.º ano?",
                        orientacaoCalculo: "Multiplica o capital inicial ($650\\\\text{ €}$) pela taxa anual decimal ($4\\\\% = 0{,}04$):",
                        valoresCorretos: [26],
                        termosValidos: [
                            "26", "26€", "26 €", "26 euros", "26,00", "26.00", "26,00€", "26,00 €", "26.00€", "26.00 €", "26,0", "26.0", "26 eur", "26 EUR", "26eur", "26EUR",
                            "650*0,04", "650 * 0,04", "650*0.04", "650 * 0.04",
                            "650x0,04", "650 x 0,04", "650x0.04", "650 x 0.04",
                            "650*4%", "650 * 4%", "650x4%", "650 x 4%",
                            "650*4/100", "650 * 4 / 100",
                            "j=26", "j = 26", "j1=26", "j1 = 26", "j_1=26", "j_1 = 26",
                            "vinte e seis", "vinte e seis euros"
                        ],
                        feedbackErro: "Tem atenção: o juro no 1.º ano é $650 \\\\times 0{,}04 = 26\\\\text{ €}$.",
                        pista: "Multiplica $650$ por $0{,}04$ para obter o juro do primeiro ano.",
                        sucesso: "Muito bem! No final do 1.º ano recebes $J_1 = 650 \\\\times 0{,}04 = 26\\\\text{ €}$."
                    },
                    '1.2': {
                        numero: 'Passo 1.2',
                        pergunta: "Qual é o valor do capital acumulado no final do 1.º ano?",
                        orientacaoCalculo: "Soma o juro obtido no 1.º ano ao capital inicial:",
                        valoresCorretos: [676],
                        termosValidos: ["676", "676€", "676 €", "676 euros"],
                        feedbackErro: "Soma o juro de $26\\\\text{ €}$ aos $650\\\\text{ €}$ iniciais: $650 + 26 = 676\\\\text{ €}$.",
                        pista: "O capital acumulado no final do primeiro ano é $C_1 = 650 + 26 = 676\\\\text{ €}$.",
                        sucesso: "Excelente! O capital acumulado no fim do 1.º ano é $C_1 = 676\\\\text{ €}$."
                    },
                    '1.3': {
                        numero: 'Passo 1.3',
                        pergunta: "Qual é o valor dos juros acumulados ao fim de 3 anos?",
                        orientacaoCalculo: "Calcula os juros ano a ano com a capitalização (no 2.º ano sobre $676\\\\text{ €}$ e no 3.º ano sobre $703{,}04\\\\text{ €}$) e soma todos os juros:",
                        valoresCorretos: [81.16],
                        termosValidos: ["81.16", "81,16", "81.16€", "81,16€", "81.16 €", "81,16 €"],
                        feedbackErro: "No 2.º ano o juro é $676 \\\\times 0{,}04 = 27{,}04\\\\text{ €}$ e no 3.º ano é $703{,}04 \\\\times 0{,}04 \\\\approx 28{,}12\\\\text{ €}$. A soma exata dos juros é $26 + 27{,}04 + 28{,}12 = 81{,}16\\\\text{ €}$.",
                        pista: "Soma os juros dos 3 anos: $26 + 27{,}04 + 28{,}12 = 81{,}16\\\\text{ €}$.",
                        sucesso: "Perfeito! O total de juros acumulados ao fim dos 3 anos é exatamente de $81{,}16\\\\text{ €}$."
                    },
                    '1.4': {
                        numero: 'Passo 1.4',
                        pergunta: "Qual é o valor do capital acumulado no final dos 3 anos?",
                        orientacaoCalculo: "Soma o total de juros acumulados ($81{,}16\\\\text{ €}$) ao capital inicial ($650\\\\text{ €}$) ou aplica $C_3 = 650(1{,}04)^3$:",
                        valoresCorretos: [731.16],
                        termosValidos: ["731.16", "731,16", "731.16€", "731,16€", "731.16 €", "731,16 €"],
                        feedbackErro: "O capital acumulado é $C_3 = 650 + 81{,}16 = 731{,}16\\\\text{ €}$.",
                        pista: "Soma o capital inicial com todos os juros: $650 + 81{,}16 = 731{,}16\\\\text{ €}$.",
                        sucesso: "Parabéns! O capital acumulado é $C_3 = 731{,}16\\\\text{ €}$. Concluíste o Exemplo 1 com sucesso. Avança agora para o Exemplo 2!"
                    }
                }
            },
            2: {
                id: 2,
                titulo: "Exemplo 2: Períodos de Capitalização Subanuais e Prazos",
                enunciadoGeral: "Determinação de capital acumulado com capitalização diária e cálculo do número de anos de vigência num depósito a prazo.",
                passosLista: ['2.1', '2.2'],
                passos: {
                    '2.1': {
                        numero: 'Passo 2.1',
                        pergunta: "Determina o capital acumulado ao fim de 11 anos num regime diário ($360\\\\text{ dias}$/ano), com capital inicial de $250\\\\,000\\\\text{ €}$ e taxa de $2{,}5\\\\%$:",
                        orientacaoCalculo: "Aplica $C_a = 250\\\\,000 \\\\times (1 + \\\\frac{2{,}5}{36\\\\,000})^{11 \\\\times 360}$ e introduz o resultado exato arredondado aos cêntimos (duas casas decimais):",
                        valoresCorretos: [329129.53],
                        termosValidos: ["329129.53", "329129,53", "329 129.53", "329 129,53"],
                        feedbackErro: "Atenção ao expoente: $11 \\\\times 360 = 3960$ dias. O capital acumulado exato aos cêntimos é $250\\\\,000 \\\\times (1 + \\\\frac{0{,}025}{360})^{3960} \\\\approx 329\\\\,129{,}53\\\\text{ €}$.",
                        pista: "Calcula a potência diária com expoente $3960$. O resultado com arredondamento aos cêntimos é $329\\\\,129{,}53\\\\text{ €}$.",
                        sucesso: "Muito bem! O capital acumulado ao fim de 11 anos é de $329\\\\,129{,}53\\\\text{ €}$."
                    },
                    '2.2': {
                        numero: 'Passo 2.2',
                        pergunta: "Num regime trimestral a $3{,}2\\\\%$, com $C_0 = 9830\\\\text{ €}$ e $C_a = 10\\\\,477{,}02\\\\text{ €}$, quantos anos ($n$) esteve o depósito em vigor?",
                        orientacaoCalculo: "Monta a equação $10\\\\,477{,}02 = 9830(1{,}008)^{4n}$ e descobre o número inteiro de anos ($n$):",
                        valoresCorretos: [2],
                        termosValidos: ["2", "2 anos", "n=2"],
                        feedbackErro: "Confere as potências: $(1{,}008)^{4 \\\\times 2} = (1{,}008)^8 \\\\approx 1{,}06582$. Como $\\\\frac{10\\\\,477{,}02}{9830} \\\\approx 1{,}06582$, o depósito esteve ativo durante 2 anos.",
                        pista: "Testa os anos na equação: para $n = 2$ obténs exatamente $(1{,}008)^8 = 1{,}06582$.",
                        sucesso: "Perfeito! O depósito a prazo esteve em vigor durante $2\\\\text{ anos}$. Concluíste o Exemplo 2 com sucesso e desbloqueaste os Exercícios 1 a 6 da Tarefa 8!"
                    }
                }
            }
        },
        exercicios: {
            1: {
                numero: 1,
                bloco: 1,
                enunciado: "Tendo em conta o primeiro exercício resolvido do Exemplo 2 (onde $C_i = 250\\\\,000\\\\text{ €}$ e a taxa anual é de $2{,}5\\\\%$), determina o valor do capital acumulado durante um período de $10\\\\text{ anos}$, sabendo que as capitalizações são mensais.",
                tabela: null,
                imagem: null,
                orientacao: "Desenvolve no teu caderno a fórmula $C_a = 250\\\\,000 \\\\times (1 + \\\\frac{2{,}5}{1200})^{120}$ e fotografa os cálculos:",
                valoresCorretos: [320922.89],
                termosValidos: ["320922.89", "320922,89"],
                feedbackErro: "Confere os cálculos: com $k = 12$ meses e $n = 10$ anos, o expoente é $120$. $C_a = 250\\\\,000(1 + \\\\frac{0{,}025}{12})^{120} \\\\approx 320\\\\,922{,}89\\\\text{ €}$.",
                pista: "O capital acumulado ao fim de 10 anos com capitalizações mensais é de exatamente $320\\\\,922{,}89\\\\text{ €}$.",
                sucesso: "Excelente resolução! O capital acumulado ao fim de 10 anos é de $320\\\\,922{,}89\\\\text{ €}$."
            },
            2: {
                numero: 2,
                bloco: 1,
                enunciado: "A Cátia investiu um determinado capital numa conta a prazo, em regime de juros compostos semestrais, a uma taxa de juro anual de $1{,}06\\\\%$. No final dos 10 anos obteve $136\\\\,038\\\\text{ €}$. Qual foi o capital inicial investido?",
                tabela: null,
                imagem: null,
                orientacao: "Substitui $C_a = 136\\\\,038$, $r = 1{,}06\\\\%$, $n = 10$, $k = 2$ na fórmula e determina $C_i$:",
                valoresCorretos: [122391.36],
                termosValidos: ["122391.36", "122391,36"],
                feedbackErro: "Atenção: como as capitalizações são semestrais ($k=2$), o número total de períodos é $20$. $136\\\\,038 = C_i(1 + \\\\frac{0{,}0106}{2})^{20} \\\\iff C_i = \\\\frac{136\\\\,038}{1{,}1115} \\\\approx 122\\\\,391{,}36\\\\text{ €}$.",
                pista: "Divide $136\\\\,038$ por $(1{,}0053)^{20} \\\\approx 1{,}111504$ para obteres o capital inicial com cêntimos ($122\\\\,391{,}36\\\\text{ €}$).",
                sucesso: "Muito bem! O capital inicial investido pela Cátia foi de exatamente $122\\\\,391{,}36\\\\text{ €}$."
            },
            3: {
                numero: 3,
                bloco: 1,
                enunciado: "Em agosto de 2023, a Mariana vendeu o seu carro por $12\\\\,500\\\\text{ €}$. Depositou o dinheiro numa conta a prazo, em regime de juros compostos, com uma taxa de juro anual de $1{,}4\\\\%$.<br><strong>3.1</strong> Será que ao fim de 4 anos o capital acumulado lhe permite comprar um carro no valor de $13\\\\,500\\\\text{ €}$? Caso não seja possível, determina o valor que deveria ter sido depositado inicialmente para conseguir comprar este carro.<br><strong>3.2</strong> Se a capitalização dos juros fosse mensal, em vez de anual, a Mariana teria mais dinheiro acumulado ao fim de 4 anos? Justifica a tua resposta.",
                tabela: null,
                imagem: null,
                orientacao: "Resolve as duas alíneas no caderno com as comparações de valores:",
                valoresCorretos: [13214.84, 12770.38, 12770, 13219.54],
                termosValidos: ["13214.84", "13214,84", "12770.38", "12770,38", "12770", "13219.54", "13219,54"],
                feedbackErro: "Para 3.1: $C_a = 12\\\\,500(1{,}014)^4 \\\\approx 13\\\\,214{,}84\\\\text{ €} < 13\\\\,500\\\\text{ €}$ (insuficiente). Precisaria de $C_i = \\\\frac{13\\\\,500}{(1{,}014)^4} \\\\approx 12\\\\,770{,}38\\\\text{ €}$. Para 3.2: mensal rende $13\\\\,219{,}54\\\\text{ €}$, logo teria mais $4{,}70\\\\text{ €}$.",
                pista: "O valor acumulado de $13\\\\,214{,}84\\\\text{ €}$ é insuficiente para $13\\\\,500\\\\text{ €}$. Deveria ter depositado $12\\\\,770{,}38\\\\text{ €}$. Na capitalização mensal teria mais dinheiro.",
                sucesso: "Excelente análise! Em 3.1 o valor é insuficiente ($13\\\\,214{,}84\\\\text{ €}$) e seriam necessários $12\\\\,770{,}38\\\\text{ €}$. Em 3.2, a capitalização mensal rende mais ($13\\\\,219{,}54\\\\text{ €}$)."
            },
            4: {
                numero: 4,
                bloco: 1,
                enunciado: "Ao fim de 7 anos, num regime de capitalização trimestral de juros compostos, obteve-se um capital final de $77\\\\,660{,}84\\\\text{ €}$. Sabendo que a taxa de juro anual foi de $3\\\\%$, determina o valor do capital inicial.",
                tabela: null,
                imagem: null,
                orientacao: "Aplica $77\\\\,660{,}84 = C_i(1 + \\\\frac{3}{400})^{28}$ e isola o valor de $C_i$:",
                valoresCorretos: [63000],
                termosValidos: ["63000", "63 000", "63000€", "63 000€"],
                feedbackErro: "Atenção aos períodos: $7 \\\\times 4 = 28$ trimestres. $C_i = \\\\frac{77\\\\,660{,}84}{(1{,}0075)^{28}} = \\\\frac{77\\\\,660{,}84}{1{,}232712} = 63\\\\,000\\\\text{ €}$.",
                pista: "Divide $77\\\\,660{,}84$ por $(1{,}0075)^{28} \\\\approx 1{,}232712$ para obter exatamente o capital inicial.",
                sucesso: "Exato! O capital inicial foi rigorosamente de $63\\\\,000\\\\text{ €}$."
            },
            5: {
                numero: 5,
                bloco: 2,
                enunciado: "O Marco vendeu uma casa por $235\\\\,000\\\\text{ €}$ e resolveu investir numa aplicação financeira a 10 anos. Consultou dois bancos:",
                tabela: `
                <table>
                    <thead>
                        <tr><th>Banco «Mar»</th><th>Banco «Montanha»</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <strong>Capital inicial:</strong> $235\\\\,000\\\\text{ €}$<br>
                                <strong>Taxa de juro anual:</strong> $3{,}8\\\\%$<br>
                                <strong>Período de capitalização:</strong> $10\\\\text{ anos}$<br>
                                <strong>Regime:</strong> Juro simples
                            </td>
                            <td>
                                <strong>Capital inicial:</strong> $235\\\\,000\\\\text{ €}$<br>
                                <strong>Taxa de juro anual:</strong> $3{,}4\\\\%$<br>
                                <strong>Período de capitalização:</strong> $10\\\\text{ anos}$<br>
                                <strong>Regime:</strong> Juro composto
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p><strong>Questão:</strong> O que sugeres ao Marco? Fundamenta a tua resposta com base no capital acumulado em cada banco.</p>
                `,
                imagem: null,
                orientacao: "Calcula o capital final nos dois bancos e formula a tua recomendação:",
                valoresCorretos: [328301.79, 324300],
                termosValidos: ["montanha", "banco montanha", "328301.79", "328 301.79", "328301,79", "324300"],
                feedbackErro: "No Banco «Mar» (simples): $235\\\\,000(1 + 0{,}038 \\\\times 10) = 324\\\\,300\\\\text{ €}$. No Banco «Montanha» (composto): $235\\\\,000(1{,}034)^{10} \\\\approx 328\\\\,301{,}79\\\\text{ €}$. O Banco «Montanha» é superior.",
                pista: "A proposta do Banco «Montanha» é mais vantajosa porque acumula $328\\\\,301{,}79\\\\text{ €}$, superando o Banco «Mar» em $4001{,}79\\\\text{ €}$.",
                sucesso: "Excelente análise financeira! O Marco deve optar pelo Banco «Montanha», pois gera $328\\\\,301{,}79\\\\text{ €}$ contra $324\\\\,300\\\\text{ €}$ do Banco «Mar»."
            },
            6: {
                numero: 6,
                bloco: 2,
                enunciado: "A Cláudia vendeu um carro por $8300\\\\text{ €}$ e depositou esse dinheiro numa conta a prazo, em regime de juros compostos, por um período de 5 anos. A taxa de juro anual foi de $1{,}8\\\\%$.<br><strong>6.1</strong> Determina o valor do capital acumulado ao fim dos 5 anos se as capitalizações forem semestrais.<br><strong>6.2</strong> Determina o valor do capital acumulado se as capitalizações forem mensais. O capital acumulado seria igual ao obtido em 6.1?",
                tabela: null,
                imagem: null,
                orientacao: "Calcula os dois montantes com $k=2$ e $k=12$ e compara os resultados:",
                valoresCorretos: [9077.63, 9080.63],
                termosValidos: ["9077.63", "9077,63", "9080.63", "9080,63"],
                feedbackErro: "Semestral: $8300(1 + \\\\frac{0{,}018}{2})^{10} \\\\approx 9077{,}63\\\\text{ €}$. Mensal: $8300(1 + \\\\frac{0{,}018}{12})^{60} \\\\approx 9080{,}63\\\\text{ €}$. O regime mensal rende mais $3{,}00\\\\text{ €}$.",
                pista: "Em 6.1 obtém-se $9077{,}63\\\\text{ €}$ e em 6.2 obtém-se $9080{,}63\\\\text{ €}$. Não são iguais; o regime mensal é ligeiramente superior.",
                sucesso: "Perfeito! Capital semestral: $9077{,}63\\\\text{ €}$; Capital mensal: $9080{,}63\\\\text{ €}$. O regime mensal rende mais $3{,}00\\\\text{ €}$ devido à frequência de capitalização."
            }
        }
    }
};

function getDadosTarefa() {
    return dadosTarefas[fichaAtivaId] || dadosTarefas['tarefa_07'];
}

function normalizarTextoResposta(txt) {
    if (!txt) return '';
    let t = String(txt).toLowerCase().trim();
    t = t.replace(/[\\$]/g, '');
    t = t.replace(/\\\\text\\s*\\{[^}]*\\}/g, ' ');
    t = t.replace(/\\\\times/g, '*');
    t = t.replace(/\\\\cdot/g, '*');
    t = t.replace(/\\\\div/g, '/');
    t = t.replace(/\\\\frac\\{([^}]+)\\}\\{([^}]+)\\}/g, '($1)/($2)');
    const extenso = {
        'vinte e seis': '26',
        'setenta e oito': '78',
        'setecentos e vinte e oito': '728',
        'treze mil e trinta e oito': '13038'
    };
    for (const [k, v] of Object.entries(extenso)) {
        t = t.replace(new RegExp('\\\\b' + k + '\\\\b', 'g'), v);
    }
    return t;
}

function avaliarAritmetica(expr) {
    try {
        if (!expr) return null;
        let e = expr.replace(/,/g, '.');
        e = e.replace(/x/gi, '*');
        e = e.replace(/·/g, '*');
        e = e.replace(/:/g, '/');
        e = e.replace(/(\\d+(?:\\.\\d+)?)\\s*%/g, '($1/100)');
        if (!/^[\\d\\s\\+\\-\\*/()\\.]+$/.test(e)) {
            return null;
        }
        const val = Function('"use strict"; return (' + e + ')')();
        if (typeof val === 'number' && !isNaN(val) && isFinite(val)) {
            return val;
        }
    } catch (err) {}
    return null;
}

function verificarAcerto(respostaTexto, valoresEsperados, termosEsperados) {
    if (!respostaTexto) return false;
    let txt = normalizarTextoResposta(respostaTexto);
    txt = txt.replace(/\\s+/g, " ");

    // 1. Verificar termos textuais esperados (ex.: "mar", "banco mar", "montanha", "2 anos", "1,06%", etc.)
    if (termosEsperados && Array.isArray(termosEsperados)) {
        for (let t of termosEsperados) {
            const termo = normalizarTextoResposta(t);
            if (!termo) continue;
            if (txt.includes(termo)) return true;
        }
    }

    if (!valoresEsperados || valoresEsperados.length === 0) return false;

    // 2. Extração de valores numéricos e monetários
    const numerosEncontrados = [];

    // 2.1 Avaliação de expressões aritméticas (ex: 650 * 0,04 ou 26 * 3 ou J = 650 * 0,04 = 26)
    const partesIgual = txt.split('=');
    for (const parte of partesIgual) {
        const parteLimpa = parte.replace(/^[a-z_0-9\\s]+:/i, '').replace(/^[jcnr]\\s*(\\d+)?/i, '').trim();
        const valCalc = avaliarAritmetica(parteLimpa);
        if (valCalc !== null) {
            numerosEncontrados.push(valCalc);
        }
    }
    const valExprTotal = avaliarAritmetica(txt.replace(/^[a-z_0-9\\s]+=/i, '').trim());
    if (valExprTotal !== null) {
        numerosEncontrados.push(valExprTotal);
    }

    // 2.2 Padrão por extenso em euros: "7 euros e 20", "7 euros e 20 cêntimos", "7€ e 20 cts"
    const regexEurosCentimos = /(\\d+)\\s*(?:euros?|€|eur)\\s*(?:e\\s*)?(\\d{1,2})\\s*(?:cêntimos?|centimos?|cents?|cts)?/gi;
    let matchEC;
    while ((matchEC = regexEurosCentimos.exec(txt)) !== null) {
        const parteEuros = parseInt(matchEC[1], 10);
        let centStr = matchEC[2];
        if (centStr.length === 1) centStr += "0";
        const parteCentimos = parseInt(centStr, 10);
        numerosEncontrados.push(parteEuros + (parteCentimos / 100));
    }

    // 2.3 Normalizar separadores de milhar (ex.: "320 922,89" ou "320.922,89" -> "320922,89")
    let txtNormalizado = txt.replace(/(\\d{1,3})[\\. ](\\d{3}[\\. ]\\d{3})/g, "$1$2");
    txtNormalizado = txtNormalizado.replace(/(\\d{1,3})[\\. ](\\d{3})/g, "$1$2");

    // 2.4 Extrair números com separador decimal (vírgula ou ponto) ou inteiros
    const regexNumeros = /(?:^|[^\\d,\\.])(\\d+(?:[\\.,]\\d+)?)(?:[^\\d,\\.]|$)/g;
    let matchNum;
    while ((matchNum = regexNumeros.exec(txtNormalizado)) !== null) {
        const valFloat = parseFloat(matchNum[1].replace(",", "."));
        if (!isNaN(valFloat)) {
            numerosEncontrados.push(valFloat);
        }
    }

    const regexDireto = /\\d+(?:[\\.,]\\d+)?/g;
    let matchD;
    while ((matchD = regexDireto.exec(txtNormalizado)) !== null) {
        const valFloat = parseFloat(matchD[0].replace(",", "."));
        if (!isNaN(valFloat)) {
            numerosEncontrados.push(valFloat);
        }
    }

    // 3. Comparação com rigor aos cêntimos (2 casas decimais / centésimas)
    for (let num of numerosEncontrados) {
        const centimosAluno = Math.round(num * 100);
        for (let v of valoresEsperados) {
            const centimosEsperado = Math.round(v * 100);
            if (centimosAluno === centimosEsperado) {
                return true;
            }
            if (Math.abs(num - v) < 0.0001) {
                return true;
            }
            if (Math.abs(num * 100 - v) < 0.0001 || Math.abs(num - v * 100) < 0.0001) {
                return true;
            }
        }
    }

    return false;
}

function carregarProgressoAluno() {
    fetch(`/api/progresso?aluno_id=${alunoAtivoId}&ficha_id=${fichaAtivaId}`)
        .then(r => r.json())
        .then(dados => {
            exerciciosValidados = new Set(dados.exercicios_validados || []);
            passosValidados = new Set(dados.passos_validados || []);
            exemplo1Concluido = dados.exemplo1_concluido || false;
            exemplo2Concluido = dados.exemplo2_concluido || false;

            // Se estiver num exercício e os pré-requisitos não estiverem concluídos, bloqueia
            const temExemplo2 = !!(getDadosTarefa().exemplos && getDadosTarefa().exemplos[2]);
            if (estadoAtual.fase === 'exercicio') {
                if (!temExemplo2) {
                    if (!exemplo1Concluido) {
                        estadoAtual.fase = 'bloqueado';
                        estadoAtual.bloqueioMotivo = 1;
                    }
                } else if (fichaAtivaId === 'tarefa_08') {
                    if (!exemplo1Concluido || !exemplo2Concluido) {
                        estadoAtual.fase = 'bloqueado';
                        estadoAtual.bloqueioMotivo = (!exemplo1Concluido) ? 1 : 2;
                    }
                } else {
                    if ((estadoAtual.exercicioId >= 1 && estadoAtual.exercicioId <= 4) && !exemplo1Concluido) {
                        estadoAtual.fase = 'bloqueado';
                        estadoAtual.bloqueioMotivo = 1;
                    } else if ((estadoAtual.exercicioId === 5 || estadoAtual.exercicioId === 6) && !exemplo2Concluido) {
                        estadoAtual.fase = 'bloqueado';
                        estadoAtual.bloqueioMotivo = 2;
                    }
                }
            } else if (estadoAtual.fase === 'exemplo') {
                const ex = getDadosTarefa().exemplos[estadoAtual.exemploId];
                if (ex) {
                    let primeiroNaoConcluido = 0;
                    for (let i = 0; i < ex.passosLista.length; i++) {
                        const pKey = ex.passosLista[i];
                        if (passosValidados.has(`${estadoAtual.exemploId}_${pKey}`)) {
                            primeiroNaoConcluido = i + 1;
                        } else {
                            primeiroNaoConcluido = i;
                            break;
                        }
                    }
                    if (primeiroNaoConcluido < ex.passosLista.length) {
                        estadoAtual.passoIndex = primeiroNaoConcluido;
                    }
                }
            }

            atualizarBarraNav();
            renderizarTela();
        });
}

function trocarTarefa(novaFichaId) {
    fichaAtivaId = novaFichaId;
    fichaDocenteId = novaFichaId;
    const selTarefa = document.getElementById('sel-tarefa');
    if (selTarefa) selTarefa.value = fichaAtivaId;
    const selDocente = document.getElementById('sel-tarefa-docente');
    if (selDocente) selDocente.value = fichaDocenteId;

    estadoAtual.fase = 'exemplo';
    estadoAtual.exemploId = 1;
    estadoAtual.passoIndex = 0;
    estadoAtual.passosLista = getDadosTarefa().exemplos[1].passosLista;
    estadoAtual.exercicioId = 1;
    timestampInicioPergunta = Date.now();

    carregarProgressoAluno();
    carregarDocente();
}

function selecionarTarefaDocente(novaFichaId) {
    fichaDocenteId = novaFichaId;
    const selDocente = document.getElementById('sel-tarefa-docente');
    if (selDocente) selDocente.value = fichaDocenteId;
    carregarDocente();
}

function trocarAluno(novoId) {
    alunoAtivoId = parseInt(novoId);
    alunoDocenteId = alunoAtivoId;
    const selDocente = document.getElementById('sel-aluno-docente');
    if (selDocente) selDocente.value = alunoDocenteId;
    const selAluno = document.getElementById('sel-aluno');
    if (selAluno) selAluno.value = alunoAtivoId;
    
    estadoAtual.fase = 'exemplo';
    estadoAtual.exemploId = 1;
    estadoAtual.passoIndex = 0;
    estadoAtual.passosLista = getDadosTarefa().exemplos[1].passosLista;
    estadoAtual.exercicioId = 1;
    timestampInicioPergunta = Date.now();
    carregarProgressoAluno();
    carregarDocente();
}

function atualizarBarraNav() {
    const bar = document.getElementById('nav-pills-bar');
    const badgeContador = document.getElementById('badge-contador-concluidos');
    const caixaCelebracao = document.getElementById('caixa-celebracao-global');

    let html = '';
    const dados = getDadosTarefa();
    const temExemplo2 = !!(dados.exemplos && dados.exemplos[2]);
    const numExercicios = Object.keys(dados.exercicios || {}).length;

    if (!temExemplo2) {
        // Tarefas 4, 5, 6: Exemplo 1 guiado -> desbloqueia todos os exercícios (1 a numExercicios)
        const ex1Ativo = (estadoAtual.fase === 'exemplo' && estadoAtual.exemploId === 1);
        const ex1Classe = `nav-pill ${ex1Ativo ? 'active' : ''} ${exemplo1Concluido ? 'completed' : ''}`;
        html += `<div class="${ex1Classe}" onclick="navegarParaItem('exemplo', 1)">📘 Exemplo 1 ${exemplo1Concluido ? '✓' : ''}</div>`;
        html += `<span style="border-right: 2px solid #cbd5e1; margin: 0 4px;"></span>`;

        for (let i = 1; i <= numExercicios; i++) {
            const isAtivo = (estadoAtual.fase === 'exercicio' && estadoAtual.exercicioId === i);
            const isVal = exerciciosValidados.has(i);
            const isLocked = !exemplo1Concluido;
            const classe = `nav-pill ${isAtivo ? 'active' : ''} ${isVal ? 'completed' : ''} ${isLocked ? 'locked' : ''}`;
            const icone = isVal ? '✓' : (isLocked ? '🔒' : '');
            html += `<div class="${classe}" onclick="navegarParaItem('exercicio', ${i})">Ex. ${i} ${icone}</div>`;
        }
    } else if (fichaAtivaId === 'tarefa_08') {
        // Tarefa 8: Exemplo 1 e Exemplo 2 sequenciais; Exercícios 1 a 6 desbloqueados apenas após o Exemplo 2
        const ex1Ativo = (estadoAtual.fase === 'exemplo' && estadoAtual.exemploId === 1);
        const ex1Classe = `nav-pill ${ex1Ativo ? 'active' : ''} ${exemplo1Concluido ? 'completed' : ''}`;
        html += `<div class="${ex1Classe}" onclick="navegarParaItem('exemplo', 1)">📘 Exemplo 1 ${exemplo1Concluido ? '✓' : ''}</div>`;

        const ex2Ativo = (estadoAtual.fase === 'exemplo' && estadoAtual.exemploId === 2);
        const ex2Classe = `nav-pill ${ex2Ativo ? 'active' : ''} ${exemplo2Concluido ? 'completed' : ''}`;
        html += `<div class="${ex2Classe}" onclick="navegarParaItem('exemplo', 2)">📘 Exemplo 2 ${exemplo2Concluido ? '✓' : ''}</div>`;

        html += `<span style="border-right: 2px solid #cbd5e1; margin: 0 4px;"></span>`;

        const todosExemplosConcluidos = (exemplo1Concluido && exemplo2Concluido);
        for (let i = 1; i <= 6; i++) {
            const isAtivo = (estadoAtual.fase === 'exercicio' && estadoAtual.exercicioId === i);
            const isVal = exerciciosValidados.has(i);
            const isLocked = !todosExemplosConcluidos;
            const classe = `nav-pill ${isAtivo ? 'active' : ''} ${isVal ? 'completed' : ''} ${isLocked ? 'locked' : ''}`;
            const icone = isVal ? '✓' : (isLocked ? '🔒' : '');
            html += `<div class="${classe}" onclick="navegarParaItem('exercicio', ${i})">Ex. ${i} ${icone}</div>`;
        }
    } else {
        // Tarefa 7 (original): Bloco 1 (Exemplo 1 -> Ex 1 a 4) e Bloco 2 (Exemplo 2 -> Ex 5 e 6)
        const ex1Ativo = (estadoAtual.fase === 'exemplo' && estadoAtual.exemploId === 1);
        const ex1Classe = `nav-pill ${ex1Ativo ? 'active' : ''} ${exemplo1Concluido ? 'completed' : ''}`;
        html += `<div class="${ex1Classe}" onclick="navegarParaItem('exemplo', 1)">📘 Exemplo 1 ${exemplo1Concluido ? '✓' : ''}</div>`;

        for (let i = 1; i <= 4; i++) {
            const isAtivo = (estadoAtual.fase === 'exercicio' && estadoAtual.exercicioId === i);
            const isVal = exerciciosValidados.has(i);
            const isLocked = !exemplo1Concluido;
            const classe = `nav-pill ${isAtivo ? 'active' : ''} ${isVal ? 'completed' : ''} ${isLocked ? 'locked' : ''}`;
            const icone = isVal ? '✓' : (isLocked ? '🔒' : '');
            html += `<div class="${classe}" onclick="navegarParaItem('exercicio', ${i})">Ex. ${i} ${icone}</div>`;
        }

        const ex2Ativo = (estadoAtual.fase === 'exemplo' && estadoAtual.exemploId === 2);
        const ex2Classe = `nav-pill ${ex2Ativo ? 'active' : ''} ${exemplo2Concluido ? 'completed' : ''}`;
        html += `<div class="${ex2Classe}" onclick="navegarParaItem('exemplo', 2)">📘 Exemplo 2 ${exemplo2Concluido ? '✓' : ''}</div>`;

        for (let i = 5; i <= 6; i++) {
            const isAtivo = (estadoAtual.fase === 'exercicio' && estadoAtual.exercicioId === i);
            const isVal = exerciciosValidados.has(i);
            const isLocked = !exemplo2Concluido;
            const classe = `nav-pill ${isAtivo ? 'active' : ''} ${isVal ? 'completed' : ''} ${isLocked ? 'locked' : ''}`;
            const icone = isVal ? '✓' : (isLocked ? '🔒' : '');
            html += `<div class="${classe}" onclick="navegarParaItem('exercicio', ${i})">Ex. ${i} ${icone}</div>`;
        }
    }

    bar.innerHTML = html;

    const totalValidados = exerciciosValidados.size;
    badgeContador.innerText = `${totalValidados} de ${numExercicios} Exercícios Validados`;

    const todosConcluidos = (totalValidados === numExercicios) && exemplo1Concluido && (!temExemplo2 || exemplo2Concluido);
    if (todosConcluidos) {
        caixaCelebracao.innerHTML = `
            <h3 style="margin: 0 0 6px 0; color: #065f46; font-size: 18px;">🏆 Parabéns! Todos os exercícios estão validados a verde!</h3>
            <p style="margin: 0; font-size: 14px; color: #047857;">
                Completaste os exemplos e todos os ${numExercicios} exercícios de aplicação da <strong>${getDadosTarefa().nome}</strong> com sucesso.
            </p>
        `;
        caixaCelebracao.style.display = 'block';
    } else {
        caixaCelebracao.style.display = 'none';
    }
}

function navegarParaItem(tipo, id) {
    if (tipo === 'exemplo') {
        estadoAtual.fase = 'exemplo';
        estadoAtual.exemploId = id;
        estadoAtual.passosLista = getDadosTarefa().exemplos[id].passosLista;
        
        let primeiroNaoConcluido = 0;
        for (let i = 0; i < estadoAtual.passosLista.length; i++) {
            const pKey = estadoAtual.passosLista[i];
            if (passosValidados.has(`${id}_${pKey}`)) {
                primeiroNaoConcluido = i + 1;
            } else {
                primeiroNaoConcluido = i;
                break;
            }
        }
        if (primeiroNaoConcluido >= estadoAtual.passosLista.length) {
            estadoAtual.passoIndex = estadoAtual.passosLista.length - 1;
        } else {
            estadoAtual.passoIndex = primeiroNaoConcluido;
        }
    } else {
        const temEx2 = !!(getDadosTarefa().exemplos && getDadosTarefa().exemplos[2]);
        if (!temEx2) {
            if (!exemplo1Concluido) {
                estadoAtual.fase = 'bloqueado';
                estadoAtual.bloqueioMotivo = 1;
                estadoAtual.exercicioId = id;
                atualizarBarraNav();
                renderizarTela();
                return;
            }
        } else if (fichaAtivaId === 'tarefa_08') {
            const todosExemplosConcluidos = (exemplo1Concluido && exemplo2Concluido);
            if (!todosExemplosConcluidos) {
                estadoAtual.fase = 'bloqueado';
                estadoAtual.bloqueioMotivo = (!exemplo1Concluido) ? 1 : 2;
                estadoAtual.exercicioId = id;
                atualizarBarraNav();
                renderizarTela();
                return;
            }
        } else {
            if ((id >= 1 && id <= 4) && !exemplo1Concluido) {
                estadoAtual.fase = 'bloqueado';
                estadoAtual.bloqueioMotivo = 1;
                estadoAtual.exercicioId = id;
                atualizarBarraNav();
                renderizarTela();
                return;
            }
            if ((id === 5 || id === 6) && !exemplo2Concluido) {
                estadoAtual.fase = 'bloqueado';
                estadoAtual.bloqueioMotivo = 2;
                estadoAtual.exercicioId = id;
                atualizarBarraNav();
                renderizarTela();
                return;
            }
        }
        estadoAtual.fase = 'exercicio';
        estadoAtual.exercicioId = id;
    }
    atualizarBarraNav();
    renderizarTela();
}

function renderizarTela() {
    timestampInicioPergunta = Date.now();
    const container = document.getElementById('conteudo-enunciado');
    const areaResp = document.getElementById('area-resposta');
    const feedbackArea = document.getElementById('feedback-area');
    feedbackArea.innerHTML = '';

    atualizarBarraNav();

    if (estadoAtual.fase === 'bloqueado') {
        const temEx2 = !!(getDadosTarefa().exemplos && getDadosTarefa().exemplos[2]);
        if (!temEx2) {
            container.innerHTML = `
                <div class="feedback-box feedback-locked" style="margin-top: 0;">
                    <h3 style="margin: 0 0 8px 0; color: #92400e;">🔒 Exercício ${estadoAtual.exercicioId} Bloqueado</h3>
                    <p style="margin: 0 0 14px 0; font-size: 14px;">
                        Para resolveres os Exercícios de Aplicação da <strong>${getDadosTarefa().nome}</strong>, deves primeiro concluir com sucesso todos os passos guiados do <strong>Exemplo 1</strong>.
                    </p>
                    <button class="btn btn-warning" onclick="navegarParaItem('exemplo', 1)">
                        📘 Ir para o Exemplo 1 ➔
                    </button>
                </div>
            `;
        } else if (fichaAtivaId === 'tarefa_08') {
            const pendenteId = (!exemplo1Concluido) ? 1 : 2;
            container.innerHTML = `
                <div class="feedback-box feedback-locked" style="margin-top: 0;">
                    <h3 style="margin: 0 0 8px 0; color: #92400e;">🔒 Exercício ${estadoAtual.exercicioId} Bloqueado</h3>
                    <p style="margin: 0 0 14px 0; font-size: 14px;">
                        Para desbloqueares os <strong>Exercícios de Aplicação (1 a 6)</strong> na Tarefa 8, deves primeiro concluir com sucesso todos os passos guiados do <strong>Exemplo 1</strong> e do <strong>Exemplo 2</strong>.
                        ${!exemplo1Concluido ? '<br>Tens ainda passos pendentes no <strong>Exemplo 1</strong>.' : '<br>O Exemplo 1 está concluído! Conclui agora o <strong>Exemplo 2</strong> para abrir todos os exercícios.'}
                    </p>
                    <button class="btn btn-warning" onclick="navegarParaItem('exemplo', ${pendenteId})">
                        📘 Ir para o Exemplo ${pendenteId} ➔
                    </button>
                </div>
            `;
        } else {
            if (estadoAtual.bloqueioMotivo === 1) {
                container.innerHTML = `
                    <div class="feedback-box feedback-locked" style="margin-top: 0;">
                        <h3 style="margin: 0 0 8px 0; color: #92400e;">🔒 Exercício ${estadoAtual.exercicioId} Bloqueado</h3>
                        <p style="margin: 0 0 14px 0; font-size: 14px;">
                            Para resolveres os <strong>Exercícios 1, 2, 3 e 4</strong>, deves primeiro concluir com sucesso todos os passos do <strong>Exemplo 1</strong>.
                        </p>
                        <button class="btn btn-warning" onclick="navegarParaItem('exemplo', 1)">
                            📘 Ir para o Exemplo 1 (Cálculo de Juros e Capital) ➔
                        </button>
                    </div>
                `;
            } else {
                container.innerHTML = `
                    <div class="feedback-box feedback-locked" style="margin-top: 0;">
                        <h3 style="margin: 0 0 8px 0; color: #92400e;">🔒 Exercício ${estadoAtual.exercicioId} Bloqueado</h3>
                        <p style="margin: 0 0 14px 0; font-size: 14px;">
                            Os <strong>Exercícios 5 e 6</strong> exigem a determinação de taxas de juro anuais.
                            Por motivos pedagógicos, não é permitido resolver o Exercício ${estadoAtual.exercicioId} antes de concluíres o <strong>Exemplo 2</strong>.
                        </p>
                        <button class="btn btn-warning" onclick="navegarParaItem('exemplo', 2)">
                            📘 Ir para o Exemplo 2 (Determinação da Taxa de Juro) ➔
                        </button>
                    </div>
                `;
            }
        }
        areaResp.innerHTML = '';
        return;
    }

    if (estadoAtual.fase === 'exemplo') {
        const ex = getDadosTarefa().exemplos[estadoAtual.exemploId];
        estadoAtual.passosLista = ex.passosLista;
        const passoKey = estadoAtual.passosLista[estadoAtual.passoIndex];
        const passo = ex.passos[passoKey];
        const passoJaFeito = passosValidados.has(`${estadoAtual.exemploId}_${passoKey}`);

        let passosNavHtml = '<div style="display: flex; gap: 8px; margin: 12px 0 6px 0; flex-wrap: wrap;">';
        for (let i = 0; i < ex.passosLista.length; i++) {
            const pKey = ex.passosLista[i];
            const pDone = passosValidados.has(`${estadoAtual.exemploId}_${pKey}`);
            const pAtivo = (estadoAtual.passoIndex === i);
            const pBloqueado = (i > 0 && !passosValidados.has(`${estadoAtual.exemploId}_${ex.passosLista[i-1]}`) && !pDone);
            const bgCor = pAtivo ? 'var(--primary)' : (pDone ? '#def7ec' : '#f1f5f9');
            const txtCor = pAtivo ? '#ffffff' : (pDone ? '#03543f' : '#475569');
            const bordaCor = pAtivo ? 'var(--primary)' : (pDone ? '#31c48d' : '#cbd5e1');
            passosNavHtml += `<button type="button" class="btn" style="padding: 5px 12px; font-size: 13px; margin: 0; background: ${bgCor}; color: ${txtCor}; border: 1px solid ${bordaCor}; cursor: ${pBloqueado ? 'not-allowed' : 'pointer'};" ${pBloqueado ? 'disabled' : ''} onclick="selecionarPassoExemplo(${i})">Passo ${pKey} ${pDone ? '✓' : ''}</button>`;
        }
        passosNavHtml += '</div>';

        container.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #1e3a8a;">${ex.titulo}</h3>
                <span style="font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 6px; ${passoJaFeito ? 'background: #def7ec; color: #047857;' : 'background: #f1f5f9; color: #475569;'}">
                    ${passo.numero}: ${passoJaFeito ? '✓ Concluído' : '⏳ Por Responder'}
                </span>
            </div>
            ${passosNavHtml}
            <p style="font-size: 15px; margin-top: 10px; color: #334155;">${formatarTextoMatematico(ex.enunciadoGeral)}</p>
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 14px 16px; border-radius: 8px; margin: 14px 0;">
                <strong style="color: #1e40af;">${passo.numero}:</strong> ${formatarTextoMatematico(passo.pergunta)}
            </div>
        `;

        if (passoJaFeito) {
            const isUltimoPasso = (estadoAtual.passoIndex === estadoAtual.passosLista.length - 1);
            areaResp.innerHTML = `
                <div class="feedback-box feedback-success" style="margin-top: 10px;">
                    <strong>✓ Este passo já foi concluído com sucesso!</strong>
                    ${!isUltimoPasso ? `
                        <div style="margin-top: 12px;">
                            <button class="btn btn-success" onclick="avancarPassoSeguinte()">
                                Avançar para o Passo ${estadoAtual.passosLista[estadoAtual.passoIndex + 1]} ➔
                            </button>
                        </div>
                    ` : (fichaAtivaId === 'tarefa_08' ? (estadoAtual.exemploId === 1 ? `
                        <div style="margin-top: 12px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exemplo', 2)">
                                🚀 Exemplo 1 Concluído! Avançar para o Exemplo 2 ➔
                            </button>
                        </div>
                    ` : `
                        <div style="margin-top: 12px;">
                            <button class="btn btn-success" onclick="concluirExemploParaExercicios(1)">
                                🚀 Exemplo 2 Concluído! Iniciar os Exercícios (Exercício 1) ➔
                            </button>
                        </div>
                    `) : (estadoAtual.exemploId === 1 ? `
                        <div style="margin-top: 12px;">
                            <button class="btn btn-success" onclick="concluirExemploParaExercicios(1)">
                                🚀 Exemplo 1 Concluído! Iniciar Exercício 1 ➔
                            </button>
                        </div>
                    ` : `
                        <div style="margin-top: 12px;">
                            <button class="btn btn-success" onclick="concluirExemploParaExercicios(5)">
                                🚀 Exemplo 2 Concluído! Desbloquear Exercício 5 ➔
                            </button>
                        </div>
                    `))}
                </div>
            `;
        } else {
            areaResp.innerHTML = `
                <div class="instrucao-calculo">
                    📌 <strong>Orientação de Resolução:</strong> ${formatarTextoMatematico(passo.orientacaoCalculo)}
                </div>
                <label style="font-weight: 600; font-size: 14px;">O teu resultado para o ${passo.numero}:</label>
                <input type="text" id="resposta-input" placeholder="Introduz aqui apenas o resultado numérico final..." onkeydown="if(event.key==='Enter') submeterPasso()">
                <div style="margin-top: 10px; display: flex; gap: 8px;">
                    <button class="btn" id="btn-submeter" onclick="submeterPasso()">Validar Resposta</button>
                </div>
            `;
        }
    } else {
        const ex = getDadosTarefa().exercicios[estadoAtual.exercicioId] || {
            numero: estadoAtual.exercicioId,
            enunciado: `Exercício ${estadoAtual.exercicioId} da ${getDadosTarefa().nome}.`,
            tabela: null,
            imagem: null,
            orientacao: "Resolve o exercício no teu caderno."
        };

        const isJaValidado = exerciciosValidados.has(estadoAtual.exercicioId);
        let tabelaHtml = ex.tabela ? ex.tabela : '';
        let imagemHtml = ex.imagem ? `<div style="margin: 16px 0;"><img src="${ex.imagem}" style="max-width: 100%; border-radius: 8px; border: 1px solid #cbd5e1;"></div>` : '';

        container.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #1e293b;">Exercício de Aplicação ${ex.numero}</h3>
                <span style="font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 6px; ${isJaValidado ? 'background: #def7ec; color: #047857;' : 'background: #f1f5f9; color: #475569;'}">
                    ${isJaValidado ? '✓ Validado a Verde' : '⏳ Por Validar'}
                </span>
            </div>
            <p style="font-size: 15px; margin-top: 10px; color: #334155;">${formatarTextoMatematico(ex.enunciado)}</p>
            ${tabelaHtml}
            ${imagemHtml}
        `;

        if (isJaValidado) {
            areaResp.innerHTML = `
                <div class="feedback-box feedback-success" style="margin-top: 10px;">
                    <strong>✓ Exercício Validado a Verde:</strong> A tua resolução manuscrita para este exercício já se encontra validada com sucesso!
                    ${(ex.numero === 4 && fichaAtivaId !== 'tarefa_08') ? `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-warning" onclick="navegarParaItem('exemplo', 2)">
                                📘 Concluíste o Bloco 1! Avançar para o Exemplo 2 ➔
                            </button>
                        </div>
                    ` : (ex.numero === 6 ? `
                        <div style="margin-top: 14px; font-weight: 700; color: #047857;">
                            🏆 Parabéns! Concluíste com êxito todos os exercícios da ${getDadosTarefa().nome}!
                        </div>
                    ` : `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exercicio', ${ex.numero + 1})">
                                Avançar para o Exercício ${ex.numero + 1} ➔
                            </button>
                        </div>
                    `)}
                </div>
                <div style="background: #f8fafc; border: 1px dashed #cbd5e1; padding: 14px; border-radius: 8px; margin-top: 14px;">
                    <p style="font-size: 13px; color: #475569; margin: 0 0 8px 0;">
                        <em>Pretendes atualizar a tua fotografia do caderno para este exercício?</em>
                    </p>
                    <input type="file" id="foto-input" accept="image/*" onchange="mostrarPreviewFoto(event)" style="padding: 6px; background: white; border: 1px solid #cbd5e1; border-radius: 6px; width: 100%;">
                    <div id="preview-foto-container" style="display: none; margin-top: 8px;">
                        <img id="preview-img" style="max-height: 120px; border-radius: 6px; border: 1px solid #cbd5e1; display: block;">
                    </div>
                    <div style="margin-top: 12px;">
                        <button class="btn btn-primary" onclick="submeterExercicio()">
                            🔄 Atualizar Resolução do Caderno
                        </button>
                    </div>
                </div>
            `;
        } else {
            areaResp.innerHTML = `
                <div class="instrucao-calculo" style="border-left-color: #d97706; background: #fffbeb; color: #92400e;">
                    📷 <strong>Resolução Manuscrita Obrigatória:</strong> Anexa uma fotografia nítida da página do teu caderno onde realizaste todos os cálculos deste exercício. A IA do Google Gemini irá ler a tua caligrafia e verificar os passos de resolução diretamente a partir da imagem.
                </div>
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 18px; border-radius: 8px; margin-top: 8px;">
                    <label style="font-weight: 600; font-size: 14px; color: #1e293b;">
                        📸 Fotografia da Resolução no Caderno:
                    </label>
                    <p style="font-size: 12px; color: #64748b; margin: 4px 0 10px 0;">
                        Seleciona ou tira uma fotografia da página do teu caderno com o desenvolvimento deste exercício:
                    </p>
                    <input type="file" id="foto-input" accept="image/*" onchange="mostrarPreviewFoto(event)" style="padding: 8px; background: white; border: 1px dashed #64748b; border-radius: 6px; width: 100%;">
                    <div id="preview-foto-container" style="display: none; margin-top: 10px;">
                        <span style="font-size: 12px; color: #057a55; font-weight: 600;">✓ Fotografia anexada com sucesso:</span>
                        <img id="preview-img" style="max-height: 140px; border-radius: 6px; border: 1px solid #cbd5e1; display: block; margin-top: 4px;">
                    </div>
                    <div style="margin-top: 16px;">
                        <button class="btn btn-success" id="btn-submeter-ex" onclick="submeterExercicio()">
                            📤 Submeter Fotografia para Avaliação
                        </button>
                    </div>
                </div>
            `;
        }
    }

    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
}

function submeterPasso() {
    const input = document.getElementById('resposta-input');
    const valor = input.value.trim();
    if (!valor) {
        input.focus();
        return;
    }

    const ex = getDadosTarefa().exemplos[estadoAtual.exemploId];
    const passoKey = estadoAtual.passosLista[estadoAtual.passoIndex];
    const passo = ex.passos[passoKey];
    const feedbackArea = document.getElementById('feedback-area');

    const acertou = verificarAcerto(valor, passo.valoresCorretos, passo.termosValidos || [String(passo.valoresCorretos[0])]);
    const duracaoSegundos = Math.max(1, Math.round((Date.now() - timestampInicioPergunta) / 1000));

    fetch('/api/tentativa', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            aluno_id: alunoAtivoId,
            ficha_id: fichaAtivaId,
            tipo: 'exemplo',
            numero: estadoAtual.exemploId,
            passo: passoKey,
            resposta_aluno: valor,
            correto: acertou,
            feedback: acertou ? passo.sucesso : passo.feedbackErro,
            pista: acertou ? null : passo.pista,
            duracao_segundos: duracaoSegundos
        })
    }).then(() => carregarDocente());

    if (acertou) {
        input.classList.remove('input-error');
        passosValidados.add(`${estadoAtual.exemploId}_${passoKey}`);
        
        const dadosT = getDadosTarefa();
        const pLista1 = dadosT.exemplos[1].passosLista;
        exemplo1Concluido = pLista1.every(p => passosValidados.has(`1_${p}`));
        if (dadosT.exemplos[2]) {
            const pLista2 = dadosT.exemplos[2].passosLista;
            exemplo2Concluido = pLista2.every(p => passosValidados.has(`2_${p}`));
        } else {
            exemplo2Concluido = true;
        }

        let botaoAvanco = '';
        const isUltimoPasso = (estadoAtual.passoIndex === estadoAtual.passosLista.length - 1);
        const temExemplo2 = !!(dadosT.exemplos && dadosT.exemplos[2]);

        if (isUltimoPasso) {
            if (!temExemplo2) {
                if (estadoAtual.exemploId === 1 && exemplo1Concluido) {
                    botaoAvanco = `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exercicio', 1)">
                                🚀 Concluir Exemplo 1 e Iniciar o Exercício 1 ➔
                            </button>
                        </div>
                    `;
                }
            } else if (fichaAtivaId === 'tarefa_08') {
                if (estadoAtual.exemploId === 1 && exemplo1Concluido) {
                    botaoAvanco = `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exemplo', 2)">
                                🚀 Concluir Exemplo 1 e Avançar para o Exemplo 2 ➔
                            </button>
                        </div>
                    `;
                } else if (estadoAtual.exemploId === 2 && exemplo2Concluido) {
                    botaoAvanco = `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exercicio', 1)">
                                🚀 Concluir Exemplo 2 e Iniciar os Exercícios (Exercício 1) ➔
                            </button>
                        </div>
                    `;
                }
            } else {
                if (estadoAtual.exemploId === 1 && exemplo1Concluido) {
                    botaoAvanco = `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exercicio', 1)">
                                🚀 Concluir Exemplo 1 e Iniciar o Exercício 1 ➔
                            </button>
                        </div>
                    `;
                } else if (estadoAtual.exemploId === 2 && exemplo2Concluido) {
                    botaoAvanco = `
                        <div style="margin-top: 14px;">
                            <button class="btn btn-success" onclick="navegarParaItem('exercicio', 5)">
                                🚀 Concluir Exemplo 2 e Desbloquear o Exercício 5 ➔
                            </button>
                        </div>
                    `;
                }
            }
        } else {
            const proximoPassoNum = estadoAtual.passosLista[estadoAtual.passoIndex + 1];
            botaoAvanco = `
                <div style="margin-top: 14px;">
                    <button class="btn btn-success" onclick="avancarPassoSeguinte()">
                        Avançar para o Passo ${proximoPassoNum} ➔
                    </button>
                </div>
            `;
        }

        atualizarBarraNav();

        feedbackArea.innerHTML = `
            <div class="feedback-box feedback-success">
                <strong>✓ Resposta Correta:</strong> ${passo.sucesso}
                ${isUltimoPasso ? `<p style="margin: 8px 0 0 0; font-weight: 600;">🎉 Parabéns! Completaste com sucesso todos os passos do Exemplo ${estadoAtual.exemploId}!</p>` : ''}
                ${botaoAvanco}
            </div>
        `;
    } else {
        input.classList.add('input-error');
        feedbackArea.innerHTML = `
            <div class="feedback-box feedback-error">
                <strong>Atenção:</strong> ${passo.feedbackErro}
                <div class="pista-box">
                    💡 <strong>Pista Pedagógica:</strong> ${passo.pista}
                </div>
                <div style="margin-top: 12px; background: #ffffff; padding: 12px; border-radius: 6px; border: 1px solid #fecaca;">
                    <strong style="color: #991b1b;">Nova Tentativa:</strong> Lê a pista acima com atenção, introduz o teu novo cálculo no campo de resposta acima e clica em <strong>Validar Resposta</strong> (ou prime Enter).
                    <div style="margin-top: 8px;">
                        <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 13px;" onclick="limparEColocarFoco()">
                            Limpar campo e tentar de novo
                        </button>
                    </div>
                </div>
            </div>
        `;
        input.select();
        input.focus();
    }

    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
}

function limparEColocarFoco() {
    const input = document.getElementById('resposta-input');
    input.value = '';
    input.classList.remove('input-error');
    input.focus();
}

function selecionarPassoExemplo(idx) {
    estadoAtual.passoIndex = idx;
    renderizarTela();
}

function avancarPassoSeguinte() {
    estadoAtual.passoIndex += 1;
    renderizarTela();
}

function concluirExemploParaExercicios(destExercicioId) {
    estadoAtual.fase = 'exercicio';
    estadoAtual.exercicioId = destExercicioId;
    renderizarTela();
}

function mostrarPreviewFoto(event) {
    const container = document.getElementById('preview-foto-container');
    const img = document.getElementById('preview-img');
    if (event.target.files && event.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
            container.style.display = 'block';
        };
        reader.readAsDataURL(event.target.files[0]);
    }
}

function formatarTextoMatematico(texto) {
    if (!texto) return '';
    let t = String(texto);

    // 1. Reconstruir barras de comandos LaTeX corrompidos por sequências de escape JSON
    t = t.replace(/\\t\\s*imes/g, ' \\\\times ');
    t = t.replace(/\\t\\s*ext/g, ' \\\\text');
    t = t.replace(/\\f\\s*rac/g, ' \\\\frac');
    t = t.replace(/(\\d+)\\s*imes\\s*(\\d+)/g, '$1 \\\\times $2');
    t = t.replace(/\\bimes\\b/g, '\\\\times');
    t = t.replace(/(^|\\s)ext\\s*\\{/g, '$1\\\\text{');
    t = t.replace(/(^|\\s)rac\\s*\\{/g, '$1\\\\frac{');
    t = t.replace(/(^|\\s)egin\\s*\\{/g, '$1\\\\begin{');

    // 2. Normalizar moedas e euros para renderização imediata MathJax
    t = t.replace(/\\\\text\\{\\s*\\\\euro\\s*\\}/g, '\\\\text{ €}');
    t = t.replace(/\\\\text\\{\\s*€\\s*\\}/g, '\\\\text{ €}');
    t = t.replace(/\\\\textyen\\b/g, '\\\\text{ €}');
    t = t.replace(/\\\\euro\\b/g, '\\\\text{ €}');

    // 3. Garantir delimitadores $...$ quando existem operadores matemáticos soltos
    if ((t.includes('\\\\times') || t.includes('\\\\frac') || t.includes('\\\\approx')) && !t.includes('$')) {
        t = '$' + t + '$';
    }

    return t;
}

function submeterExercicio() {
    const input = document.getElementById('resposta-input');
    const valor = input ? input.value.trim() : '';
    const fotoInput = document.getElementById('foto-input');
    const feedbackArea = document.getElementById('feedback-area');
    const btnSubmeter = document.getElementById('btn-submeter-ex');

    const temFoto = (fotoInput && fotoInput.files && fotoInput.files.length > 0);

    if (!temFoto) {
        feedbackArea.innerHTML = `
            <div class="feedback-box feedback-error">
                <strong>⚠️ Fotografia Obrigatória Não Detetada:</strong><br>
                Nos exercícios de aplicação <strong>não é permitida a submissão de respostas ou resultados isolados</strong>.<br>
                É obrigatório anexar uma fotografia da resolução manuscrita no teu caderno para que a IA do Google Gemini possa avaliar os passos e validar o exercício a verde.
            </div>
        `;
        if (fotoInput) fotoInput.focus();
        if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise();
        return;
    }

    const ficheiroFoto = fotoInput.files[0];
    const nomeFoto = ficheiroFoto.name;

    if (btnSubmeter) {
        btnSubmeter.disabled = true;
        btnSubmeter.innerHTML = '⏳ A analisar com Google Gemini...';
    }

    feedbackArea.innerHTML = `
        <div class="feedback-box" style="background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="spinner" style="width: 20px; height: 20px; border: 3px solid #bfdbfe; border-top-color: #1d4ed8; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
                <span><strong>🤖 Google Gemini Multimodal:</strong> A ler a caligrafia e os cálculos do caderno («${nomeFoto}») e a verificar o raciocínio matemático...</span>
            </div>
        </div>
    `;

    const leitor = new FileReader();
    leitor.onload = function(e) {
        const dataUrl = e.target.result;
        const b64Data = dataUrl.split(',')[1];
        const mimeType = ficheiroFoto.type || 'image/jpeg';

        const duracaoSegundos = Math.max(1, Math.round((Date.now() - timestampInicioPergunta) / 1000));

        fetch('/api/avaliar_foto', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                aluno_id: alunoAtivoId,
                ficha_id: fichaAtivaId,
                exercicio_id: estadoAtual.exercicioId,
                imagem_b64: b64Data,
                mime_type: mimeType,
                nota_aluno: valor,
                duracao_segundos: duracaoSegundos
            })
        })
        .then(r => r.json())
        .then(res => {
            if (btnSubmeter) {
                btnSubmeter.disabled = false;
                btnSubmeter.innerHTML = '📤 Submeter Fotografia e Validar Resolução';
            }

            if (res.correto) {
                if (input) input.classList.remove('input-error');
                exerciciosValidados.add(estadoAtual.exercicioId);
                atualizarBarraNav();
                carregarDocente();

                let botaoProgresso = '';
                if (fichaAtivaId === 'tarefa_08') {
                    if (estadoAtual.exercicioId === 6) {
                        botaoProgresso = `
                            <div style="margin-top: 14px;">
                                <p style="font-size: 15px; font-weight: 700; color: #047857;">
                                    🏆 Exercício 6 Validado a Verde! Toda a Tarefa 8 está concluída com sucesso!
                                </p>
                            </div>
                        `;
                    } else {
                        const proxId = estadoAtual.exercicioId + 1;
                        botaoProgresso = `
                            <div style="margin-top: 14px;">
                                <button class="btn btn-success" onclick="navegarParaItem('exercicio', ${proxId})">
                                    Avançar para o Exercício ${proxId} ➔
                                </button>
                            </div>
                        `;
                    }
                } else {
                    if (estadoAtual.exercicioId === 4) {
                        botaoProgresso = `
                            <div style="margin-top: 14px;">
                                <button class="btn btn-warning" onclick="navegarParaItem('exemplo', 2)">
                                    📘 Concluíste o Bloco 1! Avançar para o Exemplo 2 ➔
                                </button>
                            </div>
                        `;
                    } else if (estadoAtual.exercicioId === 6) {
                        botaoProgresso = `
                            <div style="margin-top: 14px;">
                                <p style="font-size: 15px; font-weight: 700; color: #047857;">
                                    🏆 Exercício 6 Validado a Verde! Toda a Tarefa 7 está concluída com sucesso!
                                </p>
                            </div>
                        `;
                    } else {
                        const proxId = estadoAtual.exercicioId + 1;
                        botaoProgresso = `
                            <div style="margin-top: 14px;">
                                <button class="btn btn-success" onclick="navegarParaItem('exercicio', ${proxId})">
                                    Avançar para o Exercício ${proxId} ➔
                                </button>
                            </div>
                        `;
                    }
                }

                const transcFormatada = formatarTextoMatematico(res.transcricao_caderno);
                const fbFormatado = formatarTextoMatematico(res.feedback);
                const pistaFormatada = formatarTextoMatematico(res.pista);

                feedbackArea.innerHTML = `
                    <div class="feedback-box feedback-success">
                        <strong>✓ Resolução Validada por Google Gemini:</strong> ${fbFormatado}
                        ${transcFormatada ? `<div style="margin-top: 8px; font-size: 13px; color: #065f46;"><strong>📝 O que escreveste no teu caderno:</strong> <em>${transcFormatada}</em></div>` : ''}
                        ${botaoProgresso}
                    </div>
                `;
            } else {
                if (input) input.classList.add('input-error');
                carregarDocente();

                const transcFormatada = formatarTextoMatematico(res.transcricao_caderno);
                const fbFormatado = formatarTextoMatematico(res.feedback);
                const pistaFormatada = formatarTextoMatematico(res.pista);

                feedbackArea.innerHTML = `
                    <div class="feedback-box feedback-error">
                        <strong>❌ Incorreção Detetada pela IA no Caderno:</strong><br>
                        ${fbFormatado}<br><br>
                        ${pistaFormatada ? `<strong>💡 Pista Pedagógica:</strong> ${pistaFormatada}<br><br>` : ''}
                        ${transcFormatada ? `<div style="margin-top: 8px; font-size: 13px; color: #991b1b;"><strong>🔍 O que foi identificado no teu caderno:</strong> <em>${transcFormatada}</em></div><br>` : ''}
                        <em>Corrige os cálculos na página do teu caderno e envia nova fotografia atualizada para que o exercício seja validado a verde.</em>
                    </div>
                `;
            }

            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([feedbackArea]).catch(() => {
                    window.MathJax.typesetPromise();
                });
            }
        })
        .catch(err => {
            if (btnSubmeter) {
                btnSubmeter.disabled = false;
                btnSubmeter.innerHTML = '📤 Submeter Fotografia e Validar Resolução';
            }
            feedbackArea.innerHTML = `
                <div class="feedback-box feedback-error">
                    <strong>⚠️ Erro na Comunicação com a IA:</strong> ${err.message}. Tenta novamente.
                </div>
            `;
        });
    };
    leitor.readAsDataURL(ficheiroFoto);
}

function mostrarAba(aba) {
    if (aba === 'docente' && !docenteAutenticado) {
        abrirModalLogin('docente');
        return;
    }
    document.getElementById('tab-aluno-btn').classList.toggle('active', aba === 'aluno');
    document.getElementById('tab-docente-btn').classList.toggle('active', aba === 'docente');
    document.getElementById('aba-aluno').style.display = aba === 'aluno' ? 'block' : 'none';
    document.getElementById('aba-docente').style.display = aba === 'docente' ? 'block' : 'none';
    if (aba === 'docente') {
        carregarDocente();
    } else {
        if (window.MathJax && window.MathJax.typesetPromise) {
            setTimeout(() => {
                window.MathJax.typesetPromise([document.getElementById('aba-aluno')]).catch(() => {});
            }, 60);
        }
    }
}

let turmaDocenteId = 'todas';

function selecionarTurmaDocente(novaTurma) {
    turmaDocenteId = novaTurma;
    const selTurma = document.getElementById('sel-turma-docente');
    if (selTurma) selTurma.value = turmaDocenteId;
    carregarDocente();
}

function abrirModalImportarAlunos() {
    const modal = document.getElementById('modal-importar-alunos-overlay');
    if (modal) modal.style.display = 'flex';
    const statusMsg = document.getElementById('msg-import-status');
    if (statusMsg) statusMsg.style.display = 'none';
    const textarea = document.getElementById('import-nomes');
    if (textarea) textarea.value = '';
    const selTurma = document.getElementById('import-turma');
    if (selTurma && turmaDocenteId !== 'todas') selTurma.value = turmaDocenteId;
}

function fecharModalImportarAlunos() {
    const modal = document.getElementById('modal-importar-alunos-overlay');
    if (modal) modal.style.display = 'none';
}

function submeterImportacaoAlunos() {
    const turma = document.getElementById('import-turma').value;
    const nomes = document.getElementById('import-nomes').value;
    const senhaPadrao = document.getElementById('import-senha-padrao').value || '1234';
    const statusMsg = document.getElementById('msg-import-status');

    if (!nomes.trim()) {
        if (statusMsg) {
            statusMsg.style.display = 'block';
            statusMsg.style.background = '#fef2f2';
            statusMsg.style.color = '#dc2626';
            statusMsg.innerText = 'Por favor, insere pelo menos um nome de aluno.';
        }
        return;
    }

    fetch('/api/importar_alunos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ turma, nomes, senha_padrao: senhaPadrao })
    })
    .then(r => r.json())
    .then(res => {
        if (res.sucesso) {
            if (statusMsg) {
                statusMsg.style.display = 'block';
                statusMsg.style.background = '#f0fdf4';
                statusMsg.style.color = '#166534';
                statusMsg.innerText = `✅ ${res.total} alunos importados com sucesso para ${turma}!`;
            }
            setTimeout(() => {
                fecharModalImportarAlunos();
                carregarDocente();
                carregarListaAlunosDropdown();
            }, 1000);
        } else {
            if (statusMsg) {
                statusMsg.style.display = 'block';
                statusMsg.style.background = '#fef2f2';
                statusMsg.style.color = '#dc2626';
                statusMsg.innerText = `❌ Erro: ${res.mensagem || 'Falha ao importar alunos.'}`;
            }
        }
    })
    .catch(err => {
        if (statusMsg) {
            statusMsg.style.display = 'block';
            statusMsg.style.background = '#fef2f2';
            statusMsg.style.color = '#dc2626';
            statusMsg.innerText = `❌ Erro: ${err.message}`;
        }
    });
}

function formatarDuracao(segundos) {
    if (segundos === null || segundos === undefined || isNaN(segundos) || segundos <= 0) return '—';
    const s = Math.round(segundos);
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    const resto = s % 60;
    return `${m}m ${resto < 10 ? '0' : ''}${resto}s`;
}

function selecionarAlunoDocente(novoId) {
    alunoDocenteId = parseInt(novoId);
    const selDocente = document.getElementById('sel-aluno-docente');
    if (selDocente) selDocente.value = alunoDocenteId;
    carregarDocente();
}

function mudarFiltroItensDocente(novoTipo) {
    filtroDocenteTipo = novoTipo;
    const btnEx = document.getElementById('btn-filtro-exercicios');
    const btnTodos = document.getElementById('btn-filtro-todos');
    if (btnEx && btnTodos) {
        if (novoTipo === 'exercicio') {
            btnEx.style.background = 'var(--primary)';
            btnEx.style.color = 'white';
            btnTodos.style.background = 'transparent';
            btnTodos.style.color = '#475569';
        } else {
            btnTodos.style.background = 'var(--primary)';
            btnTodos.style.color = 'white';
            btnEx.style.background = 'transparent';
            btnEx.style.color = '#475569';
        }
    }
    carregarDocente();
}

function carregarDocente() {
    fetch(`/api/estatisticas?aluno_id=${alunoDocenteId}&ficha_id=${fichaDocenteId}&turma=${encodeURIComponent(turmaDocenteId)}`)
        .then(r => r.json())
        .then(dados => {
            const alunoSel = dados.aluno_selecionado || {};
            const turmaGlob = dados.turma_global || {};
            const alunoObj = (dados.lista_alunos || []).find(a => a.id === alunoDocenteId) || {};
            const exVal = alunoObj.exercicios_validados !== undefined ? alunoObj.exercicios_validados : 0;
            const pistasTotal = alunoObj.pistas !== undefined ? alunoObj.pistas : 0;
            const primeiroNome = (alunoSel.nome || 'Aluno').split(' ')[0];

            // Atualizar dropdown de alunos da turma selecionada
            const selDocente = document.getElementById('sel-aluno-docente');
            if (selDocente && dados.lista_alunos) {
                selDocente.innerHTML = '';
                dados.lista_alunos.forEach(a => {
                    const opt = document.createElement('option');
                    opt.value = a.id;
                    opt.innerText = `${a.nome} (${a.turma})`;
                    if (a.id === alunoDocenteId) opt.selected = true;
                    selDocente.appendChild(opt);
                });
                if (selDocente.value != alunoDocenteId && selDocente.options.length > 0) {
                    alunoDocenteId = parseInt(selDocente.value);
                }
            }

            // Cartões de topo simplificados e focados
            const elExAluno = document.getElementById('stat-exercicios-aluno');
            if (elExAluno) elExAluno.innerText = `${exVal} / 6 (${alunoObj.percentual_progresso || 0}%)`;

            const elPistasAluno = document.getElementById('stat-pistas-aluno');
            if (elPistasAluno) elPistasAluno.innerText = pistasTotal;

            const elLabelProgresso = document.getElementById('stat-label-nome-progresso');
            if (elLabelProgresso) elLabelProgresso.innerText = primeiroNome;

            const elLabelPistas = document.getElementById('stat-label-nome-pistas');
            if (elLabelPistas) elLabelPistas.innerText = primeiroNome;

            const elTempoAluno = document.getElementById('stat-tempo-aluno');
            if (elTempoAluno) elTempoAluno.innerText = alunoSel.tempo_medio_formatado || '—';

            const elLabelNome = document.getElementById('stat-label-nome-aluno');
            if (elLabelNome) elLabelNome.innerText = primeiroNome;

            const elTempoTurma = document.getElementById('stat-tempo-turma');
            if (elTempoTurma) elTempoTurma.innerText = turmaGlob.tempo_medio_formatado || '—';

            const elNomeAnalise = document.getElementById('nome-aluno-analise');
            if (elNomeAnalise) elNomeAnalise.innerText = alunoSel.nome || 'Aluno';

            const selTarDoc = document.getElementById('sel-tarefa-docente');
            if (selTarDoc && selTarDoc.value != fichaDocenteId) selTarDoc.value = fichaDocenteId;

            // 1. Matriz Analítica por Pergunta do Aluno Selecionado
            const tbodyConsolidado = document.getElementById('tbody-progresso-consolidado');
            if (tbodyConsolidado) {
                tbodyConsolidado.innerHTML = '';
                const listaAlunoFiltrada = (dados.perguntas_aluno || []).filter(q => {
                    if (filtroDocenteTipo === 'exercicio') return q.tipo === 'exercicio';
                    return true;
                });

                listaAlunoFiltrada.forEach(q => {
                    const tr = document.createElement('tr');
                    const badge = q.concluido 
                        ? `<span class="badge-status badge-ok">✓ Validado com Sucesso</span>`
                        : (q.bloqueado ? `<span class="badge-status badge-pendente">🔒 Bloqueado</span>` : `<span class="badge-status badge-pendente">⏳ Por Resolver</span>`);

                    let pistasTxt = '0';
                    if (q.concluido && q.pistas === 0) {
                        pistasTxt = `<span style="color:#047857; font-weight:600;">0 <small style="font-weight:400; color:#15803d;">(À 1.ª)</small></span>`;
                    } else if (q.pistas > 0) {
                        pistasTxt = `<span style="color:#d97706; font-weight:700;">${q.pistas}</span>`;
                    }

                    const tempoValTxt = q.concluido ? `<span style="font-weight:600; color:#047857;">${q.tempo_formatado}</span>` : '—';
                    const mediaTurmaTxt = q.tempo_medio_turma_formatado || '—';

                    const tipoBadge = (q.tipo === 'exemplo')
                        ? `<span style="background: #e0f2fe; color: #0369a1; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-right: 6px;">PASSO GUIADO</span>`
                        : `<span style="background: #dcfce7; color: #15803d; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-right: 6px;">EXERCÍCIO</span>`;

                    tr.innerHTML = `
                        <td><strong>${q.bloco}</strong></td>
                        <td>${tipoBadge}${q.item}</td>
                        <td>${badge}</td>
                        <td style="text-align: center;">${pistasTxt}</td>
                        <td style="text-align: center;">${tempoValTxt}</td>
                        <td style="text-align: center; color: #475569;">${mediaTurmaTxt}</td>
                    `;
                    tbodyConsolidado.appendChild(tr);
                });
            }

            // 2. Panorama Global da Turma por Pergunta
            const tbodyTurma = document.getElementById('tbody-turma-perguntas');
            if (tbodyTurma) {
                tbodyTurma.innerHTML = '';
                const listaTurmaFiltrada = (dados.panorama_turma || []).filter(p => {
                    if (filtroDocenteTipo === 'exercicio') return p.tipo === 'exercicio';
                    return true;
                });

                listaTurmaFiltrada.forEach(p => {
                    const tr = document.createElement('tr');
                    const validadosTxt = `<span style="font-weight:600; color:#047857;">${p.alunos_validados} / ${dados.total_alunos}</span>`;
                    const pistasTxt = p.total_pistas > 0 ? `<span style="color:#d97706; font-weight:700;">${p.total_pistas}</span>` : '0';
                    const tempoMedioTxt = p.tempo_medio_formatado || '—';

                    const tipoBadge = (p.tipo === 'exemplo')
                        ? `<span style="background: #e0f2fe; color: #0369a1; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-right: 6px;">PASSO GUIADO</span>`
                        : `<span style="background: #dcfce7; color: #15803d; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-right: 6px;">EXERCÍCIO</span>`;

                    tr.innerHTML = `
                        <td>${tipoBadge}<strong>${p.item}</strong></td>
                        <td style="text-align: center;">${validadosTxt}</td>
                        <td style="text-align: center;">${pistasTxt}</td>
                        <td style="text-align: center; font-weight:600; color:#1e40af;">${tempoMedioTxt}</td>
                    `;
                    tbodyTurma.appendChild(tr);
                });
            }

            // 3. Resumo Comparativo entre Alunos
            const tbodyAlunos = document.getElementById('tbody-resumo-alunos');
            if (tbodyAlunos) {
                tbodyAlunos.innerHTML = '';
                (dados.lista_alunos || []).forEach(a => {
                    const tr = document.createElement('tr');
                    if (a.id === alunoDocenteId) tr.style.backgroundColor = '#f0fdf4';

                    const isAtivo = a.id === alunoDocenteId;
                    const tempoTxt = a.tempo_medio_formatado || '—';
                    const progressoTxt = `<strong>${a.exercicios_validados}</strong> de 6 Ex. (${a.percentual_progresso}%)`;
                    const pistasTxt = a.pistas > 0 
                        ? `<span style="color:#d97706; font-weight:700;">${a.pistas}</span>` 
                        : `<span style="color:#047857; font-weight:600;">0</span>`;

                    tr.innerHTML = `
                        <td><strong>${a.nome}</strong> ${isAtivo ? '<span style="font-size:11px; color:#15803d; font-weight:700;">(Em Foco)</span>' : ''}</td>
                        <td>${a.turma}</td>
                        <td style="text-align: center;">${progressoTxt}</td>
                        <td style="text-align: center;">${pistasTxt}</td>
                        <td style="text-align: center; font-weight:600;">${tempoTxt}</td>
                        <td style="text-align: center; display: flex; gap: 4px; justify-content: center;">
                            <button class="btn btn-primary" style="margin:0; padding:3px 8px; font-size:12px;" onclick="selecionarAlunoDocente(${a.id})">
                                Inspecionar
                            </button>
                            <button class="btn btn-secondary" style="margin:0; padding:3px 8px; font-size:12px; background: white; border: 1px solid #cbd5e1;" onclick="abrirRedefinirSenhaPrompt(${a.id}, '${a.nome.replace("'", "\\'")}')">
                                🔑 Senha
                            </button>
                        </td>
                    `;
                    tbodyAlunos.appendChild(tr);
                });
            }

            // 4. Registo Detalhado de Tentativas
            const tbodyTentativas = document.getElementById('tbody-tentativas');
            if (tbodyTentativas) {
                tbodyTentativas.innerHTML = '';
                (dados.tentativas || []).forEach(t => {
                    const tr = document.createElement('tr');
                    const statusHtml = t.correto 
                        ? `<span class="badge-status badge-ok">✓ Resolução Validada</span>`
                        : `<span class="badge-status badge-pista">💡 Pista Acionada</span>`;

                    const respFormatada = formatarTextoMatematico(t.resposta_aluno);
                    const fbFormatado = formatarTextoMatematico(t.feedback_dado);
                    const pistaFormatada = t.pista_fornecida ? formatarTextoMatematico(t.pista_fornecida) : '';
                    const tempoResp = formatarDuracao(t.duracao_segundos);

                    tr.innerHTML = `
                        <td style="font-size: 12px; color: #64748b;">${t.data_hora.substring(11, 19)}</td>
                        <td><strong>${t.tipo.toUpperCase()} ${t.numero}</strong></td>
                        <td>${t.passo}</td>
                        <td style="text-align: center; font-size: 13px; font-weight: 600; color: #475569;">${tempoResp}</td>
                        <td><span style="font-family: monospace; font-size: 13px; background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">${respFormatada}</span></td>
                        <td>${statusHtml}</td>
                        <td style="font-size: 13px;">${fbFormatado} ${pistaFormatada ? '<br><small style="color:#d97706;">💡 ' + pistaFormatada + '</small>' : ''}</td>
                    `;
                    tbodyTentativas.appendChild(tr);
                });
            }

            // Forçar compilação de todas as fórmulas LaTeX da Aba Docente no MathJax
            if (window.MathJax && window.MathJax.typesetPromise) {
                setTimeout(() => {
                    const elDocente = document.getElementById('aba-docente');
                    window.MathJax.typesetPromise([elDocente]).catch(() => {
                        window.MathJax.typesetPromise();
                    });
                }, 80);
            }
        });
}


// GESTÃO DE AUTENTICAÇÃO E SESSÕES
let alunoAutenticado = null;
let docenteAutenticado = false;
let docenteToken = null;

function abrirModalLogin(tipo = 'aluno') {
    const overlay = document.getElementById('modal-auth-overlay');
    if (overlay) overlay.style.display = 'flex';
    mudarAbaAuth(tipo);
    carregarListaAlunosDropdown();
}

function fecharModalLogin() {
    const overlay = document.getElementById('modal-auth-overlay');
    if (overlay) overlay.style.display = 'none';
}

function mudarAbaAuth(tipo) {
    const btnAluno = document.getElementById('btn-tab-auth-aluno');
    const btnDocente = document.getElementById('btn-tab-auth-docente');
    const formAluno = document.getElementById('form-auth-aluno');
    const formDocente = document.getElementById('form-auth-docente');

    if (tipo === 'aluno') {
        if (btnAluno) btnAluno.classList.add('active');
        if (btnDocente) btnDocente.classList.remove('active');
        if (formAluno) formAluno.style.display = 'block';
        if (formDocente) formDocente.style.display = 'none';
        const inputUsr = document.getElementById('input-auth-usuario');
        if (inputUsr) inputUsr.focus();
    } else {
        if (btnAluno) btnAluno.classList.remove('active');
        if (btnDocente) btnDocente.classList.add('active');
        if (formAluno) formAluno.style.display = 'none';
        if (formDocente) formDocente.style.display = 'block';
        const inputSenhaDoc = document.getElementById('input-auth-senha-docente');
        if (inputSenhaDoc) inputSenhaDoc.focus();
    }
}

function carregarListaAlunosDropdown() {
    fetch('/api/alunos_lista')
        .then(r => r.json())
        .then(lista => {
            const selRapido = document.getElementById('sel-rapido-aluno');
            if (selRapido) {
                selRapido.innerHTML = '<option value="">-- Escolhe o teu nome da turma --</option>';
                const grupos = {};
                lista.forEach(a => {
                    const t = a.turma || 'Geral';
                    if (!grupos[t]) grupos[t] = [];
                    grupos[t].push(a);
                });

                Object.keys(grupos).sort().forEach(turmaNome => {
                    const optgroup = document.createElement('optgroup');
                    optgroup.label = `📚 ${turmaNome}`;
                    grupos[turmaNome].forEach(a => {
                        const opt = document.createElement('option');
                        opt.value = a.username;
                        opt.innerText = a.nome;
                        optgroup.appendChild(opt);
                    });
                    selRapido.appendChild(optgroup);
                });
            }

            const selHeader = document.getElementById('sel-aluno');
            if (selHeader) {
                selHeader.innerHTML = '';
                const grupos = {};
                lista.forEach(a => {
                    const t = a.turma || 'Geral';
                    if (!grupos[t]) grupos[t] = [];
                    grupos[t].push(a);
                });

                Object.keys(grupos).sort().forEach(turmaNome => {
                    const optgroup = document.createElement('optgroup');
                    optgroup.label = `📚 ${turmaNome}`;
                    grupos[turmaNome].forEach(a => {
                        const opt = document.createElement('option');
                        opt.value = a.id;
                        opt.innerText = `${a.nome} (${a.turma})`;
                        if (a.id === alunoAtivoId) opt.selected = true;
                        optgroup.appendChild(opt);
                    });
                    selHeader.appendChild(optgroup);
                });
            }
        }).catch(() => {});
}

function selecionarAlunoRapido(username) {
    const inputUsr = document.getElementById('input-auth-usuario');
    const inputSenha = document.getElementById('input-auth-senha');
    if (inputUsr && username) {
        inputUsr.value = username;
        if (inputSenha) {
            inputSenha.focus();
        }
    }
}

function submeterLoginAluno() {
    const inputUsr = document.getElementById('input-auth-usuario');
    const inputSenha = document.getElementById('input-auth-senha');
    const msgErro = document.getElementById('msg-erro-login-aluno');

    const username = inputUsr ? inputUsr.value.trim() : '';
    const password = inputSenha ? inputSenha.value : '';

    if (!username) {
        if (msgErro) {
            msgErro.innerText = 'Por favor, seleciona ou digita o teu nome de utilizador.';
            msgErro.style.display = 'block';
        }
        if (inputUsr) inputUsr.focus();
        return;
    }

    if (!password) {
        if (msgErro) {
            msgErro.innerText = 'Por favor, introduz a tua palavra-passe.';
            msgErro.style.display = 'block';
        }
        if (inputSenha) inputSenha.focus();
        return;
    }

    fetch('/api/login_aluno', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, password })
    })
    .then(r => r.json())
    .then(res => {
        if (res.sucesso && res.aluno) {
            alunoAutenticado = res.aluno;
            alunoAtivoId = alunoAutenticado.id;
            docenteAutenticado = false;
            docenteToken = null;

            localStorage.setItem('tutor_aluno', JSON.stringify(alunoAutenticado));
            localStorage.removeItem('tutor_docente_token');
            sessionStorage.setItem('tutor_aluno', JSON.stringify(alunoAutenticado));
            sessionStorage.removeItem('tutor_docente_token');

            if (msgErro) msgErro.style.display = 'none';
            fecharModalLogin();
            atualizarBadgeUsuario();
            mostrarAba('aluno');
            carregarProgressoAluno();
        } else {
            if (msgErro) {
                msgErro.innerText = res.mensagem || 'Credenciais incorretas.';
                msgErro.style.display = 'block';
            }
        }
    })
    .catch(err => {
        if (msgErro) {
            msgErro.innerText = 'Erro na comunicação com o servidor: ' + err.message;
            msgErro.style.display = 'block';
        }
    });
}

function submeterLoginDocente() {
    const inputSenhaDoc = document.getElementById('input-auth-senha-docente');
    const msgErro = document.getElementById('msg-erro-login-docente');
    const senha = inputSenhaDoc ? inputSenhaDoc.value : '';

    if (!senha) {
        if (msgErro) {
            msgErro.innerText = 'Por favor, introduz a palavra-passe docente.';
            msgErro.style.display = 'block';
        }
        return;
    }

    fetch('/api/login_docente', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ senha })
    })
    .then(r => r.json())
    .then(res => {
        if (res.sucesso) {
            docenteAutenticado = true;
            docenteToken = res.token;
            alunoAutenticado = null;

            sessionStorage.setItem('tutor_docente_token', docenteToken);
            sessionStorage.removeItem('tutor_aluno');

            if (msgErro) msgErro.style.display = 'none';
            fecharModalLogin();
            atualizarBadgeUsuario();
            mostrarAba('docente');
            carregarDocente();
        } else {
            if (msgErro) {
                msgErro.innerText = res.mensagem || 'Palavra-passe incorreta.';
                msgErro.style.display = 'block';
            }
        }
    })
    .catch(err => {
        if (msgErro) {
            msgErro.innerText = 'Erro na ligação: ' + err.message;
            msgErro.style.display = 'block';
        }
    });
}

function terminarSessao() {
    alunoAutenticado = null;
    docenteAutenticado = false;
    docenteToken = null;
    localStorage.removeItem('tutor_aluno');
    localStorage.removeItem('tutor_docente_token');
    sessionStorage.removeItem('tutor_aluno');
    sessionStorage.removeItem('tutor_docente_token');
    alunoAtivoId = 1;
    atualizarBadgeUsuario();
    carregarListaAlunosDropdown();
    mostrarAba('aluno');
    carregarProgressoAluno();
}

function atualizarBadgeUsuario() {
    const badge = document.getElementById('badge-sessao-usuario');
    const btnAbaDocente = document.getElementById('tab-docente-btn');
    const btnAbaAluno = document.getElementById('tab-aluno-btn');

    if (!badge) return;

    if (alunoAutenticado) {
        badge.innerHTML = `
            <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 5px 12px; border-radius: 8px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 13px; font-weight: 600; color: #1e40af;">👨‍🎓 ${alunoAutenticado.nome}</span>
                <span style="font-size: 11px; background: #dbeafe; color: #1e3a8a; padding: 2px 6px; border-radius: 4px;">${alunoAutenticado.turma}</span>
                <button class="btn btn-secondary" style="margin: 0; padding: 3px 8px; font-size: 11px; background: white; border: 1px solid #cbd5e1; color: #64748b;" onclick="terminarSessao()">
                    🚪 Sair
                </button>
            </div>
        `;
    } else if (docenteAutenticado) {
        badge.innerHTML = `
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 5px 12px; border-radius: 8px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 13px; font-weight: 600; color: #166534;">👨‍🏫 Professor da Turma</span>
                <button class="btn btn-secondary" style="margin: 0; padding: 3px 8px; font-size: 11px; background: white; border: 1px solid #cbd5e1; color: #64748b;" onclick="terminarSessao()">
                    🚪 Sair da Área Docente
                </button>
            </div>
        `;
    } else {
        badge.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <div class="aluno-selector" style="margin: 0;">
                    <label for="sel-aluno" style="font-size: 13px;"><strong>Aluno:</strong></label>
                    <select id="sel-aluno" onchange="trocarAluno(this.value)" style="font-size: 13px; padding: 4px 8px; font-weight: 600; color: var(--primary);">
                        <option value="1">Duarte Ferreira (10.º TPE/TOE)</option>
                        <option value="2">Beatriz Silva (10.º TCR)</option>
                    </select>
                </div>
                <button class="btn btn-primary" style="margin: 0; padding: 5px 12px; font-size: 12px;" onclick="abrirModalLogin('aluno')">
                    🔑 Iniciar Sessão
                </button>
            </div>
        `;
    }
    if (btnAbaDocente) btnAbaDocente.style.display = 'inline-block';
    if (btnAbaAluno) btnAbaAluno.style.display = 'inline-block';
}

function abrirRedefinirSenhaPrompt(alunoId, alunoNome) {
    const nova = prompt(`Digita a nova palavra-passe para ${alunoNome}:`, '1234');
    if (!nova) return;
    fetch('/api/redefinir_senha_aluno', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ aluno_id: alunoId, nova_senha: nova })
    })
    .then(r => r.json())
    .then(res => {
        if (res.sucesso) {
            alert(`A palavra-passe de ${alunoNome} foi redefinida com sucesso para: ${nova}`);
        } else {
            alert('Erro ao redefinir a palavra-passe.');
        }
    });
}

function abrirCriarAlunoPrompt() {
    const nome = prompt('Nome completo do novo aluno:');
    if (!nome) return;
    const turma = prompt('Turma do aluno (ex: 10.º A):', '10.º A') || '10.º A';
    const usernameSugerido = nome.split(' ')[0].toLowerCase() + '.' + (nome.split(' ')[1] || 'aluno').toLowerCase();
    const username = prompt('Nome de utilizador (login):', usernameSugerido);
    if (!username) return;
    const senha = prompt('Palavra-passe inicial:', '1234') || '1234';

    fetch('/api/criar_aluno', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ nome, turma, username, senha })
    })
    .then(r => r.json())
    .then(res => {
        if (res.sucesso) {
            alert(`Aluno ${nome} registado com sucesso! Utilizador: ${username} | Palavra-passe: ${senha}`);
            carregarDocente();
            carregarListaAlunosDropdown();
        } else {
            alert('Não foi possível criar o aluno: ' + (res.mensagem || 'Erro desconhecido.'));
        }
    });
}

function verificarEstadoAutenticacao() {
    // 1. Carregar lista de alunos para os seletores
    carregarListaAlunosDropdown();

    // 2. Verificar se existe sessão de aluno em cache
    const alunoCache = sessionStorage.getItem('tutor_aluno') || localStorage.getItem('tutor_aluno');
    const docenteCache = sessionStorage.getItem('tutor_docente_token');

    if (alunoCache) {
        try {
            alunoAutenticado = JSON.parse(alunoCache);
            alunoAtivoId = alunoAutenticado.id;
            docenteAutenticado = false;
            atualizarBadgeUsuario();
            fecharModalLogin();
            mostrarAba('aluno');
            carregarProgressoAluno();
            return;
        } catch (e) {}
    }

    if (docenteCache) {
        docenteAutenticado = true;
        docenteToken = docenteCache;
        alunoAutenticado = null;
        atualizarBadgeUsuario();
        fecharModalLogin();
        mostrarAba('docente');
        carregarDocente();
        return;
    }

    // Se ninguém estiver autenticado:
    // Carrega o aluno padrão (ID 1 - Duarte Ferreira) e exibe os exercícios imediatamente
    alunoAtivoId = 1;
    atualizarBadgeUsuario();
    fecharModalLogin();
    mostrarAba('aluno');
    carregarProgressoAluno();
}


// Inicialização Inteligente com Restauro de Sessões
verificarEstadoAutenticacao();

</script>

</body>
</html>
"""

def reparar_latex_backend(texto):
    if not texto or not isinstance(texto, str):
        return texto
    t = texto
    t = t.replace('\x09imes', r'\times').replace('\x09ext', r'\text')
    t = t.replace('\x0crac', r'\frac').replace('\x08egin', r'\begin')
    t = t.replace('\r\x0dight', r'\right').replace('\n\x0aeq', r'\neq')
    t = t.replace(r'\text{ \euro}', r'\text{ €}').replace(r'\text{\euro}', r'\text{ €}')
    t = t.replace(r'\textyen', r'\text{ €}').replace(r'\euro', r'€')
    t = t.replace(' ext{', r' \text{').replace(' rac{', r' \frac{').replace(' imes ', r' \times ')
    return t

def formatar_duracao_backend(segundos):
    if segundos is None or segundos <= 0:
        return "—"
    s = int(round(segundos))
    if s < 60:
        return f"{s}s"
    m = s // 60
    resto = s % 60
    return f"{m}m {resto:02d}s"

class TutorHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        
        elif parsed.path == "/api/alunos_lista":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, nome, turma, username FROM alunos ORDER BY id")
            lista = [{"id": r[0], "nome": r[1], "turma": r[2], "username": r[3] or f"aluno_{r[0]}"} for r in c.fetchall()]
            conn.close()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(lista, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/progresso":
            aluno_id = int(qs.get("aluno_id", [1])[0])
            ficha_id = qs.get("ficha_id", ["tarefa_07"])[0]

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # Exercícios validados
            c.execute("""
            SELECT DISTINCT numero FROM tentativas_passos 
            WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exercicio' AND correto = 1
            """, (aluno_id, ficha_id))
            exercicios_validados = [r[0] for r in c.fetchall()]

            # Passos validados (ex: '1_1.1', '2_2.1')
            c.execute("""
            SELECT DISTINCT numero, passo FROM tentativas_passos 
            WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND correto = 1
            """, (aluno_id, ficha_id))
            passos_validados = [f"{r[0]}_{r[1]}" for r in c.fetchall()]

            # Conclusão Exemplo 1 (Passos do Exemplo 1 de acordo com a ficha)
            if ficha_id == "tarefa_04":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4', '1.5')
                """, (aluno_id, ficha_id))
                exemplo1_concluido = c.fetchone()[0] == 5
                exemplo2_concluido = True
            elif ficha_id in ("tarefa_05", "tarefa_06"):
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4')
                """, (aluno_id, ficha_id))
                exemplo1_concluido = c.fetchone()[0] == 4
                exemplo2_concluido = True
            elif ficha_id == "tarefa_08":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4')
                """, (aluno_id, ficha_id))
                exemplo1_concluido = c.fetchone()[0] == 4

                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 2 AND correto = 1 AND passo IN ('2.1', '2.2')
                """, (aluno_id, ficha_id))
                exemplo2_concluido = c.fetchone()[0] == 2
            else:
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3')
                """, (aluno_id, ficha_id, ficha_id))
                exemplo1_concluido = c.fetchone()[0] == 3

                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exemplo' AND numero = 2 AND correto = 1 AND passo IN ('2.1', '2.2')
                """, (aluno_id, ficha_id, ficha_id))
                exemplo2_concluido = c.fetchone()[0] == 2

            conn.close()

            resp = {
                "exercicios_validados": exercicios_validados,
                "passos_validados": passos_validados,
                "exemplo1_concluido": exemplo1_concluido,
                "exemplo2_concluido": exemplo2_concluido
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        elif parsed.path == "/api/estatisticas":
            aluno_id = int(qs.get("aluno_id", [1])[0])
            ficha_id = qs.get("ficha_id", ["tarefa_07"])[0]
            turma_filtro = qs.get("turma", ["todas"])[0]

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # Obter lista de alunos filtrada por turma se aplicável
            if turma_filtro and turma_filtro != "todas":
                c.execute("SELECT id, nome, turma FROM alunos WHERE turma = ? ORDER BY nome", (turma_filtro,))
            else:
                c.execute("SELECT id, nome, turma FROM alunos ORDER BY turma, nome")
            alunos_db = c.fetchall()
            if not alunos_db:
                c.execute("SELECT id, nome, turma FROM alunos ORDER BY id")
                alunos_db = c.fetchall()

            aluno_db_sel = next((a for a in alunos_db if a[0] == aluno_id), alunos_db[0] if alunos_db else (1, "Aluno", "10.º TPE/TOE"))
            aluno_id = aluno_db_sel[0]
            nome_aluno_sel = aluno_db_sel[1]
            turma_aluno_sel = aluno_db_sel[2]

            # Totais globais filtrados pela ficha e turma selecionada
            if turma_filtro and turma_filtro != "todas":
                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos tp
                JOIN alunos a ON tp.aluno_id = a.id
                WHERE a.turma = ? AND (tp.ficha_id = ? OR (? = 'tarefa_07' AND tp.ficha_id IS NULL))
                """, (turma_filtro, ficha_id, ficha_id))
                total_tentativas = c.fetchone()[0] or 0

                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos tp
                JOIN alunos a ON tp.aluno_id = a.id
                WHERE a.turma = ? AND (tp.ficha_id = ? OR (? = 'tarefa_07' AND tp.ficha_id IS NULL)) AND tp.correto = 1
                """, (turma_filtro, ficha_id, ficha_id))
                total_corretas = c.fetchone()[0] or 0

                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos tp
                JOIN alunos a ON tp.aluno_id = a.id
                WHERE a.turma = ? AND (tp.ficha_id = ? OR (? = 'tarefa_07' AND tp.ficha_id IS NULL)) AND tp.pista_fornecida IS NOT NULL AND tp.pista_fornecida != ''
                """, (turma_filtro, ficha_id, ficha_id))
                total_pistas = c.fetchone()[0] or 0
            else:
                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos 
                WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL))
                """, (ficha_id, ficha_id))
                total_tentativas = c.fetchone()[0] or 0

                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos 
                WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND correto = 1
                """, (ficha_id, ficha_id))
                total_corretas = c.fetchone()[0] or 0

                c.execute("""
                SELECT COUNT(*) FROM tentativas_passos 
                WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND pista_fornecida IS NOT NULL AND pista_fornecida != ''
                """, (ficha_id, ficha_id))
                total_pistas = c.fetchone()[0] or 0

            total_alunos = len(alunos_db)
            taxa_global_turma = round((total_corretas / total_tentativas * 100), 1) if total_tentativas > 0 else 0

            # Verificar conclusão dos Exemplos pelo aluno selecionado de acordo com a ficha
            if ficha_id == "tarefa_04":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4', '1.5')
                """, (aluno_id, ficha_id))
                ex1_concluido = c.fetchone()[0] == 5
                ex2_concluido = True
                itens_oficiais = [
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (IRS)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.1", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Segurança Social)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.2", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Salário Líquido)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.3", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Subsídio Refeição)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.4", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.5 (Total a Receber)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.5", "bloqueado": False},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Mateus - Açores)", "q_tipo": "exercicio", "q_num": 1, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Carlos - 2010 vs 2023)", "q_tipo": "exercicio", "q_num": 2, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Mariana - Junta Freguesia)", "q_tipo": "exercicio", "q_num": 3, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Carina - Parcela por Fórmula)", "q_tipo": "exercicio", "q_num": 4, "q_passo": None, "bloqueado": not ex1_concluido},
                ]
            elif ficha_id == "tarefa_05":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4')
                """, (aluno_id, ficha_id))
                ex1_concluido = c.fetchone()[0] == 4
                ex2_concluido = True
                itens_oficiais = [
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (Rendimento Anual)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.1", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Total Horas Anuais)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.2", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Salário Bruto à Hora)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.3", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Horas Extraordinárias)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.4", "bloqueado": False},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Marco - Mecânico)", "q_tipo": "exercicio", "q_num": 1, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Carlos - Horas Extraordinárias)", "q_tipo": "exercicio", "q_num": 2, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Rosa - 4 Dependentes)", "q_tipo": "exercicio", "q_num": 3, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Maria - 12h Extraordinárias)", "q_tipo": "exercicio", "q_num": 4, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Filipa - 35h Semanais)", "q_tipo": "exercicio", "q_num": 5, "q_passo": None, "bloqueado": not ex1_concluido},
                ]
            elif ficha_id == "tarefa_06":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4')
                """, (aluno_id, ficha_id))
                ex1_concluido = c.fetchone()[0] == 4
                ex2_concluido = True
                itens_oficiais = [
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1 (Rendimento Anual)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.1", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2 (Rendimento Coletável)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.2", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3 (Coleta Individual)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.3", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4 (Coleta Total Casal)", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.4", "bloqueado": False},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Rita e Afonso)", "q_tipo": "exercicio", "q_num": 1, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Manuel - Solteiro)", "q_tipo": "exercicio", "q_num": 2, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Joana e Miguel)", "q_tipo": "exercicio", "q_num": 3, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Mariana e Afonso - Deduções)", "q_tipo": "exercicio", "q_num": 4, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Eugénia e Augusto - Açores)", "q_tipo": "exercicio", "q_num": 5, "q_passo": None, "bloqueado": not ex1_concluido},
                ]
            elif ficha_id == "tarefa_08":
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3', '1.4')
                """, (aluno_id, ficha_id))
                ex1_concluido = c.fetchone()[0] == 4

                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND ficha_id = ? AND tipo = 'exemplo' AND numero = 2 AND correto = 1 AND passo IN ('2.1', '2.2')
                """, (aluno_id, ficha_id))
                ex2_concluido = c.fetchone()[0] == 2

                ex_desbloqueados = (ex1_concluido and ex2_concluido)
                itens_oficiais = [
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.1", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.1", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.2", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.2", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.3", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.3", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 1 - Passo 1.4", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.4", "bloqueado": False},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 2 - Passo 2.1", "q_tipo": "exemplo", "q_num": 2, "q_passo": "2.1", "bloqueado": not ex1_concluido},
                    {"bloco": "Exemplos Guiados", "item": "Exemplo 2 - Passo 2.2", "q_tipo": "exemplo", "q_num": 2, "q_passo": "2.2", "bloqueado": not ex1_concluido},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 1 (Depósito Prazo 10 anos)", "q_tipo": "exercicio", "q_num": 1, "q_passo": None, "bloqueado": not ex_desbloqueados},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 2 (Cátia - Depósito 10 anos)", "q_tipo": "exercicio", "q_num": 2, "q_passo": None, "bloqueado": not ex_desbloqueados},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 3 (Mariana - Férias)", "q_tipo": "exercicio", "q_num": 3, "q_passo": None, "bloqueado": not ex_desbloqueados},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 4 (Capital Inicial Composto)", "q_tipo": "exercicio", "q_num": 4, "q_passo": None, "bloqueado": not ex_desbloqueados},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 5 (Marco - Mar vs Montanha)", "q_tipo": "exercicio", "q_num": 5, "q_passo": None, "bloqueado": not ex_desbloqueados},
                    {"bloco": "Exercícios de Aplicação", "item": "Exercício 6 (Cláudia - Semestral vs Mensal)", "q_tipo": "exercicio", "q_num": 6, "q_passo": None, "bloqueado": not ex_desbloqueados},
                ]
            else:
                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exemplo' AND numero = 1 AND correto = 1 AND passo IN ('1.1', '1.2', '1.3')
                """, (aluno_id, ficha_id, ficha_id))
                ex1_concluido = c.fetchone()[0] == 3

                c.execute("""
                SELECT COUNT(DISTINCT passo) FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exemplo' AND numero = 2 AND correto = 1 AND passo IN ('2.1', '2.2')
                """, (aluno_id, ficha_id, ficha_id))
                ex2_concluido = c.fetchone()[0] == 2

                # Definição oficial de todas as 11 etapas/perguntas da Tarefa 7 (Bloco 1 e Bloco 2 originais)
                itens_oficiais = [
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.1", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.1", "bloqueado": False},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.2", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.2", "bloqueado": False},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exemplo 1 - Passo 1.3", "q_tipo": "exemplo", "q_num": 1, "q_passo": "1.3", "bloqueado": False},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 1 (Francisco)", "q_tipo": "exercicio", "q_num": 1, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 2 (Raquel)", "q_tipo": "exercicio", "q_num": 2, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 3 (Diogo)", "q_tipo": "exercicio", "q_num": 3, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Bloco 1 (Juros e Capital)", "item": "Exercício 4 (Capital Inicial)", "q_tipo": "exercicio", "q_num": 4, "q_passo": None, "bloqueado": not ex1_concluido},
                    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exemplo 2 - Passo 2.1", "q_tipo": "exemplo", "q_num": 2, "q_passo": "2.1", "bloqueado": False},
                    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exemplo 2 - Passo 2.2", "q_tipo": "exemplo", "q_num": 2, "q_passo": "2.2", "bloqueado": False},
                    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exercício 5 (Herança)", "q_tipo": "exercicio", "q_num": 5, "q_passo": None, "bloqueado": not ex2_concluido},
                    {"bloco": "Bloco 2 (Taxa de Juro)", "item": "Exercício 6 (Emília e Lino)", "q_tipo": "exercicio", "q_num": 6, "q_passo": None, "bloqueado": not ex2_concluido},
                ]

            perguntas_aluno = []
            panorama_turma = []

            for it in itens_oficiais:
                # 1. Panorama da turma para este item
                if it["q_passo"]:
                    c.execute("""
                    SELECT 
                        COUNT(*),
                        SUM(correto),
                        COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END),
                        COUNT(DISTINCT CASE WHEN correto = 1 THEN aluno_id END)
                    FROM tentativas_passos 
                    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ?
                    """, (ficha_id, ficha_id, it["q_tipo"], it["q_num"], it["q_passo"]))
                    r_turma = c.fetchone()

                    c.execute("""
                    SELECT duracao_segundos FROM tentativas_passos 
                    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ? AND correto = 1 AND duracao_segundos > 0
                    """, (ficha_id, ficha_id, it["q_tipo"], it["q_num"], it["q_passo"]))
                    tempos_item_turma = [t[0] for t in c.fetchall()]
                else:
                    c.execute("""
                    SELECT 
                        COUNT(*),
                        SUM(correto),
                        COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END),
                        COUNT(DISTINCT CASE WHEN correto = 1 THEN aluno_id END)
                    FROM tentativas_passos 
                    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ?
                    """, (ficha_id, ficha_id, it["q_tipo"], it["q_num"]))
                    r_turma = c.fetchone()

                    c.execute("""
                    SELECT duracao_segundos FROM tentativas_passos 
                    WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND correto = 1 AND duracao_segundos > 0
                    """, (ficha_id, ficha_id, it["q_tipo"], it["q_num"]))
                    tempos_item_turma = [t[0] for t in c.fetchall()]

                tentativas_turma_item = r_turma[0] or 0
                corretas_turma_item = r_turma[1] or 0
                pistas_turma_item = r_turma[2] or 0
                alunos_validados_item = r_turma[3] or 0
                taxa_turma_item = round((corretas_turma_item / tentativas_turma_item * 100), 1) if tentativas_turma_item > 0 else 0
                tempo_medio_turma_item = (sum(tempos_item_turma) / len(tempos_item_turma)) if tempos_item_turma else None

                panorama_turma.append({
                    "item": it["item"],
                    "tipo": it["q_tipo"],
                    "alunos_validados": alunos_validados_item,
                    "total_pistas": pistas_turma_item,
                    "tempo_medio_segundos": tempo_medio_turma_item,
                    "tempo_medio_formatado": formatar_duracao_backend(tempo_medio_turma_item)
                })

                # 2. Métricas do aluno selecionado para este mesmo item
                if it["q_passo"]:
                    c.execute("""
                    SELECT 
                        COUNT(*),
                        SUM(correto),
                        COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END)
                    FROM tentativas_passos 
                    WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ?
                    """, (aluno_id, ficha_id, ficha_id, it["q_tipo"], it["q_num"], it["q_passo"]))
                    r_al = c.fetchone()

                    c.execute("""
                    SELECT duracao_segundos FROM tentativas_passos 
                    WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND passo = ? AND correto = 1 AND duracao_segundos > 0
                    ORDER BY id ASC LIMIT 1
                    """, (aluno_id, ficha_id, ficha_id, it["q_tipo"], it["q_num"], it["q_passo"]))
                    r_val_tempo = c.fetchone()
                else:
                    c.execute("""
                    SELECT 
                        COUNT(*),
                        SUM(correto),
                        COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END)
                    FROM tentativas_passos 
                    WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ?
                    """, (aluno_id, ficha_id, ficha_id, it["q_tipo"], it["q_num"]))
                    r_al = c.fetchone()

                    c.execute("""
                    SELECT duracao_segundos FROM tentativas_passos 
                    WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = ? AND numero = ? AND correto = 1 AND duracao_segundos > 0
                    ORDER BY id ASC LIMIT 1
                    """, (aluno_id, ficha_id, ficha_id, it["q_tipo"], it["q_num"]))
                    r_val_tempo = c.fetchone()

                corretas_al = r_al[1] or 0
                pistas_al = r_al[2] or 0
                concluido_al = bool(corretas_al > 0)
                tempo_val_al = r_val_tempo[0] if (concluido_al and r_val_tempo) else None

                perguntas_aluno.append({
                    "bloco": it["bloco"],
                    "item": it["item"],
                    "tipo": it["q_tipo"],
                    "concluido": concluido_al,
                    "bloqueado": it["bloqueado"],
                    "pistas": pistas_al,
                    "tempo_segundos": tempo_val_al,
                    "tempo_formatado": formatar_duracao_backend(tempo_val_al),
                    "tempo_medio_turma_formatado": formatar_duracao_backend(tempo_medio_turma_item)
                })

            # 3. Lista comparativa de todos os alunos
            lista_alunos = []
            tempos_todos_validados = []

            for al in alunos_db:
                aid, anome, aturma = al[0], al[1], al[2]
                c.execute("""
                SELECT 
                    COUNT(*),
                    SUM(correto),
                    COUNT(CASE WHEN pista_fornecida IS NOT NULL AND pista_fornecida != '' THEN 1 END)
                FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL))
                """, (aid, ficha_id, ficha_id))
                r_est = c.fetchone()
                al_tentativas = r_est[0] or 0
                al_corretas = r_est[1] or 0
                al_pistas = r_est[2] or 0
                al_taxa = round((al_corretas / al_tentativas * 100), 1) if al_tentativas > 0 else 0

                c.execute("""
                SELECT COUNT(DISTINCT numero) FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND tipo = 'exercicio' AND correto = 1
                """, (aid, ficha_id, ficha_id))
                ex_validados = c.fetchone()[0] or 0
                percentual_progresso = round((ex_validados / 6) * 100)

                # Tempos de resposta com sucesso deste aluno
                c.execute("""
                SELECT duracao_segundos FROM tentativas_passos 
                WHERE aluno_id = ? AND (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL)) AND correto = 1 AND duracao_segundos > 0
                """, (aid, ficha_id, ficha_id))
                tempos_al_list = [r[0] for r in c.fetchall()]
                tempos_todos_validados.extend(tempos_al_list)
                tempo_medio_al_num = (sum(tempos_al_list) / len(tempos_al_list)) if tempos_al_list else None

                lista_alunos.append({
                    "id": aid,
                    "nome": anome,
                    "turma": aturma,
                    "interacoes": al_tentativas,
                    "taxa_sucesso": al_taxa,
                    "pistas": al_pistas,
                    "exercicios_validados": ex_validados,
                    "percentual_progresso": percentual_progresso,
                    "tempo_medio_segundos": tempo_medio_al_num,
                    "tempo_medio_formatado": formatar_duracao_backend(tempo_medio_al_num)
                })

            # Médias agregadas de tempo
            aluno_sel_obj = next((a for a in lista_alunos if a["id"] == aluno_id), None)
            tempo_medio_aluno_sel = aluno_sel_obj["tempo_medio_formatado"] if aluno_sel_obj else "—"
            tempo_medio_turma_global_num = (sum(tempos_todos_validados) / len(tempos_todos_validados)) if tempos_todos_validados else None
            tempo_medio_turma_global_str = formatar_duracao_backend(tempo_medio_turma_global_num)

            # Histórico formativo de tentativas filtrado pela ficha
            c.execute("""
            SELECT data_hora, tipo, numero, passo, resposta_aluno, correto, feedback_dado, pista_fornecida, duracao_segundos 
            FROM tentativas_passos 
            WHERE (ficha_id = ? OR (? = 'tarefa_07' AND ficha_id IS NULL))
            ORDER BY id DESC LIMIT 40
            """, (ficha_id, ficha_id))
            linhas = c.fetchall()
            conn.close()

            tentativas = []
            for r in linhas:
                tentativas.append({
                    "data_hora": r[0],
                    "tipo": r[1],
                    "numero": r[2],
                    "passo": r[3],
                    "resposta_aluno": reparar_latex_backend(r[4]),
                    "correto": bool(r[5]),
                    "feedback_dado": reparar_latex_backend(r[6]),
                    "pista_fornecida": reparar_latex_backend(r[7]),
                    "duracao_segundos": r[8] if len(r) > 8 else 0
                })

            resp = {
                "total_tentativas": total_tentativas,
                "taxa_sucesso": taxa_global_turma,
                "total_pistas": total_pistas,
                "total_alunos": total_alunos,
                "aluno_selecionado": {
                    "id": aluno_id,
                    "nome": nome_aluno_sel,
                    "turma": turma_aluno_sel,
                    "tempo_medio_formatado": tempo_medio_aluno_sel
                },
                "turma_global": {
                    "total_tentativas": total_tentativas,
                    "taxa_sucesso": taxa_global_turma,
                    "total_pistas": total_pistas,
                    "tempo_medio_formatado": tempo_medio_turma_global_str
                },
                "perguntas_aluno": perguntas_aluno,
                "panorama_turma": panorama_turma,
                "lista_alunos": lista_alunos,
                "tentativas": tentativas
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
        elif parsed.path.startswith("/fichas/"):
            rel_path = parsed.path.lstrip("/")
            full_path = os.path.abspath(os.path.join(BASE_DIR, rel_path))
            fichas_dir = os.path.abspath(os.path.join(BASE_DIR, "fichas"))
            if full_path.startswith(fichas_dir) and os.path.exists(full_path) and os.path.isfile(full_path):
                ext = os.path.splitext(full_path)[1].lower()
                mimes = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".svg": "image/svg+xml",
                    ".md": "text/markdown; charset=utf-8",
                    ".txt": "text/plain; charset=utf-8"
                }
                mime = mimes.get(ext, "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/login_aluno":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)
            username = dados.get("username", "")
            password = dados.get("password", "")
            aluno = tutor_engine.autenticar_aluno(username, password, db_path=DB_PATH)
            if aluno:
                resp = {"sucesso": True, "aluno": aluno}
            else:
                resp = {"sucesso": False, "mensagem": "Nome de utilizador ou palavra-passe incorretos."}
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/login_docente":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)
            senha = dados.get("senha", "").strip()
            senha_correta = obter_docente_senha()
            if senha == senha_correta:
                resp = {"sucesso": True, "token": "DOCENTE_AUTH_OK_2026"}
            else:
                resp = {"sucesso": False, "mensagem": "Palavra-passe de professor incorreta."}
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/redefinir_senha_aluno":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)
            aluno_id = int(dados.get("aluno_id", 0))
            nova_senha = dados.get("nova_senha", "").strip()
            sucesso = tutor_engine.redefinir_senha_aluno(aluno_id, nova_senha, db_path=DB_PATH)
            resp = {"sucesso": sucesso}
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        elif parsed.path == "/api/criar_aluno":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)
            try:
                novo_id = tutor_engine.criar_aluno(
                    nome=dados.get("nome", ""),
                    turma=dados.get("turma", "10.º TPE/TOE"),
                    username=dados.get("username", ""),
                    senha=dados.get("senha", "1234"),
                    db_path=DB_PATH
                )
                resp = {"sucesso": True, "novo_id": novo_id}
            except Exception as e:
                resp = {"sucesso": False, "mensagem": str(e)}
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/importar_alunos":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)
            turma = dados.get("turma", "10.º TPE/TOE").strip()
            nomes_texto = dados.get("nomes", "")
            senha_padrao = dados.get("senha_padrao", "1234").strip()

            linhas_nomes = [l.strip() for l in nomes_texto.splitlines() if l.strip()]
            try:
                inseridos = tutor_engine.importar_alunos_lote(linhas_nomes, turma=turma, senha_padrao=senha_padrao, db_path=DB_PATH)
                resp = {"sucesso": True, "total": len(inseridos), "alunos": inseridos}
            except Exception as e:
                resp = {"sucesso": False, "mensagem": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/tentativa":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)

            resposta_aluno = reparar_latex_backend(dados.get("resposta_aluno", ""))
            feedback = reparar_latex_backend(dados.get("feedback", ""))
            pista = reparar_latex_backend(dados.get("pista")) if dados.get("pista") else None
            duracao_segundos = float(dados.get("duracao_segundos", 0))

            tutor_engine.registar_tentativa(
                aluno_id=dados.get("aluno_id", 1),
                ficha_id=dados.get("ficha_id", "tarefa_07"),
                tipo=dados.get("tipo", "exemplo"),
                numero=dados.get("numero", 1),
                passo=str(dados.get("passo", "1")),
                resposta_aluno=resposta_aluno,
                correto=dados.get("correto", False),
                feedback=feedback,
                pista=pista,
                duracao_segundos=duracao_segundos,
                db_path=DB_PATH
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "sucesso"}')

        elif parsed.path == "/api/avaliar_foto":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = json.loads(body)

            aluno_id = dados.get("aluno_id", 1)
            ficha_id = dados.get("ficha_id", "tarefa_07")
            exercicio_id = int(dados.get("exercicio_id", 1))
            imagem_b64 = dados.get("imagem_b64", "")
            mime_type = dados.get("mime_type", "image/jpeg")
            nota_aluno = dados.get("nota_aluno", "")
            duracao_segundos = float(dados.get("duracao_segundos", 0))

            # Deteção Anti-Plágio de Fotografias Duplicadas
            import base64
            import hashlib
            try:
                foto_bytes = base64.b64decode(imagem_b64)
            except Exception:
                foto_bytes = b""

            duplicada, info_duplicacao = tutor_engine.verificar_foto_duplicada(foto_bytes, aluno_id, db_path=DB_PATH)
            if duplicada:
                nome_colega = info_duplicacao
                resultado = {
                    "correto": False,
                    "feedback": f"❌ FOTOGRAFIA DUPLICADA DETETADA: Esta mesma fotografia já foi submetida pelo colega {nome_colega}. Por motivos de integridade e veracidade da avaliação formativa, cada aluno tem obrigatoriamente de fotografar a sua própria folha de caderno.",
                    "pista": "Resolve o exercício na página do teu caderno pessoal e tira uma nova fotografia aos teus cálculos.",
                    "transcricao_caderno": "Cópia digital não autorizada.",
                    "duplicada": True
                }
                tutor_engine.registar_tentativa(
                    aluno_id=aluno_id,
                    ficha_id=ficha_id,
                    tipo="exercicio",
                    numero=exercicio_id,
                    passo="resolucao_caderno_foto",
                    resposta_aluno="[Tentativa de Envio de Fotografia Duplicada]",
                    correto=False,
                    feedback=resultado["feedback"],
                    pista=resultado["pista"],
                    foto_hash=hashlib.sha256(foto_bytes).hexdigest(),
                    duracao_segundos=duracao_segundos,
                    db_path=DB_PATH
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode("utf-8"))
                return

            foto_hash = info_duplicacao

            import avaliador_gemini
            resultado = avaliador_gemini.avaliar_com_gemini(
                imagem_b64=imagem_b64,
                mime_type=mime_type,
                exercicio_id=exercicio_id,
                ficha_id=ficha_id,
                nota_aluno=nota_aluno
            )

            correto = bool(resultado.get("correto", False))
            feedback = resultado.get("feedback", "")
            pista = resultado.get("pista", None)
            transcricao = resultado.get("transcricao_caderno", "")

            resposta_registro = f"[Foto Caderno - Gemini Vision] {nota_aluno}" if nota_aluno else f"[Foto Caderno - Gemini Vision] {transcricao[:80]}"

            tutor_engine.registar_tentativa(
                aluno_id=aluno_id,
                ficha_id=ficha_id,
                tipo="exercicio",
                numero=exercicio_id,
                passo="resolucao_caderno_foto",
                resposta_aluno=resposta_registro,
                correto=correto,
                feedback=feedback,
                pista=pista,
                foto_hash=foto_hash,
                duracao_segundos=duracao_segundos,
                db_path=DB_PATH
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode("utf-8"))

        elif parsed.path == "/api/reiniciar_testes":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM tentativas_passos")
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "reinicializado"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

def run_server(porta_inicial: int = PORT):
    global PORT
    porta = porta_inicial
    server = None
    for tentativa in range(5):
        try:
            # Escutar em todas as interfaces ("0.0.0.0") para suportar localhost e 127.0.0.1
            server = ReusableHTTPServer(("0.0.0.0", porta), TutorHandler)
            PORT = porta
            break
        except OSError as e:
            if e.errno == 48: # Address already in use
                porta += 1
            else:
                raise e

    if not server:
        raise RuntimeError(f"Não foi possível iniciar o servidor em nenhuma das portas testadas ({porta_inicial}-{porta}).")

    print(f"\n=======================================================")
    print(f"🚀 Tutor Inteligente de Matemática Ativo!")
    print(f"👉 Acesso Web: http://localhost:{PORT} ou http://127.0.0.1:{PORT}")
    print(f"👉 Painel do Professor: http://localhost:{PORT} (separador 'Painel do Professor')")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado com sucesso.")

if __name__ == "__main__":
    run_server()
