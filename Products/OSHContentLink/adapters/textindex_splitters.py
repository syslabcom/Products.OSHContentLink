###########################################################################
# A very basic splitter for TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################


import re

from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy

from Products.TextIndexNG3.src.textindexng.interfaces import ISplitter


## patterns used by the splitter (will be compiled to regexes)
SPLIT_AT = '\s|\t'
PUNCTUATION = ""
ADDITIONAL_CHARS = ""
RE_FLAGS = re.I | re.M | re.UNICODE


class UrlNotSplitter:
    """ A very simple unicode-aware splitter 
        for URLs """

    implements(ISplitter)

    def __init__(self, 
                 casefolding=1, 
                 split_at=SPLIT_AT, 
                 punctuation=PUNCTUATION, 
                 additional_chars=ADDITIONAL_CHARS,
                 *args, **kw):
        """ 'split_at' -- a regular expression that is used to split strings.
            The regular expression is passed unchanged to re.compile().
        """

        self.splitter = re.compile(split_at, RE_FLAGS)
        self.punctuation = punctuation
        self.casefolding = casefolding
        self.regex = re.compile(r'\w+[\w%s]*' % additional_chars, RE_FLAGS)

    def split(self, content):
        """ Returns the unsplitted URL plus its 'word' components.
            There is still room for becoming more sophisticated...
        """
        if self.casefolding:
            content = content.lower()
        terms = [t.strip(self.punctuation) for t in self.splitter.split(content)]
        final  = list()
        for t in terms:
            final.append(t)
            final += self.regex.findall(t)
        final = [t for t in final if t]
        return final


class UrlNotSplitterFactory:
    
    implements(IFactory)

    def __call__(self, split_at=SPLIT_AT, punctuation=PUNCTUATION, *args, **kw):
        return UrlNotSplitter(split_at=split_at, punctuation=punctuation, *args, **kw)

    def getInterfaces(self):
        return implementedBy(UrlNotSplitter)

UrlNotSplitterFactory = UrlNotSplitterFactory()
