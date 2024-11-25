import argparse
import sys

from pip._vendor.pygments import highlight
from pip._vendor.pygments.formatters import get_formatter_by_name
from pip._vendor.pygments.lexers import get_lexer_by_name , get_lexer_for_filename , guess_lexer , TextLexer
from pip._vendor.pygments.util import ClassNotFound , OptionError


def main(args=sys.argv):
    """
    Main command line entry point.
    """
    desc = "Highlight an input file and write the result to an output file."
    parser = argparse.ArgumentParser(description=desc, add_help=False)

    operation = parser.add_argument_group('Main operation')
    lexersel = operation.add_mutually_exclusive_group()
    lexersel.add_argument(
        '-l', metavar='LEXER',
        help='Specify the lexer to use.  (Query names with -L.)  If not '
        'given and -g is not present, the lexer is guessed from the filename.')
    lexersel.add_argument(
        '-g', action='store_true',
        help='Guess the lexer from the file contents, or pass through '
        'as plain text if nothing can be guessed.')
    operation.add_argument(
        '-F', metavar='FILTER[:options]', action='append',
        help='Add a filter to the token stream.  (Query names with -L.) '
        'Filter options are given after a colon if necessary.')
    operation.add_argument(
        '-f', metavar='FORMATTER',
        help='Specify the formatter to use.  (Query names with -L.) '
        'If not given, the formatter is guessed from the output filename, '
        'and defaults to the terminal formatter if the output is to the '
        'terminal or an unknown file extension.')
    operation.add_argument(
        '-O', metavar='OPTION=value[,OPTION=value,...]', action='append',
        help='Give options to the lexer and formatter as a comma-separated '
        'list of key-value pairs. '
        'Example: `-O bg=light,python=cool`.')
    operation.add_argument(
        '-P', metavar='OPTION=value', action='append',
        help='Give a single option to the lexer and formatter - with this '
        'you can pass options whose value contains commas and equal signs. '
        'Example: `-P "heading=Pygments, the Python highlighter"`.')
    operation.add_argument(
        '-o', metavar='OUTPUTFILE',
        help='Where to write the output.  Defaults to standard output.')

    operation.add_argument(
        'INPUTFILE', nargs='?',
        help='Where to read the input.  Defaults to standard input.')

    flags = parser.add_argument_group('Operation flags')
    flags.add_argument(
        '-v', action='store_true',
        help='Print a detailed traceback on unhandled exceptions, which '
        'is useful for debugging and bug reports.')
    flags.add_argument(
        '-s', action='store_true',
        help='Process lines one at a time until EOF, rather than waiting to '
        'process the entire file.  This only works for stdin, only for lexers '
        'with no line-spanning constructs, and is intended for streaming '
        'input such as you get from `tail -f`. '
        'Example usage: `tail -f sql.log | pygmentize -s -l sql`.')
    flags.add_argument(
        '-x', action='store_true',
        help='Allow custom lexers and formatters to be loaded from a .py file '
        'relative to the current working directory. For example, '
        '`-l ./customlexer.py -x`. By default, this option expects a file '
        'with a class named CustomLexer or CustomFormatter; you can also '
        'specify your own class name with a colon (`-l ./lexer.py:MyLexer`). '
        'Users should be very careful not to use this option with untrusted '
        'files, because it will import and run them.')
    flags.add_argument('--json', help='Output as JSON. This can '
        'be only used in conjunction with -L.',
        default=False,
        action='store_true')

    special_modes_group = parser.add_argument_group(
        'Special modes - do not do any highlighting')
    special_modes = special_modes_group.add_mutually_exclusive_group()
    special_modes.add_argument(
        '-S', metavar='STYLE',
        help='Output style definitions for STYLE.')
    special_modes.add_argument(
        '-L', action='store_true',
        help='List lexers, formatters, and filters.')
    special_modes.add_argument(
        '-N', metavar='FILENAME',
        help='Guess and print the lexer name for the given file.')
    special_modes.add_argument(
        '-C', action='store_true',
        help='Guess and print the lexer name for the given input.')

    parsed_opts, remaining_args = parser.parse_known_args(args[1:])

    # Handle special modes first
    if parsed_opts.L:
        # List lexers, formatters, and filters
        print("Lexers:")
        for lexer in get_all_lexers():
            print(f"  {lexer[0]} ({', '.join(lexer[1])})")
        print("\nFormatters:")
        for formatter in get_all_formatters():
            print(f"  {formatter[0]} ({', '.join(formatter[1])})")
        print("\nFilters:")
        for filter in get_all_filters():
            print(f"  {filter}")
        return 0

    if parsed_opts.N:
        lexer = find_lexer_class_for_filename(parsed_opts.N)
        if lexer is None:
            lexer = TextLexer
        print(lexer.aliases[0])
        return 0

    if parsed_opts.C:
        inp = sys.stdin.buffer.read()
        try:
            lexer = guess_lexer(inp)
        except ClassNotFound:
            lexer = TextLexer
        print(lexer.aliases[0])
        return 0

    if parsed_opts.S:
        f_opt = parsed_opts.f
        if not f_opt:
            parser.print_help(sys.stderr)
            return 2
        if parsed_opts.l or parsed_opts.INPUTFILE:
            parser.print_help(sys.stderr)
            return 2

        try:
            fmter = get_formatter_by_name(f_opt, **vars(parsed_opts))
        except ClassNotFound as err:
            print(err, file=sys.stderr)
            return 1

        print(fmter.get_style_defs(parsed_opts.a or ''))
        return 0

    if parsed_opts.a is not None:
        parser.print_help(sys.stderr)
        return 2

    # Parse -F options
    F_opts = _parse_filters(parsed_opts.F or [])

    # -x: allow custom (eXternal) lexers and formatters
    allow_custom_lexer_formatter = bool(parsed_opts.x)

    # Select lexer
    lexer = None

    # Given by name?
    lexername = parsed_opts.l
    if lexername:
        if allow_custom_lexer_formatter and '.py' in lexername:
            try:
                filename = None
                name = None
                if ':' in lexername:
                    filename, name = lexername.rsplit(':', 1)
                    if '.py' in name:
                        name = None

                if filename and name:
                    lexer = load_lexer_from_file(filename, name, **vars(parsed_opts))
                else:
                    lexer = load_lexer_from_file(lexername, **vars(parsed_opts))
            except ClassNotFound as err:
                print('Error:', err, file=sys.stderr)
                return 1
        else:
            try:
                lexer = get_lexer_by_name(lexername, **vars(parsed_opts))
            except (OptionError, ClassNotFound) as err:
                print('Error:', err, file=sys.stderr)
                return 1

    # Read input code
    code = None

    if parsed_opts.INPUTFILE:
        if parsed_opts.s:
            print('Error: -s option not usable when input file specified',
                  file=sys.stderr)
            return 2

        infn = parsed_opts.INPUTFILE
        try:
            with open(infn, 'rb') as infp:
                code = infp.read()
        except Exception as err:
            print('Error: cannot read infile:', err, file=sys.stderr)
            return 1

        # Do we have to guess the lexer?
        if not lexer:
            try:
                lexer = get_lexer_for_filename(infn, code, **vars(parsed_opts))
            except ClassNotFound as err:
                if parsed_opts.g:
                    try:
                        lexer = guess_lexer(code, **vars(parsed_opts))
                    except ClassNotFound:
                        lexer = TextLexer(**vars(parsed_opts))
                else:
                    print('Error:', err, file=sys.stderr)
                    return 1
            except OptionError as err:
                print('Error:', err, file=sys.stderr)
                return 1

    elif not parsed_opts.s:  # Treat stdin as full file (-s support is later)
        code = sys.stdin.buffer.read()
        if not lexer:
            try:
                lexer = guess_lexer(code, **vars(parsed_opts))
            except ClassNotFound:
                lexer = TextLexer(**vars(parsed_opts))

    else:  # -s option needs a lexer with -l
        if not lexer:
            print('Error: when using -s a lexer has to be selected with -l',
                  file=sys.stderr)
            return 2

    # Process filters
    for fname, fopts in F_opts:
        try:
            lexer.add_filter(fname, **fopts)
        except ClassNotFound as err:
            print('Error:', err, file=sys.stderr)
            return 1

    # Select formatter
    outfn = parsed_opts.o
    fmter = parsed_opts.f
    if fmter:
        if allow_custom_lexer_formatter and '.py' in fmter:
            try:
                filename = None
                name = None
                if ':' in fmter:
                    filename, name = fmter.rsplit(':', 1)
                    if '.py' in name:
                        name = None

                if filename and name:
                    fmter = load_formatter_from_file(filename, name, **vars(parsed_opts))
                else:
                    fmter = load_formatter_from_file(fmter, **vars(parsed_opts))
            except ClassNotFound as err:
                print('Error:', err, file=sys.stderr)
                return 1
        else:
            try:
                fmter = get_formatter_by_name(fmter, **vars(parsed_opts))
            except (OptionError, ClassNotFound) as err:
                print('Error:', err, file=sys.stderr)
                return 1

    if outfn:
        if not fmter:
            try:
                fmter = get_formatter_by_name(outfn.split('.')[-1], **vars(parsed_opts))
            except (OptionError, ClassNotFound) as err:
                print('Error:', err, file=sys.stderr)
                return 1

    # Highlight and output
    try:
        highlighted = highlight(code, lexer, fmter)
        if outfn:
            with open(outfn, 'w') as outfp:
                outfp.write(highlighted)
        else:
            sys.stdout.write(highlighted)
    except Exception as err:
        print('Error:', err, file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
