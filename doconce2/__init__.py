import os.path
import pluginbase

from . import parsers

plugin_base = pluginbase.PluginBase(
    package="doconce2.plugins",
    searchpath=[]
)

plugin_source = plugin_base.make_plugin_source(
    identifier="doconce2",
    searchpath=[
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            "plugins"
        )
    ]
)
