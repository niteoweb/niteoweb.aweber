# -*- coding: utf-8 -*-
"""
Aweber control panel configlet
------------------------------
"""

from niteoweb.aweber import AweberMessageFactory as _
from niteoweb.aweber.interfaces import IAweberSettings
from plone.app.registry.browser import controlpanel


class AweberSettingsEditForm(controlpanel.RegistryEditForm):
    """Form for configuring niteoweb.aweber."""

    schema = IAweberSettings
    label = _(u"Aweber settings")
    description = _(u"""Configure integration with Aweber API.""")


class AweberSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = AweberSettingsEditForm
