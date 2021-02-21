import errno
import os
import pty
import select
import signal
import subprocess
from . import logger

# Set signal handler for SIGINT.
signal.signal(signal.SIGINT, lambda s,f: print("received SIGINT"))


def unbuffered_Popen(cmd):
    out_r, out_w = pty.openpty()
    err_r, err_w = pty.openpty()
    process = subprocess.Popen(cmd, stdout=out_w, stderr=out_w)
    os.close(out_w)
    os.close(err_w)
    fds = {OutStream(out_r), OutStream(err_r)}
    while fds:
        while True:
            try:
                rlist, _, _ = select.select(fds, [], [])
                break
            except InterruptedError:
                continue
        # Handle all file descriptors that are ready.
        for f in rlist:
            lines, readable = f.read_lines()
            # Example: Just print every line. Add your real code here.
            for line in lines:
                logger.message(line)
            if not readable:
                # This OutStream is finished.
                fds.remove(f)


class OutStream:
    def __init__(self, fileno):
        self._fileno = fileno
        self._buffer = b""

    def read_lines(self):
        try:
            output = os.read(self._fileno, 1000)
        except OSError as e:
            if e.errno != errno.EIO: raise
            output = b""
        lines = output.split(b"\n")
        lines[0] = self._buffer + lines[0] # prepend previous
                                           # non-finished line.
        if output:
            self._buffer = lines[-1]
            finished_lines = lines[:-1]
            readable = True
        else:
            self._buffer = b""
            if len(lines) == 1 and not lines[0]:
                # We did not have buffer left, so no output at all.
                lines = []
            finished_lines = lines
            readable = False
        finished_lines = [line.rstrip(b"\r").decode()
                          for line in finished_lines]
        return finished_lines, readable

    def fileno(self):
        return self._fileno
