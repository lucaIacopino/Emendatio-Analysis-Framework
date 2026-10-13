# Thesis Log — Emendatio Analysis Framework

Running log of decisions, rationale and material reusable in the thesis.
Updated at every working session. Language: English.

---

## 0. Project summary

**Goal (from supervisor).** A Linux terminal program that supports text proofreading through an LLM, with an interface inspired by `aspell` (and partially by Overleaf).

- **Language / framework:** Python + Textual (TUI).
- **Input formats:** plain text / Markdown (LaTeX was mentioned by the supervisor; for now the format is declared to the LLM in the prompt rather than handled by dedicated parsing — see D-01).
- **Correction languages:** any language the LLM supports, selectable from CLI (like `aspell --lang`).
- **Layout:** original text (left), suggested text (right), commands/details (bottom).
- **Constraint:** corrections must NOT change meaning or style; the number of suggestions must be limited.

**Supervisor addendum.**
- aspell jumps directly to the next error instead of scrolling.
- A pane with a compact list of suggested changes.
- Key bindings to move quickly between suggestions (at least "previous error").
- Evaluate synchronized free scrolling of original and corrected text.

**Repository:** https://github.com/lucaIacopino/Emendatio-Analysis-Framework

---

## 1. Decision log

| ID | Date | Decision | Rationale | Status |
|---|---|---|---|---|
| D-01 | 2026-10-12 | Ignore file-extension-specific handling for now; Markdown considered the most appropriate default. The document format is stated in the LLM prompt. | Keeps the pipeline simple while the core loop is built; the LLM can be told what markup to preserve. | Accepted |
| D-02 | 2026-10-12 | Use **Ollama** for local inference during development. | Exposes an OpenAI-compatible endpoint, so the same client code can later target ChatGPT. Other non-compatible APIs will be added later behind an adapter. | Accepted |
| D-03 | 2026-10-12 | Start experiments on a **local model** before moving to large hosted LLMs. | Zero cost, fast iteration on prompt and output format, reproducible baseline. | Accepted |
| D-04 | 2026-10-12 | **Chunk IDs are assigned and managed by the software, not by the LLM.** | The ID is only needed for navigation (jump between chunks/suggestions); letting the LLM echo it adds a failure point with no benefit. | Accepted |
| D-05 | 2026-10-12 | LLM output: JSON with an explicit **`has_errors` flag** + a list of suggestions (`original`, `replacement`, `category`, `severity`, `explanation`). | The flag forces an explicit decision and allows a consistency check (`has_errors=true` with an empty list, or vice versa, is a detectable model failure). | Accepted (schema v0) |
| D-06 | 2026-10-12 | Localization strategy: the LLM returns the **verbatim original span**; the software locates it inside the chunk (string search, fuzzy fallback, else discard and log). | LLMs are unreliable at character counting (offsets); full-rewrite + diff loses category/explanation and encourages over-editing. | Accepted, to be validated experimentally |
| D-07 | 2026-10-12 | Architecture split into independent packages: `core/` (document, chunking, suggestions), `llm/` (client, prompts, schema), `ui/` (Textual). | Separation of concerns; core and llm testable without UI; evaluation scripts can run headless. | Accepted |
| D-08 | 2026-10-12 | aspell-style key bindings (accept, ignore, edit, next/prev, undo, ignore-all, save, quit). | Supervisor request; familiar UX for aspell users. | Accepted (details TBD) |
| D-09 | 2026-10-12 | Left sidebar listing chunks with their state (to check / corrected / no errors), navigable with arrow keys. | Fast navigation; implements the supervisor's "compact list of changes" idea at chunk level. | Accepted |
| D-10 | 2026-10-12 | Free scrolling allowed, **synchronized** between original and corrected panes. | Supervisor asked to evaluate it; useful to re-read context. | Accepted |

---

## 2. Open questions

- **Q-01 — `explanation` field:** keep a short explanation only, or also show an example below it? Undecided.
- **Q-02 — Context for chunk N:** send chunk N-1 as read-only context. Which version of N-1: original text, or text with the suggestions accepted so far? What happens when N-1 changes after N was analysed? (Proposal in session 2026-10-12: stateless requests + "stale" state, to confirm.)
- **Q-03 — Chunk length:** optimal length for precision; to be measured experimentally (literature gives precision-vs-length curves as starting point).
- **Q-04 — Local model choice:** which model fits the hardware with good quality (see §4).
- **Q-05 — Ambiguous spans:** when `original` occurs more than once in the chunk, ask for longer spans in the prompt, or add an `occurrence` field?

---

## 3. Pending code changes

| ID | Change | Owner | Status |
|---|---|---|---|
| C-01 | `Static` widgets in `main.py` parse Rich/Textual markup: user text containing `[...]` may render wrongly or raise a markup error. User text must be displayed literally. | Luca (implementation), Claude (review) | To do |
| C-02 | Restructure the project into `core/`, `llm/`, `ui/` (D-07). | — | To do |

---

## 4. Environment

- **Laptop:** MSI Katana 15 B13VFK — Intel Core i7 13th gen, NVIDIA GeForce RTX 4060 Laptop (Max-Q, 8 GB VRAM expected), 16 GB RAM DDR5-5600.
- **Implication:** 7–9B models at 4-bit quantization fit entirely in VRAM; ~12–14B models need partial CPU offload (slower).

---

## 5. Thesis material (candidate content)

Notes that can become sections of the thesis.

- **Related tools:** aspell (interactive spell checking UX), Overleaf (review/track changes), latex-checker (LLM-based, prompt used as inspiration).
- **Design rationale for the output format:** comparison of three localization strategies — character offsets vs. full rewrite + diff vs. verbatim span + software anchoring (D-06). Good candidate for a design-choices section with pros/cons table.
- **Robustness of LLM output:** schema validation, consistency check via `has_errors`, anchoring failure rate as a metric per model.
- **Context management:** stateless per-chunk requests vs. a conversation that grows (token cost, context window limits on local models, reproducibility).
- **Evaluation plan (to define):** synthetic test texts with injected errors; metrics: precision/recall of detected errors, anchoring success rate, over-correction rate (changes to correct text), latency per chunk, effect of chunk length.
- **Software engineering:** layered architecture (D-07), UI independence, testability.

---

## 6. Session history

### 2026-10-12 — Session 1
- Reviewed repository skeleton (`main.py`: Textual layout with two panes + bottom area, CLI parsing for `.txt`/`.md`).
- Agreed on: Ollama, local-first, software-managed chunk IDs, `has_errors` flag, verbatim span strategy, layered architecture, aspell-style commands, chunk sidebar, synchronized scrolling.
- Identified C-01 (markup issue) — Luca to implement after explanation.
- Drafted prompt v0 (`prompt_v0.md`).
