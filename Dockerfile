FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY src ./src
COPY data ./data

ENV PATH="/app/.venv/bin:$PATH"

CMD ["dreamtraffic", "--help"]
