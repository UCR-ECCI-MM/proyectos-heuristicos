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
    validar_lista_acl(mud_file.acl_lists, errores, advertencias)

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


def validar_lista_acl(lista_acl, errores, advertencias):
    if lista_acl is None:
        return

    if not isinstance(lista_acl, list): # si no es lista no la recorre para no causar error
        return

    for acl in lista_acl: # por cada acl revisada llama a validar acl
        validar_acl(acl, errores, advertencias)

# revisa cada objeto acl con campos como name, aces etc
def validar_acl(acl, errores, advertencias):
    if not isinstance(acl, ACL):
        errores.append("Se encontro un elemento en acl_lists que no es objeto ACL")
        return

    if acl.name is None or acl.name == "":
        errores.append("Se encontro un ACL sin name")

    if acl.type is None or acl.type == "":
        errores.append(f"El ACL '{acl.name}' no tiene type")

    if acl.aces is None:
        errores.append(f"El ACL '{acl.name}' no contiene lista de ACE")
        return

    if not isinstance(acl.aces, list):
        errores.append(f"El atributo aces del ACL '{acl.name}' no es una lista")
        return

    if len(acl.aces) == 0: # si no tiene advetencia se toma como sospechoso
        advertencias.append(f"El ACL '{acl.name}' no contiene reglas ACE")

    for ace in acl.aces:
        validar_ace(ace, acl.name, errores, advertencias)


def validar_ace(ace, nombre_acl, errores, advertencias):
    if not isinstance(ace, ACE):
        errores.append(f"Se encontro un elemento en el ACL '{nombre_acl}' que no es objeto ACE")
        return

    if ace.name is None or ace.name == "":
        errores.append(f"Se encontro un ACE sin name dentro del ACL '{nombre_acl}'")

    if ace.matches is None:
        errores.append(f"El ACE '{ace.name}' no contiene matches")
    elif not isinstance(ace.matches, dict):
        errores.append(f"El atributo matches del ACE '{ace.name}' no es un diccionario")
    elif len(ace.matches) == 0:
        advertencias.append(f"El ACE '{ace.name}' tiene matches vacio")

    if ace.actions is None:
        errores.append(f"El ACE '{ace.name}' no contiene actions")
    elif not isinstance(ace.actions, dict):
        errores.append(f"El atributo actions del ACE '{ace.name}' no es un diccionario")
    elif len(ace.actions) == 0:
        errores.append(f"El ACE '{ace.name}' tiene actions vacio")