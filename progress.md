# Progress in week 1 :

Production code so far (src/):

config.py — a typed settings schema (pydantic-settings) that reads all env vars (API keys, storage paths) from .env into one settings object every other file imports from.

src/rag/chroma_client.py — opens a persistent connection to ChromaDB on disk and creates/returns the disaster_protocols collection. Pure connection setup, no data logic.

src/rag/build_knowledge_base.py — reads real PDFs (FEMA + 3 NDMA manuals) from data/raw/protocols/, splits each into clean sentence-boundary chunks, tags each chunk by disaster type (guessed from filename), and saves ~1911 chunks into ChromaDB as searchable vectors.

src/rag/search_knowledge_base.py — takes a plain question + optional disaster type, searches the saved chunks semantically, and returns the most relevant real text — filtered to that disaster type plus general guidance.

basially whole rag system made ( using chromadb )

# Progress in week 2 :

Tools : 
tools/vision_tool.py — raw OpenAI vision call (GPT-4o-mini), handles both public URLs and local files (base64), returns structured disaster findings.
tools/weather_tool.py — real current weather via Open-Meteo (free, no key).
tools/maps_tool.py — geocode (Nominatim), get_route (OSRM), find_nearby_hospitals/find_nearest_shelter (Overpass API, global, with retry + graceful failure).
tools/copernicus_tool.py — real Copernicus EMS activations feed (any disaster type), downloads real satellite-derived GeoTIFF maps, converts to viewable PNG.
tools/dataset_tool.py — loads Kaggle/HF disaster-tweets dataset as a normalized replay source.
tools/rss_tool.py (self-built, replaced GDELT) — live disaster news via RSS, same normalized shape.

Agents

agents/state.py — shared GenesisState shape (matches real agent output dicts).
agents/alert_monitor.py — check_alert (classifies one message), check_incoming (pulls from dataset or RSS, classifies each).
agents/image_analyzer.py — check_image, handles URL/local file/no-image cases via vision_tool.
agents/response_planner.py — make_response_plan, RAG-grounded 3-phase plan, now includes real weather via geocode+get_weather.
agents/quality_checker.py — check_plan, independent second-pass grounding check (situation + context vs plan), fixed false-positive on situation-derived facts.
agents/action_executor.py — run_actions, logs dispatch actions (no real SMS/email — scoped out), attaches real nearest-hospital lookup with graceful failure.
agents/graph.py — wires all 5 agents into a LangGraph state machine: conditional retry loop (Quality Checker fail → Response Planner) + human-approval interrupt before Action Executor.

Basically Agent orchestration + tools 


# Progress in week 3 :

main.py ( wiring everything up )





