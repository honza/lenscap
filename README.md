# Tripod

Tripod is a static site generator for creating beautiful photo narratives

Write your stories in markdown and insert small snippets of code to add small
groups of images.

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

You can produce content like [the demo page][1] by running `tripod kitten.md`.

[1]: http://honza.ca/tripod/kitten.html

# Installation

`$ pip install tripod`

# Usage

# License

BSD, short and sweet
