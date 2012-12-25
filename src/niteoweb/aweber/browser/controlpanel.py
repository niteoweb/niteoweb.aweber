# -*- coding: utf-8 -*-
"""
Aweber control panel configlet
------------------------------
"""

from niteoweb.aweber import AweberMessageFactory as _
from niteoweb.aweber.interfaces import IAweberSettings
from plone.app.registry.browser import controlpanel
from z3c.form import button
from zope.schema.vocabulary import SimpleVocabulary


def list_names():
    terms = []
    terms.append(SimpleVocabulary.createTerm(1, str(1), "one"))
    terms.append(SimpleVocabulary.createTerm(2, str(2), "two"))
    return SimpleVocabulary(terms)


class AweberSettingsEditForm(controlpanel.RegistryEditForm):
    """Form for configuring niteoweb.aweber."""

    schema = IAweberSettings
    label = _(u"Aweber settings")
    description = _(u"""Configure integration with Aweber API.""")

    @button.buttonAndHandler(_('Get access'), name='get_access')
    def handle_get_access_action(self, action):
        super(AweberSettingsEditForm, self).updateWidgets()

        print "##### CONSUMER INFO #####\nkey:{0}, secret:{1}".format(
            self.widgets['consumer_key'].value,
            self.widgets['consumer_key'].value
        )

        self.widgets['access_token'].value = unicode("token3253545445")
        self.widgets['access_secret'].value = unicode("secret2453t30960")

    @button.buttonAndHandler(_('Get list names'), name='get_lists')
    def handle_get_lists_action(self, action):
        self.widgets['list_name'].field.vocabulary = list_names()
        super(AweberSettingsEditForm, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        super(AweberSettingsEditForm, self).handleSave(self, action)

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        super(AweberSettingsEditForm, self).handleCancel(self, action)


class AweberSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = AweberSettingsEditForm
