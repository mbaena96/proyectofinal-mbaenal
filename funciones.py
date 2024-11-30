from os import system

def esto_es_sano(calorias:int, es_vegetariano:bool) -> bool:
    if calorias < 100 or es_vegetariano:
        return True
    else:
        return False
    
def obtener_calorias(calorias:list) -> float:
    total_calorias = 0.0
    for caloria in calorias:
        total_calorias += caloria
    return round(total_calorias * 0.95, 2)

def obtener_costos(ingrediente1:dict, ingrediente2:dict, ingrediente3:dict) -> float:
    return ingrediente1["precio"] + ingrediente2["precio"] + ingrediente3["precio"]

def obtener_rentabilidad(precio_producto:float, ingrediente1:dict, ingrediente2:dict, ingrediente3:dict) -> float:
    return precio_producto - obtener_costos(ingrediente1, ingrediente2, ingrediente3)

def producto_mas_rentable(producto1:dict, producto2:dict, producto3:dict, producto4:dict):
    mejor_producto = producto1
    for producto in [producto2, producto3, producto4]:
        if producto["rentabilidad"] > mejor_producto["rentabilidad"]:
            mejor_producto = producto
    
    return mejor_producto["nombre"]
