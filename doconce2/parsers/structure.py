import pyparsing as pp
import os.path
import yaml
from .. import tokens


def parse_file(filename):
    filename = os.path.abspath(filename)
    with open(filename, "r") as file_pointer:
        contents = file_pointer.read()

    header_delimiter = pp.Literal("---")
    header = (
        header_delimiter +
        pp.LineEnd() +
        pp.SkipTo(header_delimiter)("contents") +
        header_delimiter +
        pp.LineEnd()
    ).setParseAction(lambda result: yaml.load(result["contents"]))

    body = (
        pp.SkipTo(pp.stringEnd)
    ).setParseAction(lambda string, location, result: {
        "type": "string",
        "string": result[0],
        "location": location,
        "filename": filename
    })

    parser = pp.Optional(header)("header") + body("body")

    result = parser.parseString(contents, parseAll=True)

    header_data = None
    if "header" in result:
        header_data = result["header"]
    return {
        "filename": filename,
        "header": header_data,
        "body": [
            result["body"]
        ],
        "type": "file"
    }


def document_strings(document):
    for part in document["body"]:
        if part["type"] == "string":
            yield part
        elif part["type"] == "paragraph":
            for child in part["children"]:
                if child["type"] == "string":
                    yield child


def document_replace(document, callback):
    body = document["body"]
    for i, part in enumerate(body):
        if part["type"] == "string":
            body[i] = callback(part)
        elif part["type"] == "paragraph":
            children = part["children"]
            for j, child in enumerate(children):
                if child["type"] == "string":
                    children[j] = callback(child)


def process_includes(document):
    current_directory = os.path.dirname(document["filename"])

    def handle_file(result):
        file_data = parse_file(
            os.path.join(current_directory, result["filename"])
        )
        process_includes(file_data)
        return file_data

    def keep_string(string, location, result):
        return {
            "type": "string",
            "string": result[0],
            "filename": document["filename"],
            "location": location
        }

    include = (
        pp.LineStart() +
        pp.Literal("!include") +
        pp.QuotedString("(", endQuoteChar=")").setResultsName("filename") +
        pp.LineEnd()
    ).setParseAction(handle_file)

    parser = pp.ZeroOrMore(
        pp.SkipTo(include).setParseAction(keep_string) +
        include
    ) + pp.SkipTo(pp.stringEnd).setParseAction(keep_string)

    new_body = []
    for part in document_strings(document):
        result = parser.parseString(part["string"], parseAll=True)
        for group in result:
            if group["type"] == "string":
                new_body.append(group)
            elif group["type"] == "file":
                for subpart in document_strings(group):
                    new_body.append(subpart)
    document["body"] = new_body


def create_block_parser(extra_tokens=None):
    all_tokens = (
        pp.White().suppress() |
        tokens.environment.environment |
        tokens.heading.heading
    )
    if extra_tokens is not None:
        all_tokens = all_tokens | extra_tokens
    all_tokens = all_tokens | tokens.paragraph.paragraph
    return pp.ZeroOrMore(all_tokens)


def process_blocks(document, extra_tokens=None):
    parser = create_block_parser(extra_tokens=extra_tokens)

    new_body = []
    for part in document["body"]:
        if part["type"] == "string":
            result = parser.parseString(part["string"]).asList()
            for group in result:
                group["filename"] = part["filename"]
                group["location"] = part["location"] + group["location"]
                new_body.append(group)
        else:
            new_body.append(part)

    document["body"] = new_body
