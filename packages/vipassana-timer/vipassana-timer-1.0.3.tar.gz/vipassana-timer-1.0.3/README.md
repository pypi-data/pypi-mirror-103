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
usage: meditate [-h] [times]

Simple vipassana meditation timer

positional arguments:
  times                 Times for each meditation posture (format: 'p5w30s30')

optional arguments:
  -h, --help            show this help message and exit

```

The script takes inputs for the three postures: prostration, walking, and sitting -
represented by the letters 'p', 'w', 's', each followed by the desired time, in minutes.

For example, if one wanted to do 10 minutes walking and 10 sitting:
```sh
# example usage
>meditate w10s10

#or
>meditate
Enter times (format: 'p5w30s30'): w10s10

#result

Times:
Walking: 10
Sitting: 10

Walking: 10:00 remaining
```

Or, to do 35 minutes of sitting:
```sh
>meditate s35

Times:
Sitting: 35

Sitting: 35:00 remaining
```


If you want to add your own posture, just edit the `POSTURES` variable in `__init__.py`.

## Good luck meditating! :)
