from __future__ import annotations

import logging
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes import api_router
from app.core.config import settings
from app.core.observability import configure_metrics, new_trace_id, set_trace_id

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version="0.1.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        trace_id = request.headers.get("x-trace-id") or new_trace_id()
        set_trace_id(trace_id)
        response = await call_next(request)
        response.headers["x-trace-id"] = trace_id
        return response


def configure_app(application: FastAPI) -> None:
    application.add_middleware(TraceIDMiddleware)
    application.include_router(api_router)
    configure_metrics(application, enabled=settings.enable_metrics)


configure_app(app)


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.environment == "development")


__all__ = ["app", "run"]
