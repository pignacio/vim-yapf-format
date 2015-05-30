===============
vim-yapf-format
===============

VIM integration for YAPF_.


Installation
============

If you use Vundle_, add to your ``.vimrc``:

.. code::

  Plugin 'pignacio/vim-yapf-format'

or with pathogen.vim_:

.. code:: sh

  cd ~/.vim/bundle
  git clone git://github.com/pignacio/vim-yapf-format

Requirements
============

* YAPF_

**NOTE:**

If ``YAPF`` is not in your ``sys.path`` you have to add the following line in
your ``.vimrc``:

.. code:: vim

  let g:yapf_format_yapf_location = '/path/to/yapf'

Usage
=====

* The ``YapfFullFormat`` command formats the whole file and tries to restore
  the cursor position after formatting.

**NOTE:**  Right now we can't do much about the cursor, so ``YapfFullFormat``
just tries to restore it to the same line and column it was before formatting.
Maybe if ``yapf`` implements something like ``clang-format.py`` ``--cursor``
argument, we can improve this.


* Use the ``YapfFormat`` command to format the current line or range. The
  cursor is reset to the beggining of the formatted range. Some examples:

.. code:: vim

  " Reformat current line
  :YapfFormat

  " Reformat current visual range
  :'<,'>YapfFormat

  " In general, reformat <range>
  :<range>YapfFormat

  " Don't do this, use YapFullFormat!
  :%YapfFormat


The style used to format the buffer is checking the following in order:

* ``b:yapf_format_style`` variable.

* Local ``.yapf.style`` for the file's project (or current directory for
  unsaved files).

* ``g:yapf_format_style`` variable.

* ``pep8``

Configuration
=============

* **Out of range changes:**

YAPF fixes code (indentation fixes, for example) outside of the ``--lines``
range.

This produces unexpected changes when using the VISUAL reformat, and makes
editing and partially reformatting a non-YAPF-compliant file vey cumbersome.

We avoid this behaviour by default, applying changes only in the direct
proximity of the selected range.

If you like the original behaviour, you can restore it setting

.. code:: vim

  let g:yapf_format_allow_out_of_range_changes = 1

* **Moving cursor to errors:**

YAPF fails when the buffer contains syntax errors. When that happens during a
reformat, the cursor is moved to the error location. To disable this behaviour,
you can set:

.. code:: vim

  let g:yapf_format_move_to_error = 0

Key Bindings
============

I use the following key bindings to reformat the whole file in normal mode,
the current line in insert mode and the current range in visual mode:

.. code:: vim

  map <C-o> :YapfFullFormat<CR>
  imap <C-o> <ESC>:YapfFormat<CR>i
  vmap <C-o> :YapfFormat<CR>

Of course, the ``<C-o>`` can be changed to any key you like ;)


Credits
=======

This script is heavily inspired by clang-format.py_


.. _YAPF: https://github.com/google/yapf
.. _Vundle: https://github.com/gmarik/vundle
.. _pathogen.vim: https://github.com/tpope/vim-pathogen
.. _clang-format.py:
  https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format.py
