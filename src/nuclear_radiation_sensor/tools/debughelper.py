import logging
logger = logging.getLogger("morse." + __name__)

import sys


class RemoteDebugHelper:
    """Helper to connect to a remote debug server. It is sufficient to call
     it once. Standard breakpoints will work afterwards.
    """

    def __init__(self, port, remote_debug_lib):
        """Constructor method

        Sets the port of the debug server and loads the needed pydevd library
        (pycharm-debug.egg for PyCharm) from the given path.
        """
        self.port = port
        if remote_debug_lib not in sys.path:
            sys.path.append(remote_debug_lib)

    def connect(self):
        """Connects to a remote debugging server.
        """
        logger.debug("Connecting to remote debugger...")
        import pydevd

        pydevd.settrace('localhost', port=self.port, stdoutToServer=True,
                        stderrToServer=True)
