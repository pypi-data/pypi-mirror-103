# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'ApplicationArtifactResponse',
    'ApplicationAuthorizationResponse',
    'ApplicationBillingDetailsDefinitionResponse',
    'ApplicationClientDetailsResponse',
    'ApplicationDefinitionArtifactResponse',
    'ApplicationDeploymentPolicyResponse',
    'ApplicationJitAccessPolicyResponse',
    'ApplicationManagementPolicyResponse',
    'ApplicationNotificationEndpointResponse',
    'ApplicationNotificationPolicyResponse',
    'ApplicationPackageContactResponse',
    'ApplicationPackageLockingPolicyDefinitionResponse',
    'ApplicationPackageSupportUrlsResponse',
    'ApplicationPolicyResponse',
    'IdentityResponse',
    'JitApproverDefinitionResponse',
    'JitAuthorizationPoliciesResponse',
    'JitSchedulingPolicyResponse',
    'PlanResponse',
    'SkuResponse',
    'UserAssignedResourceIdentityResponse',
]

@pulumi.output_type
class ApplicationArtifactResponse(dict):
    """
    Managed application artifact.
    """
    def __init__(__self__, *,
                 name: str,
                 type: str,
                 uri: str):
        """
        Managed application artifact.
        :param str name: The managed application artifact name.
        :param str type: The managed application artifact type.
        :param str uri: The managed application artifact blob uri.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The managed application artifact name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The managed application artifact type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The managed application artifact blob uri.
        """
        return pulumi.get(self, "uri")


@pulumi.output_type
class ApplicationAuthorizationResponse(dict):
    """
    The managed application provider authorization.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "roleDefinitionId":
            suggest = "role_definition_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationAuthorizationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationAuthorizationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationAuthorizationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 role_definition_id: str):
        """
        The managed application provider authorization.
        :param str principal_id: The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the managed application resources.
        :param str role_definition_id: The provider's role definition identifier. This role will define all the permissions that the provider must have on the managed application's container resource group. This role definition cannot have permission to delete the resource group.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the managed application resources.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The provider's role definition identifier. This role will define all the permissions that the provider must have on the managed application's container resource group. This role definition cannot have permission to delete the resource group.
        """
        return pulumi.get(self, "role_definition_id")


@pulumi.output_type
class ApplicationBillingDetailsDefinitionResponse(dict):
    """
    Managed application billing details definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceUsageId":
            suggest = "resource_usage_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationBillingDetailsDefinitionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationBillingDetailsDefinitionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationBillingDetailsDefinitionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 resource_usage_id: Optional[str] = None):
        """
        Managed application billing details definition.
        :param str resource_usage_id: The managed application resource usage Id.
        """
        if resource_usage_id is not None:
            pulumi.set(__self__, "resource_usage_id", resource_usage_id)

    @property
    @pulumi.getter(name="resourceUsageId")
    def resource_usage_id(self) -> Optional[str]:
        """
        The managed application resource usage Id.
        """
        return pulumi.get(self, "resource_usage_id")


@pulumi.output_type
class ApplicationClientDetailsResponse(dict):
    """
    The application client details to track the entity creating/updating the managed app resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationClientDetailsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationClientDetailsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationClientDetailsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: Optional[str] = None,
                 oid: Optional[str] = None,
                 puid: Optional[str] = None):
        """
        The application client details to track the entity creating/updating the managed app resource.
        :param str application_id: The client application Id.
        :param str oid: The client Oid.
        :param str puid: The client Puid
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if oid is not None:
            pulumi.set(__self__, "oid", oid)
        if puid is not None:
            pulumi.set(__self__, "puid", puid)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        """
        The client application Id.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter
    def oid(self) -> Optional[str]:
        """
        The client Oid.
        """
        return pulumi.get(self, "oid")

    @property
    @pulumi.getter
    def puid(self) -> Optional[str]:
        """
        The client Puid
        """
        return pulumi.get(self, "puid")


@pulumi.output_type
class ApplicationDefinitionArtifactResponse(dict):
    """
    Application definition artifact.
    """
    def __init__(__self__, *,
                 name: str,
                 type: str,
                 uri: str):
        """
        Application definition artifact.
        :param str name: The managed application definition artifact name.
        :param str type: The managed application definition artifact type.
        :param str uri: The managed application definition artifact blob uri.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The managed application definition artifact name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The managed application definition artifact type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The managed application definition artifact blob uri.
        """
        return pulumi.get(self, "uri")


@pulumi.output_type
class ApplicationDeploymentPolicyResponse(dict):
    """
    Managed application deployment policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deploymentMode":
            suggest = "deployment_mode"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationDeploymentPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationDeploymentPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationDeploymentPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 deployment_mode: str):
        """
        Managed application deployment policy.
        :param str deployment_mode: The managed application deployment mode.
        """
        pulumi.set(__self__, "deployment_mode", deployment_mode)

    @property
    @pulumi.getter(name="deploymentMode")
    def deployment_mode(self) -> str:
        """
        The managed application deployment mode.
        """
        return pulumi.get(self, "deployment_mode")


@pulumi.output_type
class ApplicationJitAccessPolicyResponse(dict):
    """
    Managed application Jit access policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "jitAccessEnabled":
            suggest = "jit_access_enabled"
        elif key == "jitApprovalMode":
            suggest = "jit_approval_mode"
        elif key == "jitApprovers":
            suggest = "jit_approvers"
        elif key == "maximumJitAccessDuration":
            suggest = "maximum_jit_access_duration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationJitAccessPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationJitAccessPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationJitAccessPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 jit_access_enabled: bool,
                 jit_approval_mode: Optional[str] = None,
                 jit_approvers: Optional[Sequence['outputs.JitApproverDefinitionResponse']] = None,
                 maximum_jit_access_duration: Optional[str] = None):
        """
        Managed application Jit access policy.
        :param bool jit_access_enabled: Whether the JIT access is enabled.
        :param str jit_approval_mode: JIT approval mode.
        :param Sequence['JitApproverDefinitionResponse'] jit_approvers: The JIT approvers
        :param str maximum_jit_access_duration: The maximum duration JIT access is granted. This is an ISO8601 time period value.
        """
        pulumi.set(__self__, "jit_access_enabled", jit_access_enabled)
        if jit_approval_mode is not None:
            pulumi.set(__self__, "jit_approval_mode", jit_approval_mode)
        if jit_approvers is not None:
            pulumi.set(__self__, "jit_approvers", jit_approvers)
        if maximum_jit_access_duration is not None:
            pulumi.set(__self__, "maximum_jit_access_duration", maximum_jit_access_duration)

    @property
    @pulumi.getter(name="jitAccessEnabled")
    def jit_access_enabled(self) -> bool:
        """
        Whether the JIT access is enabled.
        """
        return pulumi.get(self, "jit_access_enabled")

    @property
    @pulumi.getter(name="jitApprovalMode")
    def jit_approval_mode(self) -> Optional[str]:
        """
        JIT approval mode.
        """
        return pulumi.get(self, "jit_approval_mode")

    @property
    @pulumi.getter(name="jitApprovers")
    def jit_approvers(self) -> Optional[Sequence['outputs.JitApproverDefinitionResponse']]:
        """
        The JIT approvers
        """
        return pulumi.get(self, "jit_approvers")

    @property
    @pulumi.getter(name="maximumJitAccessDuration")
    def maximum_jit_access_duration(self) -> Optional[str]:
        """
        The maximum duration JIT access is granted. This is an ISO8601 time period value.
        """
        return pulumi.get(self, "maximum_jit_access_duration")


@pulumi.output_type
class ApplicationManagementPolicyResponse(dict):
    """
    Managed application management policy.
    """
    def __init__(__self__, *,
                 mode: Optional[str] = None):
        """
        Managed application management policy.
        :param str mode: The managed application management mode.
        """
        if mode is not None:
            pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        The managed application management mode.
        """
        return pulumi.get(self, "mode")


@pulumi.output_type
class ApplicationNotificationEndpointResponse(dict):
    """
    Managed application notification endpoint.
    """
    def __init__(__self__, *,
                 uri: str):
        """
        Managed application notification endpoint.
        :param str uri: The managed application notification endpoint uri.
        """
        pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The managed application notification endpoint uri.
        """
        return pulumi.get(self, "uri")


@pulumi.output_type
class ApplicationNotificationPolicyResponse(dict):
    """
    Managed application notification policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "notificationEndpoints":
            suggest = "notification_endpoints"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationNotificationPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationNotificationPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationNotificationPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 notification_endpoints: Sequence['outputs.ApplicationNotificationEndpointResponse']):
        """
        Managed application notification policy.
        :param Sequence['ApplicationNotificationEndpointResponse'] notification_endpoints: The managed application notification endpoint.
        """
        pulumi.set(__self__, "notification_endpoints", notification_endpoints)

    @property
    @pulumi.getter(name="notificationEndpoints")
    def notification_endpoints(self) -> Sequence['outputs.ApplicationNotificationEndpointResponse']:
        """
        The managed application notification endpoint.
        """
        return pulumi.get(self, "notification_endpoints")


@pulumi.output_type
class ApplicationPackageContactResponse(dict):
    """
    The application package contact information.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "contactName":
            suggest = "contact_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationPackageContactResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationPackageContactResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationPackageContactResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 email: str,
                 phone: str,
                 contact_name: Optional[str] = None):
        """
        The application package contact information.
        :param str email: The contact email.
        :param str phone: The contact phone number.
        :param str contact_name: The contact name.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "phone", phone)
        if contact_name is not None:
            pulumi.set(__self__, "contact_name", contact_name)

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        The contact email.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def phone(self) -> str:
        """
        The contact phone number.
        """
        return pulumi.get(self, "phone")

    @property
    @pulumi.getter(name="contactName")
    def contact_name(self) -> Optional[str]:
        """
        The contact name.
        """
        return pulumi.get(self, "contact_name")


@pulumi.output_type
class ApplicationPackageLockingPolicyDefinitionResponse(dict):
    """
    Managed application locking policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allowedActions":
            suggest = "allowed_actions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationPackageLockingPolicyDefinitionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationPackageLockingPolicyDefinitionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationPackageLockingPolicyDefinitionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allowed_actions: Optional[Sequence[str]] = None):
        """
        Managed application locking policy.
        :param Sequence[str] allowed_actions: The deny assignment excluded actions.
        """
        if allowed_actions is not None:
            pulumi.set(__self__, "allowed_actions", allowed_actions)

    @property
    @pulumi.getter(name="allowedActions")
    def allowed_actions(self) -> Optional[Sequence[str]]:
        """
        The deny assignment excluded actions.
        """
        return pulumi.get(self, "allowed_actions")


@pulumi.output_type
class ApplicationPackageSupportUrlsResponse(dict):
    """
    The appliance package support URLs.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "governmentCloud":
            suggest = "government_cloud"
        elif key == "publicAzure":
            suggest = "public_azure"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationPackageSupportUrlsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationPackageSupportUrlsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationPackageSupportUrlsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 government_cloud: Optional[str] = None,
                 public_azure: Optional[str] = None):
        """
        The appliance package support URLs.
        :param str government_cloud: The government cloud support URL.
        :param str public_azure: The public azure support URL.
        """
        if government_cloud is not None:
            pulumi.set(__self__, "government_cloud", government_cloud)
        if public_azure is not None:
            pulumi.set(__self__, "public_azure", public_azure)

    @property
    @pulumi.getter(name="governmentCloud")
    def government_cloud(self) -> Optional[str]:
        """
        The government cloud support URL.
        """
        return pulumi.get(self, "government_cloud")

    @property
    @pulumi.getter(name="publicAzure")
    def public_azure(self) -> Optional[str]:
        """
        The public azure support URL.
        """
        return pulumi.get(self, "public_azure")


@pulumi.output_type
class ApplicationPolicyResponse(dict):
    """
    Managed application policy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "policyDefinitionId":
            suggest = "policy_definition_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 parameters: Optional[str] = None,
                 policy_definition_id: Optional[str] = None):
        """
        Managed application policy.
        :param str name: The policy name
        :param str parameters: The policy parameters.
        :param str policy_definition_id: The policy definition Id.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if policy_definition_id is not None:
            pulumi.set(__self__, "policy_definition_id", policy_definition_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The policy name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[str]:
        """
        The policy parameters.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> Optional[str]:
        """
        The policy definition Id.
        """
        return pulumi.get(self, "policy_definition_id")


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserAssignedResourceIdentityResponse']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: The identity type.
        :param Mapping[str, 'UserAssignedResourceIdentityResponse'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

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

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserAssignedResourceIdentityResponse']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class JitApproverDefinitionResponse(dict):
    """
    JIT approver definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in JitApproverDefinitionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        JitApproverDefinitionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        JitApproverDefinitionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 display_name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        JIT approver definition.
        :param str id: The approver service principal Id.
        :param str display_name: The approver display name.
        :param str type: The approver type.
        """
        pulumi.set(__self__, "id", id)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The approver service principal Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The approver display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The approver type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class JitAuthorizationPoliciesResponse(dict):
    """
    The JIT authorization policies.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "roleDefinitionId":
            suggest = "role_definition_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in JitAuthorizationPoliciesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        JitAuthorizationPoliciesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        JitAuthorizationPoliciesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 role_definition_id: str):
        """
        The JIT authorization policies.
        :param str principal_id: The the principal id that will be granted JIT access.
        :param str role_definition_id: The role definition id that will be granted to the Principal.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The the principal id that will be granted JIT access.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The role definition id that will be granted to the Principal.
        """
        return pulumi.get(self, "role_definition_id")


@pulumi.output_type
class JitSchedulingPolicyResponse(dict):
    """
    The JIT scheduling policies.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in JitSchedulingPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        JitSchedulingPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        JitSchedulingPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 duration: str,
                 start_time: str,
                 type: str):
        """
        The JIT scheduling policies.
        :param str start_time: The start time of the request.
        :param str type: The type of JIT schedule.
        """
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "start_time", start_time)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def duration(self) -> str:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        The start time of the request.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of JIT schedule.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class PlanResponse(dict):
    """
    Plan for the managed application.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "promotionCode":
            suggest = "promotion_code"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PlanResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PlanResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PlanResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 product: str,
                 publisher: str,
                 version: str,
                 promotion_code: Optional[str] = None):
        """
        Plan for the managed application.
        :param str name: The plan name.
        :param str product: The product code.
        :param str publisher: The publisher ID.
        :param str version: The plan's version.
        :param str promotion_code: The promotion code.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "product", product)
        pulumi.set(__self__, "publisher", publisher)
        pulumi.set(__self__, "version", version)
        if promotion_code is not None:
            pulumi.set(__self__, "promotion_code", promotion_code)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The plan name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> str:
        """
        The product code.
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter
    def publisher(self) -> str:
        """
        The publisher ID.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The plan's version.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="promotionCode")
    def promotion_code(self) -> Optional[str]:
        """
        The promotion code.
        """
        return pulumi.get(self, "promotion_code")


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU for the resource.
    """
    def __init__(__self__, *,
                 name: str,
                 capacity: Optional[int] = None,
                 family: Optional[str] = None,
                 model: Optional[str] = None,
                 size: Optional[str] = None,
                 tier: Optional[str] = None):
        """
        SKU for the resource.
        :param str name: The SKU name.
        :param int capacity: The SKU capacity.
        :param str family: The SKU family.
        :param str model: The SKU model.
        :param str size: The SKU size.
        :param str tier: The SKU tier.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if model is not None:
            pulumi.set(__self__, "model", model)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The SKU name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The SKU capacity.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> Optional[str]:
        """
        The SKU family.
        """
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def model(self) -> Optional[str]:
        """
        The SKU model.
        """
        return pulumi.get(self, "model")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        The SKU size.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The SKU tier.
        """
        return pulumi.get(self, "tier")


@pulumi.output_type
class UserAssignedResourceIdentityResponse(dict):
    """
    Represents the user assigned identity that is contained within the UserAssignedIdentities dictionary on ResourceIdentity
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedResourceIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedResourceIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserAssignedResourceIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str):
        """
        Represents the user assigned identity that is contained within the UserAssignedIdentities dictionary on ResourceIdentity
        :param str principal_id: The principal id of user assigned identity.
        :param str tenant_id: The tenant id of user assigned identity.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id of user assigned identity.
        """
        return pulumi.get(self, "tenant_id")


