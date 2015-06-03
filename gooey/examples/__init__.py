import sys
import time

program_message = \
'''
Thanks for checking out out Gooey!

This is a sample message to demonstrate Gooey's functionality.

Here's are the arguments you supplied:

{0}

-------------------------------------

Gooey is an ongoing project, so feel free to submit any bugs you find to the
issue tracker on Github[1], or drop me a line at audionautic@gmail.com if ya want.

[1](https://github.com/chriskiehl/Gooey)

See ya!

^_^

'''

def display_message():
  message = program_message.format('\n-'.join(sys.argv[1:])).split('\n')
  delay = 1.8 / len(message)

  for line in message:
    print line
    time.sleep(delay)

