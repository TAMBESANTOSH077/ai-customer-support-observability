import time


async def timing_middleware(
    request,
    call_next
):

    start_time = time.perf_counter()

    response = await call_next(
        request
    )

    end_time = time.perf_counter()

    duration = end_time - start_time

    duration_ms = round(
        duration * 1000,
        2
    )

    response.headers[
        "X-Process-Time"
    ] = f"{duration_ms}ms"

    print(
        f"Request: {request.method} "
        f"{request.url.path} | "
        f"Time: {duration_ms}ms"
    )

    return response