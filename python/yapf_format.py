import difflib
import sys
import vim

try:
    from yapf.yapflib import yapf_api
    _YAPF_IMPORTED = True
except ImportError:
    sys.stderr.write("Could not import yapf_api. Have you set "
                     "g:yapf_format_yapf_location  correctly?")
    _YAPF_IMPORTED = False


def _get_vim_variable(variable_name):
    if int(vim.eval("exists('{}')".format(variable_name))):
        return vim.eval(variable_name)
    return None


def _get_style():
    return (_get_vim_variable('b:yapf_format_style') or
            _get_vim_variable('g:yapf_format_style') or 'pep8')


def main():
    if not _YAPF_IMPORTED:
        return

    buf = vim.current.buffer
    text = '\n'.join(buf)
    lines_range = (vim.current.range.start + 1, vim.current.range.end + 1)

    formatted = yapf_api.FormatCode(text,
                                    filename='<stdin>',
                                    style_config=_get_style(),
                                    lines=[lines_range],
                                    verify=False)

    lines = formatted.rstrip('\n').split('\n')
    sequence = difflib.SequenceMatcher(None, buf, lines)
    for op in reversed(sequence.get_opcodes()):
        if op[0] is not 'equal':
            vim.current.buffer[op[1]:op[2]] = lines[op[3]:op[4]]


if __name__ == '__main__':
    main()
