# -*- coding: utf-8 -*-

""" Czechtile: WikiHezky Cesky
Set Nodes
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

from sneakylang import Node

class Document(Node): pass

class Book(Node): pass
class Article(Node): pass
class Sekce(Node):pass

class Nadpis(Node):pass

class Odstavec(Node):pass

class Silne(Node):pass
class Zvyraznene(Node):pass
class Hyperlink(Node): pass

class TriTecky(Node): pass

class List(Node): pass
class ListItem(Node): pass