# Exemplo: README para API

```markdown
# Order Service API

API REST para gerenciamento de pedidos.

## Instalação

```bash
git clone https://github.com/org/order-service
npm install
cp .env.example .env
```

## Uso

```bash
npm run dev
# http://localhost:3000
```

## Endpoints

- POST /orders — Criar pedido
- GET /orders/:id — Buscar pedido
- PUT /orders/:id — Atualizar pedido

## Documentação

- [API Docs](docs/api.md)
- [Architecture](docs/architecture.md)
```