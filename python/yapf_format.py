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
    lines_range = (vim.current.range.start + 1, vim.current.range.end + 1)
    formatted = yapf_api.FormatCode(text,
                                    filename='<stdin>',
                                    style_config=vim.eval('l:style'),
                                    lines=[lines_range],
                                    verify=False)

    lines = formatted.rstrip('\n').split('\n')
    sequence = difflib.SequenceMatcher(None, unicode_buf, lines)
    for op in reversed(sequence.get_opcodes()):
        if op[0] is not 'equal':
            vim.current.buffer[op[1]:op[2]] = [l.encode(encoding)
                                               for l in lines[op[3]:op[4]]]


if __name__ == '__main__':
    main()
