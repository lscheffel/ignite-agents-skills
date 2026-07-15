---
name: adr-archive
description: Automatiza o arquivamento de ADRs plenamente implementadas de forma token-efficient. Avalia silenciosamente o status das tarefas nos arquivos TODO e, se a ADR estiver finalizada, gerencia a criação do ER faltante e arquiva os artefatos de execução, deixando apenas os ERs e ADRs pendentes visíveis na raiz.
version: 1.0.0
tags:
- architecture
- adr
- cleanup
- governance
- archive
related_skills:
- adr-generator
- implementation
---

# ADR Archive (Janitor)

Audita todas as ADRs do repositório para manter a pasta de governança organizada. Funciona como um "garbage collector" para artefatos de execução.

## Estratégia de Arquivamento

- **O que fica na raiz de ADRs (`docs/adr/`):**
  1. ADRs que ainda não foram plenamente implementadas (junto com seus BP, TODO, PI).
  2. Arquivos `ER` (Execution Reports) das ADRs que **já foram** implementadas. O ER serve como certificado de implementação na raiz.
- **O que vai para o arquivo morto (`docs/adr/archive/`):**
  1. O arquivo principal da `ADR` (que já foi executada), o `BP`, o `TODO` e o `PI`.

> Isso deixa visualmente óbvio quais arquiteturas estão pendentes (as ADRs visíveis) e quais já foram finalizadas (os ERs visíveis).

## Workflow (Passo a Passo para o Agente)

Sempre que a skill for invocada (ex: `/janitor`, "arquive as adrs", "limpe as adrs"):

1. **Rode o Auditor Nativo**
   - Execute o script python interno para mapear as ADRs gastando 0 tokens na leitura.
   ```bash
   python ~/.gemini/config/skills/adr-archive/scripts/audit.py .
   ```

2. **Analise o Output e atue nas Flags**

   - **`NEEDS_ER: ADR-XXX`**
2. **Analise o Output e o Relatório**
   O script retornará rapidamente no terminal as flags de anomalia. Porém, **a principal fonte da verdade agora é o relatório gerado**.
   O script imprimirá no final: `Report generated: <path/to/report.md>`. 
   
   - Se houver flags `READY_TO_ARCHIVE`, `ARCHIVED_NEEDS_ER` ou `ARCHIVED_MISTAKE_RETURN`, execute as mesmas regras abaixo:

   - **`READY_TO_ARCHIVE: ADR-XXX`**
     A ADR e o seu TODO foram integralmente concluídos, e o ER correspondente já existe na raiz.
     *Comando esperado:*
     ```bash
     python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --archive ADR-XXX
     ```

   - **`ARCHIVED_NEEDS_ER: ADR-XXX`**
     Se a ADR está arquivada e plenamente implementada, mas está faltando o ER na raiz:
     * Crie manualmente o artefato `ADR-XXX-ER.md` contendo o relatório de conclusão (conforme template das skills de governança).
     * Salve o ER sempre na pasta **RAIZ** das ADRs (ex: `docs/adr/ADR-XXX-ER.md`), **NÃO** no diretório archive.

   - **`ARCHIVED_MISTAKE_RETURN: ADR-XXX`**
     Se a ADR está arquivada, não possui ER e não está plenamente concluída (ainda possui pendências parciais ou totais no TODO):
     * A ADR foi arquivada prematuramente ou por erro humano.
     * Devolva todos os artefatos da ADR do `/archive` de volta para a pasta raiz das ADRs.
     * Comando esperado: `mv docs/adr/archive/ADR-XXX* docs/adr/`

3. **Consolidação de Débitos Técnicos**
   - Use a ferramenta `view_file` para ler o arquivo do relatório gerado (caminho em `docs/reports/adr-archive-report-*.md`).
   - Avalie a seção de "Débitos Técnicos Consolidados". Se existirem débitos relevantes e expressivos, sugira ao usuário a criação de uma nova ADR de Refatoração e Débito Técnico para atacá-los sistematicamente.

4. **Reporte ao Usuário**
   Forneça um relatório rápido das ações tomadas.
   Apresente ao usuário (resumidamente) a lista de débitos técnicos encontrada (ou diga que não há débitos).
