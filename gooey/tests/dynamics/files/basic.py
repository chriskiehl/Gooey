from argparse import ArgumentParser

from gooey import Events, Gooey


with open('tmp.txt', 'w') as f:
    import sys
    f.write(str(sys.argv))

def make_parser():
    parser = ArgumentParser()
    parser.add_argument('foo', type=int)
    return parser

@Gooey(use_events=[Events.VALIDATE_FORM])
def main():
    parser = make_parser()
    print(parser.parse_args())
    print('DONE')


if __name__ == '__main__':
    main()

