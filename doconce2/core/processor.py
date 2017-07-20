class Processor:
    def __init__(self, name, function, dependencies):
        self.name = name
        self.function = function
        self.dependencies = set(dependencies)

    def __repr__(self):
        return self.name


def solve_dependencies(available_processors, enabled_processors):
    processor_map = {}
    dependency_map = {}
    for processor in available_processors:
        processor_map[processor.name] = processor
        dependency_map[processor.name] = processor.dependencies
    
    queue = set(enabled_processors)
    needed_processors = set()
    while queue:
        new_queue = set()
        for name in queue:
            for dependency in dependency_map[name]:
                new_queue.add(dependency)
            needed_processors.add(name)
        queue = new_queue
            
    
    # remove missing processors from maps
    processor_map = dict(
        (name, v)
        for name, v in processor_map.items()
        if name in needed_processors
    )
    dependency_map = dict(
        (name, v)
        for name, v in dependency_map.items()
        if name in needed_processors
    )
    
    ordered_processors = []
    while dependency_map:
        ready = [
            name
            for name, dependencies in dependency_map.items()
            if not dependencies
        ]

        if not ready:
            raise ValueError("Circular dependency found!")

        for name in ready:
            del dependency_map[name]

        for dependencies in dependency_map.values():
            dependencies.difference_update(ready)

        for name in ready:
            ordered_processors.append(processor_map[name])
    
    return ordered_processors
