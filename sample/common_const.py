import sys


class _heroConst:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _heroConst()

_heroConst.HERO_NAME_DEADPOND = "Deadpond"
_heroConst.HERO_NAME_SPIDER_BOY = "Spider-Boy"
_heroConst.HERO_NAME_RUSTY_MAN = "Rusty-Man"


_heroConst.HERO_SECRET_NAME_DEADPOND = "Dive Wilson"
_heroConst.HERO_SECRET_NAME_SPIDER_BOY = "Pedro Parqueador"
_heroConst.HERO_SECRET_NAME_RUSTY_MAN = "Tommy Sharp"


_heroConst.TEAM_NAME_PREVENTERS = "Preventers"
_heroConst.TEAM_NAME_Z_FORCE = "Z-Force"
