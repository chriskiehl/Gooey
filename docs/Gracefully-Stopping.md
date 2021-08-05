# Gracefully Stopping a Running Process

>New in v1.0.9!

<p align="center">
  <img src="https://github.com/chriskiehl/GooeyImages/raw/images/docs/graceful-stopping/screenshot.PNG"/>
</p>

**Contents:**

* [How to tell Gooey which shutdown signal to use](#how-to-tell-gooey-which-signal-to-use)
* [How to catch KeyboardInterrupts](#How-to-catch-KeyboardInterrupts)
* [How to catch general interrupt signals](#How-to-catch-general-interrupt-signals)

By default, Gooey will kill the child process without any chance for cleanup. This guide will explain how to adjust that behavior so that you can detect when Gooey is attempting to close your process and use that signal to shutdown gracefully.   

### Basics: How to tell Gooey which shutdown signal to use: 

You can control the signal Gooey sends while stopping your process via `shutdown_signal` decorator argument. Signal values come from the builtin `signal` python module. On linux, any of the available constants may be used as a value. However, on Windows, only `CTRL_BREAK_EVENT`, `CTRL_C_EVENT` and `SIGTERM` are supported by the OS.   
 
 
```python
import signal 
@Gooey(shutdown_signal=signal.CTRL_C_EVENT)
def main():
    ...
```


### How to catch KeyboardInterrupts:

Keyboard interrupts are triggered in response to the `CTRL_C_EVENT` signal.

```python
import signal 
@Gooey(shutdown_signal=signal.CTRL_C_EVENT)
def main():
    ...
``` 

Catching them in your code is really easy! They conveniently show up as top-level Exceptions. Just wrap your main logic in a try/except and you'll be able to catch when Gooey tries to shut down your process.   

```python
try
   # your code here
except KeyboardInterrupt: 
   # cleanup and shutdown or ignore 
``` 

### How to catch general interrupt signals

Handling other signals is only slightly more involved than the `CTRL_C_EVENT` one. You need to install a handler via the `signal` module and tie it to the specific signal you want to handle. Let's use the `CTRL_BREAK_EVENT` signal as example. 

```python
import signal

# (1)
def handler(*args): 
    print("I am called in response to an external signal!")
    raise Exception("Kaboom!")

# (2) 
signal.signal(signal.SIGBREAK, handler)

# (3)
@Gooey(shutdown_signal=signal.CTRL_BREAK_EVENT)
def main():
    # your code here 
    # ... 
```    

Here we setup a handler called `handler` (1). This function can do anything you want in response to the signal including ignoring it entirely. Next we tie the signal we're interested in to the handler (2). Finally, we tell Gooey to send the `BREAK` signal(3) when the stop button is clicked. 

> Note: pay close attention to the different constants used while specifying a handler (e.g. `SIGBREAK`) versus specifying which signal will be sent (e.g. `CTRL_BREAK_SIGNAL`).   


