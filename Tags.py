import string
from urllib import request


def getHTMLContent(url):
    InnerHTMLPage = request.urlopen(url)
    InnerHTML = InnerHTMLPage.read().decode()
    InnerHTMLPage.close()

    return InnerHTML


# from abc import abstractmethod
# Temporarily commented as it might be needed for other classes

HTMLElementDB = {"style": {"selfClosing": False},
                 "link": {"selfClosing": True},
                 "script": {"selfClosing": False}
                 }


class HTMLElement:
    selfClosingString = string.Template("""<${elementName}$attributes/>""")
    notSelfClosingString = string.Template("""<${elementName}$attributes>$innerHTML</$elementName>""")
    attributeString = string.Template(""" $attribute='$value'""")

    def __init__(self, elementName, selfClosing=None, attributes=None, innerHTML=""):
        """
        :type elementName: str
        :type selfClosing: bool
        :type attributes: dict
        :type innerHTML: str
        """

        self.generated = False
        self.generatedContent = None

        if selfClosing is None:
            if elementName in HTMLElementDB:
                selfClosing = HTMLElementDB[elementName]["selfClosing"]
                # Add other attributes that are needed here
            else:
                # TODO: Log here that it is assuming that it's not self closing
                selfClosing = False

        if selfClosing and innerHTML:
            ValueError("Tag cannot be self closing and have inner HTML")

        self.elementName = elementName

        if attributes is None:
            attributes = {}

        self.attributes = attributes
        self.selfClosing = selfClosing
        self.innerHTML = innerHTML

    def gen(self):
        """
        :rtype: str
        """
        if self.generated:
            return self.generatedContent

        attributesPile = ""

        for attributeName in self.attributes:
            attributesPile += self.attributeString.substitute(attribute=attributeName,
                                                              value=self.attributes[attributeName])
        if self.selfClosing:
            HTML = self.selfClosingString
            self.generatedContent = HTML.substitute(elementName=self.elementName,
                                                    attributes=attributesPile)
        else:
            HTML = self.notSelfClosingString
            self.generatedContent = HTML.substitute(elementName=self.elementName,
                                                    attributes=attributesPile,
                                                    innerHTML=self.innerHTML)

        self.generated = True
        return self.generatedContent


class Style(HTMLElement):
    def __init__(self, url, embed=False, integrity=False, external=False):
        self.generated = False
        self.generatedContent = None

        if integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

        if embed:
            # TODO: Log here that you cannot have integrity and embedding. No point
            integrity = False

            InnerHTML = getHTMLContent(url)

            super(Style, self).__init__("style", selfClosing=False, innerHTML=InnerHTML)


        else:
            attributeList = {"href": url,
                             "rel": "stylesheet"
                             }

            if integrity:
                attributeList["integrity"] = integrity
                attributeList["crossorigin"] = "anonymous"

            super(Style, self).__init__("link", selfClosing=True, attributes=attributeList)


class Script(HTMLElement):
    def __init__(self, url, embed=False, integrity=False, external=False):
        if embed:
            if integrity:
                # TODO: Log here that you cannot have integrity and embedding. No point
                integrity = False

            InnerHTML = getHTMLContent(url)

            super(Script, self).__init__("script", selfClosing=False, innerHTML=InnerHTML)

        elif integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

        else:
            super(Script, self).__init__("script", selfClosing=False, attributes={"src": url})
            # TODO: Script also needs integrity
            # TODO: Script also needs embedded scripts


class Paragraph(HTMLElement):
    def __init__(self, text):
        super(Paragraph, self).__init__("p", selfClosing=False, innerHTML=text)
