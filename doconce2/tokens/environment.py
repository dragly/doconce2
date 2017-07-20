import pyparsing as pp

prefix_name = pp.Word(pp.alphanums)
suffix_name = pp.matchPreviousLiteral(prefix_name)
prefix = pp.Combine(pp.Literal("!b") + prefix_name)
suffix = pp.Combine(pp.Literal("!e") + suffix_name)

environment = (
    prefix("prefix") + pp.SkipTo(pp.lineEnd) + pp.LineEnd() +
    pp.SkipTo(suffix)("contents") +
    suffix("suffix") + pp.SkipTo(pp.lineEnd) + pp.LineEnd()
).setParseAction(lambda string, location, result: {
    "type": "environment",
    "prefix": result["prefix"],
    "contents": result["contents"],
    "suffix": result["suffix"],
    "location": location
})
