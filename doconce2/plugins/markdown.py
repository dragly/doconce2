from doconce2.core.processor import Processor
from doconce2.parsers import markdown

def setup_processors():
    return [
        Processor(
            name="markdown",
            function=markdown.process_markdown,
            dependencies=["blocks"]
        )
    ]
