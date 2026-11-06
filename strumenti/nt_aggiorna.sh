#!/bin/bash
# Sito New Trends: unica strada riproducibile.
# 1) genera da /opt/newtrends-sito/work (build.py, pages.py, i18n.py, assets_src.py) -> work/site
# 2) copia in newtrends/ (tiene le foto WebP già fatte)  3) foto WebP locali ed esterne + versione dei file
# Poi ./pubblica.sh "messaggio". Uso: strumenti/nt_aggiorna.sh
set -euo pipefail
cd "$(dirname "$0")/.."
( cd /opt/newtrends-sito/work && python3 -E -s build.py )
rsync -a --delete --exclude 'assets/img/*.webp' --exclude 'assets/img/ext/' --exclude 'LEGGIMI.txt' /opt/newtrends-sito/work/site/ newtrends/
python3 -I strumenti/nt_perf.py
python3 -I strumenti/nt_foto_esterne.py /opt/newtrends-sito/cache-foto-esterne
python3 -I strumenti/nt_perf.py | tail -1   # versione dei file dopo le foto
