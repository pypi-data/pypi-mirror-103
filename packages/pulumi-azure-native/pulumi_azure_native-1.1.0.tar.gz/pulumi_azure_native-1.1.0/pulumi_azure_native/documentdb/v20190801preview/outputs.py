# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'PrivateEndpointPropertyResponse',
    'PrivateLinkServiceConnectionStatePropertyResponse',
]

@pulumi.output_type
class PrivateEndpointPropertyResponse(dict):
    """
    Private endpoint which the connection belongs to.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Private endpoint which the connection belongs to.
        :param str id: Resource id of the private endpoint.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource id of the private endpoint.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class PrivateLinkServiceConnectionStatePropertyResponse(dict):
    """
    Connection State of the Private Endpoint Connection.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionsRequired":
            suggest = "actions_required"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionStatePropertyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionStatePropertyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkServiceConnectionStatePropertyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions_required: str,
                 description: Optional[str] = None,
                 status: Optional[str] = None):
        """
        Connection State of the Private Endpoint Connection.
        :param str actions_required: Any action that is required beyond basic workflow (approve/ reject/ disconnect)
        :param str description: The private link service connection description.
        :param str status: The private link service connection status.
        """
        pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> str:
        """
        Any action that is required beyond basic workflow (approve/ reject/ disconnect)
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The private link service connection description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The private link service connection status.
        """
        return pulumi.get(self, "status")


