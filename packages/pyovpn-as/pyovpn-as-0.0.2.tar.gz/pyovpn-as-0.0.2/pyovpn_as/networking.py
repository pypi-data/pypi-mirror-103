"""This module provides functions for managing the networking functionality of
   Access Server
"""
import ipaddress
import logging
from typing import Any

from pyovpn_as.api.cli import AccessServerClient

from . import exceptions
from . import utils


logger = logging.getLogger(__name__)


@utils.debug_log_call()
def assign_subnet_to_group(
    client: AccessServerClient,
    group: str,
    subnet: str
) -> None:
    """Assign a group to a specific subnet

    Users that are members of this group will be assigned an IP in the given subnet. Users in the group may not be assigned this IP immediately, and will need to disconnect and reconnect to be assigned the new IP.

    This function will restart the server in order to apply the changes

    Args:
        client (AccessServerClient): Client used to connect to RPC interface
        group (str): Group to apply subnet change to
        subnet (str): Subnet in CIDR format

    Raises:
        ValueError: Subnet definition is invalid
        AccessServerProfileNotFoundError: Group does not exist
        AccessServerProfileExistsError: Profile name given is not the name of a
            group
    """
    # Verify group exists
    profile_dict = client.UserPropGet(pfilt=[group,])
    group_profile = profile_dict.get(group)
    if group_profile is None:
        raise exceptions.AccessServerProfileNotFoundError(
            f'Group "{group}" does not exist on the server'
        )
    elif group_profile.get('type') != 'group':
        raise exceptions.AccessServerProfileExistsError(
            f'Profile "{group}" exists, but is not a group'
        )
    
    # Validate subnet ID
    network = ipaddress.ip_network(subnet, strict=True)
    if not isinstance(network, ipaddress.IPv4Network):
        raise ValueError('IP subnet CIDR must be an IPv4 network')
    if not network.is_private:
        raise ValueError('IP subnet range must be in a private network')

    # Assign subnet
    client.UserPropPut(
        group, 'group_subnets.0', str(network)
    )


