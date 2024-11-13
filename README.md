# codeblocks

Extract and process code blocks from Markdown files. Now you can keep code examples automatically:

* formatted (e.g. using [black][] for Python)
* type checked
* unit tested
* linted
* up-to-date with `--help`
* etc

# Quick start

(if [uv](https://docs.astral.sh/uv/) is available)

Try `codeblocks` without installing:

```
uvx codeblocks --help
```

Install to `PATH`:

```
uv tool install codeblocks
codeblocks --help
```

# Install with Python package manager

With `pip`:
```
pip install codeblocks
```

With `uv`:
```
uv add codeblocks
```

With `poetry`:
```
poetry add codeblocks
```

# Usage

```usage
Usage: codeblocks [OPTIONS] LANGUAGE FILE [COMMAND]...

  Extract or process LANGUAGE code blocks in Markdown FILE.

  Extract Python code blocks:
      codeblocks python README.md

  Reformat Python code blocks with `black`, in place:
      codeblocks python README.md -- black -

Options:
  --wrap                Wrap each code block in a function.
  --check / --no-check  Do not modify the file, just return the status. Return
                        code 0 means block matches COMMAND output. Return code
                        1 means block would be modified.
  --version             Show the version and exit.
  --help                Show this message and exit.
```

# Examples

Extract Python code blocks:
```
codeblocks python README.md
```

Check formatting of Python code blocks with black:
```
codeblocks --check python README.md -- black -
```

Reformat Python code blocks with black, **in place**:
```
codeblocks python README.md -- black -
```

Type check Python code blocks with mypy (`--wrap` puts each code block into its own function):
```
mypy somemodule anothermodule <(codeblocks python --wrap README.md)
```

Insert the output of `codeblock --help` into `usage` block in this README.md:
```
codeblocks usage README.md -- codeblocks --help
```

Check that `usage` block in this README.md is up-to-date with `--help` output:
```
codeblocks --check usage README.md -- codeblocks --help
```

# Full type checking example

```python
def plus(x: int, y: int) -> int:
    return x + y

plus(1, '2')
```

```
$ mypy --pretty <(codeblocks python README.md)
/dev/fd/63:5: error: Argument 2 to "plus" has incompatible type "str"; expected "int"  [arg-type]
        plus(1, '2')
                ^~~
Found 1 error in 1 file (checked 1 source file)
```

# Rationale

There are alternative tools, but none of them supported all of the cases above.

* [prettier][] [can reformat Markdown code blocks][prettier-md] ([PR][prettier-pr]), but it works only for supported languages like JavaScript. It does not support Python. No lint or unit test support.
* [blacken-docs][] can reformat Python code blocks, but it does not support all [black][] options. For example, [`black --check`][blacken-check] is not supported. No lint or unit test support. In addition, `codeblocks` implementation is much simpler and is not coupled with black.
* [excode][] is very similar, but does not support in place modifications.
* [gfm-code-blocks][] does not have command line interface.
* [codedown][] does not support processing and [separate code block extraction](https://github.com/earldouglas/codedown/issues/9)
* [cog][] is fully generic, but requires writing [scripts embedded in Markdown][cog-help]

[black]: https://github.com/psf/black
[prettier]: https://prettier.io
[prettier-md]: https://prettier.io/blog/2017/11/07/1.8.0.html#markdown-support
[prettier-pr]: https://github.com/prettier/prettier/pull/2943
[blacken-docs]: https://github.com/asottile/blacken-docs
[blacken-check]: https://github.com/asottile/blacken-docs/issues/42
[excode]: https://github.com/nschloe/excode
[gfm-code-blocks]: https://github.com/jonschlinkert/gfm-code-blocks
[cog-help]: https://til.simonwillison.net/python/cog-to-update-help-in-readme
[codedown]: https://github.com/earldouglas/codedown
[cog]: https://nedbatchelder.com/code/cog
