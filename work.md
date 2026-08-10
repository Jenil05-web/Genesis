

### 03_agent_orchestration.ipynb
- [x] Minimal 2-node LangGraph (learned add_node/add_edge/compile/invoke)
- [x] Added conditional edges — Quality Checker fail/pass routing with retry_count safety valve
- [x] Added MemorySaver checkpointer + interrupt_before for human-approval gate
- [x] Confirmed pause/resume works via thread_id
- Notes: this is the actual skeleton for src/agents/graph.py — 5 real nodes, same wiring


Alert Monitor says "this is a flood, severity high"
Response Planner queries ChromaDB: "get me flood-relevant protocol chunks"
Those real chunks get inserted into the prompt as context
The LLM drafts a plan using that context, not its own assumptions
Quality Checker later verifies the plan actually stuck to that context (didn't invent things — same Faithfulness idea)

### RAG system (src/rag/)
- [x] chroma_client.py — persistent client + collection singleton
- [x] build_knowledge_base.py — reads PDFs, splits by sentence boundary, tags by disaster type, saves to Chroma
- [x] search_knowledge_base.py — semantic search with disaster_type + general fallback filtering
- [x] Ingested 4 real manuals (FEMA CPG 101, NDMA flood/earthquake/cyclone) — 1911 chunks
- Notes: fixed initial bug — first chunking approach cut words mid-way (raw character slicing); switched to sentence-boundary splitting

### Agents (src/agents/)
- [x] response_planner.py — RAG-grounded 3-phase plan via GPT-4o-mini
- [x] image_analyzer.py + tools/vision_tool.py — handles URL, local file, and no-image cases
- Notes: grounded field in response_planner is self-reported, not trustworthy — real check comes in quality_checker.py

### src/tools/copernicus_tool.py
- [x] list_activations(disaster_type, limit) — real CEMS activations feed, any category
- [x] download_activation_map_image(code) — downloads ZIP, extracts GeoTIFF, converts to PNG
- [x] Fixed nodata/NaN bug causing blank images
- Limitation: CEMS rasters are often SAR (radar), not optical — vision LLM can't reliably read damage from raw radar backscatter. Documented, not solved.