#!/bin/bash
# Ricostruisce Edil Trend e Archi Trend da gruppo/ e pubblica tutto su GitHub Pages (in 1-2 minuti).
# Uso: ./pubblica.sh "cosa è cambiato"
set -euo pipefail
cd "$(dirname "$0")"
git pull -q --rebase origin main || true
rm -rf ediltrend architrend
python3 -E -s gruppo/edil3.py ediltrend >/dev/null
python3 -E -s gruppo/arch3.py architrend >/dev/null
if git ls-files --others --cached --exclude-standard | grep -Ei '\.(db|json|csv|xlsx|eml|env)$'; then echo "STOP: trovato un file che sembra contenere dati. Niente pubblicato."; exit 1; fi
git add -A
git diff --cached --quiet && { echo "Niente di nuovo da pubblicare."; exit 0; }
git commit -q -m "${1:-Aggiornamento siti}" && git push -q origin main && echo "Pubblicato: https://gruppo-newtrends.github.io/"
