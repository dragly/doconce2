from doconce2.core.processor import Processor
from doconce2.parsers import structure

def setup_processors():
    return [
        Processor(
            name="includes",
            function=structure.process_includes,
            dependencies=[]
        ),
        Processor(
            name="blocks",
            function=structure.process_blocks,
            dependencies=["includes"]
        ),
        Processor(
            name="core",
            function=lambda document: document,
            dependencies=["markdown"]
        )
    ]
