from zope.publisher.interfaces import NotFound 

from zope.app import zapi 
from zope.app.container.traversal import ContainerTraverser 
from interfaces import ICaseInsensitiveFolder


class CaseInsensitiveFolderTraverser(ContainerTraverser):

    __used_for__ = ICaseInsensitiveFolder 

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.browser.IBrowserPublisher"""
        subob = self._guessTraverse(name)
        if subob is None:
            view = zapi.queryView(self.context, name, request)
            if view is not None:
                return view
  
            raise NotFound(self.context, name, request)
  
        return subob
  
    def _guessTraverse(self, name):
        import pdb; pdb.set_trace()
        for key in self.context.keys():
            if key.lower() == name.lower():
                return self.context[key]
        return None

