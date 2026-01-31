def ok(data):
    return {
        "success": True,
        "data": data,
        "error": None
    }

def fail(code, message):
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }
