from __future__ import absolute_import, unicode_literals, division

import difflib
import sys
import os
import vim

try:
    from yapf.yapflib import yapf_api, file_resources, style
    _YAPF_IMPORTED = True
except ImportError:
    sys.stderr.write("Could not import yapf_api. Have you set "
                     "g:yapf_format_yapf_location correctly?")
    _YAPF_IMPORTED = False


def _get_file_style():
    path = vim.current.buffer.name or os.getcwd()
    project_style = file_resources.GetDefaultStyleForDir(path)
    if project_style == style.DEFAULT_STYLE:
        return None
    return project_style


def _get_style():
    return (vim.eval('l:buffer_style') or _get_file_style() or
            vim.eval('l:global_style'))


def main():
    if not _YAPF_IMPORTED:
        return

    encoding = vim.eval('&encoding')
    buf = vim.current.buffer
    text = '\n'.join(buf)
    buf_range = (vim.current.range.start, vim.current.range.end)
    lines_range = [pos + 1 for pos in buf_range]
    style_config = _get_style()
    vim.command('let l:used_style = "{}"'.format(style_config))
    try:
        formatted = yapf_api.FormatCode(text,
                                        filename='<stdin>',
                                        style_config=style_config,
                                        lines=[lines_range],
                                        verify=False)
    except (SyntaxError, IndentationError) as err:
        vim.command('let l:error_type = "{}"'.format(type(err).__name__))
        vim.command('let l:error_position = [{}, {}]'.format(err.lineno,
                                                             err.offset))
        return

    if isinstance(formatted, tuple):
        formatted = formatted[0]

    lines = formatted.rstrip('\n').split('\n')
    sequence = difflib.SequenceMatcher(None, buf, lines)

    allow_out_of_range = vim.eval("l:allow_out_of_range") != "0"

    for op in reversed(sequence.get_opcodes()):
        if op[0] == 'equal':
            continue
        # buf_range is [closed, closed], and op is [closed,open)
        # so we must offset buf_range[1]
        in_range = max(buf_range[0], op[1]) <= min(buf_range[1] + 1, op[2])
        if in_range or allow_out_of_range:
            vim.current.buffer[op[1]:op[2]] = [l.encode(encoding)
                                               for l in lines[op[3]:op[4]]]


if __name__ == '__main__':
    main()
