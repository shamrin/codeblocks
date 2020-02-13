# codeblock

Extract and process code blocks from markdown files.

# TODO

* [ ] example for black
* [ ] example for mypy
* [ ] example for pytest
* [ ] automatically add `async` for functions with `await` in them
* [ ] support other languages
* [ ] mention alternatives: blacken-docs, ...
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
