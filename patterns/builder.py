class HtmlBuilder:
    def __init__(self, root_name: str):
        self.root_name = root_name
        self.__root = HtmlElement(root_name)

    def add_child(self, name: str, text: str = ''):
        self.__root.elements.append(HtmlElement(name, text))
        return self

    def __str__(self):
        return str(self.__root)


class HtmlElement:

    def __init__(self, name: str, text: str = ''):
        self.name = name
        self.text = text
        self.elements = []

    def __str__(self):
        return self.name + "".join(str(i) for i in self.elements)

    @staticmethod
    def create(name: str) -> HtmlBuilder:
        return HtmlBuilder(name)


def main():
    el = HtmlElement.create("H1")
    el.add_child("DIV").add_child("P", "text")

    print(el)


if __name__ == "__main__":
    main()




