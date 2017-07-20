import pyparsing as pp
from pprint import pprint
from .. import utils

def parse_markdown(string, offset=0):
    italics = (
        pp.QuotedString("*")
    ).setParseAction(lambda string, location, result:{
        "type": "italics",
        "children": [{
            "type": "string",
            "string": result[0],
            "location": location + offset
        }],
        "location": location + offset
    })

    bold = (
        pp.QuotedString("_")
    ).setParseAction(lambda string, location, result:{
        "type": "bold",
        "children": [{
            "type": "string",
            "string": result[0],
            "location": location + offset
        }],
        "location": location + offset
    })

    tokens = italics | bold
    word = pp.Word(pp.printables)

    other = (
        pp.Combine(
             word + pp.ZeroOrMore(" " + ~tokens + word)
        )
    ).setParseAction(lambda string, location, result: {
        "type": "string",
        "string": "".join(result[0]),
        "location": location + offset
    })

    markdown = pp.ZeroOrMore(
        tokens |
        other
    )

#     markdown.setDebug()
#     tokens.setDebug()
#     italics.setDebug()
#     bold.setDebug()
#     other.setDebug()

    result = markdown.parseString(string, parseAll=True)
    for part in result:
        if "children" in part:
            new_children = []
            for i, child in enumerate(part["children"]):
                if child["type"] == "string":
                    new_children += parse_markdown(child["string"], offset=child["location"])
                else:
                    new_children += [child]
            part["children"] = new_children
    return result.asList()

# result = parse_markdown("Dette er noe *kursiv tekst, _som_ er _fet_* og _kan_ ha *flere(!) deler*")
# pprint(result)

def process_markdown(document):
    def node_action(node):
        if node["type"] == "string":
            return parse_markdown(node["string"])
        return [node]

    return utils.nodes.replace_document_nodes(document, node_action)
