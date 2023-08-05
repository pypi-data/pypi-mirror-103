# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'ManagedIdentityResponse',
    'MyManagedIdentityResponse',
    'MyUserAssignedIdentitiesResponse',
    'UserAssignedIdentitiesResponse',
]

@pulumi.output_type
class ManagedIdentityResponse(dict):
    """
    Customer Managed Identity
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional['outputs.UserAssignedIdentitiesResponse'] = None):
        """
        Customer Managed Identity
        :param str type: The identity type.
        :param 'UserAssignedIdentitiesResponse' user_assigned_identities: Customer Managed Identity
        """
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional['outputs.UserAssignedIdentitiesResponse']:
        """
        Customer Managed Identity
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class MyManagedIdentityResponse(dict):
    """
    Customer Managed Identity
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MyManagedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MyManagedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MyManagedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional['outputs.MyUserAssignedIdentitiesResponse'] = None):
        """
        Customer Managed Identity
        :param str type: The identity type.
        :param 'MyUserAssignedIdentitiesResponse' user_assigned_identities: Customer Managed Identity
        """
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional['outputs.MyUserAssignedIdentitiesResponse']:
        """
        Customer Managed Identity
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class MyUserAssignedIdentitiesResponse(dict):
    """
    Customer Managed Identity
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MyUserAssignedIdentitiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MyUserAssignedIdentitiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MyUserAssignedIdentitiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str):
        """
        Customer Managed Identity
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class UserAssignedIdentitiesResponse(dict):
    """
    Customer Managed Identity
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedIdentitiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedIdentitiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserAssignedIdentitiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str,
                 tenant_id: str):
        """
        Customer Managed Identity
        :param str client_id: The client ID of resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client ID of resource.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")


