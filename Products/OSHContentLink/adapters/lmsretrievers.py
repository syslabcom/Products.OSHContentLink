import Products.OSHContentLink.OSH_Link
import gocept.linkchecker.interfaces
import gocept.linkchecker.utils
import zope.component
import zope.interface
from types import *


class OSHLinkRetriever(object):
    """Retriever for documents with one or more RichText widgets."""
    zope.component.adapts(Products.OSHContentLink.OSH_Link.OSH_Link)
    zope.interface.implements(gocept.linkchecker.interfaces.IRetriever)

    def __init__(self, context):
        self.context = context

    def retrieveLinks(self):
        """Finds all links from the object and return them."""
        links = gocept.linkchecker.utils.retrieveAllRichTextFields(
            self.context)
        links.append(self.context.getRemoteUrl())
        return [x for x in links if x.strip() != '']

    def updateLink(self, oldurl, newurl):
        """Replace all occurances of <oldurl> on object with <newurl>."""
        gocept.linkchecker.utils.updateAllRichTextFields(
            oldurl, newurl, self.context)
        if self.context.getRemoteUrl() == oldurl:
            self.context.setRemoteUrl(newurl)
