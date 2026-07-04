---
name: documentation
description: Guia para criação e manutenção de documentação técnica de alta qualidade. Define padrões para README, ADRs, guias de API, documentação de arquitetura e docs-as-code. Use quando criar documentação, revisar docs, ou padronizar material técnico.
---

# Documentation

Guia para documentação técnica eficaz e padronizada.

## Quando Usar

- Criação de documentação de projeto
- Revisão de documentação existente
- Padronização de docs entre projetos
- Escrita de README, guias ou ADRs

## Princípios

1. **Docs-as-Code**: Documentação versionada no mesmo repo
2. **Single Source of Truth**: Uma fonte, não cópias
3. **Progressive Disclosure**: Informação básica primeiro, detalhes depois
4. **Actionable**: Todo documento deve ter um propósito e ação associada

## Padrões por Tipo

### README.md
- O que o projeto faz
- Por que existe
- Como começar (5 minutos)
- Links para docs detalhadas

### ADR (Architecture Decision Record)
- Decisão, contexto, consequências
- Histórico de decisões arquiteturais
- Veja skill `adr-generator`

### API Documentation
- Endpoints com exemplos request/response
- Códigos de erro
- Autenticação
- Rate limits

### Architecture Docs
- Diagramas de contexto
- Decisões arquiteturais
- Visão de componentes

## Formatação

- Use Markdown
- Headings hierárquicos (#, ##, ###)
- Code blocks com linguagem especificada
- Tabelas para dados estruturados
- Links internos relativos quando possível

## Manutenção

- Documentação desatualizada é pior que nenhuma
- Revise docs junto com código
- Marque como deprecated quando substituído
