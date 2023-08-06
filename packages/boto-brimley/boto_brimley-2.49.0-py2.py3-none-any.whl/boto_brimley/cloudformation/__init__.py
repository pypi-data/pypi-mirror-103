# Copyright (c) 2010-2011 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2010-2011, Eucalyptus Systems, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto_brimley.cloudformation.connection import CloudFormationConnection
from boto_brimley.regioninfo import RegionInfo, get_regions, load_regions
from boto_brimley.regioninfo import connect

RegionData = load_regions().get('cloudformation')


def regions():
    """
    Get all available regions for the CloudFormation service.

    :rtype: list
    :return: A list of :class:`botobrimley.RegionInfo` instances
    """
    return get_regions(
        'cloudformation',
        connection_cls=CloudFormationConnection
    )


def connect_to_region(region_name, **kw_params):
    """
    Given a valid region name, return a
    :class:`botobrimley.cloudformation.CloudFormationConnection`.

    :param str region_name: The name of the region to connect to.

    :rtype: :class:`botobrimley.cloudformation.CloudFormationConnection` or ``None``
    :return: A connection to the given region, or None if an invalid region
        name is given
    """
    return connect('cloudformation', region_name,
                   connection_cls=CloudFormationConnection, **kw_params)
