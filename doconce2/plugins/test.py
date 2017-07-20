from doconce2.core.processor import Processor

def setup_processors():
    return [
        Processor(
            name="test",
            function=lambda document: document,
            dependencies=["blocks"]
        )
    ]
