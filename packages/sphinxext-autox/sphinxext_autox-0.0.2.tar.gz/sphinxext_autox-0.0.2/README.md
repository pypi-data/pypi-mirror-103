# Sphinx-autox

A little opinionated version of autodoc and autosummary that
recursively documents your modules and creates one file per class.

## Usage

Add `sphinxext_autox` as the **first** entry to your extensions in `conf.py`:

```py
extensions = [
    'sphinxext_autox',
    ...
]
```

Create a `api.rst` file like the following:

```rst
My API
======

.. autosummary::
   :toctree: source
   :recursive:

   mymodule1
   mymodule2
```

The stub files will be created/maintained in the `source` folder.

## Critique

Unfortunately, since other files in Sphinx also try to load autodoc,
this package has to replace the original files. It isn't possible to
make a custom version without also having to change the rST tags.
