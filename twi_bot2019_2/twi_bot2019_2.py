# coding: utf-8
import logging
from lupa import LuaRuntime

__version__ = '0.4.0'

log = logging.getLogger(__name__)


def main():
    with open('test.lua') as f:
        lua_code = f.read()
    non_explode_lua = LuaRuntime(unpack_returned_tuples=False)
    non_explode_lua.execute(lua_code)
    g = non_explode_lua.globals()
    print(g.run(55))


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
        level=logging.DEBUG
    )
    main()
