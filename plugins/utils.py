import yaml
from jinja2 import Template

from preprocessors.utils import load


def _init(plugin):
    """
    plugins can either be a string like:
        <div class="{{ class }}">
    or a dict like:
        {
            'template': '<div class="{{ c }}">',
            'pre': 'preprocessors.html_tag'
        }
    """
    preprocessor = lambda k=None, v=None: v if isinstance(v, dict) else {'data': v}
    template = None
    if isinstance(plugin, str):
        template = Template(plugin)
    if isinstance(plugin, dict):
        template = Template(plugin['template'])
        preprocessor = load(plugin['pre'])
    return lambda k=None, v=None: template.render(**preprocessor(k, v))


def get_plugins(path):
    plugins = yaml.load(open(path))
    return {k: _init(v) for k, v in plugins.items()}
