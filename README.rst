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

**NOTE:**

If ``yapf`` is not in your ``sys.path`` you have to add the following line in
your ``.vimrc``:

.. code:: vim

  let g:yapf_format_yapf_location = '/path/to/yapf'

Usage
=====

Use the ``YapfFormat`` command to format the current lines or range. Some
examples:

.. code:: vim

  # Reformat current line
  :YapfFormat

  # Reformat current visual range
  :'<,'>YapfFormat

  # Reformat whole file
  :%YapfFormat

  # In general, reformat <range>
  :<range>YapfFormat


I use the following key bindings to reformat the whole file in normal mode,
the current line in insert mode and the current range in visual mode:

.. code:: vim

  map <C-o> :%YapfFormat<CR>
  imap <C-o> <ESC>:YapfFormat<CR>i
  vmap <C-o> :YapfFormat<CR>

Of course, the ``<C-o>`` can be changed to any key you like ;)


.. _YAPF: https://github.com/google/yapf
.. _Vundle: https://github.com/gmarik/vundle
.. _pathogen.vim: https://github.com/tpope/vim-pathogen
