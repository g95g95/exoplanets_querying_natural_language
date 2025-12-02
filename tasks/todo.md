# Piano di Sviluppo - Exoplanet Data Analyst Agent

## Obiettivo
Creare un agente AI che traduce domande in linguaggio naturale in query TAP SQL per interrogare il NASA Exoplanet Archive, esegue le query e restituisce specifiche di visualizzazione strutturate.

---

## Fase 1: Struttura Base e Configurazione
- [ ] Creare la struttura delle directory del progetto
- [ ] Creare requirements.txt con le dipendenze Python
- [ ] Creare file di configurazione (.env.example, config.py)

## Fase 2: Mappings - Concetti Astronomici
- [ ] Creare `src/mappings/concepts.py` con le mappature dei concetti (Earth-sized, Super-Earth, etc.)
- [ ] Creare `src/mappings/__init__.py`

## Fase 3: Schema Cache - Metadati NASA
- [ ] Creare `schema_cache/` con i metadati delle tabelle
- [ ] Creare `src/tools/schema.py` per gestire lo schema lookup

## Fase 4: Tools - Esecuzione Query TAP
- [ ] Creare `src/tools/tap_query.py` per eseguire query contro il NASA TAP endpoint
- [ ] Creare `src/tools/sql_validator.py` per validare le query SQL
- [ ] Creare `src/tools/__init__.py`

## Fase 5: Visualization - Specifiche di Visualizzazione
- [ ] Creare `src/viz/spec_builder.py` per costruire le specifiche di visualizzazione
- [ ] Creare `src/viz/__init__.py`

## Fase 6: Agent - Integrazione LLM
- [ ] Creare `src/agent/prompts.py` con i template dei prompt
- [ ] Creare `src/agent/state.py` per gestire lo stato della conversazione
- [ ] Creare `src/agent/agent.py` per l'integrazione LLM principale
- [ ] Creare `src/agent/server.py` per il server API
- [ ] Creare `src/agent/__init__.py`

## Fase 7: Tests
- [ ] Creare `tests/unit/test_mappings.py`
- [ ] Creare `tests/unit/test_sql_validator.py`
- [ ] Creare `tests/unit/test_viz_spec.py`
- [ ] Creare `tests/integration/test_tap_query.py`
- [ ] Creare `tests/conftest.py` con le fixtures

## Fase 8: Entry Points
- [ ] Creare `src/__init__.py`
- [ ] Aggiornare README.md con le istruzioni

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
(Da compilare alla fine dello sviluppo)
