from ftw.dashboard.portlets.postit import _
from ftw_formhelper import ftwNullAddForm
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.app.portlets.utils import assignment_from_key
from plone.memoize.compress import xhtml_compress
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.utils import unhashPortletInfo
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions import Unauthorized
from zope.component import getUtility
from zope.interface import implements


# Try to get the plone.protect's createToken method, because it's only
# available since version 2.0.2, otherwise we just use a mocked method.
try:
    from plone.protect import createToken
except ImportError:
    def createToken():
        return ''


class IPostItPortlet(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(IPostItPortlet)

    def __init__(self, *args, **kwargs):
        super(Assignment, self).__init__(self, *args, **kwargs)
        self.notes = []

    @property
    def title(self):
        return _(u"Post-it")


def _render_cachekey(fun, self):
    return render_cachekey(fun, self)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/postit.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.data = data

    def notes(self):
        return self.data.notes

    # XXX: @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def title(self):
        return self.data.title

    def authenticator_token(self):
        return createToken()


class AddForm(ftwNullAddForm):

    def create(self):
        return Assignment()


def get_column_and_portlet(context, portlet_info):
    # get column
    column_manager = getUtility(IPortletManager, name=portlet_info['manager'])
    userid = context.portal_membership.getAuthenticatedMember().getId()
    column = column_manager.get(USER_CATEGORY, {}).get(userid, {})

    # get portlet
    portlet = column.get(portlet_info['name'])
    if not portlet:
        portlet = assignment_from_key(context,
                                      portlet_info['manager'],
                                      portlet_info['category'],
                                      portlet_info['key'],
                                      portlet_info['name'])
    return column, portlet


class AddNote(BrowserView):

    def __call__(self, *args, **kwargs):
        value = str(self.request.get('note'))
        hash_ = self.request.get('hash')
        # get postit portlet
        portlet_info = unhashPortletInfo(hash_)
        userid = portlet_info['key']
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if userid != member.getId():
            raise Unauthorized

        column, portlet = get_column_and_portlet(self.context, portlet_info)
        # store data
        notes = portlet.notes[:]
        notes.append(value)
        portlet.notes = notes[:]


class RemoveNote(BrowserView):

    def __call__(self, *args, **kwargs):
        hash = self.request.get('hash')
        index = int(self.request.get('index'))
        # get postit portlet
        portlet_info = unhashPortletInfo(hash)
        column, portlet = get_column_and_portlet(self.context, portlet_info)
        # remove note
        notes = portlet.notes[:]
        notes = notes[0:index] + notes[index + 1:]
        portlet.notes = notes[:]
