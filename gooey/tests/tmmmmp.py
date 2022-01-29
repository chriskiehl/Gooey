from gooey import GooeyParser, Gooey



def main():
    parser = GooeyParser()
    subs = parser.add_subparsers()
    foo = subs.add_parser('foo')
    foo.add_argument('a')
    foo.add_argument('b')
    foo.add_argument('p')

    bar = subs.add_parser('bar')
    bar.add_argument('a')
    bar.add_argument('b')
    bar.add_argument('z')
    parser.parse_args(['foo'])


main()