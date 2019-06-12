import os
import re
import shutil
from collections import OrderedDict


HOME = 'generate/api'
DESTINATION = 'pytdlib/api'
SECTION_RE = re.compile(r'---(\w+)---')
COMBINATOR_RE = re.compile(r'^(\w+) (.*)?= (\w+);$')
ARGS_RE = re.compile('(\w+):([\w<>]+)')
DOCS_RE = re.compile(r'//((-)|@)(description)?([\w -.,;]+)(@?)(.*)?')
ClASS_DOCS_RE = re.compile(r"^//@class (\w+) @description (.*)")

core_types = {
    'int': 'int', 'int32': 'int', 'int53': 'int', 'int64': 'int', 'long': 'int', 'double': 'float',
    'string': 'str',
    'bytes': 'bytes',
    'Bool': 'bool'
}


def upper_first(s: str):
    return s[:1].upper() + s[1:]


def lower_first(s: str):
    return s[:1].lower() + s[1:]


def snek(s: str):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()


class Combinator:
    def __init__(self, section, name, description):
        self.section = section
        self.name = name
        self.description = description


class MethodCombinator(Combinator):
    def __init__(self, name: str, description: str, params_desc: list, args: dict, return_type: str, section='types'):
        super().__init__(section, name, description)
        self.params_description = params_desc
        self.args = args
        self.return_type = return_type


class ClassCombinator(Combinator):
    def __init__(self, name, description):
        super().__init__('types', name, description)
        self.sub_classes = set()


def start():
    shutil.rmtree('{}/types/'.format(DESTINATION), ignore_errors=True)
    shutil.rmtree('{}/functions/'.format(DESTINATION), ignore_errors=True)

    with open('{}/scheme/td_api.tl'.format(HOME), encoding='utf-8') as f:
        scheme = f.read()

    with open("{}/template/class.txt".format(HOME), encoding="utf-8") as f:
        template = f.read()

    notice = ''

    section = 'types'
    method_description = ''
    method_combinators = {}
    class_combinators = {}
    descriptions = []
    scheme_data = scheme.splitlines()
    return_types = set()

    for line in scheme_data[14:]:
        # check section changer line
        s = SECTION_RE.match(line)
        if s:
            section = s.group(1)
            continue

        # check for class description line
        c = ClASS_DOCS_RE.match(line)
        if c:
            class_name, class_desc = c.groups()
            class_combinators[class_name] = ClassCombinator(class_name, class_desc)
            continue

        # check description line
        d = DOCS_RE.match(line)
        if d:
            _, extra_desc, method_desc, desc, has_extra, extra_data = d.groups()
            # check for method description
            if method_desc is not None:
                method_description = desc
            elif extra_desc is not None:
                if descriptions:
                    descriptions[-1] += '. %s' % desc
                else:
                    method_description += '. %s' % desc
            else:
                descriptions.append(desc)
                
            # split data by @ and save in descriptions list

            if has_extra:
                descriptions.extend(des for des in extra_data.split('@'))
            continue

        combinator = COMBINATOR_RE.match(line)
        if combinator:
            name, args_text, return_type = combinator.groups()
            args = OrderedDict([(arg.split(':')[0], arg.split(':')[1]) for arg in args_text.rstrip().split(' ')] if args_text else [])
            method_combinators[name] = MethodCombinator(
                upper_first(name),
                method_description,
                descriptions,
                args,
                return_type,
                section=section
            )

            if section == 'types':
                if return_type in class_combinators:
                    class_combinators[return_type].sub_classes.add(name)
            else:
                return_types.add(return_type)
            method_description = ''
            descriptions = []

    total = len(method_combinators) + len(class_combinators)
    current = 0
    for c_name, c in {**class_combinators, **method_combinators}.items():
        print('Generating [{0:03}%] {name}'.format(
            round(current * 100 / total), name=c.name
        ), end='                                        \r', flush=True)
        current += 1

        path = "{}/{}".format(DESTINATION, c.section)
        os.makedirs(path, exist_ok=True)
        init = "{}/__init__.py".format(path)
        if not os.path.exists(init):
            with open(init, "w", encoding="utf-8") as f:
                f.write(notice)

        with open(init, "a", encoding="utf-8") as f:
            f.write("from .{} import {}\n".format(snek(c.name), c.name))

        imports = []
        doc_args = [c.description, '\n\n    Attributes:\n        ID (``str``): ``', c.name, '``\n\n    Parameters:']
        slots = []
        arguments = []
        fields = []
        return_arguments = []
        if isinstance(c, ClassCombinator):
            doc_args.append('\n        No parameters required.\n\n')
            return_read = [upper_first(r_name) for r_name in c.sub_classes]
            read_args = ['if d.get("@type"):', '    return Object.read(d)']

        else:

            read_args = []
            pre_arg_doc = []
            for arg_name, arg_type in c.args.items():

                if arg_type in core_types:
                    field_type = core_types[arg_type]
                    arg_type = "(``{}``)".format(core_types[arg_type])
                    arg_read = "d.get('{}')".format(arg_name)

                elif arg_type.startswith("vector"):
                    sub_type = arg_type.split("<", 1)[1][:-1]

                    if sub_type.startswith("vector"):
                        sub_type = sub_type.split("<", 1)[1][:-1]
                        if sub_type in core_types:
                            arg_type = "(List of List of ``{}``)".format(core_types[sub_type])
                            field_type = "list of List of {}".format(core_types[sub_type])
                            arg_read = "d.get('{}')".format(arg_name)

                        else:
                            arg_type = "(List of List of :class:`pytdlib.api.types.{}`)".format(sub_type)
                            field_type = "list of list({})".format(sub_type)
                            arg_read = "[[{}.read(v) for v in i] for i in d.get('{}', [])]".format(
                                # upper_first(sub_type),
                                "Object",
                                arg_name
                            )
                            # imports += "from .{} import {}\n".format(snek(sub_type), upper_first(sub_type))
                    else:
                        if sub_type in core_types:
                            arg_type = "(List of ``{}``)".format(core_types[sub_type])
                            field_type = "list of {}".format(core_types[sub_type])
                            arg_read = "d.get('{}')".format(arg_name)

                        else:
                            arg_type = "(List of :class:`pytdlib.api.types.{}`)".format(sub_type)
                            field_type = "list of {}".format(sub_type)
                            arg_read = "[{}.read(i) for i in d.get('{}', [])]".format(
                                # upperfirst(sub_type),
                                "Object",
                                arg_name
                            )
                            # imports += "from .{} import {}\n".format(snek(sub_type), upper_first(sub_type))

                else:
                    field_type = upper_first(arg_type)
                    arg_read = "{}.read(d.get('{}'))".format(
                        # field_type,
                        "Object",
                        arg_name
                    )
                    # imports += "from .{} import {}\n".format(snek(arg_type), field_type)
                    arg_type = "(:class:`pytdlib.api.types.{}`)".format(arg_type)

                pre_arg_doc.append(
                    "{} {}".format(
                        arg_name, arg_type,
                    )
                )

                fields.append(
                    "self.{0} = {0}  # {1}".format(arg_name, field_type)
                )
                read_args.append(
                    "{} = {}".format(arg_name, arg_read)
                )

            if pre_arg_doc:

                arguments = [arg_name for arg_name in c.args.keys()]
                return_arguments = c.args.keys()

                for arg_name, arg_desc in dict(zip(pre_arg_doc, c.params_description)).items():
                    doc_args.append('\n        ')
                    doc_args.append(arg_name)
                    for arg_d in arg_desc.split('.'):
                        doc_args.append('\n            ')
                        doc_args.append(arg_d)

            else:
                doc_args.append('\n        No parameters required.\n\n')

            slots.extend(repr(i) for i in c.args.keys())

            return_read = [c.name]

            if c.section != 'types':
                doc_args.append('\n\n    Returns:\n        ')
                doc_args.append(c.return_type)
                doc_args.append('\n\n    Raises:\n        ')
                doc_args.append(':class:`pytdlib.TLError`')
                slots.append('\'extra\'')
                arguments.append('extra=None')
                fields.append("self.extra = extra")

            if arguments:
                arguments.append('')

        with open("{}/{}/{}.py".format(DESTINATION, c.section, snek(c.name)), "w+", encoding="utf-8") as f:
            f.write(
                template.format(
                    notice=notice,
                    imports='\n'.join(imports),
                    class_name=c.name,
                    docstring=''.join(doc_args),
                    slots=', '.join(slots),
                    ID=c_name,
                    arguments=', '.join(arguments),
                    fields='\n        '.join(fields) or 'pass',
                    return_read=' or '.join(return_read),
                    read='\n        '.join(read_args),
                    return_arguments=', '.join(return_arguments)
                )
            )
    with open("{}/utils/all_types.py".format(DESTINATION), "w", encoding="utf-8") as f:

        f.write(notice + "\n\n")
        f.write("all_types = {")

        for c in filter(lambda x: x.section == "types", method_combinators.values()):
            f.write("\n    \"{0}\": \"{1}\",".format(c.name, snek(c.name)))
        f.write("\n}\n")


if '__main__' == __name__:
    HOME = "."
    DESTINATION = "../../pytdlib/api"
    start()
