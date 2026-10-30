---
name: dashboard-docente
description: Monitoriza o progresso formativo por curso (10.º TPE/TOE e 10.º TCR) com métricas de validação, tentativas, pistas acionadas e tempos de resolução por pergunta em SQLite, gerindo credenciais seguras do Modelo B.
---

# Skill: Painel Docente de Avaliação Formativa

<div align="justify">

Gere e visualiza os dados de aprendizagem persistidos em `dados/tutor.db`, disponibilizando a matriz analítica e a gestão de turmas para o professor.

## 1. Esquema SQLite (`dados/tutor.db`)
- `alunos`: `id`, `nome`, `turma`, `username`, `password_hash`, `data_registo`.
- `tentativas_passos`: `id`, `aluno_id`, `ficha_id`, `tipo`, `numero`, `passo`, `resposta_aluno`, `caminho_foto`, `foto_hash`, `correto`, `feedback_dado`, `pista_fornecida`, `data_hora`, `duracao_segundos`.
- `sessoes`: `id`, `aluno_id`, `ficha_id`, `estado_atual`, `data_inicio`, `data_fim`.

## 2. Indicadores Analíticos Focados por Pergunta
1. **Estado de Validação**: Registo de exercício validado a verde ($\checkmark$) ou pendente ($\times$);
2. **Tentativas Realizadas**: Contabilização das submissões efetuadas até à validação correta;
3. **Pistas Pedagógicas Acionadas**: Deteção de pontos de apoio pedagógico (*scaffolding*);
4. **Tempo até Validação**: Duração real decorrida até à validação correta (individual e comparativo com a média da turma).
*(Nota: As métricas redundantes de «Interações» e «Taxa de Sucesso» foram eliminadas definitivamente).*

## 3. Gestão de Turmas e Credenciais (Modelo B)
- **Cursos Filtráveis**: `10.º TPE/TOE` e `10.º TCR`;
- **Importação em Lote**: Pré-carga de turmas pelo professor via interface (`📥 Importar Lista de Alunos`) ou CLI (`importar_alunos.py`), com geração de *usernames* e palavras-passe padrão (`1234`);
- **Segurança da Palavra-passe Docente**: `DOCENTE_SENHA` guardada estritamente no servidor (`.env`), sem exposição no código cliente;
- **Integridade dos Registos**: Remoção dos botões de limpeza e recomeço do zero pelos alunos para salvaguardar a avaliação contínua.

</div>
