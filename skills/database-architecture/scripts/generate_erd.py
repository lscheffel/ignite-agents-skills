#!/usr/bin/env python3
"""
Entity Relationship Diagram (ERD) Generator for PostgreSQL & SQLite Schemas.
Asset Type: script_doc
Parent Skill: database-architecture

Usage:
    python3 generate_erd.py --schema schema.sql --output erd.png
    python3 generate_erd.py --db-path ./app.sqlite3 --format mermaid

Arguments:
    --schema    Caminho para o arquivo SQL de DDL / Schema
    --db-path   Caminho para o banco SQLite3 ativo
    --format    Formato de saída: mermaid (padrão) ou png
    --output    Arquivo de destino para o diagrama
"""

import os
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Gera diagramas ERD a partir de esquemas relacionais.")
    parser.add_argument("--schema", help="Caminho do arquivo SQL com instruções CREATE TABLE")
    parser.add_argument("--db-path", help="Caminho para banco de dados SQLite local")
    parser.add_argument("--format", choices=["mermaid", "png"], default="mermaid", help="Formato de exportação")
    parser.add_argument("--output", default="erd.mmd", help="Caminho de saída")
    return parser.parse_args()

def extract_tables_and_relations(schema_text):
    """Extrai entidades e relacionamentos de chave estrangeira (FKs)"""
    pass

if __name__ == "__main__":
    args = parse_args()
    print(f"[*] Gerando ERD a partir de {args.schema or args.db_path} em formato {args.format}...")
