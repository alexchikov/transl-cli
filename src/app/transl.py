#!/home/aleks/PycharmProjects/cli-app/.venv/bin/python
import sys
from googletrans.client import Translator
from googletrans.client import LANGCODES, LANGUAGES

__doc__ = """\033[1m\033[33mCLI app to translate inline text\033[m

\033[3m\033[33mOptions:\033[m
    > --help: returns this message;
    > -l or --language: translation language;
    > -i or --input: input text;

\033[3m\033[33mUsage:\033[m
    \033[32mtransl -l russian -i "hello, this is an app to translate text"\033[m
"""

ALLOWED_FLAGS = {'-l': 'language', '--language': 'language', '-i': 'input', '--input': 'input',
                 "--interactive": "interactive", "--help": 'help'}
ALLOWED_LANGUAGES = LANGUAGES.values()
REQUIRED_FLAGS_STACK = ['language', 'input']


def run_interactive():
    try:
        text = input("(interactive): ")
        while text.lower() != 'exit':
            translation = t.translate(text, dest=required_language)
            print(translation.text)
            text = input("(interactive): ")
        else:
            print('\nexit')
            sys.exit(1)
    except KeyboardInterrupt:
        print('\nexit')
        sys.exit(1)


if __name__ == '__main__':
    t = Translator()
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    else:
        text, required_language = "", ""
        for i in range(0, len(args)):
            if args[i] in ALLOWED_FLAGS.keys():
                match ALLOWED_FLAGS[args[i]]:
                    case 'language':
                        if 'language' in REQUIRED_FLAGS_STACK:
                            if args[i + 1].lower() in ALLOWED_LANGUAGES:
                                required_language = args[i + 1]
                                REQUIRED_FLAGS_STACK.pop(0)
                            else:
                                print('wrong language')
                                break
                        else:
                            print("Wrong arguments!")
                            break
                    case 'input':
                        if 'input' in REQUIRED_FLAGS_STACK:
                            if i < len(args) - 1:
                                text = args[i + 1]
                                REQUIRED_FLAGS_STACK.pop(0)
                            else:
                                print('Wrong command arguments')
                                break
                        else:
                            print("Wrong arguments!")
                            break
                    case "interactive":
                        if (not REQUIRED_FLAGS_STACK) and text and required_language:
                            print("We're going to interactive mode!")
                            run_interactive()
                    case 'help':
                        print(__doc__)
                        sys.exit(0)

        if text and required_language:
            translation = t.translate(text, dest=LANGCODES[required_language.lower()])
            print(translation.text)
