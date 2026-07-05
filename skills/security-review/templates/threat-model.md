# Threat Model Template

Modelo de ameaça simplificado baseado em STRIDE.

## Informações do Sistema

- **Nome do sistema:** {{system_name}}
- **Versão:** {{version}}
- **Data:** {{date}}
- **Revisor:** {{reviewer}}

## Endpoints/Expostos

| # | Endpoint/Componente | Descrição | Dados Sensíveis |
|---|---------------------|-----------|-----------------|
| 1 | {{endpoint_1}} | {{description_1}} | {{sensitive_1}} |
| 2 | {{endpoint_2}} | {{description_2}} | {{sensitive_2}} |

## Análise STRIDE

Para cada endpoint, avaliar:

### Spoofing (Falsificação)
- **Pergunta:** A autenticação é adequada?
- **Achados:** {{findings_spoofing}}
- **Risco:** 🔴 / 🟡 / 🟢

### Tampering (Adulteração)
- **Pergunta:** A integridade dos dados é protegida?
- **Achados:** {{findings_tampering}}
- **Risco:** 🔴 / 🟡 / 🟢

### Repudiação (Negação)
- **Pergunta:** Existe audit trail?
- **Achados:** {{findings_repudiation}}
- **Risco:** 🔴 / 🟡 / 🟢

### Information Disclosure (Vazamento)
- **Pergunta:** Dados sensíveis estão expostos?
- **Achados:** {{findings_disclosure}}
- **Risco:** 🔴 / 🟡 / 🟢

### Denial of Service (Indisponibilidade)
- **Pergunta:** Há rate limiting e proteção contra abuso?
- **Achados:** {{findings_dos}}
- **Risco:** 🔴 / 🟡 / 🟢

### Elevation of Privilege (Privilégio)
- **Pergunta:** O controle de acesso é adequado?
- **Achados:** {{findings_elevation}}
- **Risco:** 🔴 / 🟡 / 🟢

## Resumo de Riscos

| Severidade | Quantidade | Ações |
|------------|------------|-------|
| 🔴 Crítico | {{critical_count}} | Corrigir antes de merge |
| 🟡 Médio | {{medium_count}} | Corrigir em sprint atual |
| 🟢 Baixo | {{low_count}} | Documentar e planejar |

---

*Template de modelo de ameaça para ignite-agents-skills.*
