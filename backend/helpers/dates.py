from datetime import datetime, timedelta

def serialize_dates(data):
    """
    Serializa las fechas y los timedelta en un formato que se pueda convertir a JSON.
    
    Args:
        data: El dato a serializar.
        
    Returns:
        El dato serializado.
    """
    if isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, timedelta):
        return str(data)
    elif isinstance(data, dict):
        return {key: serializar_fechas(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serializar_fechas(item) for item in data]
    return data