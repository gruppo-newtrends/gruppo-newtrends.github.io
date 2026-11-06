# Siti del Gruppo New Trends

Archivio **pubblico**: contiene solo le pagine dei siti, che chiunque vede già online. Niente dati dei clienti, niente password.
Il CRM e i dati restano sul server del gruppo (archivio privato `new-trends`).

| Cartella | Sito | Indirizzo |
|---|---|---|
| `gruppo/edil3.py` + `gruppo/src` | Edil Trend | https://gruppo-newtrends.github.io/ediltrend/ |
| `gruppo/arch3.py` + `gruppo/src` | Archi Trend | https://gruppo-newtrends.github.io/architrend/ |
| `newtrends/` | New Trends (pagine già pronte) | https://gruppo-newtrends.github.io/newtrends/it/ |
| `firma/` | immagini della firma email | https://gruppo-newtrends.github.io/firma/ |

Le cartelle `ediltrend/` e `architrend/` sono generate: non modificarle a mano. Cambia `gruppo/edil3.py`, `gruppo/arch3.py` o `gruppo/src/`, poi esegui `./pubblica.sh "cosa è cambiato"` (serve Python con Pillow). Il sito New Trends in `newtrends/` si modifica direttamente. Ogni push sul ramo `main` va online in 1-2 minuti.
I moduli dei siti mandano le richieste al CRM sul server: `https://crm-newtrends.2-29-109-125.sslip.io/api/pubblico/richiesta`.

Provare in locale: `pip install pillow` poi `python3 gruppo/edil3.py /tmp/edil` e `python3 gruppo/arch3.py /tmp/archi`.
