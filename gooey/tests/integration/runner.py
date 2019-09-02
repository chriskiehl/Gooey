import os
import time
from concurrent import futures

from gooey.gui.util.freeze import getResourcePath
from gooey.python_bindings import config_generator
from gooey.util.functional import merge


def run_integration(module, assertionFunction, **kwargs):
    """
    Integration test harness.

    WXPython is *super* finicky when it comes to integration tests. It needs
    the main Python thread for its app loop, which means we have to integration
    test on a separate thread. The causes further strangeness in how Unittest
    and WXPython interact. In short, each test must be in its own module and
    thus import its own wx instance, and be run in its own "space."

    So long as the above is satisfied, then integration tests can run reliably.

    """
    from gooey.gui import application
    options = merge({
        'image_dir': '::gooey/default',
        'language_dir': getResourcePath('languages'),
        'show_success_modal': False
    }, kwargs)
    module_path = os.path.abspath(module.__file__)
    parser = module.get_parser()
    build_spec = config_generator.create_from_parser(parser, module_path, **options)

    time.sleep(2)
    app = application.build_app(build_spec=build_spec)
    executor = futures.ThreadPoolExecutor(max_workers=1)
    # executor runs in parallel and will submit a wx.Destroy request
    # when done making its assertions
    testResult = executor.submit(assertionFunction, app, build_spec)
    # main loop blocks the main thread
    app.MainLoop()
    # .result() blocks as well while we wait for the thread to finish
    # any waiting it may be doing.
    testResult.result()
    del app


