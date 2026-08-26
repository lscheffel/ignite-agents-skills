# Example: Repo Bootstrap

## Created Structure
```
my-service/
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── architecture/
│   └── adr/
└── src/
    ├── domain/
    ├── application/
    └── infrastructure/
```

## Commands
```bash
# Create structure
mkdir -p docs/{adr,api,architecture}
mkdir -p .github/workflows

# Copy templates
cp templates/*.md .
cp templates/ci.yml .github/workflows/
```

## Result
Repo ready for development with all governance files in place.