#!/usr/bin/python3

import math
import os
import argparse
from time import sleep

from datetime import datetime
from datetime import timedelta

import pathlib
import pkg_resources

import simpleaudio as sa

NUMS = '1234567890'
POSTURES = {'p': 'Prostration', 'w': 'Walking', 's': 'Sitting'}

bell = pathlib.Path(pkg_resources.resource_filename(__name__, "data/bell.wav"))
clear_command = 'cls' if os.name == 'nt' else 'clear'


def f(n, r=2):
    n = int(n)
    return ''.join(['0' for _ in range(r - len(str(n)))]) + str(n)


def play_bell(wait=False):
    wave_obj = sa.WaveObject.from_wave_file(bell.as_posix())
    play_obj = wave_obj.play()
    if wait:
        play_obj.wait_done()


def mins(secs):
    m = f(math.floor(secs / 60))
    s = f(secs % 60)
    return "%s:%s" % (m, s)


def countdown(m, text='', delay=0.2):
    t = m * 60
    start_datetime = datetime.now()

    def print_remaining():
        print("%s%s remaining" % ('%s: ' % text if text else '', mins(t)))

    while t > 0:
        os.system(clear_command)
        print_remaining()

        elapsed = datetime.now() - start_datetime
        t = (m * 60) - elapsed.seconds
        sleep(delay)


def get_times(string: str):
    """ what it does:
        turn 'p5w5s10' (prostration: 5, walking: 5, sitting: 10)
        into dict with the times of each posture
    """

    vals = {x: 0 for x in POSTURES}
    for i in range(len(string)):
        for v in vals:
            if v in string[i]:
                vals[v] = string[i + 1]

                # check for remaining digits
                for z in range(i + 2, len(string)):
                    if string[z] in NUMS:
                        vals[v] = vals[v] + string[z]
                    else:
                        break

                # convert str to int
                vals[v] = int(vals[v])

    # truncate empty values
    for v in list(vals):
        if vals[v] == 0:
            del vals[v]

    if not vals:
        raise IndexError('No times bigger than 0!')

    return vals


def meditate(times="", delay=0.2):
    def is_text_valid(text):
        try:
            get_times(text)
        except (ValueError, IndexError):
            print("Invalid format for times (format: 'p5w30s30')")
            return False
        else:
            return True

    if not times:
        while True:
            input_text = input("Enter times (format: 'p5w30s30'): ")
            if is_text_valid(input_text):
                times = input_text
                break

    vals = get_times(times)

    print('\nTimes: ')
    for v in vals:
        print(f'{POSTURES[v]}: {vals[v]}')

    play_bell()

    for v in vals:
        countdown(vals[v], text=POSTURES[v], delay=delay)

        # check if is last timer - if so, we have to wait on the sound to finish
        wait = len(vals) - 1 == list(vals).index(v)
        play_bell(wait=wait)


def main():
    parser = argparse.ArgumentParser(description='Simple vipassana meditation timer')
    parser.add_argument('times', nargs='?', type=str, default='',
                        help="Times for each meditation posture (format: 'p5w30s30')")
    args = parser.parse_args()

    meditate(times=args.times if args.times else '')


if __name__ == '__main__':
    main()
