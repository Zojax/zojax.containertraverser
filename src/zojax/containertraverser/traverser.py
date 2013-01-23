from zope.publisher.interfaces import NotFound 

from zope.app import zapi 
from zope.app.container.traversal import ContainerTraverser
from interfaces import ICaseInsensitiveFolder, ICaseInsensitiveConfiglet
from zope.component import getUtility, queryMultiAdapter
from zope.interface import Interface, providedBy
from zope.app.apidoc.presentation import getViews

from zope.security.checker import ProxyFactory
from zope.security.proxy import removeSecurityProxy
from zope.traversing.namespace import namespaceLookup
from zope.traversing.namespace import nsParse
from zope.traversing.interfaces import TraversalError
from zope.publisher.interfaces import IPublishTraverse


class CaseInsensitiveFolderTraverser(ContainerTraverser):

    __used_for__ = ICaseInsensitiveFolder 

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.browser.IBrowserPublisher"""
        if getUtility(ICaseInsensitiveConfiglet).isNonCaseInsensitive:
            subob = self._guessTraverse(name)
            if subob is None:
                view_name = self._guessTraverseView(name)
                view = queryMultiAdapter((self.context, request), name=view_name)
                if view is not None:
                    return view 
            return subob

        return super(CaseInsensitiveFolderTraverser, self).publishTraverse(request, name)
  
    def _guessTraverse(self, name):
        for key in getattr(self.context, 'keys', list)():
            if key.lower() == name.lower():
                return self.context[key]
        return None

    def _guessTraverseView(self, name):
        for view in getViews(providedBy(self.context), Interface):
            if view.name.lower() == name.lower():
                return view.name
        return None

def patchedTraverseName(self, request, ob, name):
    nm = name # the name to look up the object with
    if name and name[:1] in '@+':
        # Process URI segment parameters.
        ns, nm = nsParse(name)
        if ns:
            try:
                ob2 = namespaceLookup(ns, nm, ob, request)
            except (TraversalError, ValueError), e:
                raise NotFound(ob, name)

            return ProxyFactory(ob2)

    if nm == '.':
        return ob

    if IPublishTraverse.providedBy(ob):
        ob2 = ob.publishTraverse(request, nm)
    else:
        # self is marker
        adapter = queryMultiAdapter((ob, request), IPublishTraverse,
                                    default=self)
        if adapter is not self:
            if getUtility(ICaseInsensitiveConfiglet).isNonCaseInsensitive:
                try:
                    for key in removeSecurityProxy(ob).keys():
                        if key.lower() == name.lower():
                            nm = key
                except AttributeError:
                    pass
            ob2 = adapter.publishTraverse(request, nm)
        else:
            raise NotFound(ob, name, request)

    return ProxyFactory(ob2)

