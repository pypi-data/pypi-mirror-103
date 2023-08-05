# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AccessReviewInstanceArgs',
    'AccessReviewReviewerArgs',
    'IdentityArgs',
    'ManagementLockOwnerArgs',
    'NonComplianceMessageArgs',
    'ParameterDefinitionsValueArgs',
    'ParameterDefinitionsValueMetadataArgs',
    'ParameterValuesValueArgs',
    'PermissionArgs',
    'PolicyDefinitionGroupArgs',
    'PolicyDefinitionReferenceArgs',
]

@pulumi.input_type
class AccessReviewInstanceArgs:
    def __init__(__self__, *,
                 end_date_time: Optional[pulumi.Input[str]] = None,
                 start_date_time: Optional[pulumi.Input[str]] = None):
        """
        Access Review Instance.
        :param pulumi.Input[str] end_date_time: The DateTime when the review instance is scheduled to end.
        :param pulumi.Input[str] start_date_time: The DateTime when the review instance is scheduled to be start.
        """
        if end_date_time is not None:
            pulumi.set(__self__, "end_date_time", end_date_time)
        if start_date_time is not None:
            pulumi.set(__self__, "start_date_time", start_date_time)

    @property
    @pulumi.getter(name="endDateTime")
    def end_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review instance is scheduled to end.
        """
        return pulumi.get(self, "end_date_time")

    @end_date_time.setter
    def end_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_date_time", value)

    @property
    @pulumi.getter(name="startDateTime")
    def start_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review instance is scheduled to be start.
        """
        return pulumi.get(self, "start_date_time")

    @start_date_time.setter
    def start_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_date_time", value)


@pulumi.input_type
class AccessReviewReviewerArgs:
    def __init__(__self__, *,
                 principal_id: Optional[pulumi.Input[str]] = None):
        """
        Descriptor for what needs to be reviewed
        :param pulumi.Input[str] principal_id: The id of the reviewer(user/servicePrincipal)
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the reviewer(user/servicePrincipal)
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the resource.
        :param pulumi.Input['ResourceIdentityType'] type: The identity type. This is the only required field when adding a system assigned identity to a resource.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The identity type. This is the only required field when adding a system assigned identity to a resource.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ManagementLockOwnerArgs:
    def __init__(__self__, *,
                 application_id: Optional[pulumi.Input[str]] = None):
        """
        Lock owner properties.
        :param pulumi.Input[str] application_id: The application ID of the lock owner.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The application ID of the lock owner.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_id", value)


@pulumi.input_type
class NonComplianceMessageArgs:
    def __init__(__self__, *,
                 message: pulumi.Input[str],
                 policy_definition_reference_id: Optional[pulumi.Input[str]] = None):
        """
        A message that describes why a resource is non-compliant with the policy. This is shown in 'deny' error messages and on resource's non-compliant compliance results.
        :param pulumi.Input[str] message: A message that describes why a resource is non-compliant with the policy. This is shown in 'deny' error messages and on resource's non-compliant compliance results.
        :param pulumi.Input[str] policy_definition_reference_id: The policy definition reference ID within a policy set definition the message is intended for. This is only applicable if the policy assignment assigns a policy set definition. If this is not provided the message applies to all policies assigned by this policy assignment.
        """
        pulumi.set(__self__, "message", message)
        if policy_definition_reference_id is not None:
            pulumi.set(__self__, "policy_definition_reference_id", policy_definition_reference_id)

    @property
    @pulumi.getter
    def message(self) -> pulumi.Input[str]:
        """
        A message that describes why a resource is non-compliant with the policy. This is shown in 'deny' error messages and on resource's non-compliant compliance results.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: pulumi.Input[str]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter(name="policyDefinitionReferenceId")
    def policy_definition_reference_id(self) -> Optional[pulumi.Input[str]]:
        """
        The policy definition reference ID within a policy set definition the message is intended for. This is only applicable if the policy assignment assigns a policy set definition. If this is not provided the message applies to all policies assigned by this policy assignment.
        """
        return pulumi.get(self, "policy_definition_reference_id")

    @policy_definition_reference_id.setter
    def policy_definition_reference_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_definition_reference_id", value)


@pulumi.input_type
class ParameterDefinitionsValueArgs:
    def __init__(__self__, *,
                 allowed_values: Optional[pulumi.Input[Sequence[Any]]] = None,
                 default_value: Optional[Any] = None,
                 metadata: Optional[pulumi.Input['ParameterDefinitionsValueMetadataArgs']] = None,
                 type: Optional[pulumi.Input[Union[str, 'ParameterType']]] = None):
        """
        The definition of a parameter that can be provided to the policy.
        :param pulumi.Input[Sequence[Any]] allowed_values: The allowed values for the parameter.
        :param Any default_value: The default value for the parameter if no value is provided.
        :param pulumi.Input['ParameterDefinitionsValueMetadataArgs'] metadata: General metadata for the parameter.
        :param pulumi.Input[Union[str, 'ParameterType']] type: The data type of the parameter.
        """
        if allowed_values is not None:
            pulumi.set(__self__, "allowed_values", allowed_values)
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> Optional[pulumi.Input[Sequence[Any]]]:
        """
        The allowed values for the parameter.
        """
        return pulumi.get(self, "allowed_values")

    @allowed_values.setter
    def allowed_values(self, value: Optional[pulumi.Input[Sequence[Any]]]):
        pulumi.set(self, "allowed_values", value)

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[Any]:
        """
        The default value for the parameter if no value is provided.
        """
        return pulumi.get(self, "default_value")

    @default_value.setter
    def default_value(self, value: Optional[Any]):
        pulumi.set(self, "default_value", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input['ParameterDefinitionsValueMetadataArgs']]:
        """
        General metadata for the parameter.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['ParameterDefinitionsValueMetadataArgs']]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ParameterType']]]:
        """
        The data type of the parameter.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ParameterType']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ParameterDefinitionsValueMetadataArgs:
    def __init__(__self__, *,
                 assign_permissions: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 strong_type: Optional[pulumi.Input[str]] = None):
        """
        General metadata for the parameter.
        :param pulumi.Input[bool] assign_permissions: Set to true to have Azure portal create role assignments on the resource ID or resource scope value of this parameter during policy assignment. This property is useful in case you wish to assign permissions outside the assignment scope.
        :param pulumi.Input[str] description: The description of the parameter.
        :param pulumi.Input[str] display_name: The display name for the parameter.
        :param pulumi.Input[str] strong_type: Used when assigning the policy definition through the portal. Provides a context aware list of values for the user to choose from.
        """
        if assign_permissions is not None:
            pulumi.set(__self__, "assign_permissions", assign_permissions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if strong_type is not None:
            pulumi.set(__self__, "strong_type", strong_type)

    @property
    @pulumi.getter(name="assignPermissions")
    def assign_permissions(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to true to have Azure portal create role assignments on the resource ID or resource scope value of this parameter during policy assignment. This property is useful in case you wish to assign permissions outside the assignment scope.
        """
        return pulumi.get(self, "assign_permissions")

    @assign_permissions.setter
    def assign_permissions(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "assign_permissions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the parameter.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name for the parameter.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="strongType")
    def strong_type(self) -> Optional[pulumi.Input[str]]:
        """
        Used when assigning the policy definition through the portal. Provides a context aware list of values for the user to choose from.
        """
        return pulumi.get(self, "strong_type")

    @strong_type.setter
    def strong_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "strong_type", value)


@pulumi.input_type
class ParameterValuesValueArgs:
    def __init__(__self__, *,
                 value: Optional[Any] = None):
        """
        The value of a parameter.
        :param Any value: The value of the parameter.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Any]:
        """
        The value of the parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[Any]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PermissionArgs:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 not_data_actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Role definition permissions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: Allowed actions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] data_actions: Allowed Data actions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_actions: Denied actions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_data_actions: Denied Data actions.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if data_actions is not None:
            pulumi.set(__self__, "data_actions", data_actions)
        if not_actions is not None:
            pulumi.set(__self__, "not_actions", not_actions)
        if not_data_actions is not None:
            pulumi.set(__self__, "not_data_actions", not_data_actions)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Allowed actions.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="dataActions")
    def data_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Allowed Data actions.
        """
        return pulumi.get(self, "data_actions")

    @data_actions.setter
    def data_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "data_actions", value)

    @property
    @pulumi.getter(name="notActions")
    def not_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Denied actions.
        """
        return pulumi.get(self, "not_actions")

    @not_actions.setter
    def not_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_actions", value)

    @property
    @pulumi.getter(name="notDataActions")
    def not_data_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Denied Data actions.
        """
        return pulumi.get(self, "not_data_actions")

    @not_data_actions.setter
    def not_data_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_data_actions", value)


@pulumi.input_type
class PolicyDefinitionGroupArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 additional_metadata_id: Optional[pulumi.Input[str]] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None):
        """
        The policy definition group.
        :param pulumi.Input[str] name: The name of the group.
        :param pulumi.Input[str] additional_metadata_id: A resource ID of a resource that contains additional metadata about the group.
        :param pulumi.Input[str] category: The group's category.
        :param pulumi.Input[str] description: The group's description.
        :param pulumi.Input[str] display_name: The group's display name.
        """
        pulumi.set(__self__, "name", name)
        if additional_metadata_id is not None:
            pulumi.set(__self__, "additional_metadata_id", additional_metadata_id)
        if category is not None:
            pulumi.set(__self__, "category", category)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="additionalMetadataId")
    def additional_metadata_id(self) -> Optional[pulumi.Input[str]]:
        """
        A resource ID of a resource that contains additional metadata about the group.
        """
        return pulumi.get(self, "additional_metadata_id")

    @additional_metadata_id.setter
    def additional_metadata_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "additional_metadata_id", value)

    @property
    @pulumi.getter
    def category(self) -> Optional[pulumi.Input[str]]:
        """
        The group's category.
        """
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The group's description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The group's display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)


@pulumi.input_type
class PolicyDefinitionReferenceArgs:
    def __init__(__self__, *,
                 policy_definition_id: pulumi.Input[str],
                 group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterValuesValueArgs']]]] = None,
                 policy_definition_reference_id: Optional[pulumi.Input[str]] = None):
        """
        The policy definition reference.
        :param pulumi.Input[str] policy_definition_id: The ID of the policy definition or policy set definition.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_names: The name of the groups that this policy definition reference belongs to.
        :param pulumi.Input[Mapping[str, pulumi.Input['ParameterValuesValueArgs']]] parameters: The parameter values for the referenced policy rule. The keys are the parameter names.
        :param pulumi.Input[str] policy_definition_reference_id: A unique id (within the policy set definition) for this policy definition reference.
        """
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if group_names is not None:
            pulumi.set(__self__, "group_names", group_names)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if policy_definition_reference_id is not None:
            pulumi.set(__self__, "policy_definition_reference_id", policy_definition_reference_id)

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> pulumi.Input[str]:
        """
        The ID of the policy definition or policy set definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @policy_definition_id.setter
    def policy_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_definition_id", value)

    @property
    @pulumi.getter(name="groupNames")
    def group_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The name of the groups that this policy definition reference belongs to.
        """
        return pulumi.get(self, "group_names")

    @group_names.setter
    def group_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_names", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterValuesValueArgs']]]]:
        """
        The parameter values for the referenced policy rule. The keys are the parameter names.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterValuesValueArgs']]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="policyDefinitionReferenceId")
    def policy_definition_reference_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique id (within the policy set definition) for this policy definition reference.
        """
        return pulumi.get(self, "policy_definition_reference_id")

    @policy_definition_reference_id.setter
    def policy_definition_reference_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_definition_reference_id", value)


