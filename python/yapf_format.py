from __future__ import absolute_import, unicode_literals, division

import difflib
import sys
import vim

try:
    from yapf.yapflib import yapf_api
    _YAPF_IMPORTED = True
except ImportError:
    sys.stderr.write("Could not import yapf_api. Have you set "
                     "g:yapf_format_yapf_location correctly?")
    _YAPF_IMPORTED = False


def main():
    if not _YAPF_IMPORTED:
        return

    encoding = vim.eval('&encoding')
    buf = vim.current.buffer
    unicode_buf = [unicode(s, encoding) for s in buf]
    text = '\n'.join(unicode_buf)
    buf_range = (vim.current.range.start, vim.current.range.end)
    lines_range = [pos + 1 for pos in buf_range]
    formatted = yapf_api.FormatCode(text,
                                    filename='<stdin>',
                                    style_config=vim.eval('l:style'),
                                    lines=[lines_range],
                                    verify=False)

    lines = formatted.rstrip('\n').split('\n')
    sequence = difflib.SequenceMatcher(None, unicode_buf, lines)

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
