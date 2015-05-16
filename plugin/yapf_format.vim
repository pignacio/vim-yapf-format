" yapf_format.vim - YAPF vim integration
" Author:     Ignacio Rossi <http://www.github.com/pignacio>
" Version:    0.0.1

if exists("g:yapf_format_loaded")
  finish
endif

if ! has('python')
  echohl WarningMsg |
        \ echomsg "vim-yapf-format requires vim compiled with python support" |
        \ echohl None
  finish
endif

let g:yapf_format_loaded = 1

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )
let s:yapf_format_script = s:script_folder_path . '/../python/yapf_format.py'

let s:appended_yapf_path = 0

command! -range YapfFormat <line1>,<line2>call YapfFormat()
function! YapfFormat() range
  if ! s:appended_yapf_path
    if exists("g:yapf_format_yapf_location")
      py import sys
      exe 'py sys.path.append("' . expand(g:yapf_format_yapf_location) . '")'
    endif
    let s:appended_yapf_path = 1
  endif

  if exists('b:yapf_format_style')
    let l:style = b:yapf_format_style
  elseif exists('g:yapf_format_style')
    let l:style = g:yapf_format_style
  else
    let l:style = 'pep8'
  endif
  let l:allow_out_of_range = exists('g:yapf_format_allow_out_of_range_changes')?
        \ !!g:yapf_format_allow_out_of_range_changes :
        \ 0

  exe a:firstline . ',' . a:lastline . 'pyf ' . s:yapf_format_script
  if exists('l:error_type')
    let l:error_line = l:error_position[0]
    let l:error_column = l:error_position[1]
    echohl ErrorMsg  |
          \ echo l:error_type . " @ (" . l:error_line . ', ' . l:error_column . ')' |
          \ echohl None
    let l:position = getpos('.')
    let l:position[1] = l:error_line
    let l:position[2] = l:error_column
    call setpos('.', l:position)
    return 1
  endif
  return 0
endfunction

command! YapfFullFormat call YapfFullFormat()
function! YapfFullFormat()
  let l:cursor_pos = getpos(".")
  redir => l:message
  %YapfFormat
  redir END
  if l:message == ''
    call setpos(".", l:cursor_pos)
  endif
endfunction
