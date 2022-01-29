from argparse import ArgumentParser

from gooey import Events, Gooey, GooeyParser
from gooey import types as t


with open('tmp.txt', 'w') as f:
    import sys
    f.write(str(sys.argv))



def handle_success(args, state: t.PublicGooeyState):
    field = state['active_form'][0]
    field['value'] = 'success'
    return {**state, 'active_form': [field]}


def handle_error(args, state: t.PublicGooeyState):
    field = state['active_form'][0]
    field['value'] = 'error'
    return {**state, 'active_form': [field]}


def make_parser():
    parser = GooeyParser(on_error=handle_error, on_success=handle_success)
    parser.add_argument('foo')
    return parser

@Gooey(use_events=[Events.ON_ERROR, Events.ON_SUCCESS])
def main():
    parser = make_parser()
    args = parser.parse_args()
    if args.foo == 'fail':
        raise Exception('EXCEPTION')
    print('DONE')


if __name__ == '__main__':
    main()

