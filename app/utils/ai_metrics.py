# ========================================
# AI APPLICATION METRICS
# ========================================

request_count = 0
error_count = 0
slow_request_count = 0

total_processing_time = 0.0


# ========================================
# RECORD REQUEST
# ========================================

def record_request(
    duration_ms,
    success=True
):

    global request_count
    global error_count
    global slow_request_count
    global total_processing_time

    # Count request
    request_count += 1

    # Add processing time
    total_processing_time += duration_ms

    # Count errors
    if not success:
        error_count += 1

    # Request taking more than 1 second
    # is considered slow
    if duration_ms > 1000:
        slow_request_count += 1


# ========================================
# GET METRICS
# ========================================

def get_metrics():

    if request_count > 0:

        average_time = round(
            total_processing_time / request_count,
            2
        )

    else:

        average_time = 0


    return {

        "total_requests":
            request_count,

        "total_errors":
            error_count,

        "slow_requests":
            slow_request_count,

        "average_processing_time_ms":
            average_time
    }