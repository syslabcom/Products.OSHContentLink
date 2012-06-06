Introduction
============

OSH Links are used to link to external resources in the internet that provide OSH
relevant information. Several fields offer the possibility to enter meta-information about
these resources.

Boilerplate
===========

First, we must perform some setup.

    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> portal = layer['portal']
    >>> portal_url = portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in.

    >>> browser.open(portal_url + '/login_form')

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = 'admin'
    >>> browser.getControl(name='__ac_password').value = 'secret'
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

    >>> browser.open(portal_url)

Adding an OSH Link
==================

We use the 'Add new' menu to add a new content item.

XXX: Tests are currently commented out, because we need to properly
install osha.adaptation and its dependencies in the test layer.

    >>> browser.getLink(url='createObject?type_name=OSH_Link').click()
    >>> 'OSH_Link' in browser.contents
    True

Now we fill the form and submit it.

    >>> # browser.getControl(name='title').value = 'My OSH_Link'
    >>> # browser.getControl(name='text').value = 'Text...'
    >>> # browser.getControl(name='remoteUrl').value = 'http://foo.bar.com'
    >>> # browser.getControl('Save').click()
    >>> # 'Changes saved' in browser.contents
    True
