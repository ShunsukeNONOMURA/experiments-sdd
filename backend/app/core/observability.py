from __future__ import annotations

import json
import logging
import uuid
from contextvars import ContextVar
from typing import Any, Dict

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
logger = logging.getLogger("app.observability")


def new_trace_id() -> str:
    trace_id = uuid.uuid4().hex
    trace_id_ctx.set(trace_id)
    return trace_id


def set_trace_id(trace_id: str) -> None:
    trace_id_ctx.set(trace_id)


def get_trace_id() -> str:
    trace_id = trace_id_ctx.get()
    if trace_id is None:
        trace_id = new_trace_id()
    return trace_id


def standard_response(payload: Dict[str, Any] | list[Any], **meta: Any) -> Dict[str, Any]:
    base: Dict[str, Any]
    if isinstance(payload, dict):
        base = {**payload}
    else:
        base = {"data": payload}
    base["traceId"] = get_trace_id()
    if meta:
        base["meta"] = meta
    return base


def log_event(action: str, **fields: Any) -> None:
    entry = {"action": action, "traceId": get_trace_id(), **fields}
    logger.info(json.dumps(entry, ensure_ascii=False))


def configure_metrics(app: FastAPI, enabled: bool = True) -> None:
    if not enabled or getattr(app.state, "metrics_configured", False):
        return
    Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)
    app.state.metrics_configured = True
