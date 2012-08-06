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
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('zojax.containertraverser')


class ICaseInsensitiveConfiglet(interface.Interface):
    """ container traverser configlet schema """

    isNonCaseInsensitive = schema.Bool(
        title = _('Enable portal case insensitive traverser'),
        default = False,
        required = True)

class ICaseInsensitiveFolder(ISimpleReadContainer):
     """Marker for folders whose contained items keys are case insensitive.

     When traversing in this folder, all names will be converted to lower
     case. For example, if the traverser requests an item called `Foo`, in
     reality the first item matching `foo` or any upper-and-lowercase
     variants are looked up in the container."""
 
