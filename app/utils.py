def normalizar_patente(patente):
    """
    Normaliza una patente: mayúsculas, sin espacios ni guiones
    """
    if not patente:
        return None
    
    # Convertir a mayúsculas y quitar espacios/guiones
    patente_limpia = patente.upper().replace(' ', '').replace('-', '')
    
    return patente_limpia
