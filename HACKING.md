Run locally:
```
brew install python@3.7
poetry env use /usr/local/opt/python@3.7/bin/python3
poetry install
source .venv/bin/activate.fish
codeblocks --help
```

Publish:
```
poetry publish --build
```