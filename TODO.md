TODO
====

- Update parser to catch all argparse import styles
- Investigate Docopt
- better graphics

- Restart Button Change :
    * need different strategy for everything added.

- Fix vertical stacking of restart button
- system for supplying custom widgets to the GUI
  -- e.g. a FileChooser, rather than just a TextBox
- Remove debug statements current printing from program
- add optional cancel button.
- allow NoConfig to run without argparse (Issue #43)
    * display warning when this happens (could be a misfire on Gooey's end)
    * add suppress warnings flag

- Implemente a simple MVC pattern for isolate gui toolkit specifique code and
  argparse specifique code (support for tkinter, qt etc ... and docopt or unix
  cli as text)

- Make a .io site for the presentation

- More comments and basic api generation + some txt for explain the global
  design fo the project
