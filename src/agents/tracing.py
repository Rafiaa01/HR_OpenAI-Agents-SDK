
import json
from datetime import UTC, datetime
from pathlib import Path

from agents.tracing import TracingProcessor

TRACE_FILE = Path(__file__).resolve().parent / "traces.jsonl"


class LocalTracingProcessor(TracingProcessor):

    def on_trace_start(self, trace):
        self._save_event(
            "trace_started",
            {
                "trace_id": trace.trace_id,
                "name": trace.name,
            }
        )

    def on_trace_end(self, trace):
        self._save_event(
            "trace_completed",
            {
                "trace_id": trace.trace_id,
                "name": trace.name,
            }
        )

    def on_span_start(self, span):
        pass

    def on_span_end(self, span):
        self._save_event(
            "span_completed",
            span.export()
        )

    def force_flush(self):
        pass

    def shutdown(self):
        pass

    def _save_event(self, event_type, data):
        event = {
            "event": event_type,
            "timestamp": datetime.now(UTC).isoformat(),
            "data": data,
        }

        with open(TRACE_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(event, default=str) + "\n")
