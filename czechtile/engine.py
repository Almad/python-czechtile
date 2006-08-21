# -*- coding: utf-8 -*-

""" Main wiki engine.
 """

###
#RpgWiki: Fuel for your wiki
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
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
###

# CODE:


# POMOCNE FUNKCIE
# ---------------

def _strong(text):
    czech = text
    helper = ""
    a = 0
    var = [0]
    i = 0
    counter = 0
    while a < (len(text) - 1):
        b = a + 1
        if text[a] == "*" and text[b] == "*":
            c = b + 1
            while c < (len(text) - 1):
                d = c + 1
                if text[c] == "*" and text[d] == "*":
                    counter += 1
                    i += 1
                    var.append(a)
                    if i > 2:
                        helper += text[var[i - 1]:var[i]] 
                    helper += "<strong>"
                    helper += text[b + 1:c]
                    helper += "</strong>"
                    if c < len(text):
                        i += 1
                        var.append(d + 1)
                        a = var[i] - 1
                    break
                c += 1
            else:
                break
                
        a += 1
    
    if helper != "":
        czech = text[:var[1]]
        czech += helper
        czech += text[var[i]:]
    return czech


def _headings(text):
    czech = text
    helper = ""
    a = 0
    var = [0]
    i = 0
    counter = 0
    while a < (len(text) - 4):
        b = a + 1
        c = a + 2
        d = a + 3
        if text[a] == "=" and text[b] == "=" and text[c] == "=" and \
          text[d] == " ":
            e = d + 1
            while e < (len(text) - 3):
                f = e + 1
                g = e + 2
                h = e + 3
                if text[e] == " " and text[f] == "=" \
                  and text[g] == "=" and text[h] == "=":
                    counter += 1
                    i += 1
                    var.append(a)
                    if i > 2:
                        helper += text[var[i - 1]:var[i]] 
                    helper += "<h4>"
                    helper += text[d + 1:e]
                    helper += "</h4>"
                    i += 1
                    var.append(h + 1)
                    a = var[i] - 1
                    break
                e += 1
            else:
                break

        elif text[a] == "=" and text[b] == "=" and text[c] == " ":
            d = c + 1
            while d < (len(text) - 2):
                e = d + 1
                f = d + 2
                if text[d] == " " and text[e] == "=" and text[f] == "=":
                    counter += 1
                    i += 1
                    var.append(a)
                    if i > 2:
                        helper += text[var[i - 1]:var[i]] 
                    helper += "<h3>"
                    helper += text[c + 1:d]
                    helper += "</h3>"
                    i += 1
                    var.append(f + 1)
                    a = var[i] - 1
                    break
                d += 1
            else:
                break

        elif text[a] == "=" and text[b] == " ":
            c = b + 1
            while c < (len(text) - 1):
                d = c + 1
                if text[c] == " " and text[d] == "=":
                    counter += 1
                    i += 1
                    var.append(a)
                    if i > 2:
                        helper += text[var[i - 1]:var[i]] 
                    helper += "<h2>"
                    helper += text[b + 1:c]
                    helper += "</h2>"
                    i += 1
                    var.append(d + 1)
                    a = var[i] - 1
                    break
                c += 1
            else:
                break
        
                
        a += 1
    
    if helper != "":
        czech = text[:var[1]]
        czech += helper
        czech += text[var[i]:]
    return czech


        



def _zoznam(text):
    helper = ""
    czech = text 
    a = 0
    counter = 0
    var = [0]
    i = 0
    cont = 0
    nested = 0
    while a < (len(text) - 3):
        if text[a] == " " and text[a + 1] == "-" and text[a + 2] == " ":
            counter += 1
            if counter == 1:
                i += 1            
                var.append(a)
                if i > 2:
                    helper += text[var[i - 1]:var[i]]
                helper += "<ul>\n"
            text += "\n"
            x = text[a + 2:].index("\n") + (a + 2)
            helper += "<li>"
            helper += text[a + 2 + 1:x]
            helper += "</li>\n"
            if x < (len(text) - 3):
                if text[x + 1] != " " or text[x + 2] != "-" \
                  or text[x + 3] != " ":
                    helper += "</ul>"
                    i += 1
                    var.append(x)
                    counter = 0                    
                    cont = 1
            elif x == (len(text) - 1):
                helper += "</ul>"
                counter = 0
                cont = 0
            else:
                helper += "</ul>"
                counter = 0
                cont = 1
                i += 1
                var.append(x)
            text = text[:len(text) - 1]

        elif text[a] == "1" and text[a + 1] == "." and text[a + 2] == " ":
            counter += 1
            if counter == 1:
                i += 1            
                var.append(a)
                if i > 2:
                    helper += text[var[i - 1]:var[i]]
                helper += "<ol>\n"
            text += "\n"
            x = text[a + 2:].index("\n") + (a + 2)
            helper += "<li>"
            helper += text[a + 2 + 1:x]
            helper += "</li>\n"
            if x < (len(text) - 4):
                if text[x + 1] == " " and text[x + 2] == " " \
                  and text[x + 3] == "-" and text[x + 4] == " ":
                    nested = 1
                    counter = 0
                elif text[x + 1] != "1" or text[x + 2] != "." \
                  or text[x + 3] != " ":
                    helper += "</ol>"
                    i += 1
                    var.append(x)
                    counter = 0                    
                    cont = 1
            elif x == (len(text) - 1):
                helper += "</ol>"
                counter = 0
                cont = 0
            else:
                helper += "</ol>"
                counter = 0
                cont = 1
                i += 1
                var.append(x)
            text = text[:len(text) - 1]

        if nested == 1:
            if text[a] == " " and text[a + 1] == " " \
              and text[a + 2] == "-" and text[a + 3] == " ":
                counter += 1
                if counter == 1:
                    helper += "<ul>\n"
                text += "\n"
                x = text[a + 3:].index("\n") + (a + 3)
                helper += "<li>"
                helper += text[a + 3 + 1:x]
                helper += "</li>\n"
                if x < (len(text) - 4):
                    if text[x + 1] != " " or text[x + 2] != " " \
                      or text[x + 3] != "-" or text[x + 4] != " ":
                        helper += "</ul>\n"
                else:
                    helper += "</ul>\n"
 
                text = text[:len(text) - 1]
            
            
        text += "\n"
        b = a
        a = text[b:].index("\n") + b + 1        
        text = text[:len(text) - 1]
    
    if helper != "":
        czech = text[:var[1]]
        czech += helper
        if cont == 1:
            czech += text[var[i]:]

    return czech



# HLAVNA FUNKCIA transform()
# --------------------------

def transform(wikiText):
    """ Simple transformation from Czechtile text to HTML."""

    czechtile = _strong(wikiText)
    czechtile = _headings(czechtile)
    czechtile = _zoznam(czechtile)
    
    return czechtile

# - Andros
