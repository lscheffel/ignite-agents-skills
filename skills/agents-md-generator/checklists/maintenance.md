# Checklist de Manutenção - AGENTS.md

## Detecção de Mudanças

- [ ] Novos arquivos/diretórios adicionados
- [ ] Arquivos/diretórios removidos
- [ ] Tecnologias mudaram (novas dependências)
- [ ] Padrões arquiteturais mudaram
- [ ] Comandos de build/test mudaram
- [ ] Processo de deploy mudou
- [ ] Governança mudou (branching, PR, etc.)

## Validação de Atualização

- [ ] AGENTS.md ainda reflete o estado atual do projeto
- [ ] Estrutura de diretórios está correta
- [ ] Comandos estão atualizados
- [ ] Tecnologias listadas estão corretas
- [ ] Skills recomendadas ainda são pertinentes
- [ ] Anti-patterns ainda são relevantes

## Processo de Atualização

### 1. Identificar Mudanças

```bash
# Comparar estrutura atual com AGENTS.md
diff <(find . -type f -not -path './.git/*' | sort) <(grep -oP '(?<=`)[^`]+' AGENTS.md | sort)
```

### 2. Atualizar Conteúdo

- [ ] Atualizar Visão Geral se propósito mudou
- [ ] Atualizar Estrutura se diretórios mudaram
- [ ] Atualizar Comandos se scripts mudaram
- [ ] Atualizar Tecnologias se dependências mudaram
- [ ] Atualizar Governança se processos mudaram

### 3. Validar Atualização

- [ ] Todas as seções obrigatórias presentes
- [ ] Nenhum placeholder não preenchido
- [ ] Conteúdo coerente com mudanças
- [ ] Formato Markdown válido

### 4. Commit

```bash
git add AGENTS.md
git commit -m "docs: update AGENTS.md to reflect project changes"
```

## Frequência de Revisão

### Automática (a cada deploy)

- [ ] Verificar se comandos básicos estão corretos
- [ ] Verificar se estrutura básica está correta

### Mensal

- [ ] Revisão completa do conteúdo
- [ ] Verificar se skills recomendadas ainda são pertinentes
- [ ] Atualizar anti-patterns se necessário

### A cada Mudança Significativa

- [ ] Nova feature principal
- [ ] Mudança de arquitetura
- [ ] Mudança de tecnologias
- [ ] Mudança de governança

## Critérios de Atualização Obrigatória

- [ ] Mudança em mais de 20% dos arquivos do projeto
- [ ] Nova tecnologia principal adicionada
- [ ] Mudança de arquitetura
- [ ] Mudança de processo de deploy
- [ ] Mudança de governança

## Critérios de Atualização Opcional

- [ ] Mudança em menos de 20% dos arquivos
- [ ] Adição de features incrementais
- [ ] Correções de bugs
- [ ] Atualizações de dependências menores

## Validação Automatizada

```bash
# Verificar se AGENTS.md está desatualizado
echo "=== Verificação de Atualização ==="

# Verificar estrutura
echo "Estrutura:"
diff <(ls -d */ | sort) <(grep -oP '(?<=`)[^`]+/' AGENTS.md | sort) || echo "Estrutura pode estar desatualizada"

# Verificar comandos
echo "Comandos:"
grep -q "npm run dev" AGENTS.md && echo "npm run dev: OK" || echo "npm run dev: POSSÍVEL ATUALIZAÇÃO"

# Verificar tecnologias
echo "Tecnologias:"
grep -q "package.json" AGENTS.md && echo "Node.js: OK" || echo "Node.js: POSSÍVEL ATUALIZAÇÃO"
```

## Critérios de Aprovação

- Todas as mudanças significativas refletidas
- Conteúdo ainda coerente com o projeto
- Formato válido
- Sem placeholders não preenchidos

## Critérios de Reprovação

- Mudanças significativas não refletidas
- Conteúdo incoerente com o projeto
- Formato inválido
- Placeholders não preenchidos
