from zope.publisher.interfaces import NotFound 

from zope.app import zapi 
from zope.app.container.traversal import ContainerTraverser 
from interfaces import ICaseInsensitiveFolder, ICaseInsensitiveConfiglet
from zope.component import getUtility


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

