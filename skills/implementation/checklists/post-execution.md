# Checklist de Pós-Execução

> Executar este checklist após concluir toda a implementação governada.

---

## 1. Validação de Tarefas

- [ ] Todas as tarefas do TODO estão marcadas como "Concluído"
- [ ] Nenhuma tarefa está marcada como "Bloqueado"
- [ ] Nenhuma tarefa está marcada como "Em andamento"
- [ ] Tarefas "Adiadas" têm justificativa documentada

---

## 2. Validação de Build

- [ ] Build principal passa sem erros
- [ ] Build de tipos passa sem erros (typecheck)
- [ ] Não há warnings novos não justificados

---

## 3. Validação de Qualidade

- [ ] Lint passa sem erros
- [ ] Formatação está consistente
- [ ] Não há code smells introduzidos

---

## 4. Validação de Testes

- [ ] Testes unitários passam
- [ ] Testes de integração passam (se aplicável)
- [ ] Cobertura de testes não diminuiu
- [ ] Novos testes foram adicionados para novas funcionalidades

---

## 5. Validação de Documentação

- [ ] ADR está atualizada com status de implementação
- [ ] Blueprint está sincronizado com código implementado
- [ ] TODO reflete estado real (todas as tarefas concluídas)
- [ ] README foi atualizado (se aplicável)
- [ ] CHANGELOG foi atualizado (se aplicável)
- [ ] `related_skills` foram atualizados (se aplicável)

---

## 6. Validação de Registry

- [ ] `skills/index.json` foi atualizado (se nova skill)
- [ ] `validate-index.sh` passa
- [ ] `validate-skill.sh` passa para nova skill
- [ ] Todos os paths no `index.json` são válidos

---

## 7. Validação de Git

- [ ] Todos os commits seguem Conventional Commits
- [ ] Nenhum segredo ou credencial foi commitado
- [ ] Branch está limpa e pronta para PR
- [ ] Mensagens de commit são descritivas

---

## 8. Validação de Riscos

- [ ] Riscos remanescentes foram documentados
- [ ] Dívida técnica criada foi documentada
- [ ] Recomendações futuras foram registradas

---

## 9. Execution Report

- [ ] Execution Report foi gerado a partir do template
- [ ] Todos os campos obrigatórios foram preenchidos
- [ ] Relatório inclui lições aprendidas
- [ ] Relatório inclui métricas de implementação

---

## 10. Validação Final

- [ ] `validate-index.sh` passa para todas as skills
- [ ] `validate-skill.sh` passa para todas as skills
- [ ] Nenhum `related_skills` aponta para skill inexistente
- [ ] Workspace está limpo

---

## Aprovação Final

| Campo | Valor |
|-------|-------|
| Checklist completo | ✅/❌ |
| Validações passaram | ✅/❌ |
| Documentação sincronizada | ✅/❌ |
| Implementation Report gerado | ✅/❌ |
| Implementação considerada concluída | ✅/❌ |
