#!/usr/bin/env python3

"""Output code blocks from markdown file

For example: codeblocks README.md
"""

from __future__ import annotations

import re
import sys
import subprocess


PYTHON_BLOCK_RE = re.compile(
    rb"(?P<start>\n```python\n)(?P<code>.*?\n)(?P<end>```)", re.DOTALL
)


def indent(text: bytes, prefix: bytes):
    """Add 'prefix' to the beginning of all non-empty lines in 'text'

    Like textwrap.indent, but for bytes.
    """

    return b"".join(
        (prefix + line if not line.isspace() else line)
        for line in text.splitlines(True)
    )


def wrap(index: int, block: bytes):
    return b"def test_%d() -> None:\n%s" % (index, indent(block, b" " * 4),)


def main():
    option_wrap = False
    if "--wrap" in sys.argv[1:]:
        sys.argv.remove("--wrap")
        option_wrap = True

    language, filename, *args = sys.argv[1:]

    if language not in ("--py", "--python"):
        raise NotImplementedError("languages other than --python not implemented")

    command = []
    if args:
        if args[0] != "--":
            raise Exception(f"-- expected, but got {args[0]}")
        command = args[1:]

    input = open(filename, "rb").read()

    if command:

        def replace(match: re.Match[bytes]) -> bytes:
            p = subprocess.run(command, input=match.group("code"), capture_output=True)
            return match.expand(br"\g<start>%s\g<end>" % p.stdout)

        with open(filename, "wb") as output_file:
            output_file.write(PYTHON_BLOCK_RE.sub(replace, input))

    else:
        blocks = [match.group("code") for match in PYTHON_BLOCK_RE.finditer(input)]
        if not blocks:
            return
        sys.stdout.buffer.write(
            b"\n\n".join(
                wrap(i, block) if option_wrap else block
                for i, block in enumerate(blocks)
            )
        )


if __name__ == "__main__":
    main()
