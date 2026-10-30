# Tutor de Matemática Inteligente com Google Gemini
**Módulo P1: Modelos Matemáticos para a Cidadania**

<div align="justify">

Sistema de tutoria inteligente e avaliação formativa contínua em Matemática para o Ensino Profissional. A plataforma combina resolução passo a passo com desbloqueio adaptativo, avaliação multimodal de caligrafia e resoluções no caderno através do modelo de visão do Google Gemini, e painel analítico docente em tempo real.

---

### Principais Funcionalidades

1. **Tarefas Curriculares Integradas**:
   - **Tarefa 4: Matemática nos Salários** (vencimentos base, Segurança Social, IRS, subsídio de alimentação e salário líquido);
   - **Tarefa 5: Salário Bruto à Hora** (fórmula legal do Código do Trabalho, trabalho suplementar e horas extraordinárias);
   - **Tarefa 6: Imposto sobre o Rendimento (IRS)** (declaração anual, quociente conjugal, deduções específicas da Categoria A e escalões);
   - **Tarefa 7: Poupança e Crédito (Juros Simples)**;
   - **Tarefa 8: Juros Compostos** (regimes anual, semestral, trimestral e diário).

2. **Avaliação Multimodal com Visão Computacional (Google Gemini)**:
   - Leitura direta da caligrafia no caderno do aluno via OCR matemático;
   - Análise de fórmulas em notação LaTeX, passos intermédios e resultados finais;
   - Pistas pedagógicas socráticas formuladas exclusivamente na segunda pessoa do singular («tu»);
   - Deteção inteligente de submissões duplicadas por via de assinatura de imagem (*hash* criptográfico).

3. **Painel Analítico do Docente em Tempo Real**:
   - Acompanhamento do progresso de turmas e alunos individuais;
   - Métricas de taxas de sucesso, pistas pedagógicas acionadas e tempo médio até à validação;
   - Importação de alunos por turma a partir da interface;
   - Painel disponível via aplicação Web ou diretamente na linha de comandos do terminal.

---

### Instalação e Execução

1. **Configurar as Credenciais do Gemini**:
   Copia o ficheiro de exemplo e insere a tua chave de API da Google AI Studio:
   ```bash
   cp .env.example .env
   ```

2. **Iniciar o Servidor Interativo do Tutor**:
   ```bash
   python3 servidor_simulacao.py
   ```
   Abre o teu navegador em `http://localhost:8000` para aceder à interface de resolução do aluno e ao painel docente.

3. **Consultar o Painel no Terminal**:
   ```bash
   python3 dashboard.py 4  # Tarefa 4
   python3 dashboard.py 5  # Tarefa 5
   python3 dashboard.py 6  # Tarefa 6
   python3 dashboard.py 7  # Tarefa 7
   python3 dashboard.py 8  # Tarefa 8
   ```

---

### Estrutura do Projeto

* `servidor_simulacao.py`: Servidor HTTP central, interface web interativa do aluno e do professor, e rotas de API REST;
* `avaliador_gemini.py`: Integração com o Google Gemini Vision e rubricas oficiais de validação de resoluções manuscritas;
* `dashboard.py`: Módulo analítico de acompanhamento docente;
* `tutor_engine.py`: Motor de base de dados SQLite e registo de tentativas formativas;
* `fichas/`: Enunciados integrais e critérios de correção oficiais em Markdown com notação LaTeX.

</div>
