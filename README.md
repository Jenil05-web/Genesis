<div align="center">

<!-- Animated header SVG -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 220" width="900">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#07090e"/>
      <stop offset="100%" style="stop-color:#0f1219"/>
    </linearGradient>
    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:0"/>
      <stop offset="50%" style="stop-color:#2563eb;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#2563eb;stop-opacity:0"/>
    </linearGradient>
    <!-- Pulse filter -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="220" fill="url(#bg)" rx="12"/>

  <!-- Animated scan line -->
  <rect x="0" y="0" width="900" height="1" fill="url(#lineGrad)" opacity="0.6">
    <animateTransform attributeName="transform" type="translate" values="0,0;0,219;0,0" dur="4s" repeatCount="indefinite" calcMode="ease-in-out"/>
  </rect>

  <!-- Grid lines (subtle) -->
  <line x1="0" y1="55" x2="900" y2="55" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  <line x1="0" y1="110" x2="900" y2="110" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  <line x1="0" y1="165" x2="900" y2="165" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  <line x1="225" y1="0" x2="225" y2="220" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  <line x1="450" y1="0" x2="450" y2="220" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  <line x1="675" y1="0" x2="675" y2="220" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>

  <!-- Hexagonal logo mark -->
  <g transform="translate(70,110)" filter="url(#glow)">
    <!-- Outer hex -->
    <polygon points="0,-38 33,-19 33,19 0,38 -33,19 -33,-19"
             fill="none" stroke="#2563eb" stroke-width="1.8" stroke-opacity="0.9">
      <animate attributeName="stroke-opacity" values="0.9;0.4;0.9" dur="3s" repeatCount="indefinite"/>
    </polygon>
    <!-- Inner hex -->
    <polygon points="0,-24 21,-12 21,12 0,24 -21,12 -21,-12"
             fill="none" stroke="#2563eb" stroke-width="0.9" stroke-opacity="0.4">
      <animate attributeName="stroke-opacity" values="0.4;0.8;0.4" dur="3s" repeatCount="indefinite"/>
    </polygon>
    <!-- Crosshair lines -->
    <line x1="0" y1="-38" x2="0" y2="-26" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <line x1="0" y1="26" x2="0" y2="38" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <line x1="-33" y1="-19" x2="-23" y2="-13" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <line x1="23" y1="13" x2="33" y2="19" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <line x1="33" y1="-19" x2="23" y2="-13" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <line x1="-23" y1="13" x2="-33" y2="19" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <!-- Center reticle -->
    <circle cx="0" cy="0" r="7" fill="none" stroke="#2563eb" stroke-width="1.4">
      <animate attributeName="r" values="7;9;7" dur="2.5s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="1;0.4;1" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="2.5" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <!-- Pulse ring -->
    <circle cx="0" cy="0" r="12" fill="none" stroke="#2563eb" stroke-width="1" stroke-opacity="0">
      <animate attributeName="r" values="12;38;12" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.5;0;0.5" dur="3s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- GENESIS wordmark -->
  <text x="135" y="97" font-family="'Helvetica Neue', Arial, sans-serif"
        font-size="54" font-weight="800" letter-spacing="-2" fill="#dde3ef">GENESIS</text>

  <!-- Tagline -->
  <text x="137" y="126" font-family="'Helvetica Neue', Arial, sans-serif"
        font-size="14" font-weight="400" letter-spacing="4" fill="#6b7a96">EMERGENCY RESPONSE ORCHESTRATION</text>

  <!-- Separator -->
  <line x1="135" y1="142" x2="560" y2="142" stroke="#2563eb" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Descriptor text -->
  <text x="137" y="164" font-family="'Helvetica Neue', Arial, sans-serif"
        font-size="13" fill="#4e5668">Five AI agents · LangGraph state machine · Human-in-the-loop approval</text>

  <!-- Animated status dot cluster -->
  <g transform="translate(137,188)">
    <circle cx="0" cy="0" r="4" fill="#22c55e">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="10" y="4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" fill="#6b7a96">ALERT MONITOR</text>

    <circle cx="130" cy="0" r="4" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite" begin="0.4s"/>
    </circle>
    <text x="140" y="4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" fill="#6b7a96">RAG PLANNER</text>

    <circle cx="255" cy="0" r="4" fill="#d97706">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite" begin="0.8s"/>
    </circle>
    <text x="265" y="4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" fill="#6b7a96">QUALITY CHECK</text>

    <circle cx="395" cy="0" r="4" fill="#ef4444">
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" begin="1.2s"/>
    </circle>
    <text x="405" y="4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" fill="#6b7a96">HUMAN GATE</text>
  </g>

  <!-- Right side — animated pipeline visualization -->
  <g transform="translate(710,110)">
    <!-- Vertical spine -->
    <line x1="0" y1="-80" x2="0" y2="80" stroke="#2563eb" stroke-opacity="0.15" stroke-width="1.5"/>

    <!-- Pipeline nodes with staggered blink -->
    <!-- Node 1 -->
    <circle cx="0" cy="-64" r="7" fill="#0f1219" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <circle cx="0" cy="-64" r="3" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.2;1" dur="3s" begin="0s" repeatCount="indefinite"/>
    </circle>
    <text x="16" y="-60" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#4e5668">Alert Monitor</text>

    <!-- Connector pulse -->
    <circle cx="0" cy="-44" r="2" fill="#2563eb" opacity="0">
      <animate attributeName="cy" values="-56;-40" dur="1.5s" begin="0s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" begin="0s" repeatCount="indefinite"/>
    </circle>

    <!-- Node 2 -->
    <circle cx="0" cy="-32" r="7" fill="#0f1219" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <circle cx="0" cy="-32" r="3" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.2;1" dur="3s" begin="0.5s" repeatCount="indefinite"/>
    </circle>
    <text x="16" y="-28" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#4e5668">Image Analyzer</text>

    <!-- Connector pulse -->
    <circle cx="0" cy="-12" r="2" fill="#2563eb" opacity="0">
      <animate attributeName="cy" values="-24;-8" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
    </circle>

    <!-- Node 3 -->
    <circle cx="0" cy="0" r="7" fill="#0f1219" stroke="#2563eb" stroke-width="1.4" stroke-opacity="0.8"/>
    <circle cx="0" cy="0" r="3" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.2;1" dur="3s" begin="1s" repeatCount="indefinite"/>
    </circle>
    <text x="16" y="4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#4e5668">Planner + QA</text>

    <!-- Connector pulse -->
    <circle cx="0" cy="20" r="2" fill="#d97706" opacity="0">
      <animate attributeName="cy" values="8;24" dur="1.5s" begin="1s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" begin="1s" repeatCount="indefinite"/>
    </circle>

    <!-- Node 4 (human gate) -->
    <circle cx="0" cy="32" r="7" fill="#0f1219" stroke="#d97706" stroke-width="1.4">
      <animate attributeName="stroke-opacity" values="1;0.3;1" dur="2s" begin="0s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="32" r="3" fill="#d97706">
      <animate attributeName="opacity" values="1;0.2;1" dur="2s" begin="0s" repeatCount="indefinite"/>
    </circle>
    <text x="16" y="36" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#d97706">Human Approval</text>

    <!-- Connector pulse -->
    <circle cx="0" cy="52" r="2" fill="#22c55e" opacity="0">
      <animate attributeName="cy" values="40;56" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
    </circle>

    <!-- Node 5 -->
    <circle cx="0" cy="64" r="7" fill="#0f1219" stroke="#22c55e" stroke-width="1.4" stroke-opacity="0.8"/>
    <circle cx="0" cy="64" r="3" fill="#22c55e">
      <animate attributeName="opacity" values="1;0.2;1" dur="3s" begin="1.5s" repeatCount="indefinite"/>
    </circle>
    <text x="16" y="68" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#4e5668">Executor</text>
  </g>
</svg>

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3.11-07090e?style=flat-square&labelColor=1e2433&color=2563eb" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/LangGraph-Agent%20Orchestration-07090e?style=flat-square&labelColor=1e2433&color=2563eb" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-07090e?style=flat-square&labelColor=1e2433&color=2563eb" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-07090e?style=flat-square&labelColor=1e2433&color=2563eb" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-07090e?style=flat-square&labelColor=1e2433&color=22c55e" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Render-Deployed-07090e?style=flat-square&labelColor=1e2433&color=22c55e" alt="Render"/>
  <img src="https://img.shields.io/badge/Tests-pytest-07090e?style=flat-square&labelColor=1e2433&color=6b7a96" alt="Tests"/>
</p>

</div>

---

Genesis turns a chaotic disaster — SOS text, satellite imagery, weather, real emergency-response manuals — into one grounded, human-approved response plan. Five agents, one LangGraph state machine, real data at every step.

---

## Table of Contents

- [The Problem](#the-problem)
- [What Genesis Does](#what-genesis-does)
- [Architecture](#architecture)
- [Walking Through a Real Incident](#walking-through-a-real-incident)
- [Real Data Sources](#real-data-sources)
- [Tech Stack](#tech-stack)
- [Engineering Decisions](#engineering-decisions)
- [Known Limitations](#known-limitations)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Tests](#tests)
- [Roadmap](#roadmap)

---

## The Problem

When a disaster hits, the information that could save lives is scattered: SOS posts on social media, satellite imagery showing which roads are impassable, weather data on whether things are getting worse, and official response protocols nobody has time to read in the moment. Nobody is looking at all of it at once — so resources go to the wrong places and help arrives late.

---

## What Genesis Does

<!-- Animated agent pipeline diagram -->
<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 100" width="860">
  <defs>
    <linearGradient id="flowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#22c55e;stop-opacity:0.8"/>
    </linearGradient>
  </defs>
  <rect width="860" height="100" fill="#07090e" rx="8"/>

  <!-- Flow line -->
  <line x1="40" y1="50" x2="820" y2="50" stroke="#1e2433" stroke-width="2"/>
  <!-- Animated flow dot -->
  <circle cx="40" cy="50" r="3.5" fill="#2563eb" opacity="0.9">
    <animateMotion dur="4s" repeatCount="indefinite" calcMode="linear">
      <mpath href="#flowPath"/>
    </animateMotion>
  </circle>
  <path id="flowPath" d="M40,50 L820,50" fill="none"/>

  <!-- Node 1: Alert Monitor -->
  <circle cx="80" cy="50" r="16" fill="#0f1219" stroke="#2563eb" stroke-width="1.5"/>
  <text x="80" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#2563eb" font-weight="700">ALERT</text>
  <text x="80" y="80" text-anchor="middle" font-family="Arial" font-size="9" fill="#6b7a96">Alert Monitor</text>

  <!-- Arrow -->
  <polygon points="135,46 145,50 135,54" fill="#1e2433"/>

  <!-- Node 2: Image Analyzer -->
  <circle cx="185" cy="50" r="16" fill="#0f1219" stroke="#2563eb" stroke-width="1.5"/>
  <text x="185" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#2563eb" font-weight="700">IMAGE</text>
  <text x="185" y="80" text-anchor="middle" font-family="Arial" font-size="9" fill="#6b7a96">Image Analyzer</text>

  <!-- Arrow -->
  <polygon points="240,46 250,50 240,54" fill="#1e2433"/>

  <!-- Node 3: Planner -->
  <circle cx="300" cy="50" r="16" fill="#0f1219" stroke="#2563eb" stroke-width="1.5"/>
  <text x="300" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#2563eb" font-weight="700">PLAN</text>
  <text x="300" y="80" text-anchor="middle" font-family="Arial" font-size="9" fill="#6b7a96">Planner</text>

  <!-- Arrow to QA -->
  <polygon points="355,46 365,50 355,54" fill="#1e2433"/>

  <!-- Node 4: Quality Checker -->
  <circle cx="415" cy="50" r="16" fill="#0f1219" stroke="#d97706" stroke-width="1.5"/>
  <text x="415" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#d97706" font-weight="700">QA</text>
  <text x="415" y="80" text-anchor="middle" font-family="Arial" font-size="9" fill="#6b7a96">Quality Check</text>

  <!-- Retry arrow (curved back) -->
  <path d="M431,36 Q415,10 300,10 Q283,10 284,34" fill="none" stroke="#d97706" stroke-width="1" stroke-dasharray="4,3" stroke-opacity="0.5"/>
  <polygon points="281,37 284,28 290,34" fill="#d97706" opacity="0.5"/>
  <text x="360" y="10" text-anchor="middle" font-family="Arial" font-size="8" fill="#d97706" opacity="0.7">retry (max 3)</text>

  <!-- Arrow to approval -->
  <polygon points="470,46 480,50 470,54" fill="#1e2433"/>

  <!-- Node 5: Human Approval -->
  <circle cx="540" cy="50" r="20" fill="#0f1219" stroke="#d97706" stroke-width="2">
    <animate attributeName="stroke-opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="540" y="47" text-anchor="middle" font-family="Arial" font-size="8" fill="#d97706" font-weight="700">HUMAN</text>
  <text x="540" y="58" text-anchor="middle" font-family="Arial" font-size="8" fill="#d97706" font-weight="700">GATE</text>
  <text x="540" y="82" text-anchor="middle" font-family="Arial" font-size="9" fill="#d97706">⚡ Approval</text>

  <!-- Arrow to executor -->
  <polygon points="600,46 610,50 600,54" fill="#1e2433"/>

  <!-- Node 6: Executor -->
  <circle cx="660" cy="50" r="16" fill="#0f1219" stroke="#22c55e" stroke-width="1.5"/>
  <text x="660" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#22c55e" font-weight="700">EXEC</text>
  <text x="660" y="80" text-anchor="middle" font-family="Arial" font-size="9" fill="#6b7a96">Executor</text>

  <!-- Final output marker -->
  <polygon points="715,46 725,50 715,54" fill="#22c55e" opacity="0.7"/>
  <rect x="735" y="34" width="90" height="32" rx="6" fill="#0f1219" stroke="#22c55e" stroke-width="1" stroke-opacity="0.5"/>
  <text x="780" y="54" text-anchor="middle" font-family="Arial" font-size="9" fill="#22c55e">✓ Dispatched</text>
</svg>
</div>

<br/>

Five agents, each with one job, coordinated by a LangGraph state machine:

| Agent | Does | Built on |
|---|---|---|
| **Alert Monitor** | Classifies SOS text: severity, disaster type, location | GPT-4o-mini structured output |
| **Image Analyzer** | Reads aerial/satellite photos for flooding, blocked roads, collapse | GPT-4o-mini vision |
| **Response Planner** | Retrieves real emergency protocols, checks live weather, drafts a 3-phase plan | RAG (ChromaDB) + Open-Meteo |
| **Quality Checker** | Independently verifies the plan didn't invent facts not in the retrieved context | Separate LLM pass — never self-graded |
| **Action Executor** | Logs dispatch actions, finds the nearest real hospital by driving time | OpenStreetMap Overpass + OSRM |

> Nothing dispatches without a human clicking approve — the graph physically pauses before the Executor runs.

---

## Architecture

<!-- Architecture flow SVG with animated data signals -->
<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 280" width="860">
  <rect width="860" height="280" fill="#07090e" rx="10"/>

  <!-- Left column: Data sources -->
  <!-- Box: SOS Text -->
  <rect x="20" y="20" width="130" height="36" rx="5" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="85" y="43" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">📡 SOS Text / RSS</text>

  <!-- Box: Satellite -->
  <rect x="20" y="72" width="130" height="36" rx="5" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="85" y="95" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">🛰️ Satellite Imagery</text>

  <!-- Box: Weather -->
  <rect x="20" y="124" width="130" height="36" rx="5" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="85" y="147" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">🌦️ Open-Meteo</text>

  <!-- Box: Protocols -->
  <rect x="20" y="176" width="130" height="36" rx="5" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="85" y="196" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">📄 FEMA / NDMA</text>
  <text x="85" y="208" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">Protocols (1,911 chunks)</text>

  <!-- Box: Maps -->
  <rect x="20" y="228" width="130" height="36" rx="5" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="85" y="251" text-anchor="middle" font-family="Arial" font-size="10" fill="#6b7a96">🗺️ OSM / Overpass</text>

  <!-- Animated signal dots from inputs -->
  <!-- SOS → Alert -->
  <circle cx="155" cy="38" r="2.5" fill="#2563eb" opacity="0">
    <animate attributeName="cx" values="155;255" dur="1.8s" begin="0s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="1.8s" begin="0s" repeatCount="indefinite"/>
  </circle>
  <!-- Satellite → Image -->
  <circle cx="155" cy="90" r="2.5" fill="#2563eb" opacity="0">
    <animate attributeName="cx" values="155;255" dur="2s" begin="0.3s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="90;120" dur="2s" begin="0.3s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="2s" begin="0.3s" repeatCount="indefinite"/>
  </circle>
  <!-- Weather → Planner -->
  <circle cx="155" cy="142" r="2.5" fill="#2563eb" opacity="0">
    <animate attributeName="cx" values="155;445" dur="2.5s" begin="0.5s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="142;170" dur="2.5s" begin="0.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="2.5s" begin="0.5s" repeatCount="indefinite"/>
  </circle>
  <!-- Protocols → Planner -->
  <circle cx="155" cy="192" r="2.5" fill="#2563eb" opacity="0">
    <animate attributeName="cx" values="155;445" dur="2.2s" begin="0.8s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="192;170" dur="2.2s" begin="0.8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="2.2s" begin="0.8s" repeatCount="indefinite"/>
  </circle>

  <!-- Agent boxes (center) -->
  <!-- Alert Monitor -->
  <rect x="255" y="20" width="130" height="52" rx="6" fill="#0f1219" stroke="#2563eb" stroke-width="1.2"/>
  <text x="320" y="43" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">Alert Monitor</text>
  <text x="320" y="58" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">GPT-4o-mini</text>

  <!-- Image Analyzer -->
  <rect x="255" y="88" width="130" height="52" rx="6" fill="#0f1219" stroke="#2563eb" stroke-width="1.2"/>
  <text x="320" y="111" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">Image Analyzer</text>
  <text x="320" y="126" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">GPT-4o vision</text>

  <!-- Response Planner -->
  <rect x="445" y="54" width="140" height="52" rx="6" fill="#0f1219" stroke="#2563eb" stroke-width="1.2"/>
  <text x="515" y="77" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">Response Planner</text>
  <text x="515" y="92" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">RAG + GPT-4o-mini</text>

  <!-- Connector: Alert → Planner -->
  <line x1="385" y1="46" x2="445" y2="80" stroke="#2563eb" stroke-width="1" stroke-opacity="0.4"/>
  <!-- Connector: Image → Planner -->
  <line x1="385" y1="114" x2="445" y2="80" stroke="#2563eb" stroke-width="1" stroke-opacity="0.4"/>

  <!-- Quality Checker -->
  <rect x="445" y="156" width="140" height="52" rx="6" fill="#0f1219" stroke="#d97706" stroke-width="1.2"/>
  <text x="515" y="179" text-anchor="middle" font-family="Arial" font-size="10" fill="#d97706" font-weight="700">Quality Checker</text>
  <text x="515" y="194" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">GPT-4o-mini</text>

  <!-- Connector: Planner → QA -->
  <line x1="515" y1="106" x2="515" y2="156" stroke="#2563eb" stroke-width="1" stroke-opacity="0.4" stroke-dasharray="4,3"/>
  <!-- Animated pulse down -->
  <circle cx="515" cy="110" r="2.5" fill="#2563eb" opacity="0">
    <animate attributeName="cy" values="110;154" dur="1.5s" begin="1s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="1s" repeatCount="indefinite"/>
  </circle>

  <!-- Retry arrow back to Planner -->
  <path d="M445,172 Q410,172 410,80 Q410,54 443,54" fill="none" stroke="#d97706" stroke-width="1" stroke-dasharray="4,3" stroke-opacity="0.6"/>
  <polygon points="443,50 443,58 451,54" fill="#d97706" opacity="0.6"/>
  <text x="400" y="120" text-anchor="middle" font-family="Arial" font-size="9" fill="#d97706" opacity="0.8">retry</text>

  <!-- Human Gate -->
  <rect x="640" y="105" width="120" height="52" rx="6" fill="#0f1219" stroke="#d97706" stroke-width="1.8">
    <animate attributeName="stroke-opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </rect>
  <text x="700" y="128" text-anchor="middle" font-family="Arial" font-size="10" fill="#d97706" font-weight="700">Human Approval</text>
  <text x="700" y="143" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">Required ← pauses here</text>

  <!-- Connector: QA → Human Gate -->
  <line x1="585" y1="182" x2="640" y2="140" stroke="#d97706" stroke-width="1" stroke-opacity="0.4"/>
  <!-- Animated pulse -->
  <circle cx="590" cy="178" r="2.5" fill="#d97706" opacity="0">
    <animate attributeName="cx" values="590;638" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="178;143" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Action Executor -->
  <rect x="640" y="210" width="120" height="52" rx="6" fill="#0f1219" stroke="#22c55e" stroke-width="1.2"/>
  <text x="700" y="233" text-anchor="middle" font-family="Arial" font-size="10" fill="#22c55e" font-weight="700">Action Executor</text>
  <text x="700" y="248" text-anchor="middle" font-family="Arial" font-size="9" fill="#4e5668">OSM + OSRM</text>

  <!-- Human → Executor -->
  <line x1="700" y1="157" x2="700" y2="210" stroke="#22c55e" stroke-width="1" stroke-opacity="0.5"/>
  <circle cx="700" cy="162" r="2.5" fill="#22c55e" opacity="0">
    <animate attributeName="cy" values="162;208" dur="1.5s" begin="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="2s" repeatCount="indefinite"/>
  </circle>

  <!-- GenesisState label -->
  <rect x="170" y="244" width="450" height="24" rx="4" fill="#0f1219" stroke="#1e2433" stroke-width="1"/>
  <text x="395" y="260" text-anchor="middle" font-family="Arial" font-size="9" fill="#38435a">GenesisState — shared typed dict passed through every node by LangGraph</text>
</svg>
</div>

The retry loop is not a blind re-roll: when Quality Checker finds unsupported claims, those specific issues are injected back into Response Planner's next prompt as explicit correction instructions, capped at 3 retries before force-dispatching with a `quality_warning` flag.

---

## Walking Through a Real Incident

```
Input: "Severe flooding reported in Assam, India"
```

<!-- Step-by-step animated timeline -->
<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 56" width="860">
  <rect width="860" height="56" fill="#07090e" rx="8"/>
  <line x1="30" y1="28" x2="830" y2="28" stroke="#1e2433" stroke-width="1.5"/>

  <!-- Steps -->
  <!-- 1 -->
  <circle cx="70" cy="28" r="12" fill="#0f1219" stroke="#2563eb" stroke-width="1.4"/>
  <text x="70" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">1</text>
  <text x="70" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#4e5668">Input</text>
  <!-- 2 -->
  <circle cx="200" cy="28" r="12" fill="#0f1219" stroke="#2563eb" stroke-width="1.4"/>
  <text x="200" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">2</text>
  <text x="200" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#4e5668">Alert: flood/high</text>
  <!-- 3 -->
  <circle cx="330" cy="28" r="12" fill="#0f1219" stroke="#2563eb" stroke-width="1.4"/>
  <text x="330" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">3</text>
  <text x="330" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#4e5668">Image: none/honest</text>
  <!-- 4 -->
  <circle cx="460" cy="28" r="12" fill="#0f1219" stroke="#2563eb" stroke-width="1.4"/>
  <text x="460" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#2563eb" font-weight="700">4</text>
  <text x="460" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#4e5668">Plan: RAG + weather</text>
  <!-- 5 -->
  <circle cx="590" cy="28" r="12" fill="#0f1219" stroke="#d97706" stroke-width="1.4">
    <animate attributeName="stroke-opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="590" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#d97706" font-weight="700">5</text>
  <text x="590" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#d97706">Approve</text>
  <!-- 6 -->
  <circle cx="720" cy="28" r="12" fill="#0f1219" stroke="#22c55e" stroke-width="1.4"/>
  <text x="720" y="32" text-anchor="middle" font-family="Arial" font-size="10" fill="#22c55e" font-weight="700">6</text>
  <text x="720" y="50" text-anchor="middle" font-family="Arial" font-size="8" fill="#4e5668">Dispatch + hospital</text>

  <!-- Animated progress dot -->
  <circle r="4" fill="#2563eb" opacity="0.8">
    <animateMotion dur="5s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;0.16;0.33;0.5;0.66;0.83;1">
      <mpath href="#stepPath"/>
    </animateMotion>
    <animate attributeName="fill" values="#2563eb;#2563eb;#2563eb;#2563eb;#d97706;#22c55e;#2563eb" dur="5s" repeatCount="indefinite" calcMode="discrete"/>
  </circle>
  <path id="stepPath" d="M70,28 L200,28 L330,28 L460,28 L590,28 L720,28 L830,28" fill="none"/>
</svg>
</div>

1. **Alert Monitor** → `disaster_type: flood`, `severity: high`, `location_hint: "Assam, India"`
2. **Image Analyzer** → `no image provided` — says so rather than guessing
3. **Response Planner** → geocodes to `26.4074°N, 93.2551°E`, fetches live weather (`24.3°C, 0.0mm`), retrieves 1,911 NDMA/FEMA protocol chunks from ChromaDB, drafts a 3-phase plan grounded in retrieved text
4. **Quality Checker** → independently compares plan claims against retrieved context — passes only if nothing was invented
5. **Human Approval Gate** → graph pauses; operator reviews and authorizes
6. **Action Executor** → logs dispatch actions, queries OpenStreetMap for nearest real hospital with driving distance

---

## Real Data Sources

| Source | Used for | Access |
|---|---|---|
| FEMA CPG 101 + 3 NDMA guidelines | Response Planner's grounding knowledge, 1,911 chunks in ChromaDB | Downloaded PDFs, sentence-boundary chunked |
| Copernicus Emergency Management Service | Real satellite-derived disaster activation maps | Free public REST API, no key |
| HuggingFace disaster-tweets dataset | Alert Monitor's repeatable dev/eval replay | `datasets` library |
| Live news RSS | Alert Monitor's real-time ingestion | RSS feed |
| Open-Meteo | Live weather at geocoded incident coordinates | Free API, no key |
| OpenStreetMap Nominatim | Place name → lat/lon geocoding | Free API |
| OSRM | Real driving distance/time to nearest hospital | Free public routing server |
| OpenStreetMap Overpass | Real hospitals near any coordinate, globally | Free API |

---

## Tech Stack

`Python 3.11` · `LangGraph` · `OpenAI GPT-4o-mini` · `ChromaDB` · `FastAPI` · `SQLModel` + `SQLite` · `pydantic-settings` · `rasterio` · `HTML/CSS/JS frontend`

---

## Engineering Decisions

- **ChromaDB over Pinecone** — embedded, zero infra, same concepts transfer when scaling
- **No hardcoded Twitter/X dependency** — pluggable ingestion (dataset replay + RSS), source can change without touching agent logic
- **Quality Checker is a separate LLM call** — the plan's own `"grounded": true` field is never trusted; a second independent pass looks for unsupported claims
- **Failed quality checks feed forward** — specific issues passed back into the next planning prompt as correction instructions, not a blind retry
- **External API failures degrade gracefully** — GDELT/Overpass rate limits retry with exponential backoff, then fail into `None`/empty — a flaky map lookup never blocks a life-safety plan
- **Sentence-boundary chunking** — early version cut mid-word; chunks now built on real sentence boundaries
- **GeoTIFF nodata masking** — Copernicus rasters use `NaN` sentinel values; naive normalisation produced blank images until nodata was explicitly masked

---

## Known Limitations

- Copernicus EMS rasters are often SAR (radar) data — a vision LLM can describe pixel patterns but can't reliably read damage from raw radar backscatter
- Nearest-hospital lookup checks only the first 5 Overpass results within a fixed radius — not a guaranteed true-nearest search
- Geocoding precision is only as specific as the location text extracted — a broad region name resolves to that region's centroid
- SQLite on Render free tier resets on every deploy — use Render PostgreSQL for persistent incident history

---

## Project Structure

```
genesis-ai/
├── data/
│   └── raw/protocols/         FEMA/NDMA PDFs (FEMA CPG 101, NDMA flood/earthquake/cyclone)
├── frontend/
│   ├── index.html             Emergency Operations Dashboard
│   ├── style.css
│   └── app.js
├── src/
│   ├── config.py              Typed settings (pydantic-settings)
│   ├── main.py                CLI entrypoint
│   ├── agents/
│   │   ├── state.py           Shared GenesisState TypedDict
│   │   ├── graph.py           LangGraph wiring, retry loop, approval interrupt
│   │   ├── alert_monitor.py
│   │   ├── image_analyzer.py
│   │   ├── response_planner.py
│   │   ├── quality_checker.py
│   │   └── action_executor.py
│   ├── tools/
│   │   ├── vision_tool.py
│   │   ├── weather_tool.py
│   │   ├── maps_tool.py
│   │   ├── copernicus_tool.py
│   │   ├── dataset_tool.py
│   │   └── gdelt_tool.py
│   ├── rag/
│   │   ├── build_knowledge_base.py
│   │   └── search_knowledge_base.py
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   └── api/
│       ├── app.py
│       ├── schemas.py
│       └── routes/
│           ├── incidents.py
│           └── health.py
└── tests/
    ├── test_agents.py
    ├── test_tools.py
    └── test_api.py
```

---

## Setup

```bash
git clone <your-repo-url>
cd genesis-ai
python -m venv llm_env
llm_env\Scripts\activate        # Windows
pip install -r requirements.txt

cp .env.example .env
# Set OPENAI_API_KEY at minimum
```

Build the knowledge base once before first run:
```bash
python -m src.rag.build_knowledge_base
```

---

## Deployment

Backend (FastAPI Web Service) and Frontend (Static Site) are deployed separately on [Render](https://render.com).

| Service | Render Type | Start Command |
|---|---|---|
| `genesis-api` | Web Service | `uvicorn src.api.app:app --host 0.0.0.0 --port $PORT` |
| `genesis-frontend` | Static Site | *(no build step — plain HTML/JS)* |

**Environment variables required on the backend:**

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | your OpenAI key |
| `FRONTEND_URL` | your Render static site URL |
| `DATABASE_URL` | `sqlite:///./data/genesis.db` |

---

## Usage

**CLI:**
```bash
python -m src.main "Severe flooding reported in Assam, India"
```

**API + Frontend (local):**
```bash
# Terminal 1
uvicorn src.api.app:app --reload

# Terminal 2 — open frontend/index.html in your browser
# or serve it: python -m http.server 3000 --directory frontend
```

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | `GET` | Liveness check |
| `/incidents` | `POST` | Start an incident, runs pipeline up to the human-approval pause |
| `/incidents/{thread_id}/approve` | `POST` | Resume a paused incident with approve/reject, saves to database |

**POST `/incidents` body:**
```json
{ "situation": "Severe flooding in Assam.", "image_path": null }
```

**POST `/incidents/{id}/approve` body:**
```json
{ "approved": true }
```

---

## Tests

```bash
pytest
```

| File | Covers |
|---|---|
| `tests/test_agents.py` | action_executor, alert_monitor, quality_checker, graph routing, planner feedback injection |
| `tests/test_tools.py` | maps_tool, weather_tool, gdelt_tool, dataset_tool |
| `tests/test_api.py` | POST /incidents, POST /approve, GET /health |

All external calls (OpenAI, HTTP APIs) are mocked — tests run fully offline.

---

## Roadmap

- [ ] LangSmith tracing — full observability into each node's execution
- [ ] Ragas evaluation suite — measured Faithfulness/Relevancy scores over a fixed test set
- [ ] Docker containerization
- [ ] PostgreSQL persistence for production incident history

---

<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 48" width="860">
  <defs>
    <linearGradient id="footGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#07090e"/>
      <stop offset="30%" style="stop-color:#0f1219"/>
      <stop offset="70%" style="stop-color:#0f1219"/>
      <stop offset="100%" style="stop-color:#07090e"/>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:0"/>
      <stop offset="50%" style="stop-color:#2563eb;stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:#2563eb;stop-opacity:0"/>
    </linearGradient>
  </defs>
  <rect width="860" height="48" fill="url(#footGrad)" rx="8"/>
  <!-- Animated scan line -->
  <rect x="0" y="0" width="860" height="1" fill="url(#scanGrad)">
    <animateTransform attributeName="transform" type="translate" values="0,0;0,47;0,0" dur="5s" repeatCount="indefinite" calcMode="ease-in-out"/>
  </rect>

  <!-- Logo mark -->
  <g transform="translate(430,24)">
    <polygon points="0,-14 12,-7 12,7 0,14 -12,7 -12,-7" fill="none" stroke="#2563eb" stroke-width="1.3" stroke-opacity="0.7"/>
    <circle cx="0" cy="0" r="3.5" fill="none" stroke="#2563eb" stroke-width="1.2">
      <animate attributeName="r" values="3.5;5;3.5" dur="2.5s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.8;0.3;0.8" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="1.5" fill="#2563eb">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
  </g>
  <text x="455" y="29" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" fill="#38435a" font-weight="600">GENESIS</text>
  <text x="395" y="29" text-anchor="end" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" fill="#38435a">Emergency Response Orchestration  ·</text>
</svg>
</div>
