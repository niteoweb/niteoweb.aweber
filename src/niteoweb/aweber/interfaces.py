from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


#@grok.provider(IContextSourceBinder)
#def list_names(context):
def list_names():
    terms = []
    terms.append(SimpleVocabulary.createTerm(1, str(1), "one"))
    terms.append(SimpleVocabulary.createTerm(2, str(2), "two"))
    return SimpleVocabulary(terms)


class IAweberSettings(Interface):

    consumer_key = schema.TextLine(
        title=u"Consumer Key",
    )

    consumer_secret = schema.TextLine(
        title=u"Consumer Secret",
    )

    access_token = schema.TextLine(
        title=u"Access Token",
        required=False,
    )

    access_secret = schema.TextLine(
        title=u"Access Secret",
        required=False,
    )

    list_name = schema.Choice(
        title=u"List Name",
        values=["empty"],
        required=False,
    )
