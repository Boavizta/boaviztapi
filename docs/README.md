# Documentation

Documentation of Boaviztapi

Content:

1. ADR - Architecture decision records
2. assets: static content like images
3. Explanations: Functional documentation - Equations & key concepts are explained
4. DEMO - an executable openAPI spec (former swagger)
5. Getting started: some basic API queries explained.
6. How to guides - for developers who want to use the API

## Work on the documentation

### Install the documentation tools

Documentation is generated from markdown using `mkdocs` with the `material` theme.

```bash
# (preferred) Install mkdocs and its extensions
poetry install --with docs

# (old way) install mkdocs and its extensions
pip install mkdocs mkdocs-render-swagger-plugin mkdocs-material mkdocs-macros-plugin
```

💡 Do not mixup _pip_ and _brew_ installation of `mkdocs`.

See the "getting started" docs for [mkdocs](https://www.mkdocs.org/getting-started/), and [material](https://squidfunk.github.io/mkdocs-material/getting-started/) if you run into issues.

### Launch a local documentation server

```bash
# If mkdocs is installed via poetry (preferred)
make run-doc
```

```bash
# If mkdocs is installed globally
# from the root of the cloned repository
cd docs
mkdocs serve
```

Open <http://localhost:8080>

### Verify the links

```bash
cd docs
# Check the warnings in the output for broken links
poetry run mkdocs build
# Test validity of external links
poetry run poetry run linkcheckMarkdown --recurse --verbose docs
```
