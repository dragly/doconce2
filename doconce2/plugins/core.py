from doconce2.core.processor import Processor
from doconce2.parsers import structure

def setup_processors():
    return [
        Processor(
            name="core",
            function=lambda document: document,
            dependencies=["markdown"]
        )
    ]
