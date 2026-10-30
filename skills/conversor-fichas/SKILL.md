---
name: conversor-fichas
description: Converte tarefas e critérios de resolução de Matemática em ficheiros Markdown padronizados com notação LaTeX, decomposição passo a passo e critérios rigorosos para o Tutor Inteligente.
---

# Skill: Conversor de Fichas para Formato Tutor

<div align="justify">

Converte enunciados originais (em Word/PDF) e propostas de resolução em pares de ficheiros Markdown estruturados na pasta `tutor/fichas/`:
1. `tarefa_XX_nome.md` (Enunciado e contexto);
2. `tarefa_XX_resolucoes_oficiais.md` (Critérios de correção, resoluções e pistas).

## 1. Estrutura Padronizada do Enunciado (`tarefa_XX_nome.md`)
- **Cabeçalho**: Identificação clara da tarefa e do tema curricular (Módulo P1: Modelos Matemáticos para a Cidadania);
- **Alinhamento**: Texto formatado com `<div align="justify">`;
- **Exemplos Guiados (1 e 2)**:
  - Decomposição em passos atómicos sequenciais;
  - Instruções formuladas na 2.ª pessoa do singular («tu»);
  - Fórmulas e dados rigorosamente em LaTeX (`$expressão$`);
- **Exercícios de Aplicação (1 a 6)**:
  - Enunciados completos com tabelas formatadas em Markdown e valores em LaTeX;
  - Indicação expressa de que a resolução deve ser realizada no caderno manuscrito e fotografada.

## 2. Estrutura Padronizada das Resoluções (`tarefa_XX_resolucoes_oficiais.md`)
- **Chaves Numéricas Exatas**: Arredondamento obrigatório às centésimas (2 casas decimais) para quantias monetárias (ex.: $320\,922{,}89\text{ €}$);
- **Múltiplos Métodos de Resolução**: Registo das várias estratégias matemáticas válidas (fórmulas diretas ou passos sucessivos) para prevenir falsos negativos pelo validador;
- **Pistas Pedagógicas Socráticas**: Orientações de apoio que guiam o aluno ao erro sem revelar a solução final;
- **Tratamento por «Tu»**: Redação integral em Português de Portugal e no tratamento por «tu» (*«deves verificar»*, *«repara no cálculo»*).

</div>
