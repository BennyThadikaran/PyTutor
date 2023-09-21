# PyTutor
A python tutor (Quiz app) script to quickly recap usage of Linux command line tools.

Currently it supports [awk](https://www.gnu.org/software/gawk/manual/gawk.html) and [sed](https://www.gnu.org/software/sed/manual/sed.html) command line tools. More could be added in future.

The goal of this program is to practice and maintain your skills with awk and sed. It does not teach awk, sed or programming logic. It does cover the most essential features of both programs.

![pytutor interface](https://res.cloudinary.com/doyu4uovr/image/upload/s--rQKw5F6k--/f_auto/v1695317005/pytutor/pytutor-interface_aq8vt3.png)

It uses [spaced repetition learning](https://en.wikipedia.org/wiki/Spaced_repetition) technique to speed up learning. This is implemented with [SuperMemo2](https://github.com/alankan886/SuperMemo2) python package.

- On first attempt, you must answer all the questions in the module.
- You have 4 attempts to answer each question after which the correct answer is displayed.
- You can type **`help`** at any time to see the correct answer and continue to next question.
- A date is assigned to each question based on difficulty (number of attempts to answer). At the end, you are assigned a date for next review.

Questions answered on first attempt are asked less frequently. Questions which required help or multiple attempts will be asked more often till the user begins to master it.

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

**To load a module directly**, use the `-m` option followed by the module name

`python3 pytutor.py -m sed`

**To reset the review dates and start fresh**, use `-r` followed by module name to be reset.

`python3 pytutor.py -r awk`

**Cheatsheet reference for [AWK](https://quickref.me/awk) and [SED](https://quickref.me/sed)**


# How it works
The QnA modules for `awk` and `sed` are stored in `src/qa` folder as json files.

`src/data` folder contains reference files used by the QnA modules to answer the questions.

```json
{
   "meta": {
      "referFile": "emp.data",
      "review_dt": "2022-10-06"
   },
   "questions": [
      {
         "easiness": null,
         "interval": null,
         "repetitions": null,
         "review_dt": null,
         "q": "Print every line",
         "a": "awk '{ print }' data/emp.data"
      }
  ]
}
```
`questions` is a list of QnA dictionaries. QnA dictionary has keys `q` for the question and `a` for the stored answer.

- When a question is loaded, both the user's answer and the stored answer is executed in a command shell. If the output matches, the user has answered correctly.
- Every answer starts with 5 points for quality. With 1 point deducted for every wrong answer.
- You have 4 attempts to answer the question after which the correct answer is displayed.
- Using help will assign the lowest quality of 1.
- The quality points are used by superMemo2 to assess the difficulty of the question and calculate the next review date for the question.

The earliest review date for all the questions is stored in the json file under `meta` with key `review_dt`.

# IMPORTANT NOTE
The answers you submit and the answers in the json file are both directly executed on the command line. 
