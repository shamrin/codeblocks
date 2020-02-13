# codeblock

Extract and process code blocks from markdown files.

# Examples

Extract Python code blocks:
```
codeblock --python README.md
```

Check formatting of Python code blocks with black:
```
codeblock --python README.md | black --check -
```

Reformat Python code blocks with black, in place:
```
codeblock --python README.md -- black -
```

Type check Python code blocks with mypy:
```
mypy somemodule anothermodule <(codeblock --python README.md)
```

# Full type checking example

```python
def plus(x: int, y: int) -> int:
    return x + y

plus(1, '2')
```

```
$ mypy --pretty --strict <(codeblock --python README.md)
/dev/fd/63:5: error: Argument 2 to "plus" has incompatible type "str"; expected "int"
        plus(1, '2')
                ^
Found 1 error in 1 file (checked 1 source file)
```

# TODO

* [x] example for black
* [x] example for mypy
* [ ] example for pytest
* [ ] automatically add `async` for functions with `await` in them
* [ ] support other languages
* [x] mention alternatives: blacken-docs, ...
* [ ] support in-place modifications
* [ ] use proper markdown parser

# Related

* https://github.com/nschloe/excode
* https://github.com/jonschlinkert/gfm-code-blocks
* [blacken-docs][] ([does not support `black --check`][blacken-check])
* [prettier works out of the box for supported languages][prettier] ([PR][prettier-pr])

[blacken-docs]: https://github.com/asottile/blacken-docs
[blacken-check]: https://github.com/asottile/blacken-docs/issues/42
[prettier]: https://prettier.io/blog/2017/11/07/1.8.0.html#markdown-support
[prettier-pr]: https://github.com/prettier/prettier/pull/2943
