import sys
import re

COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
MAX_MSG_LENGTH = 72
PREFIXES = ["Add ", "Refactor ", "Update ", "Remove ", "Disable ",
            "Release ", "Move ", "Tslint ", "Rename ", "Merge ", "Fix "]

DEFAULT = "\033[0;0m"
VIOLET = DEFAULT+'\033[35m'
BLUE = DEFAULT+'\033[34m'
CYAN = DEFAULT+'\033[36m'
GREEN = DEFAULT+'\033[32m'
YELLOW = DEFAULT+'\033[33m'
RED = DEFAULT+'\033[31m'
FILLER = '\033[;7m'
WHITE = '\033[37m'
BLACK = '\033[30m'
BLACKFONE = FILLER+'\033[30m'
WHITEFONE = FILLER+'\033[37m'
GREENFONE = FILLER+'\033[32m'
BLUEFONE = FILLER+'\033[34m'


def show_template():
    print(f"{GREEN}EXAMPLE: Refactor Z function in X file from Y component\n\
         {BLUE}<optional part, adding it leave an empty line here>\n{GREEN}\
         - Fix ...\n\
         - Add ...\n\
         - Remove ... \n{YELLOW}\n\
HINT: to read chaos-hum team rules visit: {BLUE}\
https://github.com/dimaka-wix/commit-msg-hook.git \n{DEFAULT}")


def main(argv=None):
    if argv is None:
        argv = __extract_msg()
        __extract_args()
    run_hook(argv)


def run_hook(msg):
    __validate(msg)
    __check_length(msg)
    __check_subject_line(msg)
    __check_body(msg)
    print(f"\n{GREEN}CONGRATS! Commit message matches the chaos-hub commit rules!\
            \n{DEFAULT}")


def __extract_msg():
    args = sys.argv
    if len(args) < 2:
        print(f"\n{GREEN}This hook is made as custom plugins \
under the {BLUE}https://pre-commit.com {GREEN}hook framework\n\
and checks if commit message matches the chaos-hub team commit rules\n{YELLOW}\
HINT: to read chaos-hum team rules visit {BLUE}\
https://github.com/dimaka-wix/commit-msg-hook.git \n{DEFAULT}")
        sys.exit(0)
    path = args[len(args) - 1]
    path = COMMIT_EDITMSG if path.upper() in COMMIT_EDITMSG else path
    try:
        with open(path, "r", encoding="utf-8") as msg:
            commit_msg = msg.read()
    except FileNotFoundError:
        print(f"\n{RED}ERROR: file '{path}' not found!\n{YELLOW}\
HINT:  the commit message is usually saved in {COMMIT_EDITMSG}\n{DEFAULT}")
        sys.exit(1)
    return commit_msg


def __extract_args():
    global PREFIXES
    global MAX_MSG_LENGTH
    args = sys.argv
    if len(args) > 2:
        for arg in args[1:len(args)-1]:
            decimals = re.findall(r'\d+', arg)
            if len(decimals) == 0:
                arg = (arg.strip() + " ").lstrip()
                if len(arg) > 3:
                    PREFIXES.append(arg)
            else:
                MAX_MSG_LENGTH = int(decimals[0])
    return MAX_MSG_LENGTH, PREFIXES


def __validate(input):
    if input is None or not input:
        print(f"\n{RED}ERROR: the {BLUE}`{input}` {RED}message is invalid!\n\
- commit message can't be empty!\n{DEFAULT}")
        sys.exit(1)
    if not isinstance(input, str):
        print(f"\n{RED}ERROR: the {BLUE}`{input}` {RED}message is invalid!\n\
- commit message must be a string!\n{DEFAULT}")
        sys.exit(1)


def __check_length(msg):
    msg_length = len(msg)
    if msg_length > MAX_MSG_LENGTH:
        print(f"\n{RED}ERROR: the {BLUE}`{msg.strip()}` {RED}message is invalid!\n\
- commit message is too long: {msg_length} > {MAX_MSG_LENGTH}\n{DEFAULT}")
        sys.exit(1)


def __check_subject_line(msg):
    subj = msg.splitlines()[0]
    segment = "subject line"
    __check_content(subj, segment)
    __check_prefix(subj, segment)
    if "Release" not in subj and "Merge" not in subj and "Rename" not in subj:
        __check_in_from_format(subj, segment)
    __check_ending(subj, segment)


def __check_body(msg):
    if len(msg.splitlines()) > 1:
        body = msg.splitlines()[1:]
        if body[0].strip() != "":
            print(f"\n{RED}ERROR: the {BLUE}\n`{body}` {RED} message is invalid!\n\
- separate subject from body with a blank line!\n{DEFAULT}")
            show_template()
            sys.exit(1)
        segment = "message body lines"
        for row in body[1:]:
            row = row.strip()
            row = row[1:].lstrip() if row[0] == "-" else row
            __check_content(row, segment)
            __check_prefix(row, segment)
            __check_ending(row, segment)


def __check_content(msg, segment=""):
    words = msg.strip().split()
    if len(words) < 2:
        print(f"\n{RED}ERROR: the {BLUE}`{msg}` {RED}message is invalid!\n- a \
one-word message is not informative add more details in {segment}!\n{DEFAULT}")
        show_template()
        sys.exit(1)


def __check_prefix(msg, segment=""):
    is_valid_prefix = msg.lstrip().startswith(tuple(PREFIXES))
    if msg[0].islower():
        print(f"\n{RED}ERROR: the {BLUE}`{msg}` {RED}message is invalid!\n\
- capitalise the {segment}!\n{DEFAULT}")
        show_template()
        sys.exit(1)
    if not is_valid_prefix:
        print(f"\n{RED}ERROR: the {BLUE}`{msg}` {RED}message is invalid!\n- replace \
{segment} prefix with one of the options:\n {' '.join(PREFIXES)}\n{DEFAULT}")
        show_template()
        sys.exit(1)


def __check_in_from_format(subj, segment=""):
    if "in" not in subj or "from" not in subj:
        print(f"\n{RED}ERROR: the {BLUE}`{subj}` {RED}message is invalid!\n\
- use {GREEN}in/from {RED}format in {segment} to add the place \
where the change was made (file/component)!\n{DEFAULT}")
        show_template()
        sys.exit(1)


def __check_ending(msg, segment=""):
    if msg.rstrip().endswith("."):
        print(f"\n{RED}ERROR: the {BLUE}`{msg}` {RED}message is invalid!\n\
do not end the {segment} with a period!\n{DEFAULT}")
        sys.exit(1)


if __name__ == "__main__":
    exit(main())
