# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastmcp import FastMCP
from ner_service.api.routes import router
from ner_service.config.logger import logger


app = FastAPI(
    title="NER Service API",
    version="1.0.0",
    description="Named Entity Recognition Service"
)

app.include_router(router, prefix="/api/v1", tags=["NER"])

mcp = FastMCP.from_fastapi(app=app, timeout=30)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=18001, path="/mcp")
