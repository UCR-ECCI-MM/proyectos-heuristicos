# revisar que el resultado del parser tenga estructura correcta a partir de los objetos creados
from objects import MudFile, Mud, Policy, ACL, ACE

# funcion principal 
def validar_objetos(mud_file): # mud file es resultado final del parser
    errores = [] # es grave y sin eso el archivo no sirve
    advertencias = [] # se puede revisar despues, no rompe el programa

    if not isinstance(mud_file, MudFile): # si no es mud file no tiene sentido seguir revisando
        errores.append("El resultado principal no es un objeto MudFile")
        return errores, advertencias

    validar_mud_file(mud_file, errores, advertencias)
    validar_mud(mud_file.mud, errores, advertencias)
    # aqui falta una funcion de acl

    return errores, advertencias


# que existe mud y acl lists
def validar_mud_file(mud_file, errores, advertencias):
    if mud_file.mud is None:
        errores.append("MudFile no contiene el objeto mud")

    if mud_file.acl_lists is None:
        errores.append("MudFile no contiene la lista de ACL")
    elif not isinstance(mud_file.acl_lists, list): # que sea una lista
        errores.append("mud_file.acl_lists no es una lista")
    elif len(mud_file.acl_lists) == 0: # que no este vacia
        advertencias.append("El archivo no contiene ACL definidas")


def validar_mud(mud, errores, advertencias):
    if mud is None:
        return

    if not isinstance(mud, Mud):
        errores.append("El atributo mud no es un objeto Mud")
        return

    # validar campos obligatorios
    if mud.version is None:
        errores.append("El objeto Mud no contiene mud-version")

    if mud.url is None:
        errores.append("El objeto Mud no contiene mud-url")

    if mud.last_update is None:
        errores.append("El objeto Mud no contiene last-update")

    if mud.cache_validity is None:
        errores.append("El objeto Mud no contiene cache-validity")

    if mud.from_policy is None and mud.to_policy is None: # revisar que haya alguna politica
        errores.append("El objeto Mud no contiene from_policy ni to_policy")

    validar_policy(mud.from_policy, "from_policy", errores, advertencias)
    validar_policy(mud.to_policy, "to_policy", errores, advertencias)


def validar_policy(policy, nombre_policy, errores, advertencias):
    if policy is None:
        return

    if not isinstance(policy, Policy): # si no es objeto policy error
        errores.append(f"{nombre_policy} no es un objeto Policy")
        return

    if policy.acl_lists is None:
        errores.append(f"{nombre_policy} no contiene lista de ACL")
    elif not isinstance(policy.acl_lists, list):
        errores.append(f"{nombre_policy}.acl_lists no es una lista")
    elif len(policy.acl_lists) == 0:
        advertencias.append(f"{nombre_policy} no referencia ninguna ACL")
