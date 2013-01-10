from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from plone import api


class ListsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        try:
            lists_record = api.portal.get_registry_record(
                'niteoweb.aweber.available_lists_record'
            )
            if lists_record:
                return SimpleVocabulary.fromValues(lists_record)
        except KeyError:
            pass
        return SimpleVocabulary.fromValues([])

grok.global_utility(
    ListsVocabulary,
    name="niteoweb.aweber.available_lists_vocabulary",
)


class IAweberSettings(Interface):

    app_id = schema.TextLine(
        title=u"App ID",
        required=False,
    )

    authorization_code = schema.TextLine(
        title=u"Authorization Code",
        required=False,
    )

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

    list_name = schema.Choice(
        title=u"List Name",
        vocabulary="niteoweb.aweber.available_lists_vocabulary",
        required=False,
    )
