# -*- coding: utf-8 -*-

import re

from sneakylang import parse, Macro, Document
from sneakylang.parser import ParserRollback

from czechtile import nodes

class CzechtileMacro(Macro):

    def _macroCallWithoutRequiredQuotes(self, *args):
        content = ''.join([''.join([arg, ' ']) for arg in args])[:-1]
        return self.expand(content)

    def parse_argument_string(self, argument_string):
        self.arguments = [argument_string]

class CzechtileInlineMacro(CzechtileMacro):
    def expand_to_nodes(self, content):
        node = self.node()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class MacroWrappingParagraph(CzechtileMacro):

    def wrap_text_nodes(self, node):
        # we must go with numbers as we must replace textnode with it's tree on same position
        for child in node.children:
            if isinstance(child, nodes.TextNode):
                self.builder.set_actual_node(child)
                text = re.sub("^(\s)*", "", re.sub("(\s)*$", "", child.content))
                for para_content in text.split('\n\n'):
                    if para_content:
                        macro = Odstavec.argument_call(para_content, \
                          self.register, self.builder, self.state)
                        macro.expand()

class Book(MacroWrappingParagraph):
    name = 'kniha'
    help = '((kniha text knihy))'

    def expand_to_nodes(self, content):
        node = nodes.Book()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.wrap_text_nodes(node)
        self.builder.move_up()

class Article(MacroWrappingParagraph):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand_to_nodes(self, content):
        node = nodes.Article()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.wrap_text_nodes(node)
        self.builder.move_up()


class Sekce(Document):
    name = 'sekce'
    help = '((sekce text sekce))'

class Nadpis(CzechtileMacro):
    name = 'nadpis'
    help = '((nadpis cislo_urovne text nadpisu))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split()
        try:
            level = int(args[0])
        except ValueError, err:
            raise ParserRollback(err)

        self.arguments = [level, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, level, content):
        node = nodes.Nadpis()
        node.level = level
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        assert node == self.builder.actual_node
        self.builder.move_up()

class Odstavec(CzechtileMacro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand_to_nodes(self, content):
        node = nodes.Odstavec()
        self.builder.append(node, move_actual=False)
        if isinstance(node.parent, nodes.TextNode):
            self.builder.replace(node)
        self.builder.set_actual_node(node)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        assert node == self.builder.actual_node
        self.builder.move_up()

class NeformatovanyText(CzechtileMacro):
    name = 'neformatovany-text'
    help = '((neformatovany-text nenaformatovany obsah textu))'

    def expand_to_nodes(self, content):
        node = nodes.NeformatovanyText()
        self.builder.append(node, move_actual=True)
        tn = nodes.TextNode()
        tn.content = content
        self.builder.append(tn, move_actual=False)
        self.builder.move_up()

class Zvyraznene(CzechtileInlineMacro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'
    node = nodes.Zvyraznene

class FootNote(CzechtileInlineMacro):
    name = 'poznamka'
    help = '((poznamka text pod carou))'
    node = nodes.FootNote


class Silne(CzechtileInlineMacro):
    name = 'silne'
    help = '((silne zesilneny text))'
    node = nodes.Silne

class Hyperlink(CzechtileMacro):
    name = 'odkaz'
    help = '((odkaz http://adresa/linku text linku))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split()
        link = args[0]
        self.arguments = [link, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, link, content):
        node = nodes.Hyperlink()
        node.link = link
        self.builder.append(node, move_actual = True)
        if link == content:
            tn = nodes.TextNode()
            tn.content = content
            self.builder.append(tn, move_actual=False)
        else:
            parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()


class TriTecky(CzechtileMacro):
    name = 'tri_tecky'
    help = '((tri_tecky))'

    def expand_to_nodes(self, *args):
        self.builder.append(nodes.TriTecky(), move_actual=False)

class Trademark(CzechtileMacro):
    name = 'trademark'
    help = '((trademark))'

    def expand_to_nodes(self, *args):
        self.builder.append(nodes.Trademark(), move_actual=False)

class Copyright(CzechtileMacro):
    name = 'copyright'
    help = '((copyright))'

    def expand_to_nodes(self, *args):
        self.builder.append(nodes.Copyright(), move_actual=False)

class RightsReserved(CzechtileMacro):
    name = 'rights-reserved'
    help = '((rights-reserved))'

    def expand_to_nodes(self, *args):
        self.builder.append(nodes.RightsReserved(), move_actual=False)

class Pomlcka(CzechtileMacro):
    name = 'pomlcka'
    help = '((pomlcka))'

    def expand_to_nodes(self, string):
        node = nodes.Pomlcka()
        signals = [0, 1]
        spaces = []

        if string.startswith(u' '):
            spaces.append(signals[0])
        if string.endswith(u' '):
            spaces.append(signals[1])

        if spaces == []:
            node.spojovnik = True
        else:
            node.spojovnik = False

        if signals[0] in spaces:
            self.builder.append(nodes.PevnaMedzera(), move_actual=False)
        self.builder.append(node, move_actual=False)
        if signals[1] in spaces:
            self.builder.append(nodes.PevnaMedzera(), move_actual=False)

class Uvozovky(CzechtileInlineMacro):
    name = 'uvozovky'
    help = '((uvozovky text v uvozovkach))'
    node = nodes.Uvozovky

class List(CzechtileMacro):
    name = 'seznam'
    help = '((seznam token obsah))'

    def parse_argument_string(self, argument_string):
        self.arguments = argument_string.split(' ', 1)

    def expand_to_nodes(self, token, content):
        node = nodes.List()
        node.token = token
        self.builder.append(node, move_actual=True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        assert self.builder.actual_node == node
        self.builder.move_up()

class ListItem(CzechtileMacro):
    name = 'polozka'
    help = '((polozka text))'

    def expand_to_nodes(self, content):
        node = nodes.ListItem()
        self.builder.append(node, move_actual=True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class Preskrtnute(CzechtileInlineMacro):
    name = 'preskrtnute'
    help = '((preskrtnute preskrtnuty text))'
    node = nodes.Preskrtnute

class Obrazek(CzechtileMacro):
    name = 'obrazek'
    help = '((obrazek lokace))'

    def expand_to_nodes(self, source):
        if len(source.strip()) == 0:
            raise ParserRollback(u"Empty image source")

        node = nodes.Obrazek()
        node.source = source.strip()
        self.builder.append(node, move_actual=True)
        self.builder.move_up()

class HorniIndex(CzechtileInlineMacro):
    name = 'horni-index'
    help = '((horni-index text posazeny do horniho indexu))'
    node = nodes.HorniIndex

class DolniIndex(CzechtileInlineMacro):
    name = 'dolni-index'
    help = '((dolni-index text posazeny do dolniho indexu))'
    node = nodes.DolniIndex
