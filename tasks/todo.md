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

---

## Note Tecniche

### Architettura
```
User Question → LLM Agent → TAP SQL Generation → NASA TAP API → JSON Results → Visualization Spec
```

### Endpoint NASA TAP
`https://exoplanetarchive.ipac.caltech.edu/TAP`

### Tabelle Principali
- `ps` - Planetary Systems
- `pscomppars` - Planetary Systems Composite Parameters
- `keplernames` - Kepler Objects of Interest

---

## Review

### Riepilogo delle Modifiche

Implementazione completa dell'agente di analisi dati sugli esopianeti:

1. **Struttura Base**: Directory organizzata secondo le specifiche CLAUDE.md, requirements.txt con pyvo, requests, fastapi, openai, anthropic, pytest.

2. **Mappings**: 15+ concetti astronomici mappati (Earth-sized, Super-Earth, Hot Jupiter, habitable zone, etc.) con aliases per variazioni comuni.

3. **Schema Cache**: JSON con metadati per tabelle ps, pscomppars, keplernames. Tool per lookup e validazione colonne.

4. **Tools TAP**:
   - `tap_query.py`: Esecuzione query con validazione sicurezza (solo SELECT, no DROP/DELETE)
   - `sql_validator.py`: Validazione schema, rilevamento SELECT *, controllo LIMIT

5. **Visualization**: Spec builder con supporto per scatter, line_chart, bar_chart, histogram, table, kpi. Suggerimenti automatici basati su colonne.

6. **Agent**:
   - Prompt system completo con schema reference e concept mappings
   - State management per contesto conversazionale
   - Server FastAPI con endpoint /ask, /clear, /health, /schema

7. **Tests**: Unit tests per mappings, SQL validator, viz spec. Integration tests per query TAP reali.

### File Creati (20 file)
- `requirements.txt`
- `.env.example`
- `src/config.py`
- `src/__init__.py`
- `src/mappings/__init__.py`
- `src/mappings/concepts.py`
- `src/tools/__init__.py`
- `src/tools/schema.py`
- `src/tools/tap_query.py`
- `src/tools/sql_validator.py`
- `src/viz/__init__.py`
- `src/viz/spec_builder.py`
- `src/agent/__init__.py`
- `src/agent/prompts.py`
- `src/agent/state.py`
- `src/agent/agent.py`
- `src/agent/server.py`
- `schema_cache/columns.json`
- `tests/` (6 file)
- `README.md` (aggiornato)
