# vipassana-timer
Meditation timer for vipassana (insight meditation) with different postures

## Requirements
 - simpleaudio

## Installation
```sh
pip install vipassana-timer
```

or

```sh
git clone https://github.com/toxicologist/vipassana-timer
cd vipassana-timer
python setup.py install
```

## Usage
```
>meditate -h
usage: meditate [-h] [-t TIMES] [-a] [-s]

Simple vipassana meditation timer

optional arguments:
  -h, --help            show this help message and exit
  -t TIMES, --times TIMES
                        Times for each meditation
                        posture (format: 'p5w30s30')
  -a, --accurate        Use accurate datetime for
                        countdown instead of time.sleep
                        (leave this on if you're in a
                        hurry)
  -s, --show_end_times  Show expected vs. real time
                        delta at the end of the
                        session. Useful if you're using
                        time.sleep, to see how delayed
                        the countdown is
```

The script takes inputs for the three postures: prostration, walking, and sitting -
represented by the letters 'p', 'w', 's', each followed by the desired time, in minutes.

For example, if you wanted 10 minutes walking and 10 sitting:
```sh
# example usage
>meditate -t w10s10

#or
>meditate
Enter times (format: 'p5w30s30'): w10s10

#result

Times:
Walking: 10
Sitting: 10

Walking: 10:00 remaining
```

Or, if you only want to do 35 minutes of sitting:
```sh
>meditate -t s35

Times:
Sitting: 35

Sitting: 35:00 remaining
```

`-a` uses accurate `datetime.datetime` instead of `time.sleep()` for the timer.
* Since `time.sleep()` can be affected by system load and other variables, it often
results in a slight elongation of the timer.
  * If you want to test how long the delay is for your machine, you can use the `-s` 
    flag, which will show the difference between expected vs. real time delta, after
    the end of your session. Ofc this only makes sense if not using `-a`.
* With `-a` your timer will finish at exactly the time you set it to, which can be useful 
if you have a tight schedule.
* **Otherwise, it is recommended to stay at the mercy of your CPU speed, and have a slightly
longer meditation session!**

If you want to add your own posture, just edit the `POSTURES` variable in `__init__.py`.

## Good luck meditating! :)
