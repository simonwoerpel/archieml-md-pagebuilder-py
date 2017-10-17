import markdown

from parser import MARKDOWN_NLINES


def process(key=None, value=[]):
    """
    convert a list of ordered dicts from an `ArchieML` freeform array
    into dict form with only 1 'text' key
    """
    data = {}
    text = []
    for token in value:
        k, v = token.values()
        if k == 'text':
            text.append(v)
        else:
            data[k] = v
    data['text'] = MARKDOWN_NLINES.join(text)
    if data.get('md', False):
        data['text'] = markdown.markdown(data['text'])
    return data
