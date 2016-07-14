# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'firmware-driver'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class FirmwareDrivers(object):

    URI = '/rest/firmware-drivers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Enclosures. The collection is based on optional sorting and filtering, and
        constrained by start and count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items.
                The actual number of items in the response may differ from the requested
                count if the sum of start and count exceed the total number of items, or
                if returning the requested number of items would take too long.
            filter:
                A general filter/query string to narrow the list of items returned. The
                default is no filter - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: list of firmware baseline resources

        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get_by(self, field, value):
        """
        Gets the list of firmware baseline resources managed by the appliance. Optional parameters can be used to
        filter the list of resources returned.
        The search is case insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: list of firmware baseline resources

        """
        firmwares = self.get_all()
        matches = []
        for item in firmwares:
            if item.get(field) == value:
                matches.append(item)
        return matches

    def get_by_file_name(self, file_name):
        """
        Gets a firmware resource with match the file name.

        Args:
            file_name: file name to filter (without path)
        Returns:
            dict: firmware baseline resource

        """
        firmwares = self.get_all()
        for firmware in firmwares:
            if firmware['fwComponents'][0]['fileName'] == file_name:
                return firmware
        return None

    def get(self, id_or_uri):
        """
        Gets the individual firmware baseline resource for the given URI. Note that the view
        parameter is not currently supported.
        Args:
            id: ID or URI of firmware baseline resource

        Returns:
            dict: firmware baseline resource
        """
        return self._client.get(id_or_uri)

    def delete(self, resource, force=False, timeout=-1):
        """
        Delete the firmware baseline resource with the specified id. If force is set to true, the firmware baseline
        resource will be deleted even if it is assigned to devices.

        Args:
            resource: dict object to delete
            force:
                If set to true the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            bool:
        """
        return self._client.delete(resource, force=force, timeout=timeout)
