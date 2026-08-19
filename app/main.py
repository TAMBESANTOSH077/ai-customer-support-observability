from pathlib import Path
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.middleware.request_id import request_id_middleware
from app.utils.logger import setup_logger

from app.utils.ai_metrics import (
    record_request,
    get_metrics
)


# ========================================
# PATHS
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"


# ========================================
# APP
# ========================================

app = FastAPI(
    title="AI Customer Support Observability API",
    description="Production debugging and observability system",
    version="1.0.0"
)


# ========================================
# LOGGER
# ========================================

logger = setup_logger()


# ========================================
# STATIC FILES
# ========================================

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# ========================================
# REQUEST ID
# ========================================

app.middleware(
    "http"
)(request_id_middleware)


# ========================================
# TIMING + METRICS
# ========================================

@app.middleware("http")
async def timing_middleware(
    request: Request,
    call_next
):

    start_time = time.perf_counter()

    try:

        response = await call_next(
            request
        )

        success = (
            response.status_code < 400
        )

    except Exception as error:

        success = False

        request_id = getattr(
            request.state,
            "request_id",
            "unknown"
        )

        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "error": str(error)
            }
        )

        raise

    finally:

        duration_ms = round(
            (
                time.perf_counter()
                - start_time
            ) * 1000,
            2
        )

        request_id = getattr(
            request.state,
            "request_id",
            "unknown"
        )

        # Record metrics
        record_request(
            duration_ms,
            success
        )

        # Log request
        logger.info(
            "Request completed",
            extra={
                "request_id":
                    request_id,

                "method":
                    request.method,

                "path":
                    request.url.path,

                "duration_ms":
                    duration_ms
            }
        )

    # Add response headers

    response.headers[
        "X-Process-Time"
    ] = f"{duration_ms}ms"

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response


# ========================================
# FRONTEND
# ========================================

@app.get("/")
def frontend():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# ========================================
# HEALTH CHECK
# ========================================

@app.get("/health")
def health(
    request: Request
):

    request_id = (
        request.state.request_id
    )

    logger.info(
        "Health check called",
        extra={
            "request_id":
                request_id
        }
    )

    return {

        "status":
            "healthy",

        "service":
            "AI Customer Support API",

        "request_id":
            request_id
    }


# ========================================
# SUPPORT API
# ========================================

@app.get("/support")
def support(
    question: str,
    request: Request
):

    request_id = (
        request.state.request_id
    )

    logger.info(
        "Support request received",
        extra={
            "request_id":
                request_id,

            "question":
                question
        }
    )


    # --------------------------------
    # Empty question
    # --------------------------------

    if not question.strip():

        return JSONResponse(

            status_code=400,

            content={

                "error":
                    "Question cannot be empty",

                "request_id":
                    request_id
            }
        )


    # --------------------------------
    # Simulate slow request
    # --------------------------------

    if "slow" in question.lower():

        time.sleep(5)


    # --------------------------------
    # Simulate application error
    # --------------------------------

    if "error" in question.lower():

        raise Exception(
            "Simulated AI service failure"
        )


    # --------------------------------
    # Normal response
    # --------------------------------

    return {

        "question":
            question,

        "answer":
            "This is a sample AI customer-support response.",

        "request_id":
            request_id
    }


# ========================================
# METRICS
# ========================================

@app.get("/metrics")
def metrics():

    return get_metrics()


# ========================================
# GLOBAL ERROR HANDLER
# ========================================

@app.exception_handler(Exception)
async def error_handler(
    request: Request,
    exc: Exception
):

    request_id = getattr(
        request.state,
        "request_id",
        "unknown"
    )

    logger.error(
        "Application error",
        extra={
            "request_id":
                request_id,

            "error":
                str(exc)
        }
    )

    return JSONResponse(

        status_code=500,

        content={

            "error":
                "Internal server error",

            "message":
                "Something went wrong while processing the request.",

            "request_id":
                request_id
        }
    )