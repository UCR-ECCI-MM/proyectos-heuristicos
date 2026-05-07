
#funcion muy basicasolo para ver si el reporte esta bien

# function to validate that the objects are correct 
def validar_objetos(resultado):
    errores = []

    if resultado.mud is None:
        errores.append("No existe el bloque mud")

    if not isinstance(resultado.acl_lists, list):
        errores.append("acl_lists no es una lista")

    return errores

# function to validate consistency rules on the objects
def validar_consistencia(resultado):
    errores = []
    advertencias = []

    if resultado.mud.from_policy and len(resultado.acl_lists) == 0:
        errores.append("Hay from-policy pero no hay ACLs")

    if resultado.mud.to_policy and len(resultado.acl_lists) == 0:
        errores.append("Hay to-policy pero no hay ACLs")

    if len(resultado.acl_lists) == 0:
        advertencias.append("No hay ACLs definidas")

    return errores, advertencias