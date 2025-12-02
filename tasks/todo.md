# Piano di Sviluppo - Exoplanet Data Analyst Agent

## Obiettivo
Creare un agente AI che traduce domande in linguaggio naturale in query TAP SQL per interrogare il NASA Exoplanet Archive, esegue le query e restituisce specifiche di visualizzazione strutturate.

---

## Fase 1: Struttura Base e Configurazione
- [x] Creare la struttura delle directory del progetto
- [x] Creare requirements.txt con le dipendenze Python
- [x] Creare file di configurazione (.env.example, config.py)

## Fase 2: Mappings - Concetti Astronomici
- [x] Creare `src/mappings/concepts.py` con le mappature dei concetti (Earth-sized, Super-Earth, etc.)
- [x] Creare `src/mappings/__init__.py`

## Fase 3: Schema Cache - Metadati NASA
- [x] Creare `schema_cache/` con i metadati delle tabelle
- [x] Creare `src/tools/schema.py` per gestire lo schema lookup

## Fase 4: Tools - Esecuzione Query TAP
- [x] Creare `src/tools/tap_query.py` per eseguire query contro il NASA TAP endpoint
- [x] Creare `src/tools/sql_validator.py` per validare le query SQL
- [x] Creare `src/tools/__init__.py`

## Fase 5: Visualization - Specifiche di Visualizzazione
- [x] Creare `src/viz/spec_builder.py` per costruire le specifiche di visualizzazione
- [x] Creare `src/viz/__init__.py`

## Fase 6: Agent - Integrazione LLM
- [x] Creare `src/agent/prompts.py` con i template dei prompt
- [x] Creare `src/agent/state.py` per gestire lo stato della conversazione
- [x] Creare `src/agent/agent.py` per l'integrazione LLM principale
- [x] Creare `src/agent/server.py` per il server API
- [x] Creare `src/agent/__init__.py`

## Fase 7: Tests
- [x] Creare `tests/unit/test_mappings.py`
- [x] Creare `tests/unit/test_sql_validator.py`
- [x] Creare `tests/unit/test_viz_spec.py`
- [x] Creare `tests/integration/test_tap_query.py`
- [x] Creare `tests/conftest.py` con le fixtures

## Fase 8: Entry Points
- [x] Creare `src/__init__.py`
- [x] Aggiornare README.md con le istruzioni

## Fase 9: Query Cache (Aggiunta)
- [x] Creare `src/tools/cache.py` con cache in-memory e su file
- [x] Integrare cache in `tap_query.py`
- [x] Aggiungere endpoint `/cache/stats` e `/cache/clear`

## Fase 10: Frontend React (Aggiunta)
- [x] Setup Vite + React + Tailwind CSS
- [x] Creare componenti UI (Header, QueryInput, ExampleQueries)
- [x] Creare ResultCard con toggle SQL
- [x] Implementare ChartRenderer con Recharts (Scatter, Bar, Line, KPI, Table)
- [x] Styling tema spaziale con gradienti e animazioni

---

## Note Tecniche

### Architettura
```
User Question → LLM Agent → TAP SQL Generation → NASA TAP API → JSON Results → Visualization Spec
                    ↓
              [Query Cache]
                    ↓
            React Frontend → Recharts Visualization
```

### Endpoint NASA TAP
`https://exoplanetarchive.ipac.caltech.edu/TAP`

### Tabelle Principali
- `ps` - Planetary Systems
- `pscomppars` - Planetary Systems Composite Parameters
- `keplernames` - Kepler Objects of Interest

---

## Review Finale

### Riepilogo delle Modifiche

Implementazione completa dell'agente di analisi dati sugli esopianeti con frontend React:

1. **Backend Python**:
   - FastAPI server con CORS per frontend
   - LLM integration (OpenAI/Anthropic)
   - TAP query execution con validazione sicurezza
   - Query cache (in-memory + file, TTL 15min)
   - 15+ concept mappings astronomici

2. **Frontend React**:
   - Vite + React 18 + Tailwind CSS
   - Tema scuro "space" con gradienti
   - 6 tipi di visualizzazione (Recharts)
   - Query input con esempi suggeriti
   - SQL viewer con toggle
   - Indicatore cache status
   - Design responsive

### Stack Tecnologico
- **Backend**: Python 3.10+, FastAPI, Pydantic, requests
- **Frontend**: React 18, Vite, Tailwind CSS, Recharts, Lucide Icons
- **LLM**: OpenAI GPT-4o / Anthropic Claude
- **Data**: NASA Exoplanet Archive TAP API

### File Totali
- Backend: ~20 file Python
- Frontend: ~10 file JS/JSX/CSS
- Config: 5 file (package.json, vite.config, tailwind.config, etc.)
- Tests: 6 file

### Come Usare
```bash
# Backend
pip install -r requirements.txt
cp .env.example .env  # Configurare API key
python -m src.agent.server

# Frontend
cd frontend
npm install
npm run dev
```

Aprire `http://localhost:3000` per usare l'interfaccia.
