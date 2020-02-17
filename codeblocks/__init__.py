#!/usr/bin/env python3

"""Output code blocks from markdown file

For example: codeblocks README.md
"""

from __future__ import annotations

import re
import sys
from textwrap import indent
import subprocess


PYTHON_BLOCK_RE = re.compile(
    rb"(?P<start>\n```python\n)(?P<code>.*?)(?P<end>\n```)", re.DOTALL
)


def main():
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
            input = match.group("code")
            output = subprocess.run(command, input=input, capture_output=True).stdout
            return match.expand(br"\g<start>%s\g<end>" % output)

        with open(filename, "wb") as output_file:
            output_file.write(PYTHON_BLOCK_RE.sub(replace, input))

    else:
        blocks = [
            match.group("code").decode("utf8")
            for match in PYTHON_BLOCK_RE.finditer(input)
        ]
        if not blocks:
            return
        print(
            "\n\n\n".join(
                f'def test_{i}() -> None:\n{indent(block, " " * 4)}'
                for i, block in enumerate(blocks)
            )
        )


if __name__ == "__main__":
    main()
