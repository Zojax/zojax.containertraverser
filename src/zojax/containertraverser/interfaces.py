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
""" zojax.containertraverser interfaces

$Id$
"""
from zope.publisher.interfaces import INotFound
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import ISimpleReadContainer
from zope.interface import Interface

_ = MessageFactory('zojax.containertraverser')


class IContainerTraverserConfiglet(interface.Interface):
    """ container traverser configlet schema """

    isNonCaseSencetiveTraverser = schema.Bool(
        title = _('Enabled portal non case censative traverser'),
        default = False,
        required = True)

