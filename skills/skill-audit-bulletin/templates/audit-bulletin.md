# Skill Audit Bulletin — {skill_name} (v{version})

**Audit date:** {date}
**Overall grade:** {S/A/B/C/D/F} — {0-100}/100
**One-line verdict:** {frase única, sem hedging}
**Recommended action:** {ADOTAR AS-IS / ADOTAR COM AJUSTES / REFATORAR / DEPRECIAR}

## 1. Executive Summary
- Ponto mais forte: {evidenciado}
- Ponto mais fraco: {evidenciado}
- Principal risco se implantada sem alteração: {1 frase}
- Esforço para alcançar a próxima faixa de nota: {BAIXO / MÉDIO / ALTO}

## 2. Compliance Estrutural e Metadata
| Campo | Status | Comentário |
|---|---|---|
| name | ✅/⚠️/❌ | |
| description | ✅/⚠️/❌ | |
| version | ✅/⚠️/❌ | |
| tags | ✅/⚠️/❌ | |
| related_skills | ✅/⚠️/❌ | |

## 3. Análise Semântica de Triggering
- Score da description: {0-10}
- Lacunas de cobertura de keywords: {lista + frase de exemplo}
- Risco de colisão com related/sibling skills: {lista + likelihood}
- Cenário(s) de falso positivo: {exemplo concreto}
- Cenário(s) de falso negativo: {exemplo concreto}

## 4. Aplicabilidade e Escopo
- Score de clareza de fronteira: {0-10}
- Solidez da decision tree: {evidenciado}
- Sobreposição/conflito com related_skills: {evidenciado}

## 5. Profundidade e Cobertura de Workflow
- Avaliação fase a fase: {tabela ou lista}
- Qualidade dos checkpoints: {evidenciado}
- Estimativa de cobertura de edge cases: {%} — faltando: {lista}

## 6. Correção Técnica e Robustez
- Exemplos/comandos validados: {lista com pass/fail + justificativa}
- Issues de correção encontrados: {evidenciado, com referência de seção}

## 7. Universalidade e Portabilidade
- Lock-ins de ambiente: {lista}
- Comportamento fora do ambiente assumido: {gracioso / falha silenciosa / desconhecido}

## 8. Manutenibilidade
- Disciplina de versionamento: {evidenciado}
- Modularidade (seções atualizáveis isoladamente?): {evidenciado}
- Risco de rot externo (horizonte de 12 meses): {lista + likelihood}

## 9. Ergonomia para o Agente Executor
- Acionabilidade sem inferência: {0-10}
- Adequação de densidade/tamanho: {evidenciado}
- Confiança excessiva no julgamento do modelo executor: {evidenciado}

## 10. Matriz de Risco
| Risco | Likelihood | Impacto | Mitigação (ref) |
|---|---|---|---|
| | | | → ver §13 |

## 11. Pros
- {bullet evidenciado}

## 12. Cons
- {bullet evidenciado} → mitigado em §13

## 13. Mitigações e Recomendações
### Quick wins (< 1h)
- {edição concreta e específica}
### Médio (estrutural mas escopado)
- {edição concreta e específica}
### Estrutural (nível de redesign)
- {edição concreta e específica}

## 14. Scoring Breakdown
| Categoria | Peso | Score (0-10) | Ponderado |
|---|---|---|---|
| Semantic Triggering Precision | 20% | | |
| Aplicabilidade / Clareza de Fronteira | 10% | | |
| Profundidade e Cobertura | 15% | | |
| Correção Técnica | 15% | | |
| Universalidade / Portabilidade | 10% | | |
| Manutenibilidade | 10% | | |
| Ergonomia do Agente Executor | 10% | | |
| Perfil de Risco (invertido) | 10% | | |
| **Total** | 100% | | **{X}/100** |

## 15. Veredito Final
{2-3 frases, diretas, sem hedging. Declarar explicitamente se esta skill é
segura para auto-load em um registry de produção hoje.}