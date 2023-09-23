# PyTutor

A Python tutor (Quiz app) to quickly review usage of Linux command line tools.

It supports [AWK](https://www.gnu.org/software/gawk/manual/gawk.html) and [Sed](https://www.gnu.org/software/sed/manual/sed.html) commands, with plans to add more soon.

The goal is to practice and maintain your skills. It does not teach AWK, Sed, or programming logic. It does cover the most essential features of both programs.

![pytutor interface](https://res.cloudinary.com/doyu4uovr/image/upload/s--rQKw5F6k--/f_auto/v1695317005/pytutor/pytutor-interface_aq8vt3.png)

It uses [spaced repetition learning](https://en.wikipedia.org/wiki/Spaced_repetition) to speed up learning. It uses the SM2 algorithm implemented with the [SuperMemo2](https://github.com/alankan886/SuperMemo2) python package.

- On the first attempt, you must answer all the questions in the module.
- You have 4 chances to answer the question before the correct answer is displayed.
- You can type **`help`** any time to see the correct answer and continue to the next question.
- Each question is assigned a date based on difficulty (Number of attempts to answer). On completion, you receive the next review date.
- Set a reminder on your calendar to run this program again and refresh your memory.

Questions answered on the first attempt appear less frequently. Questions that require help or multiple attempts get asked more often till the user begins to master them.

# SETUP

PyTutor requires Python version >= 3.7 and works only on Linux. (Could work with WSL on Windows - not tested yet)

**Clone the repository**

`git clone https://github.com/BennyThadikaran/PyTutor.git`

**Setup venv (Optional step)**

```bash
python3 -m venv PyTutor
source bin/activate
```

**Install dependencies**

```bash
cd PyTutor`
pip3 install -r requirements.txt
```

# Usage

```bash
cd src
python3 pytutor.py
```

PyTutor has a command line interface. You can use `-h` or `--help` to access help.

```bash
$ python3 pytutor.py -h
usage: pytutor.py [-h] [-m {awk,sed}] [-r {awk,sed}]

A Python tutor to recap usage of Linux command line tools.

options:
  -h, --help            show this help message and exit
  -m {awk,sed}, --module {awk,sed}
                        Load module by name.
  -r {awk,sed}, --reset {awk,sed}
                        Reset the Module to begin fresh.
```

**To load a module directly**, use the `-m` or `--module` option followed by the module name

`python3 pytutor.py -m sed`

**To reset the review dates and start fresh**, use `-r` or `--reset` followed by the module name.

`python3 pytutor.py -r awk`

# Answering the questions

Type the answer as you would execute the program in the command line.

`awk '{ print }' data/emp.data`

If unsure of the answer, type `help` and hit enter to view the suggested solution. (There may be multiple ways to answer the same question.)

You can also write the awk program in a file and execute it in the script. PyTutor only compares the output of the program, not the actual command.

`awk -f test.awk data/emp.data`

# How it works

The Q&A modules for `AWK` and `Sed` are JSON files in the `src/qa` folder.

`src/data` folder contains reference files used by the Q&A modules to answer the questions.

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

`questions` are a list of Q&A dictionaries. Q&A dictionary has keys `q` for the question and `a` for the stored answer.

- The answer provided by the user and the stored answer are both executed in a command shell. If the output matches, the user has answered correctly.
- Every answer starts with 5 points for quality. With 1 point deducted for every wrong answer.
- You have 4 chances to answer the question before the correct answer is displayed.
- Using help will assign the lowest quality of 1.
- SuperMemo2 uses the quality points to assess the difficulty of the question and calculate the next review date for the question.

The earliest review date for all the questions gets saved to the JSON file under `meta` with key `review_dt`.

# Learning Resources

### Sed

- [Sed Guide](https://www.grymoire.com/Unix/Sed.html#uh-0)
- [Sed Cheatsheet](https://quickref.me/sed)

### AWK

- [AWK Guide](https://www.grymoire.com/Unix/Awk.html#uh-0)
- [Sed Cheatsheet](https://quickref.me/awk)

# IMPORTANT NOTE

The answers you submit and the answers in the JSON file are both directly executed on the command line.

For example, an answer like `rm somefile.txt` will delete that file on your system.

When answering questions or creating a Q&A module, keep this in mind.
