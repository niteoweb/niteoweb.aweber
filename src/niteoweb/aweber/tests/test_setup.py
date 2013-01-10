# -*- coding: utf-8 -*-
"""
Setup/installation tests for niteoweb.aweber
------------------------------------------------
"""

from AccessControl import Unauthorized
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from niteoweb.aweber.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone.app.testing import logout
from niteoweb.aweber.interfaces import IAweberSettings

import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of niteoweb.aweber into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if niteoweb.aweber is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('niteoweb.aweber'))

    def test_disable_registration_for_anonymous(self):
        """Test if anonymous visitors are prevented to register to the site."""
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        self.assertFalse(
            'Add portal member' in [r['name'] for r in
            self.portal.permissionsOfRole('Anonymous') if r['selected']])

    def test_use_email_as_login(self):
        """Test if email is indeed used as username."""
        site_properties = self.portal.portal_properties.site_properties
        self.assertTrue(site_properties.getProperty('use_email_as_login'))

    def test_aweber_controlpanel_available(self):
        """Test if aweber control panel configlet is available."""
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="aweber-settings")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_aweber_controlpanel_view_protected(self):
        """Check that access to aweber settings is restricted."""
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@aweber-settings')

    def assert_record(self, record_name):
        """Test that the record is in the registry."""
        registry = getUtility(IRegistry)
        record = registry.records[
            'niteoweb.aweber.interfaces.IAweberSettings.{0}'.format(
                record_name
            )
        ]
        self.assertIn(record_name, IAweberSettings)
        record.value = u'testvalue'
        self.assertEquals(record.value, u'testvalue')

    def test_record_app_id(self):
        self.assert_record('app_id')

    def test_record_authorization_code(self):
        self.assert_record('authorization_code')

    def test_record_consumer_key(self):
        self.assert_record('consumer_key')

    def test_record_consumer_secret(self):
        self.assert_record('consumer_secret')

    def test_record_access_token(self):
        self.assert_record('access_token')

    def test_record_access_secret(self):
        self.assert_record('access_secret')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
