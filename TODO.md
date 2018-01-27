Release TODO
============

 - [ ] MUST add new entries to all language files

 - [ ] Fix user supplied directory path when packaged. Currently gives super cryptic failures
 - [X] need ability to call out to external seed function for dynamic defaults
    - [ ] update readme (SavingOverIt could be example use case)
    - [ ] extend this to all types (currently only works for Dropdowns)
    - [ ] think about stuff. Need a friendly way to specify mappings that's more
          flexible than options_strings
 - [X] success/error screen after a ForceStop should be configurable. Stopping early does not necessarily error

 - [ ] customizable button text
 - [X] text encoding
 - [X] pass down the font info to the console
 - [X] pass down the style info to the console


Issue #234
 - allow general options

README:

 - update README with all the things
 - [ ] RadioGroup
    - [ ] `initial_selection` option
    - [ ] group name options
 - [ ] force_stop_is_error
 - [X] validation howto
 - [ ] advanced layout howto
 - [ ] turning on/off dialog options
 - [X] full list of custom widgets and their options
 - [ ] progress bar management


Custom Validation:

 - [X] make sure user supplied validators fail gracefully and report something useful
 - [ ] validator should be able to call outside itself -- either to a separate cmdline util, or a subset of the host prog


Later TODO:
 - overview of Gooey for peeps who wanna dev against it
