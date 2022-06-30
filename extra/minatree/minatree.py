# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import re


def print_hi(name):
    debug = 1

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    fpath = "C:\\Users\\SURIKUMA\\Downloads\\Telegram Desktop\\DataExport_2021-11-22"
    fh = open(fpath + '\\' + 'result.json', "rt", encoding="utf-8")

    data = json.loads(fh.read())

    # Iterating through the json
    # list
    print(data['about'])

    for groupiter in data['chats']['list']:
        print(groupiter['name'])

        msg_count = 0

        if re.search('Telegram Group', groupiter['name']):
            print('got it')

            for msgiter in groupiter['messages']:

                if debug > 1:
                    print(msgiter['type'])

                if msgiter['type'] == 'service':
                    if debug > 1:
                        print(msgiter['action'])
                elif msgiter['type'] == 'message':
                    msg_count += 1
                    print(msgiter['text'])

        print('message count', msg_count)

    # Closing file
    fh.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
