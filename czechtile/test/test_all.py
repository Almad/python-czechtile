#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main
from czechtile import *

from module_test import *

#logging.basicConfig(level=logging.DEBUG)

class TestAll(OutputTestCase):

    def testAll(self):

        string = '''=  Plány programů a akcí =

 - každý za svůj program zpracuje """koncepci""", která bude sloužit k lepšímu plánování - cíle tohoto roku, konkrétní aktivity, průběh tohoto roku
 - zaměřit na možnost """zapojení dobrovolníků""" - nabídka konkrétních činností
 - bude propráno a mozkovybouřeno na příští poradě
 - """vytvořit sekci na brontowebu""" - nabídník nárazové i dlouhodobé věci, vyčlenit novou pro sponzory, konkrétní nabídky, co jim může naše činnost dát

= WWW Stránky =

 - otázka bannerů
 - zprávy z kanceláře
 - článek o přestěhování kanclu do aktualit, upravit mapu, celkově projít celý web a zkontrolovat
 - kontaktovat webmastery ostatních portálů a informovat je o změně a zařídit
 - představení článků - texty od nich, umístit dosavadně vytvořené - redigovat je...
 - korektury - měl by dělat někdo jiný, než text tvoří - """práce pro dobrovolníka"""
 - profily zaměstnanců kanceláře - jejich pracovní náplň, fotografie...
 - podpora jinému, než automobilovému způsobu dopravy - baner, nálepky...
 - nová sekce - """Podporují nás"""

= Zpravodaj =

 - vyjde zpravodaj """KAM?""" - uzávěrka 16.1. - do konce ledna vyjde, jeho působnost je do konce dubna, ke Dni Země vyjde nové číslo
  - nápady na obsah, informace o akcích, příspěvky

= Válná Hromada =

 - ještě před ní (23. - 25.2.) udělat schůzku a vyzkoumat, co je třeba nadnést, """podněty z praxe"""
 - program, jídlo - Áďa, Cody

= Tiskoviny =

 - průkazky členské a OHB - vymyslet jejich dotisk
 - samolepky - Michal Žižka
 - propagační letáky - jednotná forma skládanky, v prvé fázi obecná o Hnutí (Cody [ještě více zapůsobit na možnost volného členství, za týden se sejít a přinést návrhy {od 16.00, umístit na web, rozeslat na brontl}]), Akci Příroda (Žblebt) a BRĎu (Ctibor [probrat na sekci BRĎO]) - zpracovat a vydat do Dnů Země, grafika (Michal Žižka, pokud někdo jiný - koordinace, aby byl podobný vzhled a forma
 - přidat """návratku""" pro toho, kdo chce podpořit - možnost vyplnění na """Ekostanu"""
 - """panely""" - také mohou být obdobně zpracovány pro jednotlivé prezentované celky a témata - """sekce Ekostanu"""
 - plakátky k """Dobrovolníkům""", """Ekostany""" - distribuce k začátku letního semestru

= Databáze & Maily =

 - je na webu, nasázet dobrovolníky, Cody potřebuje poslat na Síťku pro výkaz
 - zavést paralelní offline systém - pro případ havárie
 - """správce serveru""" -  vyřešit některé důležité problémy, spam, přeposílání, záloha databáze

= Trička & Kabele =

 - zjistit a nechat vyrobit, pevnější materiál, dlouhé uši pouze - Katarína, Lenka

= Organizace práce =

 - rozvrh toho, kdo kdy bude na kanceláři - zatím stejný, změní se dle rozvrhů
 - sešit na vzkazy u telefonu
 - """adresář""" - dokompletit a rozeslat, doplnit ICQ
 - """seznam článků""" - aktualizace změn, obnovené, změněné a zaniklé články, články ať si zkontrolují údaje

= Projetky =

 - MŽP (?), Partnerství (nevyšlo), MŠMT (je v procesu)
 - projekty v zahraničí - problémy se zadáním
 - """Ekostan jako akce""" - výkazy, náklady (evidovat během tohoto roku) - možnost dotací MŠMT
 - """Vzdělávání"""
 - Co je na """Jižní Moravě""" financovat z """ESF""", zbytek z """MŠMT"""
 - na """MŠMT""" 70% lidí do 26 let je třeba
 - projekty k podání
  - """Nadace rozvoje občanské společnosti""" - Norské peníze
   - víc malých projektů
   - přidat návrhy na aktivity
  - do března
 - """Krajský úřad""" - životní prostředí
 - """Partnerství"""
  - """Strom života"""
   - problém Skansky
   - uzávěrka je do 19.1.
   - """malé granty""" na konkrétní akce - nářadí, propagace konkrétní akce...

= Sponzoři =

 - Jihomoravská energetika
 - Cenin
 - Lesy ČR
 - JMP

= Závěrečné zprávy =

 - do konce ledna uzávěrky
 - Katarína - sponozři (Ekostan 2006)

= Soutěž plakátků PsB =

 - málo kandidátů
 - nehlasovat  na webu, ale pouze na Valné Hromadě
 - ceny pro lidi, co vytvořili trička

= Ekokvíz =

 - uveřejnit vylosované vítěze
 - vítězům dat cenu - poslat jim něco z inventáře kanceláře (knížka :-))

= Nový pracovník =

 - několik kandidátů - dva jsou vyloženě vhodní - pozvat a vybrat
 - administrační funkce, pravidlený dochoz, systematičnost práce

= Adresa kanceláře =

 - změnit v dokumentech
 - přeposílání pošty

= Kancelář =

 - dodělání zvonků, jmenovek, nálepek, zvonků...
 - nábytek, police - spojit s promítáním nebo jinou švandou
 - zavedení nějakých večerů - vzdělávačně-zábavných
 - slavnostní otevření v půlce února - program

'''

        tree = parse(string, register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Plány programů a akcí')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[1].type_, 'itemized')
        self.assertEquals(tree.children[0].children[1].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[0].level, 0)
        self.assertEquals(tree.children[0].children[1].children[0].children[0].content, 'každý za svůj program zpracuje ')
        self.assertEquals(tree.children[0].children[1].children[0].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[1].children[0].children[1].children[0].content, 'koncepci')
        self.assertEquals(tree.children[0].children[1].children[0].children[2].content, ', která bude sloužit k lepšímu plánování - cíle tohoto roku, konkrétní aktivity, průběh tohoto roku')
        self.assertEquals(tree.children[0].children[1].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[1].level, 0)
        self.assertEquals(tree.children[0].children[1].children[1].children[0].content, 'zaměřit na možnost ')
        self.assertEquals(tree.children[0].children[1].children[1].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[1].children[1].children[1].children[0].content, 'zapojení dobrovolníků')
        self.assertEquals(tree.children[0].children[1].children[1].children[2].content, ' - nabídka konkrétních činností')
        self.assertEquals(tree.children[0].children[1].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[2].level, 0)
        self.assertEquals(tree.children[0].children[1].children[2].children[0].content, 'bude propráno a mozkovybouřeno na příští poradě')
        self.assertEquals(tree.children[0].children[1].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[3].level, 0)
        self.assertEquals(tree.children[0].children[1].children[3].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[1].children[3].children[0].children[0].content, 'vytvořit sekci na brontowebu')
        self.assertEquals(tree.children[0].children[1].children[3].children[1].content, ' - nabídník nárazové i dlouhodobé věci, vyčlenit novou pro sponzory, konkrétní nabídky, co jim může naše činnost dát')

        self.assertEquals(tree.children[0].children[2].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[2].children[0].content, 'WWW Stránky')
        self.assertEquals(tree.children[0].children[3].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[3].type_, 'itemized')
        self.assertEquals(tree.children[0].children[3].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[0].level, 0)
        self.assertEquals(tree.children[0].children[3].children[0].children[0].content, 'otázka bannerů')
        self.assertEquals(tree.children[0].children[3].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[1].level, 0)
        self.assertEquals(tree.children[0].children[3].children[1].children[0].content, 'zprávy z kanceláře')
        self.assertEquals(tree.children[0].children[3].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[2].level, 0)
        self.assertEquals(tree.children[0].children[3].children[2].children[0].content, 'článek o přestěhování kanclu do aktualit, upravit mapu, celkově projít celý web a zkontrolovat')
        self.assertEquals(tree.children[0].children[3].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[3].level, 0)
        self.assertEquals(tree.children[0].children[3].children[3].children[0].content, 'kontaktovat webmastery ostatních portálů a informovat je o změně a zařídit')
        self.assertEquals(tree.children[0].children[3].children[4].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[4].level, 0)
        self.assertEquals(tree.children[0].children[3].children[4].children[0].content, 'představení článků - texty od nich, umístit dosavadně vytvořené - redigovat je')
        self.assertEquals(tree.children[0].children[3].children[4].children[1].__class__, nodes.TriTecky)
        self.assertEquals(tree.children[0].children[3].children[5].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[5].level, 0)
        self.assertEquals(tree.children[0].children[3].children[5].children[0].content, 'korektury - měl by dělat někdo jiný, než text tvoří - ')
        self.assertEquals(tree.children[0].children[3].children[5].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[3].children[5].children[1].children[0].content, 'práce pro dobrovolníka')
        self.assertEquals(tree.children[0].children[3].children[6].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[6].level, 0)
        self.assertEquals(tree.children[0].children[3].children[6].children[0].content, 'profily zaměstnanců kanceláře - jejich pracovní náplň, fotografie')
        self.assertEquals(tree.children[0].children[3].children[6].children[1].__class__, nodes.TriTecky)
        self.assertEquals(tree.children[0].children[3].children[7].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[7].level, 0)
        self.assertEquals(tree.children[0].children[3].children[7].children[0].content, 'podpora jinému, než automobilovému způsobu dopravy - baner, nálepky')
        self.assertEquals(tree.children[0].children[3].children[7].children[1].__class__, nodes.TriTecky)
        self.assertEquals(tree.children[0].children[3].children[8].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[3].children[8].level, 0)
        self.assertEquals(tree.children[0].children[3].children[8].children[0].content, 'nová sekce - ')
        self.assertEquals(tree.children[0].children[3].children[8].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[3].children[8].children[1].children[0].content, 'Podporují nás')

        self.assertEquals(tree.children[0].children[4].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[4].children[0].content, 'Zpravodaj')
        self.assertEquals(tree.children[0].children[5].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[5].type_, 'itemized')
        self.assertEquals(tree.children[0].children[5].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[5].children[0].level, 0)
        self.assertEquals(tree.children[0].children[5].children[0].children[0].content, 'vyjde zpravodaj ')
        self.assertEquals(tree.children[0].children[5].children[0].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[5].children[0].children[1].children[0].content, 'KAM?')
        self.assertEquals(tree.children[0].children[5].children[0].children[2].content, ' - uzávěrka 16.1. - do konce ledna vyjde, jeho působnost je do konce dubna, ke Dni Země vyjde nové číslo')
        self.assertEquals(tree.children[0].children[5].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[5].children[1].level, 1)
        self.assertEquals(tree.children[0].children[5].children[1].children[0].content, 'nápady na obsah, informace o akcích, příspěvky')

        self.assertEquals(tree.children[0].children[6].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[6].children[0].content, 'Válná Hromada')
        self.assertEquals(tree.children[0].children[7].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[7].type_, 'itemized')
        self.assertEquals(tree.children[0].children[7].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[7].children[0].level, 0)
        self.assertEquals(tree.children[0].children[7].children[0].children[0].content, 'ještě před ní (23. - 25.2.) udělat schůzku a vyzkoumat, co je třeba nadnést, ')
        self.assertEquals(tree.children[0].children[7].children[0].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[7].children[0].children[1].children[0].content, 'podněty z praxe')
        self.assertEquals(tree.children[0].children[7].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[7].children[1].level, 0)
        self.assertEquals(tree.children[0].children[7].children[1].children[0].content, 'program, jídlo - Áďa, Cody')

        self.assertEquals(tree.children[0].children[8].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[8].children[0].content, 'Tiskoviny')
        self.assertEquals(tree.children[0].children[9].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[9].type_, 'itemized')
        self.assertEquals(tree.children[0].children[9].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[0].level, 0)
        self.assertEquals(tree.children[0].children[9].children[0].children[0].content, 'průkazky členské a OHB - vymyslet jejich dotisk')
        self.assertEquals(tree.children[0].children[9].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[1].level, 0)
        self.assertEquals(tree.children[0].children[9].children[1].children[0].content, 'samolepky - Michal Žižka')
        self.assertEquals(tree.children[0].children[9].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[2].level, 0)
        self.assertEquals(tree.children[0].children[9].children[2].children[0].content, 'propagační letáky - jednotná forma skládanky, v prvé fázi obecná o Hnutí (Cody [ještě více zapůsobit na možnost volného členství, za týden se sejít a přinést návrhy {od 16.00, umístit na web, rozeslat na brontl}]), Akci Příroda (Žblebt) a BRĎu (Ctibor [probrat na sekci BRĎO]) - zpracovat a vydat do Dnů Země, grafika (Michal Žižka, pokud někdo jiný - koordinace, aby byl podobný vzhled a forma')
        self.assertEquals(tree.children[0].children[9].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[3].level, 0)
        self.assertEquals(tree.children[0].children[9].children[3].children[0].content, 'přidat ')
        self.assertEquals(tree.children[0].children[9].children[3].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[3].children[1].children[0].content, 'návratku')
        self.assertEquals(tree.children[0].children[9].children[3].children[2].content, ' pro toho, kdo chce podpořit - možnost vyplnění na ')
        self.assertEquals(tree.children[0].children[9].children[3].children[3].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[3].children[3].children[0].content, 'Ekostanu')
        self.assertEquals(tree.children[0].children[9].children[4].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[4].level, 0)
        self.assertEquals(tree.children[0].children[9].children[4].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[4].children[0].children[0].content, 'panely')
        self.assertEquals(tree.children[0].children[9].children[4].children[1].content, ' - také mohou být obdobně zpracovány pro jednotlivé prezentované celky a témata - ')
        self.assertEquals(tree.children[0].children[9].children[4].children[2].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[4].children[2].children[0].content, 'sekce Ekostanu')
        self.assertEquals(tree.children[0].children[9].children[5].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[9].children[5].level, 0)
        self.assertEquals(tree.children[0].children[9].children[5].children[0].content, 'plakátky k ')
        self.assertEquals(tree.children[0].children[9].children[5].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[5].children[1].children[0].content, 'Dobrovolníkům')
        self.assertEquals(tree.children[0].children[9].children[5].children[2].content, ', ')
        self.assertEquals(tree.children[0].children[9].children[5].children[3].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[9].children[5].children[3].children[0].content, 'Ekostany')
        self.assertEquals(tree.children[0].children[9].children[5].children[4].content, ' - distribuce k začátku letního semestru')

        self.assertEquals(tree.children[0].children[10].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[10].children[0].content, 'Databáze & Maily')
        self.assertEquals(tree.children[0].children[11].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[11].type_, 'itemized')
        self.assertEquals(tree.children[0].children[11].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[11].children[0].level, 0)
        self.assertEquals(tree.children[0].children[11].children[0].children[0].content, 'je na webu, nasázet dobrovolníky, Cody potřebuje poslat na Síťku pro výkaz')
        self.assertEquals(tree.children[0].children[11].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[11].children[1].level, 0)
        self.assertEquals(tree.children[0].children[11].children[1].children[0].content, 'zavést paralelní offline systém - pro případ havárie')
        self.assertEquals(tree.children[0].children[11].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[11].children[2].level, 0)
        self.assertEquals(tree.children[0].children[11].children[2].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[11].children[2].children[0].children[0].content, 'správce serveru')
        self.assertEquals(tree.children[0].children[11].children[2].children[1].content, ' - vyřešit některé důležité problémy, spam, přeposílání, záloha databáze')

        self.assertEquals(tree.children[0].children[12].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[12].children[0].content, 'Trička & Kabele')
        self.assertEquals(tree.children[0].children[13].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[13].type_, 'itemized')
        self.assertEquals(tree.children[0].children[13].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[13].children[0].level, 0)
        self.assertEquals(tree.children[0].children[13].children[0].children[0].content, 'zjistit a nechat vyrobit, pevnější materiál, dlouhé uši pouze - Katarína, Lenka')

        self.assertEquals(tree.children[0].children[14].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[14].children[0].content, 'Organizace práce')
        self.assertEquals(tree.children[0].children[15].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[15].type_, 'itemized')
        self.assertEquals(tree.children[0].children[15].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[15].children[0].level, 0)
        self.assertEquals(tree.children[0].children[15].children[0].children[0].content, 'rozvrh toho, kdo kdy bude na kanceláři - zatím stejný, změní se dle rozvrhů')
        self.assertEquals(tree.children[0].children[15].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[15].children[1].level, 0)
        self.assertEquals(tree.children[0].children[15].children[1].children[0].content, 'sešit na vzkazy u telefonu')
        self.assertEquals(tree.children[0].children[15].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[15].children[2].level, 0)
        self.assertEquals(tree.children[0].children[15].children[2].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[15].children[2].children[0].children[0].content, 'adresář')
        self.assertEquals(tree.children[0].children[15].children[2].children[1].content, ' - dokompletit a rozeslat, doplnit ICQ')
        self.assertEquals(tree.children[0].children[15].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[15].children[3].level, 0)
        self.assertEquals(tree.children[0].children[15].children[3].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[15].children[3].children[0].children[0].content, 'seznam článků')
        self.assertEquals(tree.children[0].children[15].children[3].children[1].content, ' - aktualizace změn, obnovené, změněné a zaniklé články, články ať si zkontrolují údaje')

        self.assertEquals(tree.children[0].children[16].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[16].children[0].content, 'Projetky')
        self.assertEquals(tree.children[0].children[17].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[17].type_, 'itemized')
        self.assertEquals(tree.children[0].children[17].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[0].level, 0)
        self.assertEquals(tree.children[0].children[17].children[0].children[0].content, 'MŽP (?), Partnerství (nevyšlo), MŠMT (je v procesu)')
        self.assertEquals(tree.children[0].children[17].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[1].level, 0)
        self.assertEquals(tree.children[0].children[17].children[1].children[0].content, 'projekty v zahraničí - problémy se zadáním')
        self.assertEquals(tree.children[0].children[17].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[2].level, 0)
        self.assertEquals(tree.children[0].children[17].children[2].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[2].children[0].children[0].content, 'Ekostan jako akce')
        self.assertEquals(tree.children[0].children[17].children[2].children[1].content, ' - výkazy, náklady (evidovat během tohoto roku) - možnost dotací MŠMT')
        self.assertEquals(tree.children[0].children[17].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[3].level, 0)
        self.assertEquals(tree.children[0].children[17].children[3].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[3].children[0].children[0].content, 'Vzdělávání')
        self.assertEquals(tree.children[0].children[17].children[4].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[4].level, 0)
        self.assertEquals(tree.children[0].children[17].children[4].children[0].content, 'Co je na ')
        self.assertEquals(tree.children[0].children[17].children[4].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[4].children[1].children[0].content, 'Jižní Moravě')
        self.assertEquals(tree.children[0].children[17].children[4].children[2].content, ' financovat z ')
        self.assertEquals(tree.children[0].children[17].children[4].children[3].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[4].children[3].children[0].content, 'ESF')
        self.assertEquals(tree.children[0].children[17].children[4].children[4].content, ', zbytek z ')
        self.assertEquals(tree.children[0].children[17].children[4].children[5].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[4].children[5].children[0].content, 'MŠMT')
        self.assertEquals(tree.children[0].children[17].children[5].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[5].level, 0)
        self.assertEquals(tree.children[0].children[17].children[5].children[0].content, 'na ')
        self.assertEquals(tree.children[0].children[17].children[5].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[5].children[1].children[0].content, 'MŠMT')
        self.assertEquals(tree.children[0].children[17].children[5].children[2].content, ' 70% lidí do 26 let je třeba')
        self.assertEquals(tree.children[0].children[17].children[6].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[6].level, 0)
        self.assertEquals(tree.children[0].children[17].children[6].children[0].content, 'projekty k podání')
        self.assertEquals(tree.children[0].children[17].children[7].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[7].level, 1)
        self.assertEquals(tree.children[0].children[17].children[7].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[7].children[0].children[0].content, 'Nadace rozvoje občanské společnosti')
        self.assertEquals(tree.children[0].children[17].children[7].children[1].content, ' - Norské peníze')
        self.assertEquals(tree.children[0].children[17].children[8].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[8].level, 2)
        self.assertEquals(tree.children[0].children[17].children[8].children[0].content, 'víc malých projektů')
        self.assertEquals(tree.children[0].children[17].children[9].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[9].level, 2)
        self.assertEquals(tree.children[0].children[17].children[9].children[0].content, 'přidat návrhy na aktivity')
        self.assertEquals(tree.children[0].children[17].children[10].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[10].level, 1)
        self.assertEquals(tree.children[0].children[17].children[10].children[0].content, 'do března')
        self.assertEquals(tree.children[0].children[17].children[11].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[11].level, 0)
        self.assertEquals(tree.children[0].children[17].children[11].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[11].children[0].children[0].content, 'Krajský úřad')
        self.assertEquals(tree.children[0].children[17].children[11].children[1].content, ' - životní prostředí')
        self.assertEquals(tree.children[0].children[17].children[12].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[12].level, 0)
        self.assertEquals(tree.children[0].children[17].children[12].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[12].children[0].children[0].content, 'Partnerství')
        self.assertEquals(tree.children[0].children[17].children[13].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[13].level, 1)
        self.assertEquals(tree.children[0].children[17].children[13].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[13].children[0].children[0].content, 'Strom života')
        self.assertEquals(tree.children[0].children[17].children[14].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[14].level, 2)
        self.assertEquals(tree.children[0].children[17].children[14].children[0].content, 'problém Skansky')
        self.assertEquals(tree.children[0].children[17].children[15].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[15].level, 2)
        self.assertEquals(tree.children[0].children[17].children[15].children[0].content, 'uzávěrka je do 19.1.')
        self.assertEquals(tree.children[0].children[17].children[16].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[17].children[16].level, 2)
        self.assertEquals(tree.children[0].children[17].children[16].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[17].children[16].children[0].children[0].content, 'malé granty')
        self.assertEquals(tree.children[0].children[17].children[16].children[1].content, ' na konkrétní akce - nářadí, propagace konkrétní akce')
        self.assertEquals(tree.children[0].children[17].children[16].children[2].__class__, nodes.TriTecky)

        self.assertEquals(tree.children[0].children[18].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[18].children[0].content, 'Sponzoři')
        self.assertEquals(tree.children[0].children[19].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[19].type_, 'itemized')
        self.assertEquals(tree.children[0].children[19].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[19].children[0].level, 0)
        self.assertEquals(tree.children[0].children[19].children[0].children[0].content, 'Jihomoravská energetika')
        self.assertEquals(tree.children[0].children[19].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[19].children[1].level, 0)
        self.assertEquals(tree.children[0].children[19].children[1].children[0].content, 'Cenin')
        self.assertEquals(tree.children[0].children[19].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[19].children[2].level, 0)
        self.assertEquals(tree.children[0].children[19].children[2].children[0].content, 'Lesy ČR')
        self.assertEquals(tree.children[0].children[19].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[19].children[3].level, 0)
        self.assertEquals(tree.children[0].children[19].children[3].children[0].content, 'JMP')

        self.assertEquals(tree.children[0].children[20].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[20].children[0].content, 'Závěrečné zprávy')
        self.assertEquals(tree.children[0].children[21].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[21].type_, 'itemized')
        self.assertEquals(tree.children[0].children[21].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[21].children[0].level, 0)
        self.assertEquals(tree.children[0].children[21].children[0].children[0].content, 'do konce ledna uzávěrky')
        self.assertEquals(tree.children[0].children[21].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[21].children[1].level, 0)
        self.assertEquals(tree.children[0].children[21].children[1].children[0].content, 'Katarína - sponozři (Ekostan 2006)')

        self.assertEquals(tree.children[0].children[22].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[22].children[0].content, 'Soutěž plakátků PsB')
        self.assertEquals(tree.children[0].children[23].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[23].type_, 'itemized')
        self.assertEquals(tree.children[0].children[23].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[23].children[0].level, 0)
        self.assertEquals(tree.children[0].children[23].children[0].children[0].content, 'málo kandidátů')
        self.assertEquals(tree.children[0].children[23].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[23].children[1].level, 0)
        self.assertEquals(tree.children[0].children[23].children[1].children[0].content, 'nehlasovat na webu, ale pouze na Valné Hromadě')
        self.assertEquals(tree.children[0].children[23].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[23].children[2].level, 0)
        self.assertEquals(tree.children[0].children[23].children[2].children[0].content, 'ceny pro lidi, co vytvořili trička')

        self.assertEquals(tree.children[0].children[24].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[24].children[0].content, 'Ekokvíz')
        self.assertEquals(tree.children[0].children[25].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[25].type_, 'itemized')
        self.assertEquals(tree.children[0].children[25].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[25].children[0].level, 0)
        self.assertEquals(tree.children[0].children[25].children[0].children[0].content, 'uveřejnit vylosované vítěze')
        self.assertEquals(tree.children[0].children[25].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[25].children[1].level, 0)
        self.assertEquals(tree.children[0].children[25].children[1].children[0].content, 'vítězům dat cenu - poslat jim něco z inventáře kanceláře (knížka :-))')

        self.assertEquals(tree.children[0].children[26].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[26].children[0].content, 'Nový pracovník')
        self.assertEquals(tree.children[0].children[27].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[27].type_, 'itemized')
        self.assertEquals(tree.children[0].children[27].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[27].children[0].level, 0)
        self.assertEquals(tree.children[0].children[27].children[0].children[0].content, 'několik kandidátů - dva jsou vyloženě vhodní - pozvat a vybrat')
        self.assertEquals(tree.children[0].children[27].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[27].children[1].level, 0)
        self.assertEquals(tree.children[0].children[27].children[1].children[0].content, 'administrační funkce, pravidlený dochoz, systematičnost práce')

        self.assertEquals(tree.children[0].children[28].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[28].children[0].content, 'Adresa kanceláře')
        self.assertEquals(tree.children[0].children[29].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[29].type_, 'itemized')
        self.assertEquals(tree.children[0].children[29].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[29].children[0].level, 0)
        self.assertEquals(tree.children[0].children[29].children[0].children[0].content, 'změnit v dokumentech')
        self.assertEquals(tree.children[0].children[29].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[29].children[1].level, 0)
        self.assertEquals(tree.children[0].children[29].children[1].children[0].content, 'přeposílání pošty')

        self.assertEquals(tree.children[0].children[30].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[30].children[0].content, 'Kancelář')
        self.assertEquals(tree.children[0].children[31].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[31].type_, 'itemized')
        self.assertEquals(tree.children[0].children[31].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[31].children[0].level, 0)
        self.assertEquals(tree.children[0].children[31].children[0].children[0].content, 'dodělání zvonků, jmenovek, nálepek, zvonků')
        self.assertEquals(tree.children[0].children[31].children[0].children[1].__class__, nodes.TriTecky)
        self.assertEquals(tree.children[0].children[31].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[31].children[1].level, 0)
        self.assertEquals(tree.children[0].children[31].children[1].children[0].content, 'nábytek, police - spojit s promítáním nebo jinou švandou')
        self.assertEquals(tree.children[0].children[31].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[31].children[2].level, 0)
        self.assertEquals(tree.children[0].children[31].children[2].children[0].content, 'zavedení nějakých večerů - vzdělávačně-zábavných')
        self.assertEquals(tree.children[0].children[31].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[31].children[3].level, 0)
        self.assertEquals(tree.children[0].children[31].children[3].children[0].content, 'slavnostní otevření v půlce února - program')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<h1>Plány programů a akcí</h1><ul><li>každý za svůj program zpracuje <strong>koncepci</strong>, která bude sloužit k lepšímu plánování - cíle tohoto roku, konkrétní aktivity, průběh tohoto roku</li><li>zaměřit na možnost <strong>zapojení dobrovolníků</strong> - nabídka konkrétních činností</li><li>bude propráno a mozkovybouřeno na příští poradě</li><li><strong>vytvořit sekci na brontowebu</strong> - nabídník nárazové i dlouhodobé věci, vyčlenit novou pro sponzory, konkrétní nabídky, co jim může naše činnost dát</li></ul><h1>WWW Stránky</h1><ul><li>otázka bannerů</li><li>zprávy z kanceláře</li><li>článek o přestěhování kanclu do aktualit, upravit mapu, celkově projít celý web a zkontrolovat</li><li>kontaktovat webmastery ostatních portálů a informovat je o změně a zařídit</li><li>představení článků - texty od nich, umístit dosavadně vytvořené - redigovat je&#8230;</li><li>korektury - měl by dělat někdo jiný, než text tvoří - <strong>práce pro dobrovolníka</strong></li><li>profily zaměstnanců kanceláře - jejich pracovní náplň, fotografie&#8230;</li><li>podpora jinému, než automobilovému způsobu dopravy - baner, nálepky&#8230;</li><li>nová sekce - <strong>Podporují nás</strong></li></ul><h1>Zpravodaj</h1><ul><li>vyjde zpravodaj <strong>KAM?</strong> - uzávěrka 16.1. - do konce ledna vyjde, jeho působnost je do konce dubna, ke Dni Země vyjde nové číslo</li><ul><li>nápady na obsah, informace o akcích, příspěvky</li></ul></ul><h1>Válná Hromada</h1><ul><li>ještě před ní (23. - 25.2.) udělat schůzku a vyzkoumat, co je třeba nadnést, <strong>podněty z praxe</strong></li><li>program, jídlo - Áďa, Cody</li></ul><h1>Tiskoviny</h1><ul><li>průkazky členské a OHB - vymyslet jejich dotisk</li><li>samolepky - Michal Žižka</li><li>propagační letáky - jednotná forma skládanky, v prvé fázi obecná o Hnutí (Cody [ještě více zapůsobit na možnost volného členství, za týden se sejít a přinést návrhy {od 16.00, umístit na web, rozeslat na brontl}]), Akci Příroda (Žblebt) a BRĎu (Ctibor [probrat na sekci BRĎO]) - zpracovat a vydat do Dnů Země, grafika (Michal Žižka, pokud někdo jiný - koordinace, aby byl podobný vzhled a forma</li><li>přidat <strong>návratku</strong> pro toho, kdo chce podpořit - možnost vyplnění na <strong>Ekostanu</strong></li><li><strong>panely</strong> - také mohou být obdobně zpracovány pro jednotlivé prezentované celky a témata - <strong>sekce Ekostanu</strong></li><li>plakátky k <strong>Dobrovolníkům</strong>, <strong>Ekostany</strong> - distribuce k začátku letního semestru</li></ul><h1>Databáze &amp; Maily</h1><ul><li>je na webu, nasázet dobrovolníky, Cody potřebuje poslat na Síťku pro výkaz</li><li>zavést paralelní offline systém - pro případ havárie</li><li><strong>správce serveru</strong> - vyřešit některé důležité problémy, spam, přeposílání, záloha databáze</li></ul><h1>Trička &amp; Kabele</h1><ul><li>zjistit a nechat vyrobit, pevnější materiál, dlouhé uši pouze - Katarína, Lenka</li></ul><h1>Organizace práce</h1><ul><li>rozvrh toho, kdo kdy bude na kanceláři - zatím stejný, změní se dle rozvrhů</li><li>sešit na vzkazy u telefonu</li><li><strong>adresář</strong> - dokompletit a rozeslat, doplnit ICQ</li><li><strong>seznam článků</strong> - aktualizace změn, obnovené, změněné a zaniklé články, články ať si zkontrolují údaje</li></ul><h1>Projetky</h1><ul><li>MŽP (?), Partnerství (nevyšlo), MŠMT (je v procesu)</li><li>projekty v zahraničí - problémy se zadáním</li><li><strong>Ekostan jako akce</strong> - výkazy, náklady (evidovat během tohoto roku) - možnost dotací MŠMT</li><li><strong>Vzdělávání</strong></li><li>Co je na <strong>Jižní Moravě</strong> financovat z <strong>ESF</strong>, zbytek z <strong>MŠMT</strong></li><li>na <strong>MŠMT</strong> 70% lidí do 26 let je třeba</li><li>projekty k podání</li><ul><li><strong>Nadace rozvoje občanské společnosti</strong> - Norské peníze</li><ul><li>víc malých projektů</li><li>přidat návrhy na aktivity</li></ul><li>do března</li></ul><li><strong>Krajský úřad</strong> - životní prostředí</li><li><strong>Partnerství</strong></li><ul><li><strong>Strom života</strong></li><ul><li>problém Skansky</li><li>uzávěrka je do 19.1.</li><li><strong>malé granty</strong> na konkrétní akce - nářadí, propagace konkrétní akce&#8230;</li></ul></ul></ul><h1>Sponzoři</h1><ul><li>Jihomoravská energetika</li><li>Cenin</li><li>Lesy ČR</li><li>JMP</li></ul><h1>Závěrečné zprávy</h1><ul><li>do konce ledna uzávěrky</li><li>Katarína - sponozři (Ekostan 2006)</li></ul><h1>Soutěž plakátků PsB</h1><ul><li>málo kandidátů</li><li>nehlasovat na webu, ale pouze na Valné Hromadě</li><li>ceny pro lidi, co vytvořili trička</li></ul><h1>Ekokvíz</h1><ul><li>uveřejnit vylosované vítěze</li><li>vítězům dat cenu - poslat jim něco z inventáře kanceláře (knížka :-))</li></ul><h1>Nový pracovník</h1><ul><li>několik kandidátů - dva jsou vyloženě vhodní - pozvat a vybrat</li><li>administrační funkce, pravidlený dochoz, systematičnost práce</li></ul><h1>Adresa kanceláře</h1><ul><li>změnit v dokumentech</li><li>přeposílání pošty</li></ul><h1>Kancelář</h1><ul><li>dodělání zvonků, jmenovek, nálepek, zvonků&#8230;</li><li>nábytek, police - spojit s promítáním nebo jinou švandou</li><li>zavedení nějakých večerů - vzdělávačně-zábavných</li><li>slavnostní otevření v půlce února - program</li></ul>''', res)


if __name__ == "__main__":
    main()
