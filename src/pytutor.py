from supermemo2 import SMTwo
from argparse import ArgumentParser
from subprocess import run
from json import loads, dumps, JSONEncoder
from datetime import datetime, time
from pathlib import Path


class C:
    '''Class for holding terminal colors'''

    CYAN = '\033[1;96m'
    SAFE = '\033[1;92m'
    WARN = '\033[1;93m'
    RED = '\033[1;91m'
    ENDC = '\033[0m'


class DateTimeEncoder(JSONEncoder):
    '''JSON encoder to stringify dates'''

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()


def datetimeDecoder(x):
    '''JSON decoder to parse date strings'''

    if 'review_dt' in x and not x['review_dt'] is None:
        x['review_dt'] = datetime.fromisoformat(x['review_dt'])

    return x


def fmtQuestion(ques, referFile, data):
    '''return the formatted question string with terminal colors applied.'''

    question = f'Q. {ques}\n\n'
    question += f'File: data/{referFile}\n{data}\nExpected Output:\n{expected}'
    return C.CYAN + question + C.ENDC


def fmtShowAns(ans):
    '''Return the formatted answer string with terminal colors applied.'''

    print(f'Ans: {C.SAFE}{ans}{C.ENDC}')


def fmtSucess(cmd):
    '''Return the formatted success string with terminal colors applied.'''

    hr = ('-' * 30) + '\n'
    out = f'{C.WARN}Our Answer: {cmd}\n{C.SAFE}Correct ✔{C.ENDC}\n{hr}'
    print(out)


def fmtFail(output):
    '''Return the formatted failure string with terminal colors applied.'''

    return f'{C.RED}{output}{C.ENDC}\nNot quite there, try again{prompt}'


def getQuestionCount(data):
    '''Returns the total questions to be reviewed in the current session
    based on the review date'''

    return sum(x['review_dt'] is None or x['review_dt'] <= today for x in data)


def execCmd(cmd):
    '''Execute the cmd in the shell and return the output or error string'''

    out = run(cmd, capture_output=True, shell=True)

    return (out.stdout or out.stderr).decode()


def assignRating(quality, data) -> SMTwo:
    '''Returns an instance of SMTwo used to determine the next review date'''

    if data['easiness'] is None:
        return SMTwo.first_review(quality)
    else:
        easiness, interval, repetitions, dt, *_ = data.values()
        return SMTwo(easiness, interval, repetitions).review(quality, dt)


def checkQuestionCount(count, start=False):
    '''Print status of questions remaining'''

    if start:
        return print(f'{C.SAFE}Total: {count} questions{C.ENDC}')

    if count == 0:
        return print(f'{C.SAFE}Done.{C.ENDC}')

    return print(f'{C.SAFE}{count} remaining{C.ENDC}')


DIR = Path(__file__).parent
QA_DIR = DIR / 'qa'

moduleList = tuple(f.name[:-5] for f in QA_DIR.iterdir())

parser = ArgumentParser(
    prog='pytutor.py',
    description='A python tutor to recap usage of linux command line tools.')

parser.add_argument('-m', '--module',
                    action='store',
                    choices=moduleList,
                    help='Load module by name.')

parser.add_argument('-r', '--reset',
                    action='store',
                    choices=moduleList,
                    help='Reset Module to begin fresh.')

args = parser.parse_args()

# Reset the module to default
if args.reset:
    QA_FILE = QA_DIR / f'{args.reset}.json'
    qa = loads(QA_FILE.read_bytes())

    for dct in qa['questions']:
        dct['easiness'] = None
        dct['interval'] = None
        dct['repetitions'] = None
        dct['review_dt'] = None

    QA_FILE.write_text(dumps(qa, indent=3, cls=DateTimeEncoder))
    exit(f'Module {args.reset.upper()} has been reset.')


# Load Module
if args.module is None:
    moduleList = '\n'.join(moduleList)
    moduleName = input(f'Enter Module to load:\n{moduleList}\n$ ')
    modulePath = QA_DIR / f'{moduleName}.json'
else:
    modulePath = QA_DIR / f'{args.module}.json'

fmt = '%Y-%m-%d'
today = datetime.combine(datetime.today(), time(0, 0))

# load questions
qna = loads(modulePath.read_bytes(), object_hook=datetimeDecoder)

# load data file to supplement questions
referFile = qna['meta']['referFile']
data = (DIR / 'data' / referFile).read_text()

nextReview = qna['meta']['review_dt']

if not nextReview is None and nextReview > today:
    exit(f'{C.SAFE}Nothing for Today :)\nNext Review: {nextReview:%d %b %Y}{C.ENDC}')

# reset nextReview to None
# after 1st answer, new review date will be assigned
nextReview = None
prompt = '\n$ '

failedAnswer = '\nType "next" to continue or Ctrl - C to exit\n$ '

qCount = getQuestionCount(qna['questions'])

checkQuestionCount(qCount, start=True)


try:
    for qNo, q in enumerate(qna['questions']):

        if not q['review_dt'] is None and q['review_dt'] > today:
            continue

        qCount -= 1

        # execute the command provided in the answer to get the expected output
        expected = execCmd(q['a'])

        # We start with 5 and minus 1 for every wrong answer.
        # Asking for help will immediately reduce quality to 1.
        # Quality is passed as an input to SMTwo to calculate review dates
        quality = 5

        ques = fmtQuestion(q['q'], referFile, data)

        # ask the question
        userAns = input(ques + prompt)

        # loop until max tries or correct answer or user requests help
        while True:

            if userAns == 'help':
                quality = 1
                fmtShowAns(q['a'])
                break

            output = execCmd(userAns)

            if output == expected:
                fmtSucess(q['a'])
                break

            quality -= 1

            if quality <= 1:
                fmtShowAns(q['a'])
                break

            userAns = input(fmtFail(output))

        r = assignRating(quality, q)

        qna['questions'][qNo]['easiness'] = r.easiness
        qna['questions'][qNo]['interval'] = r.interval
        qna['questions'][qNo]['repetitions'] = r.repetitions
        qna['questions'][qNo]['review_dt'] = r.review_date

        # Get the earliest date on which user must review this module
        # save it in qna['meta'] for later reference
        if nextReview is None:
            nextReview = r.review_date
        elif r.review_date < nextReview:
            nextReview = r.review_date
            qna['meta']['nextReview'] = r.review_date

        modulePath.write_text(dumps(qna, indent=3, cls=DateTimeEncoder))

        if quality == 1:
            if qCount > 0:
                input(failedAnswer)

            checkQuestionCount(qCount)
            continue

        checkQuestionCount(qCount)

except KeyboardInterrupt:
    exit('\nExiting application')

print(f'{C.SAFE}Next Review: {nextReview:%d %b %Y}{C.ENDC}')
