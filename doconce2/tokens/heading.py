import pyparsing as pp


def create_heading(symbol):
    return symbol.suppress() + pp.SkipTo(symbol) + symbol.suppress() + pp.LineEnd().suppress()


heading_symbol = pp.Literal("=")
heading_chapter_symbol = heading_symbol * 9
heading_section_symbol = heading_symbol * 7
heading_subsection_symbol = heading_symbol * 5
heading_subsubsection_symbol = heading_symbol * 3

heading_chapter = create_heading(heading_chapter_symbol).setResultsName("heading_chapter")
heading_section = create_heading(heading_section_symbol).setResultsName("heading_section")
heading_subsection = create_heading(heading_subsection_symbol).setResultsName("heading_subsection")
heading_subsubsection = create_heading(heading_subsubsection_symbol).setResultsName("heading_subsubsection")

heading = (
    heading_chapter |
    heading_section |
    heading_subsection |
    heading_subsubsection
).setParseAction(lambda string, location, result: {
    "type": result.getName(),
    "string": result[0],
    "location": location
})
