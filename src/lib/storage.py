
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom


class Storage(object):

    def prettify(elem):
        """ Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
