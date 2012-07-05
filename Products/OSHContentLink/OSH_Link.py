# -*- coding: utf-8 -*-
#
# File: OSH_Link.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.0-beta11
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """syslab.com gmbh <info@syslab.com>"""
__docformat__ = 'plaintext'

from Products.Archetypes.atapi import *

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from AccessControl import ClassSecurityInfo
from plone.memoize import ram
from Products.OSHContentLink.config import *
from Products.OSHContentLink import OSHContentLinkMessageFactory as _
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from zope.interface import implements

import interfaces


schema = Schema((

    TextField(
        name='text',
        required=True,
        widget=RichWidget(
            label=_(u'oshlink_text_label', default=u"Description"),
            description=_(u'oshlink_text_description',
                          default="A descriptive text of the linked content."),
            rows=10,
        ),
        searchable=True,
        validators=("python:('isTidyHtmlWithCleanup'", ')', ''),
        default_output_type='text/x-html-safe',
        storage=AnnotationStorage(migrate=True),
        primary=True,
    ),
    TextField(
        name='description',
        required=False,
        widget=TextAreaWidget(
            visible={'view': 'invisible', 'edit': 'invisible'},
            label=_(u'oshlink_description_label', default=u'Description'),
        ),
    ),
    StringField(
        name='remoteUrl',
        required=True,
        widget=StringField._properties['widget'](
            label=_(u'oshlink_remoteUrl_label', default=u"External URL"),
            size=80,
            description=_(u'oshlink_remoteUrl_description',
                default=u"The web address of the information we link to."),
        ),
    ),
    StringField(
        name='provider',
        required=False,
        widget=ComputedWidget(
            label=_(u'oshlink_provider_label',
                    default=u'"Old style" Provider'),
            description=_(u'oshlink_provider_description',
                default=u'This information is displayed for historic reasons, '
                        u'since Providers used to be entered as plain text. '
                        u'Please choose the appropriate provider from the '
                        u'"Provider of the linked information" field below.'),
            condition="python:object.getProvider()!='' and not object.getRemoteProvider()",
        ),
    ),
    ReferenceField(
        name='remoteProvider',
        widget=ReferenceBrowserWidget(
            label=_(u'ra_remoteProvider_label',
                    default=u'Provider of this information'),
            description=_(u'ra_remoteProvider_description', default=u''),
            allow_browse=False,
            show_results_without_query=True,
        ),
        allowed_types=('Provider'),
        relationship="provider_of",
        multiValued=True,
    ),
    LinesField(
        name='remoteLanguage',
        widget=MultiSelectionWidget(
            description=_(u'oshlink_remoteLanguage_description',
                default=u"Select the languages in which the referenced "
                        u"information is available in. This does not refer to "
                        u" this page but to the link target!"),
            label=_(u'oshlink_remoteLanguage_description',
                    default=u"Languages of the target"),
        ),
        vocabulary='getLanguages',
    ),
    # country, site_position( subcat), MTsubj, NACE are inserted HERE
    TextField(
        name='cas',
        widget=TextAreaWidget(
            label=_(u'oshlink_cas_label', default=u"CAS"),
            description=_(u'oshlink_cas_description',
                          default=u"CAS Numbers. Enter one element per line"),
        ),
    ),
    TextField(
        name='einecs',
        widget=TextAreaWidget(
            label=_(u'oshlink_einecs_label', default=u"EINECS"),
            description=_(u'oshlinl_einecs_description',
                    default=u"EINECS Codes. Enter one element per line."),
        ),
    ),
    TextField(
        name='general_comments',
        widget=TextAreaWidget(
            label=_(u'oshlink_general_comments_label',
                    default=u"General comments"),
            description=_(u'oshlink_general_comments_description',
                default=u"Add arbitrary comments to communicate during the "
                        u"workflow. These comments are not shown to the "
                        u"public."),
        ),
    ),
    StringField(
        name='author',
        widget=StringField._properties['widget'](
            label=_(u'oshlink_author_label', default=u"Author"),
            description=_(u'oshlink_author_description',
                default=u"The author of the published journal/article"),
            size=80,
        ),
    ),
    StringField(
        name='printref',
        widget=StringField._properties['widget'](
            label=_(u'oshlink_printref_label', default=u"Print reference"),
            description=_(u'oshlink_printref_description',
                          default=u"Print reference"),
        ),
    ),
    StringField(
        name='organisation_name',
        widget=StringField._properties['widget'](
            label=_(u'oshlink_organisation_name_label',
                    default=u"Organisation name"),
            description=_(u'oshlink_organisation_name_description',
                default=u"The Name of the organisation providing the linked "
                        u"information."),
        ),
    ),
    TextField(
        name='isbn_d',
        widget=TextAreaWidget(
            label=_(u'oshlink_isbn_d_label', default=u"ISBN D"),
            description=_(u'oshlink_isbn_d_description',
                default=u"ISBN numbers applicable to this information."),
        ),
    ),
    DateTimeField(
        name='publication_date',
        widget=CalendarWidget(
            label=_(u'oshlink_publication_date_label',
                    default=u"Publication date"),
            description=_(u'oshlink_publication_date_description',
                default=u"The date on which this information has been "
                        u"published."),
        ),
    ),
),
)

OSH_Link_schema = BaseSchema.copy() + \
     ATDocumentSchema.copy() + \
    schema.copy()

# Subjects will be determined based on the choosen category. Only gettable!
OSH_Link_schema['subject'].widget.visible['edit'] = 'invisible'
OSH_Link_schema['subject'].widget.visible['view'] = 'invisible'


finalizeATCTSchema(OSH_Link_schema)

unwantedFields = ['relatedItems', 'location', 'excludeFromNav',
    'tableContents', 'presentation', 'allowDiscussion']
for name in unwantedFields:
    OSH_Link_schema[name].widget.visible['edit'] = 'invisible'
    OSH_Link_schema[name].widget.visible['view'] = 'invisible'
    OSH_Link_schema.changeSchemataForField(name, 'default')

# hide effectiveDate (will be filled automatically)
OSH_Link_schema['effectiveDate'].widget.visible['edit'] = 'invisible'
OSH_Link_schema['effectiveDate'].widget.visible['view'] = 'invisible'
OSH_Link_schema.changeSchemataForField('effectiveDate', 'default')

# move expirationDate to the default tab under publication_date
OSH_Link_schema.changeSchemataForField('expirationDate', 'default')

# move language to settings
OSH_Link_schema.changeSchemataForField('language', 'settings')


class OSH_Link(ATDocumentBase, BaseContent, BrowserDefaultMixin):
    """OSH Product for holding 'links' data
    """
    security = ClassSecurityInfo()
    implements(interfaces.IOSH_Link)

    meta_type = 'OSH_Link'
    _at_rename_after_creation = True
    archetype_name = 'OSH Link'
    schema = OSH_Link_schema

    security.declarePublic('getRecordtypeValues')
    def getRecordtypeValues(self):
        """Get all possible values for osh_recordtype"""
        properties = self.portal_properties
        if (hasattr(properties, 'osha_properties') and
            hasattr(properties.osha_properties, 'osh_recordtypes')):
            return ('',) + properties.osha_properties.osh_recordtypes
        else:
            return ('',)

    security.declarePublic('getLanguages')
    def getLanguages(self):
        """Get all possible languages"""
        langs = self.portal_languages.listSupportedLanguages()
        langs.sort()
        return tuple(langs)

    # Manually created methods

    security.declareProtected('View', 'getDescription')
    def getDescription(self):
        """Accessor to fetch description generated from bodytext"""
        text = self.getText()
        # THis behaviour is not wanted anyway because too many oshlinks rely
        # on old html in their description. removed 15.9.2008
        # text = scrubHTML(text, valid={}, remove_javascript=True,
        #                  raise_error=False)
        return text

    security.declareProtected('View', 'getDescription')
    def Description(self):
        """ Accessor to fetch description generated from bodytext """
        return self.getDescription()

#    def getCountry(self):
#        """Returns all countries set on this Link. Country describes in which
#        countries the link target is applicable to.
#        """
#        return self.getField('country').getAccessor(self)()

    security.declareProtected('View', 'EffectiveDate')
    def EffectiveDate(self):
        """ compatibility to DC """
        return self.getPublication_date()

    security.declareProtected('View', 'effective')
    def effective(self):
        """Dublin Core element - date resource becomes effective,
        returned as DateTime.
        """
        effective = self.getField('publication_date').get(self)
        return effective is None and FLOOR_DATE or effective

    def getRemoteProviderUID(self):
        """Return the UID of the provider, stored via reference. Used for
        indexing.
        """
        f = self.getField('remoteProvider')
        return f.getRaw(self)

    security.declarePublic('Provider')
    def Provider(self):
        """ compatibility to DC """
        return self.getProvider()

    def _render_cachekey_related(method, self):
        preflang = getToolByName(
            self, 'portal_languages').getPreferredLanguage()
        path = "/".join(self.getPhysicalPath())
        modified = self.modified()
        return (preflang, path, modified)

    @ram.cache(_render_cachekey_related)
    def getRelatedSections(self):
        """Retrieve all sections implementing ISubsite that match the local
        Subjects.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        sections = portal_catalog(
            object_provides='osha.policy.interfaces.ISingleEntryPoint',
            Subject=self.Subject(),
            review_state="published")
        rs = []
        for section in sections:
            rs.append(dict(title=section.Title, url=section.getURL()))
        rs.sort(lambda x, y: cmp(x['title'].lower(), y['title'].lower()))
        return rs

    @ram.cache(_render_cachekey_related)
    def getRelatedTerms(self):
        """ Retrieve all MLTTerms that match the local terms """
        portal_vocabularies = getToolByName(self, 'portal_vocabularies')
        portal_languages = getToolByName(self, 'portal_languages')
        lang = portal_languages.getPreferredLanguage()
        portal_url = getToolByName(self, 'portal_url')

        manager = portal_vocabularies.MultilingualThesaurus._getManager()

        myterms = self.getField('multilingual_thesaurus').getAccessor(self)()

        rs = []
        for term in myterms:
            caption = manager.getTermCaptionById(term, lang)
            if caption:
                caption = caption.strip()
                letter = caption[0].upper()
                url = "%s/@@index_alphabetical?letter=%s&term_id=%s" % (
                    portal_url.getPortalPath(), letter, term)
                rs.append(dict(id=term, title=caption, url=url))

        rs.sort(lambda x, y: cmp(x['title'], y['title']))
        return rs


registerType(OSH_Link, PROJECTNAME)
