from json import loads

from jsoni18n.languages import getAvailableLanguages


def getMessages(language, messagefiles):
    availableLangCodes = getAvailableLanguages(messagefiles)
    with open(messagefiles.format('eng'), 'r') as messagefileeng:
        messages = loads(messagefileeng.read())
        if language in availableLangCodes:
            if language != 'eng':
                with open(messagefiles.format(language), 'r') as messagefilelangs:
                    filedata = loads(messagefilelangs.read())
                    for message in filedata.keys():
                        messages[message] = filedata[message]
        else:
            raise ValueError("Language is not available")
    return messages
