from pycountry import languages


def getLangDict():
    langdict = {}
    for lang in languages:
        langdict[lang.alpha_3] = lang.name
    return langdict


def getAvailableLanguages(messageLocation):
    availableLanguages = []
    for langcode in getLangDict():
        try:
            open(messageLocation.format(langcode), 'r')
            availableLanguages.append(langcode)
        except (OSError, IOError):  # https://stackoverflow.com/a/15032444
            pass
    return availableLanguages
