import asyncio
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
#from .style import CSS, JS, EXAMPLES, HEADER_HTML
#from .style_patch import CSS_PATCH, JS_PATCH
from css_styles.styles import CSS, JS, EXAMPLES, HEADER_HTML
from tools.report_export import generate_downloads

load_dotenv(override=True)

# Merge the Claude-style button / thinking-indicator CSS onto whatever
# style.py already defines, rather than editing style.py directly.
#CSS = CSS + CSS_PATCH
#JS = (JS or "") + JS_PATCH


THINKING_HTML = (
    '<div id="pulse-thinking">'
    '<span class="pulse-dot">\u2726</span> Researching&hellip;'
    "</div>"
)


async def run(query: str, cancel_event: asyncio.Event | None):
    """Stream status updates from the research manager for a given query.

    Yields a (markdown_text, markdown_text) pair each step: one copy renders
    live in the report panel, the other is captured into `report_state` so
    the final text is available afterwards for the PDF/DOCX export step.

    `cancel_event` is a fresh per-run flag (see `enter_running_state`) that
    the Stop button sets. We pass it straight through to `ResearchManager`,
    which checks it between steps and exits cleanly on its own -- we
    deliberately do NOT use Gradio's `cancels=[...]` task-cancellation here,
    since cancelling a chained `.then()` step mid-flight left Gradio's queue
    bookkeeping for that event inconsistent across repeated runs (the Stop
    button would stop reappearing on the second/third run). Cooperative
    cancellation avoids that entirely: every run, cancelled or not, always
    finishes its `.then()` chain the same way.
    """
    if not query or not query.strip():
        msg = "Enter a research question above to get started."
        yield msg, msg
        return
    async for status_update in ResearchManager().run(query, cancel_event=cancel_event):
        yield status_update, status_update


def enter_running_state():
    """Swap the Investigate button out for a Stop button, show the thinking
    indicator, hide any download buttons left over from a previous run, and
    hand out a fresh cancellation flag for this run.
    """
    return (
        gr.update(visible=False),  # run_button
        gr.update(visible=True),  # stop_button
        gr.update(visible=True),  # thinking_indicator
        gr.update(visible=False, value=None),  # pdf_download
        gr.update(visible=False, value=None),  # docx_download
        asyncio.Event(),  # cancel_state -- this run's own stop flag
    )


def enter_idle_state():
    """Restore the default controls once a run finishes, errors, or is stopped."""
    return (
        gr.update(visible=True, interactive=True),  # run_button
        gr.update(visible=False),  # stop_button
        gr.update(visible=False),  # thinking_indicator
    )


def request_stop(cancel_event: asyncio.Event | None):
    """Flip the current run's cancellation flag and restore idle controls.

    Note this can't interrupt a model call that's already in flight -- the
    running step has to return first, exactly like before -- but it always
    reliably signals the generator to stop *afterwards*, and always leaves
    the UI in the same, predictable idle state.
    """
    if cancel_event is not None:
        cancel_event.set()
    return enter_idle_state()


with gr.Blocks(title="Research Manager") as ui:
    gr.HTML(HEADER_HTML)

    with gr.Row(elem_classes="pulse-query-row"):
        query_textbox = gr.Textbox(
            placeholder="Type a research question...",
            show_label=False,
            container=False,
            autofocus=True,
            elem_id="pulse-query",
            scale=5,
        )
        run_button = gr.Button("Investigate", variant="primary", elem_id="pulse-run", scale=1)
        stop_button = gr.Button("Stop", elem_id="pulse-stop", scale=1, visible=False)

    thinking_indicator = gr.HTML(THINKING_HTML, elem_id="pulse-thinking-wrap", visible=False)

    gr.HTML('<div class="pulse-examples-label">Try one</div>')
    gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="pulse-examples")

    report = gr.Markdown(elem_id="pulse-report")
    report_state = gr.State("")
    # Holds this session's current asyncio.Event used to signal a Stop
    # request to the in-progress run. Recreated fresh at the start of every
    # run so each run has its own independent flag.
    cancel_state = gr.State(None)

    with gr.Row(elem_classes="pulse-download-row"):
        pdf_download = gr.DownloadButton(
            "Download as PDF", elem_id="pulse-download-pdf", visible=False
        )
        docx_download = gr.DownloadButton(
            "Download as Word", elem_id="pulse-download-docx", visible=False
        )

    # Each trigger: flip to the "running" control state (and mint a fresh
    # cancel flag), stream the report, generate the downloadable files, then
    # flip back to "idle" once the generator finishes -- whether it finished
    # naturally or was told to stop early.
    click_run_event = run_button.click(
        enter_running_state,
        outputs=[run_button, stop_button, thinking_indicator, pdf_download, docx_download, cancel_state],
    ).then(run, inputs=[query_textbox, cancel_state], outputs=[report, report_state])
    click_run_event.then(generate_downloads, inputs=report_state, outputs=[pdf_download, docx_download])
    click_run_event.then(enter_idle_state, outputs=[run_button, stop_button, thinking_indicator])

    submit_run_event = query_textbox.submit(
        enter_running_state,
        outputs=[run_button, stop_button, thinking_indicator, pdf_download, docx_download, cancel_state],
    ).then(run, inputs=[query_textbox, cancel_state], outputs=[report, report_state])
    submit_run_event.then(generate_downloads, inputs=report_state, outputs=[pdf_download, docx_download])
    submit_run_event.then(enter_idle_state, outputs=[run_button, stop_button, thinking_indicator])

    # Stop just flips this run's cancel flag and resets the controls through
    # Gradio's normal reactive update path -- no Gradio-level task
    # cancellation and no manual DOM patching involved, so the chain
    # completes identically (and correctly) every single run.
    stop_button.click(
        request_stop,
        inputs=[cancel_state],
        outputs=[run_button, stop_button, thinking_indicator],
    )


if __name__ == "__main__":
    # `default_concurrency_limit` matters here: Gradio's own default is 1,
    # meaning EVERY event in the whole app -- Examples clicks, a second
    # Investigate click, even Stop -- shares a single global worker slot and
    # has to wait for the entire previous event's full `.then()` chain
    # (including PDF/DOCX generation) to finish first. Raising it lets
    # lightweight UI events run immediately instead of queuing behind a
    # still-finishing research run.
    ui.queue(default_concurrency_limit=10)
    ui.launch(css=CSS, js=JS, theme=gr.themes.Base())