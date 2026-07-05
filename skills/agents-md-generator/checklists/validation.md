# Checklist de Validação - AGENTS.md

## Pré-Geração

- [ ] Projeto existe e tem estrutura básica
- [ ] Tecnologias podem ser detectadas
- [ ] Contexto pode ser determinado
- [ ] Template adequado está disponível

## Geração

- [ ] Contexto detectado corretamente
- [ ] Template selecionado apropriado
- [ ] Todos os placeholders preenchidos
- [ ] Conteúdo faz sentido para o contexto

## Validação Estrutural

- [ ] Arquivo existe
- [ ] Tem ≥30 linhas
- [ ] Tem todas as seções obrigatórias:
  - [ ] Visão Geral
  - [ ] Estrutura do Projeto
  - [ ] Padrões de Código
  - [ ] Comandos Importantes
  - [ ] Governança
  - [ ] Skills Recomendadas
  - [ ] Anti-patterns
  - [ ] Edge Cases
- [ ] Nenhum placeholder não preenchido
- [ ] Formato Markdown válido

## Validação de Conteúdo

- [ ] Descrição do projeto está correta
- [ ] Estrutura de diretórios reflete projeto real
- [ ] Comandos são relevantes para o projeto
- [ ] Governança está alinhada com práticas do projeto
- [ ] Skills recomendadas são pertinentes
- [ ] Anti-patterns são relevantes para o contexto
- [ ] Edge cases documentados são plausíveis

## Validação Técnica

- [ ] Comandos de build/test/deploy estão corretos
- [ ] Tecnologias listadas existem no projeto
- [ ] Padrões arquiteturais estão documentados
- [ ] Models de dados estão corretos (se aplicável)

## Pós-Geração

- [ ] Arquivo salvo no local correto
- [ ] Nome do arquivo está correto (AGENTS.md)
- [ ] Encoding UTF-8
- [ ] Sem caracteres especiais problemáticos

## Validação Automatizada

```bash
# Verificar se arquivo existe
test -f AGENTS.md && echo "OK" || echo "FAIL"

# Verificar número de linhas
wc -l AGENTS.md | awk '$1 >= 30 {print "OK"} {print "FAIL"}'

# Verificar seções obrigatórias
for section in "Visão Geral" "Estrutura" "Padrões" "Comandos" "Governança" "Skills" "Anti-patterns" "Edge Cases"; do
  grep -q "$section" AGENTS.md && echo "$section: OK" || echo "$section: FAIL"
done

# Verificar placeholders não preenchidos
grep -q '{{' AGENTS.md && echo "Placeholders não preenchidos: FAIL" || echo "Placeholders: OK"
```

## Critérios de Aprovação

- Todos os itens obrigatórios marcados
- Nenhum item crítico falhando
- Conteúdo coerente com o projeto
- Formato válido

## Critérios de Reprovação

- Arquivo não existe
- Menos de 30 linhas
- Seções obrigatórias faltando
- Placeholders não preenchidos
- Conteúdo incoerente com o projeto
