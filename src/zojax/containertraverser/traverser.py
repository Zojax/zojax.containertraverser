from zope.publisher.interfaces import NotFound 

from zope.app import zapi 
from zope.app.container.traversal import ContainerTraverser, ItemTraverser
from interfaces import ICaseInsensitiveFolder, ICaseInsensitiveConfiglet
from zope.component import getUtility
from z3c.traverser.traverser import ContainerTraverserPlugin, PluggableTraverser, BasePluggableTraverser
from z3c.traverser.interfaces import IPluggableTraverser
from zope.interface import implements
from zope.component import subscribers, queryAdapter, queryMultiAdapter
from zope.app.publication.publicationtraverse import PublicationTraverser


from zope.publisher.interfaces import NotFound
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
            if subob is not None:
                 return subob
        return super(CaseInsensitiveFolderTraverser, self).publishTraverse(request, name)
  
    def _guessTraverse(self, name):
        for key in self.context.keys():
            if key.lower() == name.lower():
                return self.context[key]
        return None

def patchedTraverseName(self, request, ob, name):
    nm = name # the name to look up the object with
    if name and name[:1] in '@+':
        # Process URI segment parameters.
        ns, nm = nsParse(name)
        if ns:
            try:
                ob2 = namespaceLookup(ns, nm, ob, request)
            except TraversalError:
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

