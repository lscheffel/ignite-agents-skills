# Checklist: Revisão de Schema

Use este checklist antes de commitar mudanças no schema do banco de dados.

## Estrutura

- [ ] Todas as tabelas têm chave primária definida
- [ ] PKs são UUID ou BIGSERIAL (não INTEGER)
- [ ] Chaves estrangeiras têm ON DELETE e ON UPDATE definidos
- [ ] Colunas NOT NULL estão corretamente configuradas
- [ ] Colunas nullable são intencionalmente nullable

## Tipos de Dados

- [ ] IDs são UUID (não VARCHAR ou INTEGER)
- [ ] Datas usam TIMESTAMPTZ (não TIMESTAMP)
- [ ] Valores monetários usam NUMERIC (não FLOAT)
- [ ] Strings têm tamanho máximo definido (VARCHAR(n))
- [ ] Booleanos são BOOLEAN (não INTEGER ou SMALLINT)

## Validação

- [ ] CHECK constraints para valores permitidos
- [ ] UNIQUE constraints para colunas que precisam ser únicas
- [ ] ENUMs são VARCHAR com CHECK (não tipos ENUM do banco)

## Performance

- [ ] Índices para queries frequentes
- [ ] Índices compostos seguem ordem de seletividade
- [ ] Sem SELECT * em queries de produção
- [ ] Paginação implementada para listas

## Documentação

- [ ] Comentários em todas as tabelas
- [ ] Comentários em colunas importantes
- [ ] Diagrama ER atualizado
- [ ] README do schema documentado

## Migrações

- [ ] Migração tem seção UP e DOWN
- [ ] Rollback testado localmente
- [ ] Migração não quebra dados existentes
- [ ] Nomeclatura consistente (YYYYMMDD_descricao)
