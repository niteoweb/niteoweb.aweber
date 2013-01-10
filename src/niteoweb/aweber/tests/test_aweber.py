# -*- coding: utf-8 -*-
"""
Test Aweber methods
------------------------------------------------
"""

from Products.PloneTestCase import PloneTestCase as PTC
from mock import patch
from niteoweb.aweber.interfaces import IAweberSettings
from niteoweb.aweber.tests.base import FunctionalTestCase
from niteoweb.aweber.tests.base import MockedLoggingHandler as logger
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getUtility

import transaction


class TestAweber(FunctionalTestCase):
    """Test Aweber."""

    def setUp(self):
        """Prepare testing environment."""
        self.portal = self.layer['portal']

        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IAweberSettings)
        self.settings.app_id = u'appid'
        self.settings.authorization_code = u'authorizationcode'
        self.settings.consumer_key = u'consumerkey'
        self.settings.consumer_secret = u'consumersecret'
        self.settings.access_token = u'accesstoken'
        self.settings.access_secret = u'accesssecret'
        transaction.commit()

        self.browser = Browser(self.portal)
        self.login_as_admin()

    def login_as_admin(self):
        # login as admin
        self.browser.open(self.portal.absolute_url() + '/login')
        self.browser.getLink('Log in').click()
        self.browser.getControl(name='__ac_name').value = "admin"
        self.browser.getControl(name='__ac_password').value = \
            PTC.default_password
        self.browser.getControl(name='submit').click()

    def tearDown(self):
        """Clean up after yourself."""

        # logout
        self.browser.open(self.portal.absolute_url() + '/logout')

        # reset our mocked logger
        logger.reset()

    def test_controlpanel_view(self):
        """Test for control panel view.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@aweber-settings'
        )
        self.assertIn(
            '<h1 class="documentFirstHeading">Aweber settings</h1>',
            self.browser.contents
        )

    def test_save(self):
        """Test save button.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.browser.getControl(name='form.widgets.app_id').value = \
            u'temp_app_id'
        self.browser.getControl(name="form.buttons.save").click()

        # test if value is saved
        self.assertEqual(
            self.settings.app_id,
            u'temp_app_id'
        )

    def test_cancel(self):
        """Test cancel button.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.browser.getControl(name='form.widgets.app_id').value = \
            u'temp_app_id'
        self.browser.getControl(name="form.buttons.cancel").click()

        # test if value is unchanged
        self.assertEqual(
            self.settings.app_id,
            u'appid'
        )

    def test_get_auth(self):
        """Test get authorization code button.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.browser.getControl(name="form.buttons.get_auth").click()

        url = "https://auth.aweber.com/1.0/oauth/authorize_app/{0}".format(
            self.browser.getControl(name="form.widgets.app_id").value
        )
        message = "Visit '{0}' and copy authorization code " \
            "to Authorization Code field".format(url)
        self.assertIn(message, self.browser.contents)

    @patch("niteoweb.aweber.browser.controlpanel.parse_auth_code")
    @patch("niteoweb.aweber.browser.controlpanel.set_list_names")
    def test_parse_auth(self, set_list_names, parse_auth_code):
        """Test get authorization code button.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.browser.getControl(name="form.buttons.parse_auth").click()
        assert set_list_names.called
        assert parse_auth_code.called

    @patch("niteoweb.aweber.browser.controlpanel.set_list_names")
    def test_update_lists(self, set_list_names):
        """Test update lists button.
        """
        self.browser.open(self.portal.absolute_url() + "/@@aweber-settings")
        self.browser.getControl(name="form.buttons.update_lists").click()
        assert set_list_names.called
