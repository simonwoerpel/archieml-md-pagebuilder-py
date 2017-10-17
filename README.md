# archieml-md-pagebuilder-py

this is a proof of concept for a simple python-powered build chain for creating one-pagers or longreads via markdown and [ArchieML](http://archieml.org/). You can define simple plugin-snippets that can render html-components inside the text.

## purpose

for use e.g. in a newsroom: editors can just write markdown files, or even use something like *google docs* with their text. all they need to know how to write plugins like images or whatever their nerds provide them.

for example, an image could be rendered like this:

```markdown

Here comes some normal text. Now we want to show an image
and specify how it should be rendered via the ArchieML syntax:

[.+image]
src: /path/to/image.jpg
width: paragraph
caption: here comes the caption
[]

Here the text continues.
```

it could even be possible to have some data from an underlying cms or database available if you write custom `preprocessors` that have access to your other python codebase.

## custom plugins

plugins are defined in simple `yaml`-syntax with template snippets in `Jinja2`.

see `plugins/plugins.yaml` for some defaults (e.g. basic html tags)

the corresponding `ArchieML`-object is rendered into the `Jinja2`-template defined.

here define some boxes:

```yaml
box: '<div style="border: 1px solid {{ border }}">{{ content }}</div>'
```

use it in the markdown source file like this:

```markdown

# Headline

Ea culpa sint amet voluptas explicabo a. Rem exercitationem libero quasi dicta. Voluptas dolorum placeat saepe iusto et molestiae nisi culpa. Cumque et magnam velit molestiae dolor.

[.+box]
border: green

this paragraf appears in a box with green border.
[]
```

### preprocessors

here is a more complex custom plugin:

```yaml
box2:
  pre: 'preprocessors.extract_freeform'
  template: '<section style="border:1px solid {{ border }}">{{ text }}</section>'
```

as you can see, you can make use of `preprocessors`.

they live in `./preprocessors/` and need a function called `process`, that looks like this (for the purpose of extracting freeform arrays from `ArchieMl`):


```python
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
```

as you can see, a preprocessor is just normal python code, so you could do *everything* here.

## Full example

source:

```markdown
[+content]

# hello world

this is a simple example.

span: my-span-class

this text is wrapped in a `span` with class "my-span-class"

/span

## Heading 2

[.+span]
style: background-color:red
id: my-id

this is red text.

[]

here we render a custom plugin (see `plugins.yaml`):

[.+box]
border: green
md: true

### markdown enabled
this can be done either this way.

[]

{.box2}
border: red
content: or this.

this is a comment!
{}


### lists
are possible via `markdown` or with `ArchieML`-arrays.

use markdown:

- item 1
- item 2


[.ul]
* item 1
* item 2
[]

[.ol]
* item 1
* item 2
[]
```

after running `python ./parser.py`, this results in the following html:

```html

<h1>hello world</h1>
<p>this is a simple example.</p>
<span class="my-span-class">
<p>this text is wrapped in a <code>span</code> with class "my-span-class"</p>
</span>
<h2>Heading 2</h2>
<span id="my-id" style="background-color:red">
this is red text.
</span>
<p>here we render a custom plugin (see <code>plugins.yaml</code>):</p>
<section style="border:1px solid green"><h3>markdown enabled</h3>
<p>this can be done either this way.</p></section>
<div style="border: 1px solid red">or this.</div>
<h3>lists</h3>
<p>are possible via <code>markdown</code> or with <code>ArchieML</code>-arrays.</p>
<p>use markdown:</p>
<ul>
<li>
<p>item 1</p>
</li>
<li>
<p>item 2</p>
</li>
</ul>
<ul><li>item 1</li><li>item 2</li></ul>
<ol><li>item 1</li><li>item 2</li></ol>
```
