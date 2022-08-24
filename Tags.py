from Logger import getLogger
from IO import getHTMLContent, Read
from urllib import request
import hashlib
import string
import base64


localLogger = getLogger()


def generateID(text):
    return hashlib.sha512(str(text).encode()).hexdigest()


def getIntegrity(data):
    if type(data) is str:
        data = data.encode()
    elif type(data) is not bytes:
        raise ValueError("Can only digest utf-8 strings and bytes")

    # TODO: This is ugly, please fix.
    return "sha384-" + str(base64.b64encode(hashlib.sha384(data).digest()))[2:-1]


class HTMLElement:
    selfClosingString = string.Template("""<${elementName}$attributes/>""")
    notSelfClosingString = string.Template("""<${elementName}$attributes>$innerHTML</$elementName>""")
    attributeString = string.Template(""" $attribute="$value\"""")
    pattributeString = string.Template(""" $pattribute""")

    def __init__(self, elementName, selfClosing=None, attributes=None, pattributes=None, innerHTML=""):
        """
        :type elementName: str
        :type selfClosing: bool
        :type attributes: dict
        :type pattributes: list
        :type innerHTML: str
        :type innerHTML: object

        if passing an object into innerHTML, it should be able to be represented as a string.
        """

        innerHTML = str(innerHTML)

        # Inner HTML can have invalid html that needs to be removed
        # TODO: implement a full list of bad tags that cannot be inside <p> and correctly extract them
        if elementName == "p":
            badTags = ["ul", "ol"]
            for badTag in badTags:
                innerHTML = innerHTML.replace("<{}>".format(badTag), "</p><{}>".format(badTag))
                innerHTML = innerHTML.replace("</{}>".format(badTag), "</{}><p>".format(badTag))

        self.generated = False
        self.generatedContent = None

        if selfClosing is None:
            raise Exception("Self closing is not defined for tag {}".format(elementName))

        if selfClosing and innerHTML:
            ValueError("Tag cannot be self closing and have inner HTML")

        self.elementName = elementName

        if attributes is None:
            attributes = {}

        if pattributes is None:
            pattributes = []

        self.attributes = attributes
        self.selfClosing = selfClosing
        self.innerHTML = innerHTML
        self.pattributes = pattributes

    def __str__(self):
        """
        :rtype: str
        """
        if self.generated:
            return self.generatedContent

        attributesPile = ""

        for attributeName in self.attributes:
            attributesPile += self.attributeString.substitute(attribute=attributeName,
                                                              value=self.attributes[attributeName])
        for pattribute in self.pattributes:
            attributesPile += self.pattributeString.substitute(pattribute=pattribute)

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

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return str(self) + str(other)


class Style(HTMLElement):
    def __init__(self, url=None, embed=False, internalPath=None):
        self.url = url
        self.generated = False
        self.generatedContent = None
        self.internalPath = internalPath

        InnerHTML = None

        if internalPath is not None:
            InnerHTML = Read(internalPath)
        elif url is not None:
            if embed:
                InnerHTML = getHTMLContent(url)
        else:
            raise ValueError("You need to input either a url or an internal path")

        if embed:
            if InnerHTML is None:
                raise Exception("Unknown error")

            super(Style, self).__init__("style", selfClosing=False, innerHTML=InnerHTML)

        else:
            attributeList = {"href": url, "rel": "stylesheet", "crossorigin": "anonymous"}
            super(Style, self).__init__("link", selfClosing=True, attributes=attributeList)

    def getResourceInfo(self):
        if self.url is None:
            return self.internalPath
        else:
            return self.url


class Script(HTMLElement):
    def __init__(self, url=None, embed=False, integrity=False, internalPath=None):
        self.generated = False
        self.generatedContent = None
        self.url = url
        self.internalPath = internalPath

        if embed and integrity:
            localLogger.warning("It's impossible to embed and have integrity checks. Disabling integrity checking")
            integrity = False

        data = None
        if internalPath is not None:
            data = Read(internalPath)
            localLogger.debug("Generating local for: " + internalPath)
        elif url is not None:
            if embed or integrity:
                data = getHTMLContent(url)
        else:
            raise ValueError("You need to input either a url or an internal path")

        if not embed:
            attributes = {"src": url}
            localLogger.debug("Generated for URL: " + url)
            if integrity:
                attributes["integrity"] = getIntegrity(data.encode())
                attributes["crossorigin"] = "anonymous"

            super(Script, self).__init__("script", selfClosing=False, attributes=attributes)
        else:
            super(Script, self).__init__("script", selfClosing=False, innerHTML=data)

    def getResourceInfo(self):
        if self.url is None:
            return self.internalPath
        else:
            return self.url


class NoScript(HTMLElement):
    def __init__(self, text, attributes=None):
        super(NoScript, self).__init__("noscript", selfClosing=False, innerHTML=text, attributes=attributes)


class Paragraph(HTMLElement):
    def __init__(self, text, attributes=None):
        super(Paragraph, self).__init__("p", selfClosing=False, innerHTML=text, attributes=attributes)


class Div(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Div, self).__init__("div", selfClosing=False, innerHTML=text, attributes=attributes)


class Article(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Article, self).__init__("article", selfClosing=False, innerHTML=text, attributes=attributes)


class Section(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Section, self).__init__("section", selfClosing=False, innerHTML=text, attributes=attributes)


class Header(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Header, self).__init__("header", selfClosing=False, innerHTML=text, attributes=attributes)


class Hx(HTMLElement):
    def __init__(self, level, text="", attributes=None):
        """
        :type level: int
        level can be 1,2,3,4,5,6
        """
        if level > 6 or level < 1:
            ValueError("tag h" + str(level) + " doesn't exist.")

        super(Hx, self).__init__("h" + str(level), selfClosing=False, innerHTML=text, attributes=attributes)


class Body(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Body, self).__init__("body", selfClosing=False, innerHTML=text, attributes=attributes)


class Main(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Main, self).__init__("main", selfClosing=False, innerHTML=text, attributes=attributes)


class Nav(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Nav, self).__init__("nav", selfClosing=False, innerHTML=text, attributes=attributes)


class Image(HTMLElement):
    def __init__(self, url, attributes=None):  # Support embedding
        if attributes is None:
            attributes = {}

        attributes["src"] = url

        super(Image, self).__init__("img", selfClosing=True, attributes=attributes)


class Figure(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Figure, self).__init__("figure", selfClosing=False, innerHTML=text, attributes=attributes)


class FigCaption(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(FigCaption, self).__init__("figcaption", selfClosing=False, innerHTML=text, attributes=attributes)


class FigureImageCombo(Figure):
    def __init__(self, imageURL, imageSubtext, imageAttributes=None, imageSubtextAttributes=None, attributes=None):
        image = Image(imageURL, attributes=imageAttributes)
        figureText = FigCaption(text=imageSubtext, attributes=imageSubtextAttributes)
        super(FigureImageCombo, self).__init__(text=image + figureText, attributes=attributes)


class Title(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Title, self).__init__("title", selfClosing=False, innerHTML=text, attributes=attributes)


class Meta(HTMLElement):
    def __init__(self, attributes=None):
        super(Meta, self).__init__("meta", selfClosing=True, attributes=attributes)


class Head(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Head, self).__init__("head", selfClosing=False, innerHTML=text, attributes=attributes)


class Link(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Link, self).__init__("link", selfClosing=True, innerHTML=text, attributes=attributes)


localLogger.debug("Phrased Tags.py fully")
