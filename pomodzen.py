#!/usr/bin/env python

###########################################
# config shit, edit to yr own tastes
###########################################



bg   = "#444"
fg   = "#F33"
font = "droid sans mono-18"

height = 40
width  = 265

# in seconds, please
pomodoro_length = (60) / 6.0

# runs at the end of the pomodoro
done_cmd = "mplayer ~/vuvuzela.opus"



###########################################
# party starts here
###########################################

from subprocess import Popen, PIPE, call
import time
import math

# bullshit value having to do with the text width and width of window
# adjust this if you change the font and it looks fucked up
max_offset = 192

dzen_cmd = [
    "dzen2",
     "-p",
     "-xs", "2",

     "-fn", font,

     "-bg", bg,
     "-fg", fg,

     "-ta", "l",
     "-h", height,
     "-y", "-{0}".format(height),
     "-w", width,
     "-x", "-{0}".format(width)]

dzen_ctrl = """^p({offset}){m:02.0f}:{s:02.0f}^p(+5)^r(500x40)
"""

class dzen(object):
    pipe_to = None

    def __init__(self, cmd):
        self.pipe_to = Popen([str(x) for x in cmd], stdin=PIPE)

    def kill(self):
        self.pipe_to.kill()

class pomodzen(dzen):
    start = None
    now = None
    end = None

    last_left = None
    last_offset = None

    def __init__(self, length, cmd, done_cmd):
        dzen.__init__(self, cmd)

        self.start = time.time()
        self.now = self.start
        self.end = self.start + length + 1

        self.done_cmd = done_cmd

    def __call__(self):
        while True:
            self.now = time.time()
            if self.now > self.end:
                break

            self.update(dzen_ctrl)
            time.sleep(.1)

        call(self.done_cmd, shell=True)
        self.kill()

    def update(self, ctrl):
        left = self.end - self.now
        offset = int(max_offset - ((left / pomodoro_length) * max_offset))

        if left == self.last_left and offset == self.last_offset:
            return

        self.last_left = left
        self.last_offset = offset

        m = math.floor(left / 60)
        s = int(left - (m * 60))

        ctrl = ctrl.format(m=m, s=s, h=height, offset=offset)

        self.pipe_to.stdin.write(ctrl.encode("ascii"))

if __name__ == "__main__":
    pomodzen(
        length=pomodoro_length,
        cmd=dzen_cmd,
        done_cmd=done_cmd)()
