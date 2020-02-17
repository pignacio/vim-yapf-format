" yapf_format.vim - YAPF vim integration
" Author:     Ignacio Rossi <http://www.github.com/pignacio>
" Version:    0.0.1

if exists("g:yapf_format_loaded")
  finish
endif

if ! has('python3')
  echohl WarningMsg |
        \ echomsg "vim-yapf-format requires vim compiled with python support" |
        \ echohl None
  finish
endif

function! GetVar(...)
  let l:varName = a:1
  let l:varValue = a:2
  if exists('b:yapf_format_' . l:varName)
    exe "let l:varValue = b:yapf_format_" . l:varName
  elseif exists('g:yapf_format_' . l:varName)
    exe "let l:varValue = g:yapf_format_" . l:varName
  endif
  return l:varValue
endfunction

let g:yapf_format_loaded = 1

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )
let s:yapf_format_script = s:script_folder_path . '/../python/yapf_format.py'
let s:appended_yapf_path = 0

command! -range YapfFormat <line1>,<line2>call YapfFormat()
function! YapfFormat() range
  if ! s:appended_yapf_path
    if exists("g:yapf_format_yapf_location")
      py3 import sys
      exe 'py3 sys.path.append("' . expand(g:yapf_format_yapf_location) . '")'
    endif
    let s:appended_yapf_path = 1
  endif

  if exists('b:yapf_format_style')
    let l:buffer_style = b:yapf_format_style
  else
    let l:buffer_style = ''
  endif

  if exists('g:yapf_format_style')
    let l:global_style = g:yapf_format_style
  else
    let l:global_style = 'pep8'
  endif

  let l:allow_out_of_range = exists('g:yapf_format_allow_out_of_range_changes')?
        \ !!g:yapf_format_allow_out_of_range_changes :
        \ 0

  exe a:firstline . ',' . a:lastline . 'py3file ' . s:yapf_format_script


  if exists('l:error_type')
    let l:error_line = l:error_position[0]
    let l:error_column = l:error_position[1]
    echohl ErrorMsg  |
          \ echon "<ERROR> " . l:error_type . " @ (" . l:error_line . ', ' .
          \ l:error_column . ')' | echohl None
    if GetVar('move_to_error', 1) == 1
      let l:position = getpos('.')
      let l:position[1] = l:error_line
      let l:position[2] = l:error_column
      call setpos('.', l:position)
    endif
    return 1
  endif
  echon "Used style: " . l:used_style . " "
  return 0
endfunction

command! YapfFullFormat call YapfFullFormat()
function! YapfFullFormat()
  let l:cursor_pos = getpos(".")
  redir => l:message
  %YapfFormat
  redir END
  if l:message !~ '<ERROR>' || GetVar('move_to_error', 1) != 1
    call setpos(".", l:cursor_pos)
  endif
endfunction
