"""
Возможности по умолчанию
"""

def reponse(data: dict, status: str = "OK") -> dict:
    """
    Формирует тело ответа и возвращает его
    """
    if status.lower() == "ok":
        return {
            "status": status,
            "data": data
        }
    else:
        return {
            "error": status,
            "message": data
        }