# comprobar relaciones en la estructura
# evitar errores de consistencia
from objects import Policy, ACL

# funcion principal
def validar_consistencia(mud_file): # reciibe objeto final parser
    errores = []
    advertencias = []

    # funcion que recorre todas las acl reales del archivo y extrae sus nombres
    nombres_acl_definidas = obtener_nombres_acl_definidas(mud_file)
    nombres_acl_referenciadas = [] # se va llenando con los nombres acl que van apareciendo en from y to policy

    if mud_file.mud.from_policy is not None: # revisa primero igual que todos si existe from policy
        revisar_policy(mud_file.mud.from_policy, "from_policy", nombres_acl_definidas,
            nombres_acl_referenciadas, errores)

    # politica de trafico hacia el dispositivo
    if mud_file.mud.to_policy is not None:
        revisar_policy(mud_file.mud.to_policy, "to_policy", nombres_acl_definidas, 
                       nombres_acl_referenciadas, errores)

    revisar_acl_no_referenciadas( # detecta acl que estan definidas pero no se usan
        nombres_acl_definidas,
        nombres_acl_referenciadas,
        advertencias
    )

    return errores, advertencias


def obtener_nombres_acl_definidas(mud_file): # recorre todas las acl que existen realmente en el archivo
    nombres = [] # lista vacia para guardar nombres

    for acl in mud_file.acl_lists:
        if isinstance(acl, ACL): # verifica que el elemento sea si o si un objeto acl
            if acl.name not in nombres:
                nombres.append(acl.name)

    return nombres


def revisar_policy(policy, nombre_policy, nombres_acl_definidas, nombres_acl_referenciadas, errores):
    if not isinstance(policy, Policy):
        errores.append(f"{nombre_policy} no es un objeto Policy.")
        return

    for nombre_acl in policy.acl_lists:
        if nombre_acl not in nombres_acl_referenciadas:
            nombres_acl_referenciadas.append(nombre_acl) # sirve despues para saber cuales acl fueron usadas

        if nombre_acl not in nombres_acl_definidas:
            errores.append(f"La ACL '{nombre_acl}' esta referenciada en {nombre_policy}, pero no existe en la lista de ACL.")


def revisar_acl_no_referenciadas(nombres_acl_definidas, nombres_acl_referenciadas, advertencias):
    for nombre_acl in nombres_acl_definidas:
        if nombre_acl not in nombres_acl_referenciadas:
            advertencias.append(f"La ACL '{nombre_acl}' existe, pero no esta referenciada en from_policy ni en to_policy.")