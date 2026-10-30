# Tutor Inteligente de Matemática: Especificação Operacional Consolidada

<div align="justify">

Este documento constitui a especificação operacional definitiva e consolidada de todo o ecossistema do **Tutor Inteligente de Matemática** (Módulo P1: Modelos Matemáticos para a Cidadania), integrando todas as decisões pedagógicas, arquiteturais, de segurança e de monitorização analítica estabelecidas.

---

### 1. Diretrizes Globais de Estilo e Comunicação
- **Norma Linguística**: Português de Portugal (Português Europeu) estrito em todo o código, documentação e interfaces. Sem translineação (nenhuma palavra partida com hífen em quebras de linha).
- **Alinhamento e Paginação**: Documentos e relatórios em Markdown formatados obrigatoriamente com alinhamento justificado (`<div align="justify">`). Nas aplicações web e páginas HTML, o alinhamento de texto é estritamente à esquerda (`text-align: left;`).
- **Notação Matemática Obrigatória**: Recurso estrito à notação LaTeX em todas as fórmulas, variáveis, cálculos e quantias monetárias ($J = C \times i \times t$, $C_n = C_0 \times (1 + i)^n$, $320\,922{,}89\text{ €}$, $0{,}04$, $2\%$).
- **Tratamento Pedagógico por «Tu» (2.ª Pessoa do Singular)**: Toda a comunicação do tutor, pistas pedagógicas, mensagens da IA e orientações dirigem-se sem exceção ao aluno por «tu» (*«calculaste»*, *«no teu caderno»*, *«deves rever»*, *«repara que»*). É expressamente proibido falar na 3.ª pessoa (*«o aluno calculou»*).

---

### 2. Rigor Numérico e Critérios de Aceitação Monetária
- **Arredondamento Monetário Obrigatório**: Exige-se sempre o valor numérico exato arredondado aos cêntimos (duas casas decimais / centésimas).
- **Rejeição de Arredondamentos Grosseiros**: É estritamente proibido aceitar valores inteiros truncados quando o cálculo envolve cêntimos (ex.: rejeitar $320\,922\text{ €}$ se o valor correto for $320\,922{,}89\text{ €}$; rejeitar $122\,391\text{ €}$ se for $122\,391{,}36\text{ €}$).
- **Equivalências Matemáticas e Flexibilidade**: Aceitam-se notações equivalentes para o mesmo valor numérico (ex.: $7{,}2\text{ €}$ para $7{,}20\text{ €}$, «7 euros e 20 cêntimos»), expressões aritméticas diretas ($650 \times 0{,}04$, $26 \times 3$, $650 + 78$) e equações com incógnitas ($J = 26$).
- **Taxas Percentuais**: Aceitam-se na forma percentual (ex.: $1{,}06\%$, $1{,}3\%$, $2\%$) ou na fração decimal equivalente ($0{,}0106$, $0{,}013$, $0{,}02$).

---

### 3. Dinâmica Pedagógica e Avaliação Formativa
- **Exemplos Guiados**: Decompostos passo a passo interativo. O estudante introduz os valores numéricos diretamente nos campos de texto para validação imediata e assimilação do método.
- **Exercícios de Aplicação (1 a 6)**: **Fotografia do caderno manuscrito obrigatória**. A IA multimodal (`gemini-3.5-flash-lite`) analisa o raciocínio matemático, operações intermédias e o resultado final.
- **Método Socrático e Pistas Pedagógicas**: Quando surge uma incorreção, o tutor nunca dá o resultado final; explica o fundamento do lapso e faculta uma pista pedagógica (*scaffolding*) orientando a correção no caderno.
- **Integridade da Avaliação (Sem «Recomeçar do Zero»)**: Foi eliminado qualquer botão de reinicialização arbitrária pelos alunos. Uma vez resolvido ou submetido, o histórico pedagógico é preservado integralmente na base de dados, garantindo fidelidade na avaliação contínua.

---

### 4. Estrutura Diferenciada por Tarefa e Novas Fichas
- **Tarefa 7 (Juros Simples)**:
  - *Bloco 1*: Exemplo 1 (Passos 1.1 a 1.3) $\to$ Desbloqueia os Exercícios de Aplicação 1, 2, 3 e 4.
  - *Bloco 2*: Exemplo 2 (Passos 2.1 e 2.2) $\to$ Desbloqueia os Exercícios de Aplicação 5 e 6.
- **Tarefa 8 (Juros Compostos)**:
  - *Estrutura Sequencial*: Exemplo 1 (Passos 1.1 a 1.4) $\to$ Exemplo 2 (Passos 2.1 e 2.2) $\to$ Desbloqueia simultaneamente os Exercícios de Aplicação 1 a 6.
- **Protocolo de Conversão de Novas Fichas**:
  - Cada nova ficha de trabalho convertida deve ser guardada em `tutor/fichas/` sob a forma de dois ficheiros Markdown (`.md`):
    1. `tarefa_XX_nome.md`: Enunciado completo, contextualização e formulação rigorosa das questões;
    2. `tarefa_XX_resolucoes_oficiais.md`: Resoluções oficiais com critérios de correção, chaves numéricas exatas, tolerâncias, passos esperados no caderno e pistas pedagógicas para o Gemini Vision.

---

### 5. Gestão de Turmas, Credenciais e Segurança (Modelo B)
- **Turmas e Cursos Profissionais Ativos**:
  - **10.º TPE/TOE** (Técnico de Produção e Operações Empresariais / Técnico de Operações Empresariais)
  - **10.º TCR** (Técnico de Comunicação e Relações Públicas)
- **Modelo de Credenciais Centralizado (Modelo B)**:
  - O professor faz a pré-carga dos alunos em lote (*batch import*) via interface web (`📥 Importar Lista de Alunos`) ou via linha de comandos (`python3 tutor/importar_alunos.py --importar`).
  - Cada aluno tem um *username* único gerado automaticamente a partir do nome e uma palavra-passe pessoal inicial (`1234`), cifrada com hash SHA-256.
  - O professor dispõe de controlo total para redefinir palavras-passe de alunos esquecidos diretamente no painel.
- **Segurança Absoluta da Senha Docente**:
  - A palavra-passe do professor (`DOCENTE_SENHA=profmat2026`) está configurada estritamente no ficheiro de ambiente `.env` e validada por hash SHA-256 no servidor.
  - É expressamente proibida a publicação ou injeção da palavra-passe docente em qualquer código HTML, CSS ou JavaScript enviado ao navegador.
- **Proteção Anti-Plágio de Cadernos (Hash SHA-256)**:
  - O servidor calcula uma impressão digital criptográfica para cada fotografia enviada. Tentativas de envio da mesma imagem por estudantes diferentes são bloqueadas e sinalizadas.

---

### 6. Monitorização Analítica do Professor
- **Métricas Focadas e Sem Redundâncias**:
  - Foram removidas as colunas vazias ou redundantes de «Interações» e «Taxas de Sucesso».
  - As métricas acompanhadas em tempo real na matriz por pergunta são:
    1. **Estado de Validação**: Validação a verde ($\checkmark$) ou pendente ($\times$);
    2. **Tentativas Realizadas**: Número de submissões registadas até à validação;
    3. **Pistas Solicitadas**: Pistas pedagógicas ativadas pelo aluno;
    4. **Duração**: Tempo real decorrido desde o início da visualização até à validação correta.
- **Filtros do Painel Docente**:
  - Filtro por Curso/Turma: `Todas as Turmas`, `10.º TPE/TOE` ou `10.º TCR`;
  - Filtro por Ficha/Tarefa (`Tarefa 7`, `Tarefa 8`);
  - Seletor dinâmico do aluno em análise.

---

### 7. Mapa Arquitetural do Ecossistema Técnico

| Ficheiro / Módulo | Função e Responsabilidade |
| :--- | :--- |
| `servidor_simulacao.py` | Servidor HTTP autónomo unificado (porta 8000), API REST, autenticação, rotas de estática e interface web responsiva (Aluno + Painel do Professor). |
| `tutor_engine.py` | Núcleo de gestão da base de dados SQLite (`tutor/dados/tutor.db`), sessões, importação de alunos, registo de tentativas e anti-plágio. |
| `avaliador_gemini.py` | Motor de inteligência artificial multimodal com Google Gemini (`gemini-3.5-flash-lite`), OCR de cadernos e geração de feedback formativo. |
| `dashboard.py` | Painel analítico de terminal e componentes Streamlit com visualização do progresso das turmas. |
| `importar_alunos.py` | Utilitário CLI para listagem, criação e importação massiva de turmas a partir de ficheiros de texto. |
| `fichas/` | Diretoria central das tarefas pedagógicas em formato Markdown (`.md`), imagens e resoluções de referência. |
| `.env` | Variáveis de ambiente protegidas (`GEMINI_API_KEY`, `GEMINI_MODEL`, `DOCENTE_SENHA`). |

</div>
