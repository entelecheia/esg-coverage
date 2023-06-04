---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Examples

This page contains a few examples of how you can use The Analyst Pathway in ESG package.

## Installation

You can install The Analyst Pathway in ESG using `pip`:

```{code-cell}
pip install esg-coverage
```

## Usage

```python
from esgcov import get_version

print(get_version())
```