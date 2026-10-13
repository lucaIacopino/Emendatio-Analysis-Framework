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
| D-11 | 2026-10-13 | The document format (and the language) are given **from the CLI** at launch and are injected directly into the prompt (`{doc_format}`, `{format_rules}`, `{language}`). | One single source of truth: the user's CLI choice drives both file handling and LLM instructions; adding a format = adding a rules block, not new code paths. | Accepted |
| D-12 | 2026-10-13 | The previous chunk is sent **only and exclusively as read-only context**. The prompt states explicitly that it may contain uncorrected errors, must not be corrected, and must not be used as a model of style or rules for the target. | Prevents the model from (a) correcting outside the target, (b) "learning" from errors the user chose to keep, (c) imitating context choices. | Accepted |
| D-13 | 2026-10-13 | Requests are **stateless** (one request per chunk, explicit context). When a chunk changes after the following one was analysed, the following chunk becomes **`stale`** and is re-analysed **on demand** (dedicated key), with a visible flag in the sidebar. | Bounded token cost, no context-window overflow, reproducible results; on-demand re-analysis avoids blocking the UI with a slow local model. Resolves Q-02. | Accepted |
| D-14 | 2026-10-13 | Synchronized scrolling is **per chunk**: each chunk occupies in both panes the height of the longer of its two versions (original / corrected), computed dynamically at render time (not fixed a priori), so paragraphs stay aligned. | Line-level sync breaks as soon as a correction changes the text length; fixed heights would truncate or waste space. | Accepted |
| D-15 | 2026-10-13 | **One widget per chunk** in both main panes. No visible borders on chunks; only the chunk currently under review gets a **slightly different background tint** (chosen over a left bar: it does not change the layout and stays unobtrusive). Spacing between chunks = one blank line, like normal paragraphs. | Chunk widgets give natural targets for navigation, sidebar sync and per-chunk height alignment (D-14); text must still read as a continuous document. | Accepted |
| D-16 | 2026-10-13 | The source text is displayed **as raw text, never interpreted** (no Markdown/LaTeX rendering, no Textual markup), through a single format-aware render function in `ui/` (format → renderer registry). Today every format maps to "literal text"; syntax highlighting can be added later per format without touching the rest. | Proofreading works on the raw characters: rendering would hide symbols (`**`, `\emph{}`) and break the mapping between suggestions and positions. A single entry point mirrors the `{format_rules}` design (D-11). | Accepted |
| D-17 | 2026-10-13 | **Sequential anchoring:** suggestions are anchored in order, each search starting after the previous match (cursor). The prompt asks for suggestions in order of appearance. Fallbacks: unique match → use it; several matches → first one after the cursor; none after the cursor → search from the start; still none → fuzzy; else discard. No `occurrence` field for now. | Solves most ambiguous spans (Q-05) without asking the LLM for counts it may get wrong; order compliance becomes another measurable property. | Accepted (to validate experimentally) |
| D-18 | 2026-10-13 | **Explanation depth by category:** `semantic` suggestions get a deeper explanation (2-3 sentences, example not mandatory); all other categories (grammar, spelling, punctuation, …) keep one short sentence. No separate `example` field. Prompt v0.3, rule 9. | Grammar errors are self-evident and a long text would slow reading and generation; semantic errors need reasoning to be understood and accepted by the user. Resolves Q-01. | Accepted |
| D-19 | 2026-10-13 | The LLM returns **only fragments** (`original`, `replacement`), never the full chunk text. The full text is held by the software. | Fewer output tokens (faster, cheaper, especially on local models); no risk of the model silently altering untouched parts of the chunk. | Accepted |

---

## 2. Open questions

- ~~**Q-01 — `explanation` field**~~ → resolved by D-18 (deeper explanation for semantic suggestions only).
- ~~**Q-02 — Context for chunk N**~~ → resolved by D-12 and D-13 (context = current version of N-1 with accepted changes only; `stale` + on-demand re-analysis).
- **Q-03 — Chunk length:** optimal length for precision; to be measured experimentally (literature gives precision-vs-length curves as starting point).
- **Q-04 — Local model choice:** which model fits the hardware with good quality (see §4).
- ~~**Q-05 — Ambiguous spans**~~ → resolved by D-17 (sequential anchoring); `occurrence` field kept as a fallback idea if experiments show it is needed.

---

## 3. Pending code changes

| ID | Change | Owner | Status |
|---|---|---|---|
| C-01 | `Static` widgets in `main.py` parse Rich/Textual markup: user text containing `[...]` may render wrongly or raise a markup error. User text must be displayed literally, via the single render function of D-16 (`ui/render.py`, solution provided in session 2). | Luca | To do — at the start of the implementation phase |
| C-02 | Restructure the project into `core/`, `llm/`, `ui/` (D-07). | — | To do |
| C-03 | CLI: add `--format` (e.g. `md`, `txt`, later `tex`) and `--lang` options; their values feed the prompt (D-11). | Luca | To do |
| C-04 | Add `docs/thesis_log.md` and `prompts/` to the repository so they are versioned with the code. | Luca | In progress |

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
- **Anchoring rate (metric):** for every suggestion, record the outcome of locating `original` in the chunk — `exact`, `fuzzy`, `ambiguous`, `not_found`. Aggregated per model (and per prompt version), it measures how reliably each LLM follows the "verbatim" instruction. A suggestion that cannot be anchored is lost for the user even if it was correct, so this is a usability metric, not only a formatting one. Related metric: **schema consistency rate** (valid JSON + coherent `has_errors` flag).
- **Context leakage rate (metric):** share of suggestions that target text found only in `<context>` (or that copy its deliberate errors). Measures compliance with D-12.
- **Order compliance (metric):** share of responses whose suggestions are listed in order of appearance (needed by D-17).
- **Why anchoring is done in software:** the LLM only returns text; it cannot see or edit the document as held by the application. The software must map each suggestion to a position (for highlighting, navigation and replacement) and must not trust the model output blindly.
- **Evaluation plan (to define):** synthetic test texts with injected errors; metrics: precision/recall of detected errors, anchoring success rate, over-correction rate (changes to correct text), latency per chunk, effect of chunk length.
- **Software engineering:** layered architecture (D-07), UI independence, testability.

---

## 6. Session history

### 2026-10-12 — Session 1
- Reviewed repository skeleton (`main.py`: Textual layout with two panes + bottom area, CLI parsing for `.txt`/`.md`).
- Agreed on: Ollama, local-first, software-managed chunk IDs, `has_errors` flag, verbatim span strategy, layered architecture, aspell-style commands, chunk sidebar, synchronized scrolling.
- Identified C-01 (markup issue) — Luca to implement after explanation.
- Drafted prompt v0 (`prompts/prompt.md`).

### 2026-10-13 — Session 2
- Decided: format and language from CLI injected into the prompt (D-11); previous chunk as strictly read-only context (D-12); stateless requests, `stale` state with on-demand re-analysis (D-13); per-chunk synchronized scrolling using the taller version (D-14).
- Clarified why anchoring is a software responsibility; defined the anchoring rate metric.
- Prompt updated to v0.1 (context rules, per-format rules block), then v0.2 (suggestions in order of appearance).
- C-01 (markup) explained with examples; implementation pending (Luca).
- Next step agreed: build the `llm/` layer in isolation (no UI).
- Later in the session: raw-text display through a format-aware render function (D-16); chunk widgets with light, layout-neutral highlight (D-15); sequential anchoring proposal (D-17); Q-01 options listed; new metrics (context leakage, order compliance). Log and prompt moved to the repository (C-04).
- Render function for raw text defined (D-16, `ui/render.py`); background tint for the active chunk (D-15); explanation depth by category, prompt v0.3 (D-18); LLM returns fragments only (D-19). Q-01 and Q-05 closed.
