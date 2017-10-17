from preprocessors.extract_freeform import process as extract_freeform


def _get_tag_props(value):
    return ' '.join(['{}="{}"'.format(k, v) for k, v in value.items()])


def process(k=None, v=None):
    tag = '<{} {}>'
    value = v

    # span: .my-span-class
    if isinstance(v, str):
        if v.startswith('#'):
            value = 'id="{}"'.format(v.lstrip('#'))
        value = 'class="{}"'.format(v.lstrip('.'))

    # [.+div]
    # style: background-color: red
    # this is text
    # []
    elif isinstance(v, list):
        data = extract_freeform(value=v)
        text = data.pop('text')
        value = '{}>\n{}\n</{}'.format(_get_tag_props(data), text, k)
    else:
        try:
            v = dict(v)
            value = _get_tag_props(v)
        except:
            pass
    return {'tag': tag.format(k, value)}
