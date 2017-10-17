import archieml
import markdown

from plugins.utils import get_plugins


data = archieml.load(open('./examples/simple.md'))

MARKDOWN_NLINES = '\n\n'

PLUGINS = get_plugins('./plugins/plugins.yaml')


def parse(archie, plugins=PLUGINS):
    text = []
    content = []
    for token in archie:
        k, v = token.values()
        if k == 'text':
            if v in plugins:
                content.append(plugins[v]())
            else:
                # gather text lines
                text.append(v)
        if k in plugins:
            if text:
                # convert gathered text as a whole to markdown:
                content.append(markdown.markdown(MARKDOWN_NLINES.join(text)))
                # empty text for new gathering
                text = []
            content.append(plugins[k](k, v))
    return '\n'.join(content)


print(parse(data['content']))
