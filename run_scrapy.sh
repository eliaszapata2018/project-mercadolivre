#!/bin/bash

# Ir a la raíz del proyecto
cd "$(dirname "$0")"

# Ejecutar el spider usando scrapy.cfg y sin pasar settings manualmente
scrapy crawl mercado_ofertas -o data/products/ofertas_dia.jsonl

# Verificar si el archivo se generó correctamente
if [ -f data/products/ofertas_dia.jsonl ]; then
    echo "✅ Scraping finalizado. Archivo generado en data/products/"
else
    echo "❌ Scraping fallido. No se generó el archivo ofertas_dia.jsonl"
fi
