import pyparsing as pp

paragraph_divisor = (pp.lineEnd + pp.lineEnd) | pp.StringEnd()
paragraph = pp.SkipTo(paragraph_divisor) + paragraph_divisor.suppress()
paragraph = paragraph.setParseAction(lambda string, location, result: {
    "type": "paragraph",
    "children": [{
        "type": "string",
        "string": result[0].replace("\n", " "),
        "location": location
    }],
    "location": location
})
