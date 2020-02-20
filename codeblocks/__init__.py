#!/usr/bin/env python3

"""Output code blocks from markdown file

For example: codeblocks README.md
"""

from __future__ import annotations

import re
import sys
import subprocess

import click

PYTHON_BLOCK_RE = re.compile(
    rb"(?P<start>\n```python\n)(?P<code>.*?\n)(?P<end>```)", re.DOTALL
)

WORD_RE = re.compile(rb"\w+")
AWAIT_RE = re.compile(rb"\bawait\b")


def indent(text: bytes, prefix: bytes):
    """Add 'prefix' to the beginning of all non-empty lines in 'text'

    Like textwrap.indent, but for bytes.
    """

    return b"".join(
        (prefix + line if not line.isspace() else line)
        for line in text.splitlines(True)
    )


def wrap_python(index: int, block: bytes):
    return b"%sdef test_%d() -> None:\n%s" % (
        b"async " if AWAIT_RE.search(block) else b"",
        index,
        indent(block, b" " * 4),
    )


@click.command()
@click.option("--python", "--py", is_flag=True, help="Extract Python code blocks.")
@click.option("--wrap", is_flag=True, help="Wrap each code block in a function.")
@click.argument("source", type=click.Path(dir_okay=False, exists=True, allow_dash=True))
@click.argument("command", nargs=-1)
def main(source, python, wrap, command):
    if not python:
        raise NotImplementedError("languages other than --python not implemented")

    input = click.open_file(source, "rb").read()

    if command:

        def replace(match: re.Match[bytes]) -> bytes:
            code = match.group("code")
            p = subprocess.run(command, input=code, capture_output=True)
            if set(WORD_RE.findall(code)) != set(WORD_RE.findall(p.stdout)):
                raise Exception(
                    f"Command did not produce matching output: {' '.join(command)}"
                )
            return match.expand(br"\g<start>%s\g<end>" % p.stdout)

        output = PYTHON_BLOCK_RE.sub(replace, input)
        with click.open_file(source, "wb", atomic=True) as output_file:
            output_file.write(output)

    else:
        blocks = [match.group("code") for match in PYTHON_BLOCK_RE.finditer(input)]
        if blocks:
            sys.stdout.buffer.write(
                b"\n\n".join(
                    wrap_python(i, block) if wrap else block
                    for i, block in enumerate(blocks)
                )
            )


if __name__ == "__main__":
    main()
