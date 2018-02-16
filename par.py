
import lark

#to convert the parse tree into a usable format.
class tran(lark.Transformer):

    def parameters(_, n):
        if len(n) > 0:
            return tuple(n)

    dcl = list

    l_begin   = lambda _, n: ("Label_Begin", str(n[0]))
    l_end     = lambda _, __: "Label_End"

    loop      = lambda _, n: ("Loop", n[0])

    property  = lambda _, n: ("Property", tuple(n))
    method    = lambda _, n: ("Method", tuple(n))

    const_dcl = lambda _, n: ("Constant", n[0])
    var_dcl   = lambda _, n: ("Variable", n[0])

    screen    = lambda _, n: ("Screen", tuple(n))
    asset     = lambda _, n: ("Asset",  tuple(n))

    bool      = lambda _, n: bool(n[0])
    string    = lambda _, n: str(n[0][1:-1])


with open("grammar.g") as file:
    script_grammar = r''.join([line for line in file])

script_parser = lark.Lark(
    script_grammar,
    start  = "expr",
    parser = "lalr"
)


def get_parse_tree(file_path):

    with open(file_path) as file:
        script_code = [
            line
                .replace("\\~", chr(0x4))
                .replace("~", "\n~")
                .split("~")[0]
                .replace(chr(0x4), "~")

            for line in file
        ]

    expression_list = []

    for line in script_code:

        if line != "\n":
            parse = script_parser.parse(line)
            expression_list.append(parse)
            # print(parse.pretty())

    return expression_list


def get_data(parse_tree):

    cleaned_tree = []

    local_transformer = tran()

    for item in parse_tree:

        cleaned_tree.append(local_transformer.transform(item))

    return cleaned_tree

