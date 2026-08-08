

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

