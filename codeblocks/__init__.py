#!/usr/bin/env python3

"""Output code blocks from markdown file

For example: codeblocks README.md
"""

from __future__ import annotations

import re
import sys
from textwrap import indent
import subprocess
from typing import Tuple


def main():
    language, filename, *args = sys.argv[1:]

    if language not in ("--py", "--python"):
        raise NotImplementedError("languages other than --python not implemented")

    command = []
    if args:
        if args[0] != "--":
            raise Exception(f"-- expected, but got {args[0]}")
        command = args[1:]

    if command:

        def replace(match: re.Match[bytes]) -> bytes:
            input = match.group("code")
            output = subprocess.run(command, input=input, capture_output=True).stdout
            return match.expand(br"\g<start>%s\g<end>" % output)

        pattern = re.compile(
            rb"(?P<start>\n```python\n)(?P<code>.*?\n)(?P<end>```)", re.DOTALL
        )

        input = open(filename, 'rb').read()

        with open(filename, "wb") as output_file:
            output_file.write(re.sub(pattern, replace, input, re.DOTALL))

    else:
        blocks = re.findall(
            r"\n```python\n(.*?)\n```", open(filename).read(), re.DOTALL
        )
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
