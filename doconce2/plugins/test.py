from doconce2.core.processor import Processor
import pyparsing as pp

def setup_processors():
    return [
        Processor(
            name="test",
            function=lambda document: document,
            dependencies=["blocks"]
        )
    ]

def setup_blocks():
    prefix_name = pp.Word(pp.alphanums)
    suffix_name = pp.matchPreviousLiteral(prefix_name)
    prefix = pp.Combine(pp.Literal("$begin") + prefix_name)
    suffix = pp.Combine(pp.Literal("$end") + suffix_name)

    environment = (
        prefix("prefix") + pp.SkipTo(pp.lineEnd) + pp.LineEnd() +
        pp.SkipTo(suffix)("contents") +
        suffix("suffix") + pp.SkipTo(pp.lineEnd) + pp.LineEnd()
    ).setParseAction(lambda string, location, result: {
        "type": "my_test",
        "prefix": result["prefix"],
        "contents": result["contents"],
        "suffix": result["suffix"],
        "location": location
    })

    return [
        environment
    ]
