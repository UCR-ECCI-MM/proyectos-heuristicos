# para la raiz
class MudFile:
    #constructor que recibe un objeto mud y una lista de objetos ACL
    def __init__(self, mud, acl_lists):
        self.mud = mud
        self.acl_lists = acl_lists
    #para imprimirlo de forma legible
    def __repr__(self):
        return f"MudFile(mud={self.mud}, acl_lists={len(self.acl_lists)} ACLs)"

# para la parte de mud
class Mud:
    def __init__(self, version, url, last_update, cache_validity,
                 from_policy=None, to_policy=None, opcionales=None):
        #obligatorios
        self.version = version
        self.url = url
        self.last_update = last_update
        self.cache_validity = cache_validity
        self.from_policy = from_policy
        self.to_policy = to_policy
        #opcionales
        self.opcionales = opcionales or {}

    def __repr__(self):
        # Si hay campos opcionales se muestran
        if self.opcionales:
            return (
                f"Mud(version={self.version}, url={self.url}, "
                f"last_update={self.last_update}, cache_validity={self.cache_validity}, "
                f"from_policy={self.from_policy}, to_policy={self.to_policy}, "
                f"opcionales={self.opcionales})"
            )
        #si no no se muestran
        else:
            return (
                f"Mud(version={self.version}, url={self.url}, "
                f"last_update={self.last_update}, cache_validity={self.cache_validity}, "
                f"from_policy={self.from_policy}, to_policy={self.to_policy})"
            )
        
class ACE:
    def __init__(self, name, matches, actions):
        self.name = name
        self.matches = matches
        self.actions = actions

    def __repr__(self): # para debug
        return f"ACE(name={self.name}, matches={self.matches}, actions={self.actions})"

class Policy:
    def __init__(self, acl_lists):
        self.acl_lists = acl_lists
    def __repr__(self):
        return f"Policy(acl_lists={len(self.acl_lists)} ACLs)"

class ACL:
    def __init__(self, name, type, aces):
        self.name = name
        self.type = type
        self.aces = aces  # lista de objetos ACE
    def __repr__(self):
        return f"ACL(name={self.name}, type={self.type}, aces={len(self.aces)} ACEs)"

