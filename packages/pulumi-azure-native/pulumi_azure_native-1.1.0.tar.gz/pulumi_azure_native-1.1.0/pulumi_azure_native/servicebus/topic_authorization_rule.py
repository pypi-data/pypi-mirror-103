# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = ['TopicAuthorizationRuleArgs', 'TopicAuthorizationRule']

@pulumi.input_type
class TopicAuthorizationRuleArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 rights: pulumi.Input[Sequence[pulumi.Input['AccessRights']]],
                 topic_name: pulumi.Input[str],
                 authorization_rule_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TopicAuthorizationRule resource.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input['AccessRights']]] rights: The rights associated with the rule.
        :param pulumi.Input[str] topic_name: The topic name.
        :param pulumi.Input[str] authorization_rule_name: The authorization rule name.
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "rights", rights)
        pulumi.set(__self__, "topic_name", topic_name)
        if authorization_rule_name is not None:
            pulumi.set(__self__, "authorization_rule_name", authorization_rule_name)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The namespace name
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Input[Sequence[pulumi.Input['AccessRights']]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, "rights")

    @rights.setter
    def rights(self, value: pulumi.Input[Sequence[pulumi.Input['AccessRights']]]):
        pulumi.set(self, "rights", value)

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Input[str]:
        """
        The topic name.
        """
        return pulumi.get(self, "topic_name")

    @topic_name.setter
    def topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic_name", value)

    @property
    @pulumi.getter(name="authorizationRuleName")
    def authorization_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The authorization rule name.
        """
        return pulumi.get(self, "authorization_rule_name")

    @authorization_rule_name.setter
    def authorization_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_rule_name", value)


class TopicAuthorizationRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_rule_name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rights: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Description of a namespace authorization rule.
        API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_rule_name: The authorization rule name.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input['AccessRights']]] rights: The rights associated with the rule.
        :param pulumi.Input[str] topic_name: The topic name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TopicAuthorizationRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Description of a namespace authorization rule.
        API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param TopicAuthorizationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TopicAuthorizationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_rule_name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rights: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TopicAuthorizationRuleArgs.__new__(TopicAuthorizationRuleArgs)

            __props__.__dict__["authorization_rule_name"] = authorization_rule_name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if rights is None and not opts.urn:
                raise TypeError("Missing required property 'rights'")
            __props__.__dict__["rights"] = rights
            if topic_name is None and not opts.urn:
                raise TypeError("Missing required property 'topic_name'")
            __props__.__dict__["topic_name"] = topic_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:servicebus:TopicAuthorizationRule"), pulumi.Alias(type_="azure-native:servicebus/v20140901:TopicAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20140901:TopicAuthorizationRule"), pulumi.Alias(type_="azure-native:servicebus/v20150801:TopicAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20150801:TopicAuthorizationRule"), pulumi.Alias(type_="azure-native:servicebus/v20170401:TopicAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20170401:TopicAuthorizationRule"), pulumi.Alias(type_="azure-native:servicebus/v20180101preview:TopicAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20180101preview:TopicAuthorizationRule"), pulumi.Alias(type_="azure-native:servicebus/v20210101preview:TopicAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20210101preview:TopicAuthorizationRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(TopicAuthorizationRule, __self__).__init__(
            'azure-native:servicebus:TopicAuthorizationRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TopicAuthorizationRule':
        """
        Get an existing TopicAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TopicAuthorizationRuleArgs.__new__(TopicAuthorizationRuleArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["rights"] = None
        __props__.__dict__["type"] = None
        return TopicAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Output[Sequence[str]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, "rights")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

