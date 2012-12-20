from zope.interface import Interface
from zope import schema


class IAweberSettings(Interface):

    consumer_key = schema.TextLine(
        title=u"Consumer Key",
    )
    consumer_secret = schema.TextLine(
        title=u"Consumer Secret",
    )
    access_token = schema.TextLine(
        title=u"Access Token",
    )
    access_secret = schema.TextLine(
        title=u"Access Secret",
    )
