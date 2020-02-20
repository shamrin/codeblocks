#!/usr/bin/env python3

"""Output code blocks from markdown file

For example: codeblocks README.md
"""

from __future__ import annotations

import re
import sys
import subprocess
from textwrap import shorten

import click

BLOCK_RE = re.compile(
    rb"(?P<start>\n```(?P<type>\w+)\n)(?P<code>.*?\n)(?P<end>```)", re.DOTALL
)

WORD_RE = re.compile(rb"\w+")
AWAIT_RE = re.compile(rb"\bawait\b")


def exit(command, message):
    sys.exit(f"codeblocks: command `{' '.join(command)}` {message}.")


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


def wrap_block(index: int, block_type: str, block: bytes):
    if block_type == "python":
        return wrap_python(index, block)
    else:
        raise NotImplementedError(
            f"wrapping `{block_type}` code blocks not implemented"
        )


@click.command()
@click.option("--type", help="Select code blocks of specified type only.")
@click.option("--wrap", is_flag=True, help="Wrap each code block in a function.")
@click.argument("source", type=click.Path(dir_okay=False, exists=True, allow_dash=True))
@click.argument("command", nargs=-1)
def main(source, type, wrap, command):
    """Extract or process code blocks in Markdown FILE.

    \b
    Extract Python code blocks:
        codeblocks --type python README.md

    \b
    Reformat Python code blocks using black, in place:
        codeblocks --type python README.md black -
    """

    input = click.open_file(source, "rb").read()

    if command:

        def replace(match: re.Match[bytes]) -> bytes:
            block_type = match.group("type").decode("utf8")

            if type is not None and block_type != type:
                return match.expand(br"\g<start>\g<code>\g<end>")

            code = match.group("code")

            p = subprocess.run(command, input=code, capture_output=True)
            if p.returncode != 0:
                sys.stderr.buffer.write(p.stderr)
                exit(command, f"returned non-zero exit status {p.returncode}")
            if set(WORD_RE.findall(code)) != set(WORD_RE.findall(p.stdout)):
                short = shorten(p.stdout.decode("utf8", "ignore"), 40)
                exit(command, f"did not produce matching output: `{short}`")

            return match.expand(br"\g<start>%s\g<end>" % p.stdout)

        output = BLOCK_RE.sub(replace, input)
        with click.open_file(source, "wb", atomic=True) as output_file:
            output_file.write(output)

    else:
        blocks = [
            (match.group("type").decode("utf8"), match.group("code"))
            for match in BLOCK_RE.finditer(input)
        ]
        if blocks:
            sys.stdout.buffer.write(
                b"\n\n".join(
                    wrap_block(i, block_type, block) if wrap else block
                    for i, (block_type, block) in enumerate(blocks)
                    if type is None or block_type == type
                )
            )


if __name__ == "__main__":
    main()
