# -*- coding: utf-8 -*-

""" Parsers
"""

__version__ = 0.1

###
#Czechtile: WikiHezkyCesky
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

from sneakylang import Parser
import macros

class Document(Parser):
    start = None
    macro = macros.Document

    def resolveContent(self):
        self.content = self.stream
        self.stream = ''
        self.args = self.content

class Book(Document):
    start = None
    macro = macros.Book
    end = ''

class Article(Document):
    start = None
    macro = macros.Article

class Sekce(Document):
    start = None
    macro = macros.Sekce

class Odstavec(Parser):
    start = ['^(\n){2}$']
    end = ['^(\n){2}$']
    macro = macros.Odstavec

class Silne(Parser):
    start = ['^("){3}$']
    end = ['^("){3}$']
    macro = macros.Silne

class Zvyraznene(Parser):
    start = ['^("){2}$']
    end = ['^("){2}$']
    macro = macros.Zvyraznene

class Nadpis(Parser):
    start = ['^(=){1,5}$']
    end = ['^(=){1,5}$']
    macro = macros.Nadpis