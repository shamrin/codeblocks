# codeblocks

Extract and process code blocks from Markdown files. Now you can keep code examples automatically:

* formatted (e.g. using [black][] for Python)
* type checked
* unit tested
* linted
* up-to-date with `--help`
* etc

# Usage

```usage
Usage: codeblocks [OPTIONS] LANGUAGE FILE [COMMAND]...

  Extract or process LANGUAGE code blocks in Markdown FILE.

  Extract Python code blocks:
      codeblocks python README.md

  Reformat Python code blocks using black, in place:
      codeblocks python README.md black -

Options:
  --wrap  Wrap each code block in a function.
  --help  Show this message and exit.
```

# Examples

Extract all named code blocks:
```
codeblocks README.md
```

Extract Python code blocks:
```
codeblocks python README.md
```

Check formatting of Python code blocks with black:
```
codeblocks python README.md | black --check -
```

Reformat Python code blocks with black, **in place**:
```
codeblocks python README.md black -
```

Type check Python code blocks with mypy (`--wrap` puts each code block into its own function):
```
mypy somemodule anothermodule <(codeblocks python --wrap README.md)
```

Make sure `usage` block in this README.md is up-to-date with `--help` output:
```
diff -u <(codeblocks usage README.md) <(codeblocks --help)
```

# Full type checking example

```python
def plus(x: int, y: int) -> int:
    return x + y

plus(1, '2')
```

```
$ mypy --pretty --strict <(codeblocks python README.md)
/dev/fd/63:5: error: Argument 2 to "plus" has incompatible type "str"; expected "int"
        plus(1, '2')
                ^
Found 1 error in 1 file (checked 1 source file)
```

# Rationale

There are alternative tools, but none of them supported all of the cases above.

* [prettier][] [can reformat Markdown code blocks][prettier-md] ([PR][prettier-pr]), but it works only for supported languages like JavaScript. It does not support Python. No lint or unit test support.
* [blacken-docs][] can reformat Python code blocks, but it does not support all [black][] options. For example, [`black --check`][blacken-check] is not supported. No lint or unit test support. In addition, `codeblocks` implementation is much simpler and is not coupled with black.
* [excode][] is very similar, but does not support in place modifications.
* [gfm-code-blocks][] does not have command line interface.

[black]: https://github.com/psf/black
[prettier]: https://prettier.io
[prettier-md]: https://prettier.io/blog/2017/11/07/1.8.0.html#markdown-support
[prettier-pr]: https://github.com/prettier/prettier/pull/2943
[blacken-docs]: https://github.com/asottile/blacken-docs
[blacken-check]: https://github.com/asottile/blacken-docs/issues/42
[excode]: https://github.com/nschloe/excode
[gfm-code-blocks]: https://github.com/jonschlinkert/gfm-code-blocks
