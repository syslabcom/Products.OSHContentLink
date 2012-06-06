from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.testing import z2


class OSHContentLink(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.OSHContentLink
        self.loadZCML('configure.zcml', package=Products.OSHContentLink)

        import osha.policy.browser
        self.loadZCML('configure.zcml', package=osha.policy.browser)

        z2.installProduct(app, 'Products.OSHContentLink')

    def setUpPloneSite(self, portal):
        # Needed to make skins work
        applyProfile(portal, 'Products.CMFPlone:plone')

        applyProfile(portal, 'Products.OSHContentLink:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.OSHContentLink')


OSHCONTENTLINK_FIXTURE = OSHContentLink()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(OSHCONTENTLINK_FIXTURE,),
    name="OSHContentLink:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OSHCONTENTLINK_FIXTURE,),
    name="OSHContentLink:Functional")
