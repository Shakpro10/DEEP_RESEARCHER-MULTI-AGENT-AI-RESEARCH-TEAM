EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Top AI companies in Nigeria in 2026",
    "Top Defence companies in Nigeria specializing in armoured vehicles in 2026",
]

HEADER_HTML = """
<div class="pulse-brand">
    <div class="pulse-mark" aria-hidden="true">
        <span class="pulse-ring pulse-ring-1"></span>
        <span class="pulse-ring pulse-ring-2"></span>
        <span class="pulse-sweep"></span>
        <span class="pulse-core"></span>
    </div>
    <div class="pulse-titles">
        <p class="pulse-eyebrow">Multi-source web research</p>
        <h1>Research<span class="pulse-slash">//</span>Manager</h1>
    </div>
    <div class="pulse-status">
        <span class="pulse-status-dot"></span>
        <span class="pulse-status-text">system online</span>
    </div>
</div>
"""

CSS = """
:root, .gradio-container {
    --void: #06060c;
    --surface: rgba(19, 21, 36, 0.72);
    --surface-solid: #10111d;
    --edge: rgba(124, 130, 163, 0.22);
    --edge-bright: rgba(124, 130, 163, 0.42);
    --text: #eef1fb;
    --muted: #8288a6;
    --cyan: #29f5ff;
    --pink: #ff2f92;
    --lime: #b6ff3c;
    --cyan-dim: rgba(41, 245, 255, 0.16);
    --pink-dim: rgba(255, 47, 146, 0.16);
}

.gradio-container {
    max-width: 1040px !important;
    margin: 0 auto !important;
    padding: 2.75rem 2rem 4.5rem !important;
    color: var(--text) !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
    background:
        radial-gradient(ellipse 900px 500px at 12% -8%, rgba(41, 245, 255, 0.10), transparent 60%),
        radial-gradient(ellipse 800px 600px at 100% 15%, rgba(255, 47, 146, 0.09), transparent 55%),
        repeating-linear-gradient(0deg, rgba(124, 130, 163, 0.05) 0px, rgba(124, 130, 163, 0.05) 1px, transparent 1px, transparent 40px),
        repeating-linear-gradient(90deg, rgba(124, 130, 163, 0.05) 0px, rgba(124, 130, 163, 0.05) 1px, transparent 1px, transparent 40px),
        var(--void) !important;
}

body { background: var(--void, #06060c); }

@media (prefers-reduced-motion: reduce) {
    * { animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; }
}

/* === HEADER / BRAND === */
.pulse-brand {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 1.25rem;
    padding-bottom: 1.4rem;
    border-bottom: 1px solid var(--edge);
    margin-bottom: 2.75rem;
}

.pulse-mark {
    position: relative;
    width: 46px;
    height: 46px;
    flex-shrink: 0;
}

.pulse-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 1.5px solid var(--cyan);
    opacity: 0.55;
}

.pulse-ring-2 { inset: 9px; border-color: var(--pink); opacity: 0.5; }

.pulse-sweep {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(from 0deg, transparent 0deg, transparent 260deg, var(--cyan) 340deg, transparent 360deg);
    animation: pulse-rotate 2.6s linear infinite;
    filter: drop-shadow(0 0 5px var(--cyan));
}

.pulse-core {
    position: absolute;
    inset: 19px;
    border-radius: 50%;
    background: var(--lime);
    box-shadow: 0 0 10px 2px var(--lime);
    animation: pulse-beat 2s ease-in-out infinite;
}

@keyframes pulse-rotate { to { transform: rotate(360deg); } }
@keyframes pulse-beat {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.55; transform: scale(0.82); }
}

.pulse-titles h1 {
    font-family: "Space Grotesk", "Inter", sans-serif;
    font-size: clamp(1.6rem, 3.6vw, 2.35rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0.15rem 0 0;
    line-height: 1;
    color: var(--text);
}

.pulse-slash { color: var(--pink); font-weight: 400; }

.pulse-eyebrow {
    font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.66rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    margin: 0;
    color: var(--cyan);
}

.pulse-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: "JetBrains Mono", ui-monospace, monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--edge);
    border-radius: 999px;
    padding: 0.4rem 0.85rem;
}

.pulse-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--muted);
}

.pulse-status.is-running .pulse-status-dot {
    background: var(--lime);
    box-shadow: 0 0 8px 1px var(--lime);
    animation: pulse-beat 1.1s ease-in-out infinite;
}

/* === QUERY ROW === */
.pulse-query-row {
    gap: 0 !important;
    align-items: stretch !important;
}

#pulse-query, #pulse-query > div, #pulse-query .wrap, #pulse-query .form, #pulse-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#pulse-query {
    position: relative;
}

#pulse-query .wrap::before {
    content: ">";
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--cyan);
    font-family: "JetBrains Mono", monospace;
    font-weight: 700;
    font-size: 1.05rem;
    z-index: 2;
    pointer-events: none;
}

#pulse-query textarea, #pulse-query input {
    background: var(--surface-solid) !important;
    color: var(--text) !important;
    border: 1px solid var(--edge-bright) !important;
    border-radius: 10px 0 0 10px !important;
    padding: 1.05rem 1.2rem 1.05rem 2.35rem !important;
    font-size: 1.02rem !important;
    font-family: "Inter", sans-serif !important;
    box-shadow: none !important;
    line-height: 1.45 !important;
    resize: none !important;
    min-height: 56px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}

#pulse-query textarea:focus, #pulse-query input:focus {
    outline: none !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px var(--cyan), 0 0 18px rgba(41, 245, 255, 0.35) !important;
}

#pulse-query textarea::placeholder, #pulse-query input::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}

#pulse-run, #pulse-stop {
    border-left: none !important;
    border-radius: 0 10px 10px 0 !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-size: 0.78rem !important;
    min-width: 118px !important;
    padding: 0 1.4rem !important;
    box-shadow: none !important;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
}

#pulse-run {
    background: var(--surface-solid) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--edge-bright) !important;
}

#pulse-run::before {
    content: "\\2726";
    margin-right: 0.5rem;
    font-size: 0.85em;
}

#pulse-run:hover {
    background: var(--cyan-dim) !important;
    border-color: var(--cyan) !important;
    color: var(--text) !important;
    box-shadow: inset 0 0 0 1px var(--cyan), 0 0 14px rgba(41, 245, 255, 0.22) !important;
}

#pulse-run:active { transform: scale(0.98); }

#pulse-stop {
    background: var(--surface-solid) !important;
    color: var(--pink) !important;
    border: 1px solid var(--edge-bright) !important;
    animation: pulse-edge-glow 1.6s ease-in-out infinite;
}

#pulse-stop::before {
    content: "\\25A0";
    margin-right: 0.5rem;
    font-size: 0.68em;
}

#pulse-stop:hover {
    background: var(--pink-dim) !important;
    border-color: var(--pink) !important;
    color: var(--text) !important;
    box-shadow: inset 0 0 0 1px var(--pink), 0 0 14px rgba(255, 47, 146, 0.22) !important;
}

#pulse-stop:active { transform: scale(0.98); }

@keyframes pulse-edge-glow {
    0%, 100% { border-color: var(--edge-bright); }
    50% { border-color: var(--pink); }
}

/* === EXAMPLES === */
.pulse-examples-label {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.64rem;
    letter-spacing: 0.26em;
    color: var(--muted);
    text-transform: uppercase;
    margin: 2.1rem 0 0.9rem 0;
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.pulse-examples-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--edge);
}

#pulse-examples, #pulse-examples > div, #pulse-examples .wrap, #pulse-examples .block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

#pulse-examples label, #pulse-examples .label-wrap, #pulse-examples > div > .label-wrap {
    display: none !important;
}

#pulse-examples table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: auto !important;
    background: transparent !important;
    border: none !important;
}

#pulse-examples thead { display: none !important; }
#pulse-examples tbody { background: transparent !important; }

#pulse-examples tr {
    background: transparent !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    border: none !important;
}

#pulse-examples td, #pulse-examples button {
    background: var(--surface) !important;
    backdrop-filter: blur(6px);
    border: 1px solid var(--edge) !important;
    padding: 0.65rem 1.05rem !important;
    cursor: pointer !important;
    transition: border-color 0.15s, color 0.15s, box-shadow 0.15s !important;
    font-size: 0.88rem !important;
    font-family: "JetBrains Mono", monospace !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    margin: 0 !important;
    text-align: left !important;
    box-shadow: none !important;
}

#pulse-examples td::before, #pulse-examples button::before {
    content: "> ";
    color: var(--cyan);
}

#pulse-examples td:hover, #pulse-examples button:hover {
    border-color: var(--cyan) !important;
    color: var(--text) !important;
    box-shadow: 0 0 14px rgba(41, 245, 255, 0.22) !important;
}

/* === REPORT === */
#pulse-report {
    margin-top: 2.6rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text) !important;
    min-height: 40px;
}

#pulse-report > div, #pulse-report .prose {
    background: transparent !important;
    color: var(--text) !important;
}

#pulse-report:not(:empty) {
    border-top: 1px solid var(--edge) !important;
    padding-top: 1.85rem !important;
}

#pulse-report h1 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--cyan);
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem;
    letter-spacing: -0.01em;
    text-shadow: 0 0 18px rgba(41, 245, 255, 0.25);
}

#pulse-report h2 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.28rem;
    color: var(--pink);
    font-weight: 700;
    margin-top: 1.85rem;
}

#pulse-report h3 {
    font-size: 1.05rem;
    color: var(--text);
    font-weight: 700;
    margin-top: 1.5rem;
}

#pulse-report p { line-height: 1.75; color: var(--text); }

#pulse-report a {
    color: var(--cyan);
    text-decoration: underline;
    text-decoration-thickness: 1.5px;
    text-underline-offset: 3px;
}

#pulse-report a:hover { color: var(--lime); }

#pulse-report code {
    background: #0a0b14;
    border: 1px solid var(--edge);
    color: var(--lime);
    padding: 0.12rem 0.42rem;
    font-size: 0.9em;
    border-radius: 5px;
}

#pulse-report pre {
    background: #0a0b14;
    border: 1px solid var(--edge);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
}

#pulse-report blockquote {
    border-left: 3px solid var(--pink) !important;
    background: var(--surface);
    padding: 0.9rem 1.2rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
    color: var(--muted);
}

#pulse-report ul, #pulse-report ol { padding-left: 1.5rem; }
#pulse-report li { margin: 0.35rem 0; line-height: 1.65; }

#pulse-report table {
    border-collapse: collapse;
    border: 1px solid var(--edge-bright);
    border-radius: 8px;
    overflow: hidden;
}

#pulse-report th, #pulse-report td {
    border: 1px solid var(--edge);
    padding: 0.55rem 0.9rem;
    text-align: left;
}

#pulse-report th {
    background: var(--surface);
    font-weight: 700;
    color: var(--cyan);
}

footer { display: none !important; }

/* ---- Download buttons, matched to the dark/outline theme above ---- */
#pulse-download-pdf, #pulse-download-docx {
    background: var(--surface-solid) !important;
    color: var(--text) !important;
    border: 1px solid var(--edge-bright) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: none !important;
    transition: border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
}

#pulse-download-pdf:hover, #pulse-download-docx:hover {
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(41, 245, 255, 0.2) !important;
}

/* ---- Hide Gradio's default blinking progress bar on the report panel ----
   Selector names come from Gradio's internal CSS and can shift between
   versions; if a blinking bar still appears after upgrading Gradio, inspect
   the element in devtools and add its class here. */
#pulse-report .generating,
#pulse-report .progress-bar,
#pulse-report .eta-bar,
#pulse-report .meta-text,
#pulse-report .meta-text-center {
    display: none !important;
    opacity: 0 !important;
}

/* ---- Custom "thinking" indicator, shown in place of the progress bar ---- */
#pulse-thinking {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0 10px 0;
    font-size: 0.95em;
    color: var(--cyan);
}
#pulse-thinking .pulse-dot {
    display: inline-block;
    animation: pulse-fade 1.2s ease-in-out infinite;
}
@keyframes pulse-fade {
    0%, 100% { opacity: 0.25; transform: scale(0.85); }
    50% { opacity: 1; transform: scale(1.15); }
}

/* ---- Stuck-UI safety net ----
   Purely a stylesheet rule (not a runtime DOM mutation), so it can't
   desync Svelte's own reactive tracking the way directly poking element
   attributes from JS can. Keeps these controls clickable even if Gradio
   briefly marks queued components "pending" (pointer-events: none) while
   a streaming event is in flight. */
#pulse-run, #pulse-stop, #pulse-query textarea, #pulse-query input,
#pulse-examples button, #pulse-examples td {
    pointer-events: auto !important;
}




@media (max-width: 700px) {
    .gradio-container { padding: 1.5rem 1rem 3rem !important; }
    .pulse-brand { grid-template-columns: auto 1fr; row-gap: 0.75rem; }
    .pulse-status { grid-column: 1 / -1; justify-self: start; }
    .pulse-query-row { flex-direction: column !important; }
    #pulse-run, #pulse-stop {
        border-left: 1px solid var(--edge-bright) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        width: 100% !important;
    }
    #pulse-query textarea, #pulse-query input { border-radius: 10px 10px 0 0 !important; }
}
"""

JS = """
() => {
    const focus = () => {
        const el = document.querySelector("#pulse-query textarea, #pulse-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""