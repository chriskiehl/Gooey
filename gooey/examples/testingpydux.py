from pydux.create_store import create_store
from functools import reduce


def assign(*args):
    return reduce(lambda acc, x: acc.update(x) or acc, args, {})


def mylistener(*args, **kwargs):
    print('mylistener', args, kwargs)


def todo_reducer(state, action):
    if not state:
        return {'todos': []}
    if action['type'] == 'ADD_TODO':
        return assign(state, {
            'foo': 'bar'
        })
    else:
        return state


store = create_store(todo_reducer)
store.subscribe(mylistener)
a = store.dispatch({'type': 'ADD_TODO'})
print('state:', store['get_state']())
print(a)
a = store.dispatch({'type': 'ADD_TODO'})
# a = {'asdf': 1234}
# b = {'asdf': 3456}
#
# print(assign(a,b))
# print(a)
# print(b)

