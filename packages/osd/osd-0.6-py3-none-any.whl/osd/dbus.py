from gi.repository import GLib, Gio
from typing import List, Dict

class uint(int):
    pass

class variant:
    pass

def export(f):
    def get_out_arg(x):
        if isinstance(x, tuple):
            name, t = x
            return ('out', name, t)
        else:
            return ('out', None, x)

    types = f.__annotations__
    f.__dbus_in__ = [('in', n, types.get(n)) for n in f.__code__.co_varnames[1:]]
    if 'return' in types:
        out_type = types['return']
        if isinstance(out_type, list) or isinstance(out_type, str):
            f.__dbus_out__ = [get_out_arg(t) for t in out_type]
        else:
            f.__dbus_out__ = [get_out_arg(out_type)]
    else:
        f.__dbus_out__ = []
    f.__dbus_export__ = True

    return f

def interface(name):
    def decorate(f):
        f.__dbus_interface__ = name
        return f
    return decorate

def publish_object(name, path, object):
    xml = node_xml([type(object)])
    iface = Gio.DBusNodeInfo.new_for_xml(xml).interfaces[0]

    def on_bus_acquired(conn, name):
        conn.register_object(path,
                             iface,
                             on_method_call,
                             None,
                             None)

    def on_method_call(conn, sender, path, iface, name, params, inv):
        method = getattr(object, name)
        result = method(*params)
        types = [dbus_type(t) for (_,_,t) in method.__dbus_out__]
        type = "({})".format("".join(types))
        if len(types) == 0:
            result = ()
        elif len(types) == 1:
            result = (result, )

        inv.return_value(GLib.Variant(type, result))

    def on_property_set(conn, sender, path, iface, method, params, inv):
        pass

    return Gio.bus_own_name(Gio.BusType.SESSION,
                            name,
                            Gio.BusNameOwnerFlags.NONE,
                            on_bus_acquired,
                            lambda conn, name: None,
                            lambda conn, name: None)
def dbus_type(t):
    if type(t) == str:
        return t[0]
    elif getattr(t, '__origin__', None) == list:
        return 'a{}'.format(dbus_type(t.__args__[0]))
    elif getattr(t, '__origin__', None) == dict:
        return 'a{{{}{}}}'.format(*(dbus_type(a) for a in t.__args__))
    else:
        return t.__name__[0]

def arg_xml(direction, name, type):
    props = [('type', dbus_type(type)),
             ('name', name),
             ('direction', direction)]
    return '<arg {} />'.format(
        " ".join('{}="{}"'.format(k,v) for
                 (k,v) in props if v is not None))

def method_xml(method):
    args = method.__dbus_in__ + method.__dbus_out__
    return '<method name="{}">\n{}\n</method>'.format(
        method.__name__,
        "\n".join(arg_xml(*arg) for arg in args))

def interface_xml(t):
    return '<interface name="{}">\n{}\n</interface>'.format(
        t.__dbus_interface__,
        "\n".join(method_xml(method)
                  for name in dir(t)
                  for method in [getattr(t, name)]
                  if hasattr(method, '__dbus_export__')))

def node_xml(ts):
    return '<node>\n{}\n</node>'.format(
        "\n".join(interface_xml(t) for t in ts))
