# pytutor
A python tutor (Quiz app) script to quickly recap usage of Linux command line tools.

It uses [spaced repetition learning](https://en.wikipedia.org/wiki/Spaced_repetition) technique to speed up learning. This is implemented with [SuperMemo2](https://github.com/alankan886/SuperMemo2) python package.

Currently it supports [awk](https://www.gnu.org/software/gawk/manual/gawk.html) and [sed](https://www.gnu.org/software/sed/manual/sed.html) command line tools. More could be added in future.
# SETUP
PyTutor requires python version >= 3.7 and works only on Linux platform currently. (Could work with WSL on Windows - not tested yet)

**Clone the repository**

`git clone https://github.com/BennyThadikaran/pytutor.git`

**Setup venv (Optional step)**

```bash
python3 -m venv pytutor
source bin/activate
```

**Install dependencies**

```bash
cd pytutor`
pip3 install -r requirements.txt
```

# Usage
```bash
cd src
python3 pytutor.py
```

pytutor has a command line interface. You can use `-h` to access help.
```bash
$ python3 pytutor.py -h
usage: pytutor.py [-h] [-m {awk,sed}] [-r {awk,sed}]

A python tutor to recap usage of linux command line tools.

options:
  -h, --help            show this help message and exit
  -m {awk,sed}, --module {awk,sed}
                        Load module by name.
  -r {awk,sed}, --reset {awk,sed}
                        Reset Module to begin fresh.
```
