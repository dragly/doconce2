def replace_node_children(node, scope, callback):
    if "children" in node:
        children = node["children"]
        new_children = []
        for child in children:
            replace_node_children(
                child,
                scope + [child["type"]],
                callback
            )
            new_children += callback(child)
        node["children"] = new_children
    return node


def replace_document_nodes(document, callback):
    scope = ["file"]
    new_body = []
    for block in document["body"]:
        replace_node_children(
            block,
            scope + [block["type"]],
            callback
        )
        new_body += callback(block)
    document["body"] = new_body
    return document
