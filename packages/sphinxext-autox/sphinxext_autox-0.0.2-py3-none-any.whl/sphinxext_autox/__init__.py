import os
import sphinx.ext

__version__ = '0.0.2'

# override sphinx.ext with our patched versions
sphinx.ext.__path__.insert(
    0,
    os.path.abspath(
        os.sep.join([os.path.dirname(__file__), 'sphinx', 'ext'])))
print("[sphinxext_autox] replacing built-in exts, sphinx.ext.__path__ is now", sphinx.ext.__path__)

def setup(app):
    app.setup_extension('sphinx.ext.autosummary')
    app.setup_extension('sphinx.ext.autodoc')
    return {
        'version': __version__,
    }
