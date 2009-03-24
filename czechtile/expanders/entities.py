
from czechtile.expanders.base import CzechtileExpander

class TriTecky(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&#8230;'

class Trademark(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&#0153;'

class Pomlcka(CzechtileExpander):
    def expand(self, node, format, node_map):
        if node.spojovnik:
            return u'-'
        else:
            return u'&#8211;'

class PevnaMedzera(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&nbsp;'

class Uvozovky(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'&#8222;', u'&#8220;')

