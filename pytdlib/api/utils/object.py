from collections import OrderedDict
from json import dumps


class Object:
    all = {}
    __slots__ = []
    ID = 'object'

    @staticmethod
    def read(q: dict, *args):
        if q is None:
            return None
        return Object.all[q["@type"]].read(q, *args)

    def __str__(self, indent: int = 1) -> str:
        def stringify(obj, indent):
            if isinstance(obj, Object):
                result = [obj.ID[:1].upper(), obj.ID[1:], '(', '\n']
                for attr in obj.__slots__:
                    value = getattr(obj, attr)

                    if value is None:
                        continue

                    result.append('\t' * indent)
                    result.append(attr)
                    result.append('=')

                    def sub_stringify(value, indent):
                        if isinstance(value, Object):
                            return stringify(value, indent + 1)
                        elif isinstance(value, (str, int, bytes)):
                            return repr(value)
                        elif hasattr(value, '__iter__'):
                            res = ['[\n']
                            indent += 1
                            for x in value:
                                res.append('\t' * indent)
                                res.append(stringify(x, indent + 1))
                                res.append(',\n')
                            indent -= 1
                            res.append('\t' * indent)
                            res.append(']')
                            return ''.join(res)
                        else:
                            return repr(value)

                    result.append(sub_stringify(value, indent))
                    result.append(',\n')
                else:
                    result[-1] = '\n'

                result.append('\t' * (indent - 1))
                result.append(')')
                return ''.join(result)
            else:
                return repr(obj)

        return stringify(self, indent)

    def __bytes__(self) -> bytes:
        def default(obj: Object):
            r = OrderedDict(
                [('@type', obj.ID)]
                + [(attr, getattr(obj, attr))
                   for attr in obj.__slots__
                   if getattr(obj, attr) is not None]
            )
            if r.get("extra"):
                r["@extra"] = r.pop("extra")
            return r

        return dumps(self, default=default).encode('utf-8')

    def __len__(self) -> int:
        return len(self.__bytes__())

    def __getitem__(self, item):
        return getattr(self, item)
