from zope.component import adapts
from zope.interface import implements

from Products.OSHContentLink.interfaces import IOSH_Link

try:
    from osha.theme.adapter_textindexng3 import ContentAdapter as CMFContentAdapter
except ImportError:
    from Products.TextIndexNG3.adapters.cmf_adapters import CMFContentAdapter

from Products.TextIndexNG3.src.textindexng.content import IndexContentCollector as ICC
from Products.TextIndexNG3.src.textindexng.interfaces import IIndexableContent

class OSHLinkContentAdapter(CMFContentAdapter):

    """An adapter for OSH_Links files.
    """
    adapts(IOSH_Link)
    
    def indexableContent(self, fields):
        icc = ICC()
        if 'getId' in fields:
            self.addIdField(icc)
        if 'Title' in fields:
            self.addTitleField(icc)
        if 'Description' in fields:
            self.addDescriptionField(icc)
        if 'SearchableText' in fields:
            self.addSearchableTextField(icc)
        if 'getRemoteUrl' in fields:
            self.addRemoteUrlField(icc)
        return icc


    def addRemoteUrlField(self, icc):
        remote_url = self._c(self.context.getRemoteUrl())
        icc.addContent('getRemoteUrl', remote_url, self.language)
