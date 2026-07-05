# Checklist de Pré-Execução

> Executar este checklist antes de iniciar qualquer implementação governada.

---

## 1. Validação de Artefatos

- [ ] ADR existe e está em `docs/adr/ADR-XXX.md`
- [ ] ADR contém seção "Decisão" preenchida
- [ ] ADR contém seção "Contexto" preenchida
- [ ] ADR contém seção "Consequências" preenchida
- [ ] Blueprint existe em `docs/adr/ADR-XXX-BP.md`
- [ ] Blueprint contém tarefas documentadas com dependências
- [ ] Blueprint contém estimativas de tempo
- [ ] TODO existe em `docs/adr/ADR-XXX-TODO.md`
- [ ] TODO contém tarefas com estados (pendente/em andamento/concluído)
- [ ] TODO contém dependências entre tarefas
- [ ] TODO contém prioridades definidas

---

## 2. Validação de Coerência

- [ ] Tarefas do Blueprint existem no TODO
- [ ] Dependências no TODO são consistentes com Blueprint
- [ ] Estimativas no TODO são consistentes com Blueprint
- [ ] Nenhuma tarefa está duplicada entre Blueprint e TODO
- [ ] ADR está alinhada com o escopo do Blueprint

---

## 3. Validação do Ambiente

- [ ] Branch atual não é main/master (ou há PR aberto)
- [ ] Workspace está limpo (sem uncommitted changes)
- [ ] Branch está atualizada com remote
- [ ] Não há conflitos de merge pendentes
- [ ] Diretório de trabalho está correto

---

## 4. Validação de Arquivos Impactados

- [ ] Todos os arquivos listados no Blueprint existem
- [ ] Arquivos estão acessíveis (permissões corretas)
- [ ] Não há arquivos lockados por outro processo
- [ ] Backup foi considerado (se aplicável)

---

## 5. Validação de Critérios

- [ ] Critérios de aceite estão definidos no TODO
- [ ] Critérios de rollback estão definidos no Blueprint
- [ ] Testes relevantes foram identificados
- [ ] Comandos de validação foram documentados

---

## 6. Validação de Dependências Externas

- [ ] Skills relacionadas estão disponíveis no registry
- [ ] Dependências de build estão instaladas
- [ ] Ferramentas de lint/test estão configuradas
- [ ] CI/CD está funcional (se aplicável)

---

## 7. Geração do Execution Contract

- [ ] Execution Contract foi gerado a partir do template
- [ ] Todos os campos obrigatórios foram preenchidos
- [ ] Contrato foi validado pelo agente
- [ ] Próximo passo foi definido

---

## 8. Construção do Change Plan

- [ ] DAG foi construído a partir do TODO
- [ ] DAG está livre de ciclos
- [ ] Ordem de execução foi definida (topological sort)
- [ ] Tarefas paralelizáveis foram identificadas
- [ ] Estimativa total foi calculada

---

## Aprovação

| Campo | Valor |
|-------|-------|
| Checklist completo | ✅/❌ |
| Contrato aprovado | ✅/❌ |
| Plano aprovado | ✅/❌ |
| Implementação autorizada | ✅/❌ |
