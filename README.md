# Support Scripts for the Speed of Recognition of Environmental Sound Sources study

Scripts to support experimental study carried out in [The Department of Sound Engineering](http://www.chopin.edu.pl/en/departments-of-the-university/sound-engineering/) of [Fryderyk Chopin University of Music](http://www.chopin.edu.pl/). The objective of the study was to measure listener’s reaction time in the recognition of the sources of environmental sounds embedded in various acoustic sceneries. The secondary objective of the study was to determine whether people with musical (hearing training) education background recognize the sounds faster than non-musicians and whether the sound recognition reaction time is influenced by the congruency of the sound and the scenery in which the sound is presented.

## Input & the goal

The study produces two tracks of recorded audio files: one with recorded prompts that were played over ambient acoustic scenery (**prompts**) other with recorded audio file of listeners' responses naming the prompts (**responses**). The experiment needs tagging of both & measuring the time distance between appropriate prompts & responses and the cognition's accuracy.

## Baseline

Each file has to be listened by auditor and appropriate tags have to be placed around prompts & responses. This takes huge amount of time.

## Better solution

Process both **prompts** & **responses** audio files with software to identify as much information as possible.

## Tagging script (wav2time.py)

### Information

The script does three things: traces prompts audio file & inserts tags to mark prompt's occurrence, traces responses audio file & tags all answers, does speech recognition to eliminate non-valid answers in the survey recording.

**Requirements:** python 3.5+, [sox](http://sox.sourceforge.net/sox.html) binary in path, python libraries: [wave](https://docs.python.org/3/library/wave.html), [audioop](https://docs.python.org/2/library/audioop.html) and [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/).

### Usage

Script requires one parameter: a name of the prompts audio file:

```bash
python wav2time.py data/efekty-11_24_1033.wav
```

### Output

The output result is a [Audacity](http://www.audacityteam.org/) acceptable labels format, an UTF-8 text file containing three columns: *beginning of the tag* (in seconds), *end of the tag*  (in seconds), *class* (`prompt #` or `answer #`) combined with *recognized response*:

```
0.875011	2.746757	prompt #1:
8.503673	10.378413	prompt #2:
17.558095	19.543583	prompt #3:
1.594376	2.418503	answer #1: telefon
9.060408	10.009252	answer #2: gwizdek
18.804263	19.800000	answer #3: chodzenie
```

The name of the output file in the example would be:

```bash
data/etykiety-in-11_24_1033.txt
```

The file is [Audacity](http://www.audacityteam.org/) acceptable labels format.

## Results calculation script (time2csv.py)

The script takes the output of the middle stage of the workflow, reviewed tags from Audacity and calculates delay between appropriate prompts and answers & outputs it in the form of CSV table.

**Requirements:** Python 3.5+.

### Usage

Script requires one parameter: a name of the audited tags file:

```bash
python time2csv.py data/etykiety-out-11_24_1033.txt
```

### Output

The name of the output file in the example would be:

```bash
data/etykiety-in-11_24_1033.csv
```

And the contents in the above example would be (also see Workflow below):

```
Id [#];Delay [ms];Prompt [txt];Answer [txt];Match [bool];Notes [txt]
#1;719;telefon;telefon;YES;
#2;556;gwizdek;gwizdek;YES;
#3;1246;kroki;kroki;YES;
```

## Workflow

### 1. Run tagging script

```bash
python wav2time.py data/efekty-11_24_1033.wav
```

### 2. Audit tags in Audacity

![Alt text](/media/screenshot-1.png?raw=true "Optional Title")

Adjust tags placement (rarely required) and prompt/answer codes.

![Alt text](/media/screenshot-2.png?raw=true "Optional Title")

Export audited labels to a text file.

### 3. Run results calculation script

```bash
python time2csv.py data/etykiety-out-11_24_1033.txt
```

The result is a CSV file ready for opening in other software and analysis.

## Savings

In practical tests scripts save over 50% of time required to produce the labels suitable for calculating the required delays. The whole fun is the step which does speech recognition as it could potentially automate the process nearly in full once the emission log is available.

## Possible Improvements

Accurate log of prompts' emissions could automate nearly everything. Simple look-up table of responses ("kroki": "chodzenie", "obcasy", ...) could allow the system to skip prompts' identification workflow step and match responses to prompts reliably without any human intervention.