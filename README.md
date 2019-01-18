# Lenscap

Lenscap is a static site generator for creating beautiful photo narratives

Write your stories in markdown and insert small snippets of code to add small
groups of images.

[Demo][1]

# Example

Given a directory structure of

```
kitten.md
photos/
    1.jpg
    2.jpg
    3.jpg
```

And a markdown file of

    # Kittens

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pretium
    elit sit amet posuere congue. Nam felis augue, pretium ac auctor quis,
    facilisis non nunc. Nullam in erat magna. Duis rhoncus felis id erat
    maximus, ac condimentum felis efficitur. Nunc ac mattis ante. Etiam sed
    orci tortor. Ut gravida orci eu dictum vulputate. Vestibulum dui augue,
    condimentum ac tempus ac, mollis non ante. Pellentesque aliquam, est vitae
    sollicitudin tristique, tortor massa tincidunt nibh, eu tempus sem dolor
    vitae diam. Proin sodales velit nec nisi euismod, id facilisis elit
    consequat. Nam eros magna, vulputate ac turpis quis, rhoncus euismod justo.

    ```yaml
    rows: 1, 2
    items:
        - 1.jpg
        - 2.jpg
        - 3.jpg
    ```

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pretium
    elit sit amet posuere congue. Nam felis augue, pretium ac auctor quis,
    facilisis non nunc. Nullam in erat magna. Duis rhoncus felis id erat
    maximus, ac condimentum felis efficitur.

    Nunc ac mattis ante. Etiam sed orci tortor. Ut gravida orci eu dictum
    vulputate. Vestibulum dui augue, condimentum ac tempus ac, mollis non ante.
    Pellentesque aliquam, est vitae sollicitudin tristique, tortor massa
    tincidunt nibh, eu tempus sem dolor vitae diam. Proin sodales velit nec
    nisi euismod, id facilisis elit consequat. Nam eros magna, vulputate ac
    turpis quis, rhoncus euismod justo.

You can produce content like [the demo page][1] by running `lenscap kitten.md`.

[1]: http://honza.ca/lenscap/kitten.html

# Installation

`$ pip install lenscap`

# Usage

Throw some high resolution photos into a `photos/` directory and then write
your essay in a markdown file.  You can use regular markdown and specify your
photo layouts using fenced blocks.

The fenced in block uses simple yaml syntax to specify your meta data.  All you
really need to do is tell it how many rows of photos you want and how many
photos are in each row.  Then you list the files and lenscap does the rest.

So, if you want to have a 2 photos over 3, you'd say `rows: 2, 3`.  If you want
a single image, you can skip the `rows` directive.

Lenscap will check that your photos are big enough in terms of resolution and
will refuse to continue if the photos are too small.  You can also tell lenscap
to resize your high resolution photos to just the right size.

You invoke the `lenscap` command on your file:

```
$ lenscap kitten.md
```

And this will create a file called `kitten.html` in the same directory.

```
Usage: lenscap [options] files

Options:
  -h, --help                   show this help message and exit
  -o FILE, --output=FILE       Output filename, defaults to same but with .html
  -p DIR, --photos=DIR         Directory with photos (default: photos/)
  -t DIR, --templates=DIR      Directory with templates (default: None)
  -s FILE, --stylesheet=FILE   Stylesheet file
  -m THEME, --theme=THEME      Theme (default, narrow)
  -r, --resize                 Resize images (default: False)
```

# Themes

Currently, there are only two themes: default and narrow.  The default theme
uses a width of 16 skeleton columns and the narrow one uses a narrower 8 column
width for text and expands to 16 for images.

Adding a new theme is just a matter of copying the `lenscap/templates/default`
directory and editing the `base.html` and `rows.html` files.

# Contributing

Contributions are most welcome.  If you have any cool ideas, open a ticket.
Especially design-related tweaks and new themes are welcome.

# License

BSD, short and sweet
