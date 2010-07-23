# -*- coding: utf-8 -*-

""" Czechtile: WikiHezky Cesky
Set Nodes
"""

from sneakylang.document import DocumentNode
from sneakylang.node import Node, TextNode

class Book(Node): pass
class Article(Node): pass
class Sekce(Node): pass

class Nadpis(Node): pass

class Odstavec(Node): pass
class NeformatovanyText(Node): pass
class ZdrojovyKod(Node): pass

class Silne(Node): pass
class Zvyraznene(Node): pass
class Preskrtnute(Node): pass
class Hyperlink(Node): pass

class TriTecky(Node): pass
class Pomlcka(Node): pass
class Trademark(Node): pass
class Copyright(Node): pass
class RightsReserved(Node): pass
class NovyRadek(Node): pass

class List(Node): pass
class ListItem(Node): pass

class FootNote(Node): pass
class HorniIndex(Node): pass
class DolniIndex(Node): pass

class Uvozovky(Node): pass
class PevnaMedzera(Node): pass

class Obrazek(Node): pass
