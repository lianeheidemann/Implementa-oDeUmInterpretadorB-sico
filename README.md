# Interpretador Simples em Python

Trabalho desenvolvido para a disciplina **Compiladores**.  
Este repositório contém um **interpretador básico em Python** que analisa e executa um subconjunto de instruções de uma linguagem fictícia.

## Funcionalidades Gerais

- **Analisador Léxico:** identifica números, identificadores, operadores, palavras-chave (`var`, `if`, `else`, `main`), tipos (`int`, `float`, `bool`) e símbolos (`;`, `{`, `}`, `:`).
- **Declaração e atribuição de variáveis** com suporte a tipos básicos.
- **Expressões aritméticas e lógicas** com precedência correta.
- **Estruturas condicionais** (`if-else`) e blocos aninhados.
- **Bloco principal** definido pela palavra-chave `main`.

## Observações

- Código educacional para demonstrar conceitos de **compiladores e interpretadores**.
- Não requer bibliotecas externas além do módulo padrão `re`.
- Erros de sintaxe ou caracteres inválidos geram exceções durante a execução.
