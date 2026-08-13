from agents import trace, gen_trace_id
from agentss.search_agent import search_agent
from agentss.planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from agentss.writer_agent import writer_agent, ReportData
from agentss.email_agent import email_agent
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime, UTC
from agents.tracing import set_trace_processors
from agentss.rerun_func import run_with_retry

# ============================================================
# STEP 2: Define production-style local trace processor
# ============================================================
class LocalFileTraceProcessor:
    """
    Mirrors OpenAI's trace dashboard structure:
    - Trace-level: ID, workflow name, total duration
    - Span-level: type, parent, timing (ms), hierarchical depth
    - Outputs a human-readable console view + structured JSONL log
    """

    def __init__(self, log_path="traces.json5"):
        self.log_path = Path(log_path)
        self._trace_start_times = {}   # trace_id -> start epoch
        self._span_start_times  = {}   # span_id  -> start epoch
        self._span_parents      = {}   # span_id  -> parent_span_id
        self._span_depth        = {}   # span_id  -> depth level (for indentation)
        self._active_trace      = None
 
    # ----------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------
    def _write(self, record: dict):
        record["logged_at"] = datetime.now(UTC).isoformat()
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def _indent(self, span_id: str) -> str:
        depth = self._span_depth.get(span_id, 0)
        return "  " * depth

    def _span_type(self, span) -> str:
        """Extract clean span type name, mirroring OpenAI's labels."""
        return span.span_data.__class__.__name__.replace("SpanData", "")

    def _elapsed_ms(self, start: float) -> float:
        return round((time.perf_counter() - start) * 1000, 2)

    # ----------------------------------------------------------
    # Trace lifecycle
    # ----------------------------------------------------------
    def on_trace_start(self, trace):
        self._trace_start_times[trace.trace_id] = time.perf_counter()
        self._active_trace = trace

        header = f"{'─' * 60}" 
        print(f"\n{header}")
        print(f"  📋 Trace: {trace.name}")
        print(f"  🔑 ID:    {trace.trace_id}")
        print(f"  🕐 Started: {datetime.now(UTC).strftime('%H:%M:%S UTC')}")
        print(f"{header}")

        self._write({
            "event":      "trace_start",
            "name":       trace.name,
            "trace_id":   trace.trace_id,
        })

    def on_trace_end(self, trace):
        start    = self._trace_start_times.pop(trace.trace_id, None)
        duration = self._elapsed_ms(start) if start else "N/A"

        print(f"{'─' * 60}")
        print(f"  ✅ Trace complete: {trace.name}")
        print(f"  ⏱  Total duration: {duration}")
        print(f"{'─' * 60}\n")
 
        self._write({
            "event":    "trace_end",
            "name":     trace.name,
            "trace_id": trace.trace_id,
            "duration": duration,
        })         
   
    # ----------------------------------------------------------
    # Span lifecycle
    # ----------------------------------------------------------
    def on_span_start(self, span):
        self._span_start_times[span.span_id] = time.perf_counter()

        # Infer depth from parent chain
        parent_id = getattr(span, "parent_id", None)
        self._span_parents[span.span_id] = parent_id
        parent_depth = self._span_depth.get(parent_id, -1) if parent_id else -1
        self._span_depth[span.span_id] = parent_depth + 1

        indent    = self._indent(span.span_id)
        span_type = self._span_type(span)

        # Mirror OpenAI's span type icons
        icons = {
            "Agent":    "🤖",
            "LLM":      "🌐",  # POST /v1/responses equivalent
            "Tool":     "🔧",
            "Handoff":  "🔀",
            "Custom":   "📌",
        }
        icon = icons.get(span_type, "▶")

        print(f"{indent}{icon} [{span_type}] started  —  span_id: {span.span_id[:12]}...")

        self._write({
            "event":     "span_start",
            "trace_id":  getattr(self._active_trace, "trace_id", None),
            "span_id":   span.span_id,
            "parent_id": parent_id,
            "type":      span_type,
            "depth":     self._span_depth[span.span_id],
        })

    def on_span_end(self, span):
        start     = self._span_start_times.pop(span.span_id, None)
        duration  = self._elapsed_ms(start) if start else "N/A"
        indent    = self._indent(span.span_id)
        span_type = self._span_type(span)

        # Extract useful payload depending on span type
        detail = ""
        data   = span.span_data
        if hasattr(data, "output") and data.output:
            detail = f"→ output: {str(data.output)[:2000]}" # or just str(data.output), no cap
        elif hasattr(data, "name") and data.name:
            detail = f"→ {data.name}"

        print(f"{indent}  ✔ [{span_type}]  {duration}  {detail}")

        self._write({
            "event":     "span_end",
            "trace_id":  getattr(self._active_trace, "trace_id", None),
            "span_id":   span.span_id,
            "parent_id": self._span_parents.get(span.span_id),
            "type":      span_type,
            "depth":     self._span_depth.get(span.span_id, 0),
            "duration":  duration,
            "detail":    detail,
        })

    # ----------------------------------------------------------
    # SDK-required lifecycle hooks
    # ----------------------------------------------------------
    def shutdown(self):
        print("🛑 Trace processor shut down.")

    def force_flush(self):
        pass  # nothing buffered — every write is immediate

# ============================================================
# STEP 4: Replace default trace processors with our local one
# (prevents the 401 error from OpenAI's default backend)
# ============================================================
set_trace_processors([LocalFileTraceProcessor()])

class ResearchManager:

    async def run(self, query: str, cancel_event=None):
        """Run the research process, yielding status updates and the final report.

        `cancel_event` (an `asyncio.Event`, optional) is checked between each
        major step below. If the Stop button has set it, we yield a final
        "stopped" message and return -- cleanly ending the generator -- instead
        of relying on Gradio's task-level cancellation to interrupt us via
        `asyncio.CancelledError`. Note this can only take effect *between*
        steps: a model call that's already in flight (inside `run_with_retry`)
        still has to finish first, since there's no way to abort an
        already-dispatched HTTP request from here.
        """
        def stopped() -> bool:
            return cancel_event is not None and cancel_event.is_set()

        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"Starting research. Trace ID: {trace_id} (logged locally to traces.json5)"

            search_plan = await self.plan_searches(query)
            if stopped():
                yield "Research stopped."
                return
            yield f"Searches planned, starting {len(search_plan.searches)} searches..."

            search_results = await self.perform_searches(search_plan)
            if stopped():
                yield "Research stopped."
                return
            yield "Searches complete, writing report..."

            report = await self.write_report(query, search_results)
            if stopped():
                yield "Research stopped."
                return
            yield "Report written, sending email..."

            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        result = await run_with_retry(planner_agent, f"Query: {query}")
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await run_with_retry(search_agent, input_message)
        return result.final_output

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        input_message = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await run_with_retry(writer_agent, input_message)
        return result.final_output
    
    async def send_email(self, report: ReportData) -> None:
        await run_with_retry(email_agent, report.markdown_report)