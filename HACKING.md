Install [uv](https://docs.astral.sh/uv/).

Run locally:
```
uv run codeblocks --help
```

Sanity check:
```
# modify `usage` block in our README
uv run codeblocks usage README.md -- codeblocks --help

# confirm that mypy fails with `incompatible type` error with our README
uv run mypy --pretty <(uv run codeblocks python README.md)
```

Publish:
```
uv build
# put PyPI API token as `UV_PUBLISH_TOKEN=...` in `.env` file
env $(cat .env) uv publish
```