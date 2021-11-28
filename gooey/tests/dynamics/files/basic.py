from argparse import ArgumentParser

from gooey import Events, Gooey

parser = ArgumentParser()
parser.add_argument('foo', type=int)

@Gooey(use_events=[Events.VALIDATE_FORM])
def main():
    print(parser.parse_args())


if __name__ == '__main__':
    main()

