import time

requests = {}

LIMIT = 5
WINDOW = 60


async def rate_limit_middleware(request, call_next):

    client_ip = request.client.host

    now = time.time()

    if client_ip not in requests:
        requests[client_ip] = []

    requests[client_ip] = [
        t for t in requests[client_ip]
        if now - t < WINDOW
    ]

    if len(requests[client_ip]) >= LIMIT:

        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "message": "Please try again later."
            }
        )

    requests[client_ip].append(now)

    return await call_next(request)