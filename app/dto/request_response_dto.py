
def get_response(status, detail=None, data=None):
    response = {
        "status": status
    }

    if (detail):
        response["detail"] = detail

    if (data):
        response["data"] = data

    return response
