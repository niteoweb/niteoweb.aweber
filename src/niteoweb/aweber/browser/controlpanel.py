# -*- coding: utf-8 -*-
"""
Aweber control panel configlet
------------------------------
"""

from niteoweb.aweber import AweberMessageFactory as _
from niteoweb.aweber.interfaces import IAweberSettings
from plone.app.registry.browser import controlpanel
from z3c.form import button
from plone import api
from aweber_api import AWeberAPI
from niteoweb.aweber import aweberapi


def set_list_names(widgets):
    """Writes list names to registry record.
    """
    consumer_key = widgets['consumer_key'].value
    consumer_secret = widgets['consumer_secret'].value
    access_token = widgets['access_token'].value
    access_secret = widgets['access_secret'].value

    aweber = AWeberAPI(consumer_key, consumer_secret)
    account = aweber.get_account(access_token, access_secret)

    api.portal.set_registry_record(
        'niteoweb.aweber.available_lists_record',
        [l.name for l in account.lists]
    )


def parse_auth_code(widgets):
    """Parse authorization code.
    """
    auth = AWeberAPI.parse_authorization_code(
        widgets['authorization_code'].value
    )

    c_key, c_secret, a_key, a_secret = auth

    widgets['consumer_key'].value = c_key
    widgets['consumer_secret'].value = c_secret
    widgets['access_token'].value = a_key
    widgets['access_secret'].value = a_secret


class AweberSettingsEditForm(controlpanel.RegistryEditForm):
    """Form for configuring niteoweb.aweber."""

    schema = IAweberSettings
    label = _(u"Aweber settings")
    description = _(u"""Configure integration with Aweber API.<br>
    1. Enter App ID and click 'Get auth code'<br>
    2. Follow the link on top of the page<br>
    3. Enter your credentials
    and copy over authorization code to second field<br>
    4. Click second button to parse authorization code and update list names
    <br>
    5. Click Save button!
    """)

    @button.buttonAndHandler(_('Get auth code'), name='get_auth')
    def handle_get_auth_action(self, action):
        app_id = self.widgets['app_id'].value
        url = "https://auth.aweber.com/1.0/oauth/authorize_app/{0}".format(
            app_id
        )
        api.portal.show_message(
            message="Visit '{0}' and copy authorization code "
                    "to Authorization Code field".format(url),
            request=self.request
        )

    @button.buttonAndHandler(
        _('Parse auth code and update lists'),
        name='parse_auth'
    )
    def handle_parse_auth_action(self, action):
        parse_auth_code(self.widgets)
        set_list_names(self.widgets)
        self.reload_settings_page()

    @button.buttonAndHandler(_('Update lists only'), name='update_lists')
    def handle_update_lists_action(self, action):
        set_list_names(self.widgets)
        self.reload_settings_page()

    @button.buttonAndHandler(_('Subscribe new user'), name='subscribe_user')
    def handle_subscribe_user_action(self, action):
        try:
            aweberapi.subscribe_to_aweber_mailinglist(
                self.widgets['subscribe_email'].value,
                self.widgets['subscribe_fullname'].value,
            )
            self.widgets['subscribe_email'].value = ""
            self.widgets['subscribe_fullname'].value = ""
        except Exception as e:
            api.portal.show_message(
                message=e.message,
                request=self.request,
                type='error'
            )

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        super(AweberSettingsEditForm, self).handleSave(self, action)

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        super(AweberSettingsEditForm, self).handleCancel(self, action)

    def reload_settings_page(self):
        self.context.REQUEST.response.redirect(
            api.portal.get().absolute_url() + "/@@aweber-settings"
        )


class AweberSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = AweberSettingsEditForm
