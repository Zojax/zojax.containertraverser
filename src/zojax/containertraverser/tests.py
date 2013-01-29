##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" zojax.containertraverser tests

$Id$
"""
__docformat__ = "reStructuredText"

import unittest
from zope.app.container.tests import test_containertraverser
from traverser import CaseInsensitiveFolderTraverser
from interfaces import ICaseInsensitiveConfiglet
from zope.component import getGlobalSiteManager

from zope.interface import implements



class Container(test_containertraverser.TestContainer):

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, name):
        return self.__dict__[name]

class InsensitiveCaseTraverserTest(test_containertraverser.TraverserTest):
  
    def setUp(self):
        return super(InsensitiveCaseTraverserTest, self).setUp()
  
    def _getTraverser(self, context, request):
        class FakeCaseInsensitiveConfiglet(object):
            implements(ICaseInsensitiveConfiglet)
            isNonCaseInsensitive = True

        gsm = getGlobalSiteManager()
        fakeCIC = FakeCaseInsensitiveConfiglet()
        gsm.registerUtility(fakeCIC)
        return CaseInsensitiveFolderTraverser(context, request)

    def _getContainer(self, **kw):
        return Container(**kw)

    def test_allLowerCaseItemTraversal(self):
        self.assertEquals(
                self.traverser.publishTraverse(self.request, 'foo'),
                self.traverser.publishTraverse(self.request, 'FOO'))
  
    def test_allLowerCaseViewTraversal(self):
        self.assertEquals(
                self.traverser.publishTraverse(self.request, 'viewfoo').__class__,
                self.traverser.publishTraverse(self.request, 'VIEWFOO').__class__)
  
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(InsensitiveCaseTraverserTest),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
