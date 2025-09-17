
# FastAPI Server Setup Guide

This directory contains the FastAPI backend service. Follow the steps below to set up and run the server.

## Requirements
- Python 3.12 or above
- All dependencies installed (see `pyproject.toml`)


## Install Dependencies

Use [uv](https://github.com/astral-sh/uv) to install dependencies:

```bash
uv sync
```

## Start the Server

```bash
uv run fastapi dev main.py
```

By default, the API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
