"""Uptrace client for Python"""

from typing import Optional

from opentelemetry import trace

from .dsn import DSN
from .util import remove_prefix

DUMMY_SPAN_NAME = "__dummy__"


class Client:
    """Uptrace client for Python"""

    def __init__(self, dsn: DSN):
        self._dsn = dsn
        self._tracer = None

    def report_exception(self, exc: Exception) -> None:
        """Reports an exception as a span event creating a dummy span if necessary."""

        span = trace.get_current_span()
        if span.is_recording():
            span.record_exception(exc)
            return

        span = self._get_tracer().start_span(DUMMY_SPAN_NAME)
        span.record_exception(exc)
        span.end()

    def trace_url(self, span: Optional[trace.Span] = None) -> str:
        """Returns the trace URL for the span."""

        if span is None:
            span = trace.get_current_span()

        dsn = self._dsn
        host = remove_prefix(dsn.host, "api.")
        trace_id = span.get_span_context().trace_id
        return f"{dsn.scheme}://{host}/search/{dsn.project_id}?q={trace_id:0{32}x}"

    def _get_tracer(self):
        if self._tracer is None:
            self._tracer = trace.get_tracer("uptrace-python")
        return self._tracer
