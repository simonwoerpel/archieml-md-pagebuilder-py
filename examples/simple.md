[+content]

# hello world

this is a simple example.

`span: my-span-class`
span: my-span-class

this text is wrapped in a `span` with class "my-span-class"

/span

## Heading 2

`[.+span]`
`style: background-color:red`
`id: my-id`

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


`[.ul]`
[.ul]
* item 1
* item 2
[]

`[.ol]`
[.ol]
* item 1
* item 2
[]


hello?


**some bold text at the bottom**
