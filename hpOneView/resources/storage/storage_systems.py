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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'storage-systems'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class StorageSystems(object):
    URI = '/rest/storage-systems'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets information about all managed storage systems. Filtering and sorting are supported with the retrieval of
        managed storage systems. The following storage system attributes can be used with filtering and sorting
        operation: name, model, serialNumber, firmware, status, managedDomain, and state.

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
            list: A list of all managed storage systems
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def add(self, resource, timeout=-1):
        """
        Adds a storage system for management by the appliance. The storage system resource created will be in a
        "Connected" state and will not yet be available for further operations. Users are required to perform a PUT API
        on the storage system resource to complete the management of the storage system resource. An asynchronous task
        will be created as a result of this API call to discover available domains, target ports, and storage pools.
        Args:
            resource (dict): Object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Created storage system.

        """
        return self._client.create(resource, timeout=timeout)

    def get_host_types(self):
        """
        Gets the list of supported host types.

        Returns:
            list: host types
        """
        uri = self.URI + "/host-types"
        return self._client.get(uri)

    def get_storage_pools(self, id_or_uri):
        """
        Gets a list of Storage pools. Returns a list of storage pools belonging to the storage system referred by the
        Path property parameters--id (serial number) or uri. Filters are supported for the following storage pool
        attributes only - name, domain, deviceSpeed, deviceType, supprtedRAIDLevel, status and state.

        Args:
            id_or_uri: Could be either the storage system id (serial number) or the storage system uri
        Returns:
            dict: host types
        """
        uri = self._client.build_uri(id_or_uri) + "/storage-pools"
        return self._client.get(uri)

    def get(self, id_or_uri):
        """
        Gets the specified storage system resource by ID or by uri
        Args:
            id_or_uri: Could be either the storage system id or the storage system uri

        Returns:
            dict: The storage system
        """
        return self._client.get(id_or_uri)

    def update(self, resource, timeout=-1):
        """
        Updates the storage system. To complete the action of adding a storage system for management by the appliance,
        this must be called after create() of a storage system.
        This method can be used to update storage system credentials, storage system attributes or to request a refresh
        of storage system. For updating credentials, users are allowed to update IP/hostname, username, and password.
        To request a refresh of a storage system user must set the "refreshState" attribute to RefreshPending state.
        Args:
            resource (dict): Object to update
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Updated storage system.
        """
        return self._client.update(resource, timeout=timeout)

    def remove(self, resource, force=False, timeout=-1):
        """
        Removes the storage system from OneView

        Args:
            resource (dict): object to delete
            force (bool):
                 If set to true the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Details of associated resource

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_managed_ports(self, id_or_uri, port_id_or_uri=''):
        """
        Gets all ports or a specific managed target port for the specified storage system

        Args:
            id_or_uri: Could be either the storage system id or the storage system uri
            port_id_or_uri: Could be either the port id or the port uri

        Returns:
            dict: managed ports
        """
        if port_id_or_uri:
            uri = self._client.build_uri(port_id_or_uri)
            if "/managedPorts" not in uri:
                uri = self._client.build_uri(
                    id_or_uri) + "/managedPorts" + "/" + port_id_or_uri

        else:
            uri = self._client.build_uri(id_or_uri) + "/managedPorts"

        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Get all storage systems that match the filter
        The search is case insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns: dict of storage systems

        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Retrieve a resource by his name
        Args:
            name: resource name

        Returns: dict
        """
        return self._client.get_by_name(name=name)

    def get_by_ip_hostname(self, ip_hostname):
        """
        Retrieve a storage system by his IP
        Args:
            ip_hostname: storage system IP or hostname

        Returns: dict
        """
        resources = self._client.get_all()

        resources_filtered = [x for x in resources if x['credentials']['ip_hostname'] == ip_hostname]

        if resources_filtered:
            return resources_filtered[0]
        else:
            return None
