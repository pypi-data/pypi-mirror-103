pandaspraxis
===============================

A SQL to Pandas translator

Installation
------------

To install use pip:

    $ pip install pandaspraxis

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/UP/pandaspraxis.git
    $ cd pandaspraxis
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix pandaspraxis
    $ jupyter nbextension enable --py --sys-prefix pandaspraxis

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite pandaspraxis

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
