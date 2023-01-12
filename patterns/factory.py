class GreekLocalizer:

    def __init__(self) -> None:
        self.translations = {"dog": "σκύλος", "cat": "γάτα"}

    def localize(self, msg: str) -> str:
        return self.translations.get(msg, msg)


class EnglishLocalizer:

    def localize(self, msg: str) -> str:
        return msg


def get_localizer(language: str = "English") -> object:

    localizers = {
        "English": EnglishLocalizer,
        "Greek": GreekLocalizer,
    }

    return localizers[language]()


def main():

    e = get_localizer(language="English")
    g = get_localizer(language="Greek")

    for msg in "dog parrot cat bear".split():
        print(e.localize(msg), g.localize(msg))


if __name__ == "__main__":
    main()
