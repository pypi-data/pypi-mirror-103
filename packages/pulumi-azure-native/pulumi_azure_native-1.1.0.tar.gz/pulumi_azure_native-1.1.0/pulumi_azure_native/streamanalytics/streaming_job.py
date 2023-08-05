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
from ._inputs import *

__all__ = ['StreamingJobArgs', 'StreamingJob']

@pulumi.input_type
class StreamingJobArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 compatibility_level: Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]] = None,
                 data_locale: Optional[pulumi.Input[str]] = None,
                 events_late_arrival_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_policy: Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]] = None,
                 functions: Optional[pulumi.Input[Sequence[pulumi.Input['FunctionArgs']]]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input['InputArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 output_error_policy: Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]] = None,
                 output_start_mode: Optional[pulumi.Input[Union[str, 'OutputStartMode']]] = None,
                 output_start_time: Optional[pulumi.Input[str]] = None,
                 outputs: Optional[pulumi.Input[Sequence[pulumi.Input['OutputArgs']]]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transformation: Optional[pulumi.Input['TransformationArgs']] = None):
        """
        The set of arguments for constructing a StreamingJob resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[Union[str, 'CompatibilityLevel']] compatibility_level: Controls certain runtime behaviors of the streaming job.
        :param pulumi.Input[str] data_locale: The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        :param pulumi.Input[int] events_late_arrival_max_delay_in_seconds: The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        :param pulumi.Input[int] events_out_of_order_max_delay_in_seconds: The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        :param pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']] events_out_of_order_policy: Indicates the policy to apply to events that arrive out of order in the input event stream.
        :param pulumi.Input[Sequence[pulumi.Input['FunctionArgs']]] functions: A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        :param pulumi.Input[Sequence[pulumi.Input['InputArgs']]] inputs: A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        :param pulumi.Input[str] job_name: The name of the streaming job.
        :param pulumi.Input[str] location: Resource location. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[Union[str, 'OutputErrorPolicy']] output_error_policy: Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        :param pulumi.Input[Union[str, 'OutputStartMode']] output_start_mode: This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        :param pulumi.Input[str] output_start_time: Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        :param pulumi.Input[Sequence[pulumi.Input['OutputArgs']]] outputs: A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        :param pulumi.Input['SkuArgs'] sku: Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input['TransformationArgs'] transformation: Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if compatibility_level is not None:
            pulumi.set(__self__, "compatibility_level", compatibility_level)
        if data_locale is not None:
            pulumi.set(__self__, "data_locale", data_locale)
        if events_late_arrival_max_delay_in_seconds is not None:
            pulumi.set(__self__, "events_late_arrival_max_delay_in_seconds", events_late_arrival_max_delay_in_seconds)
        if events_out_of_order_max_delay_in_seconds is not None:
            pulumi.set(__self__, "events_out_of_order_max_delay_in_seconds", events_out_of_order_max_delay_in_seconds)
        if events_out_of_order_policy is not None:
            pulumi.set(__self__, "events_out_of_order_policy", events_out_of_order_policy)
        if functions is not None:
            pulumi.set(__self__, "functions", functions)
        if inputs is not None:
            pulumi.set(__self__, "inputs", inputs)
        if job_name is not None:
            pulumi.set(__self__, "job_name", job_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if output_error_policy is not None:
            pulumi.set(__self__, "output_error_policy", output_error_policy)
        if output_start_mode is not None:
            pulumi.set(__self__, "output_start_mode", output_start_mode)
        if output_start_time is not None:
            pulumi.set(__self__, "output_start_time", output_start_time)
        if outputs is not None:
            pulumi.set(__self__, "outputs", outputs)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if transformation is not None:
            pulumi.set(__self__, "transformation", transformation)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]]:
        """
        Controls certain runtime behaviors of the streaming job.
        """
        return pulumi.get(self, "compatibility_level")

    @compatibility_level.setter
    def compatibility_level(self, value: Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]]):
        pulumi.set(self, "compatibility_level", value)

    @property
    @pulumi.getter(name="dataLocale")
    def data_locale(self) -> Optional[pulumi.Input[str]]:
        """
        The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        """
        return pulumi.get(self, "data_locale")

    @data_locale.setter
    def data_locale(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_locale", value)

    @property
    @pulumi.getter(name="eventsLateArrivalMaxDelayInSeconds")
    def events_late_arrival_max_delay_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        """
        return pulumi.get(self, "events_late_arrival_max_delay_in_seconds")

    @events_late_arrival_max_delay_in_seconds.setter
    def events_late_arrival_max_delay_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "events_late_arrival_max_delay_in_seconds", value)

    @property
    @pulumi.getter(name="eventsOutOfOrderMaxDelayInSeconds")
    def events_out_of_order_max_delay_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        """
        return pulumi.get(self, "events_out_of_order_max_delay_in_seconds")

    @events_out_of_order_max_delay_in_seconds.setter
    def events_out_of_order_max_delay_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "events_out_of_order_max_delay_in_seconds", value)

    @property
    @pulumi.getter(name="eventsOutOfOrderPolicy")
    def events_out_of_order_policy(self) -> Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]]:
        """
        Indicates the policy to apply to events that arrive out of order in the input event stream.
        """
        return pulumi.get(self, "events_out_of_order_policy")

    @events_out_of_order_policy.setter
    def events_out_of_order_policy(self, value: Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]]):
        pulumi.set(self, "events_out_of_order_policy", value)

    @property
    @pulumi.getter
    def functions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FunctionArgs']]]]:
        """
        A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "functions")

    @functions.setter
    def functions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FunctionArgs']]]]):
        pulumi.set(self, "functions", value)

    @property
    @pulumi.getter
    def inputs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InputArgs']]]]:
        """
        A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        """
        return pulumi.get(self, "inputs")

    @inputs.setter
    def inputs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InputArgs']]]]):
        pulumi.set(self, "inputs", value)

    @property
    @pulumi.getter(name="jobName")
    def job_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the streaming job.
        """
        return pulumi.get(self, "job_name")

    @job_name.setter
    def job_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="outputErrorPolicy")
    def output_error_policy(self) -> Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]]:
        """
        Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        """
        return pulumi.get(self, "output_error_policy")

    @output_error_policy.setter
    def output_error_policy(self, value: Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]]):
        pulumi.set(self, "output_error_policy", value)

    @property
    @pulumi.getter(name="outputStartMode")
    def output_start_mode(self) -> Optional[pulumi.Input[Union[str, 'OutputStartMode']]]:
        """
        This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        """
        return pulumi.get(self, "output_start_mode")

    @output_start_mode.setter
    def output_start_mode(self, value: Optional[pulumi.Input[Union[str, 'OutputStartMode']]]):
        pulumi.set(self, "output_start_mode", value)

    @property
    @pulumi.getter(name="outputStartTime")
    def output_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        """
        return pulumi.get(self, "output_start_time")

    @output_start_time.setter
    def output_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_start_time", value)

    @property
    @pulumi.getter
    def outputs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OutputArgs']]]]:
        """
        A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        """
        return pulumi.get(self, "outputs")

    @outputs.setter
    def outputs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OutputArgs']]]]):
        pulumi.set(self, "outputs", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def transformation(self) -> Optional[pulumi.Input['TransformationArgs']]:
        """
        Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "transformation")

    @transformation.setter
    def transformation(self, value: Optional[pulumi.Input['TransformationArgs']]):
        pulumi.set(self, "transformation", value)


class StreamingJob(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compatibility_level: Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]] = None,
                 data_locale: Optional[pulumi.Input[str]] = None,
                 events_late_arrival_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_policy: Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]] = None,
                 functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FunctionArgs']]]]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InputArgs']]]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 output_error_policy: Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]] = None,
                 output_start_mode: Optional[pulumi.Input[Union[str, 'OutputStartMode']]] = None,
                 output_start_time: Optional[pulumi.Input[str]] = None,
                 outputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutputArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transformation: Optional[pulumi.Input[pulumi.InputType['TransformationArgs']]] = None,
                 __props__=None):
        """
        A streaming job object, containing all information associated with the named streaming job.
        API Version: 2016-03-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'CompatibilityLevel']] compatibility_level: Controls certain runtime behaviors of the streaming job.
        :param pulumi.Input[str] data_locale: The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        :param pulumi.Input[int] events_late_arrival_max_delay_in_seconds: The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        :param pulumi.Input[int] events_out_of_order_max_delay_in_seconds: The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        :param pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']] events_out_of_order_policy: Indicates the policy to apply to events that arrive out of order in the input event stream.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FunctionArgs']]]] functions: A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InputArgs']]]] inputs: A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        :param pulumi.Input[str] job_name: The name of the streaming job.
        :param pulumi.Input[str] location: Resource location. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[Union[str, 'OutputErrorPolicy']] output_error_policy: Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        :param pulumi.Input[Union[str, 'OutputStartMode']] output_start_mode: This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        :param pulumi.Input[str] output_start_time: Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutputArgs']]]] outputs: A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[pulumi.InputType['TransformationArgs']] transformation: Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StreamingJobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A streaming job object, containing all information associated with the named streaming job.
        API Version: 2016-03-01.

        :param str resource_name: The name of the resource.
        :param StreamingJobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StreamingJobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compatibility_level: Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]] = None,
                 data_locale: Optional[pulumi.Input[str]] = None,
                 events_late_arrival_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_policy: Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]] = None,
                 functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FunctionArgs']]]]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InputArgs']]]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 output_error_policy: Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]] = None,
                 output_start_mode: Optional[pulumi.Input[Union[str, 'OutputStartMode']]] = None,
                 output_start_time: Optional[pulumi.Input[str]] = None,
                 outputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutputArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transformation: Optional[pulumi.Input[pulumi.InputType['TransformationArgs']]] = None,
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
            __props__ = StreamingJobArgs.__new__(StreamingJobArgs)

            __props__.__dict__["compatibility_level"] = compatibility_level
            __props__.__dict__["data_locale"] = data_locale
            __props__.__dict__["events_late_arrival_max_delay_in_seconds"] = events_late_arrival_max_delay_in_seconds
            __props__.__dict__["events_out_of_order_max_delay_in_seconds"] = events_out_of_order_max_delay_in_seconds
            __props__.__dict__["events_out_of_order_policy"] = events_out_of_order_policy
            __props__.__dict__["functions"] = functions
            __props__.__dict__["inputs"] = inputs
            __props__.__dict__["job_name"] = job_name
            __props__.__dict__["location"] = location
            __props__.__dict__["output_error_policy"] = output_error_policy
            __props__.__dict__["output_start_mode"] = output_start_mode
            __props__.__dict__["output_start_time"] = output_start_time
            __props__.__dict__["outputs"] = outputs
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["transformation"] = transformation
            __props__.__dict__["created_date"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["job_id"] = None
            __props__.__dict__["job_state"] = None
            __props__.__dict__["last_output_event_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:streamanalytics:StreamingJob"), pulumi.Alias(type_="azure-native:streamanalytics/v20160301:StreamingJob"), pulumi.Alias(type_="azure-nextgen:streamanalytics/v20160301:StreamingJob"), pulumi.Alias(type_="azure-native:streamanalytics/v20170401preview:StreamingJob"), pulumi.Alias(type_="azure-nextgen:streamanalytics/v20170401preview:StreamingJob")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StreamingJob, __self__).__init__(
            'azure-native:streamanalytics:StreamingJob',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StreamingJob':
        """
        Get an existing StreamingJob resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StreamingJobArgs.__new__(StreamingJobArgs)

        __props__.__dict__["compatibility_level"] = None
        __props__.__dict__["created_date"] = None
        __props__.__dict__["data_locale"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["events_late_arrival_max_delay_in_seconds"] = None
        __props__.__dict__["events_out_of_order_max_delay_in_seconds"] = None
        __props__.__dict__["events_out_of_order_policy"] = None
        __props__.__dict__["functions"] = None
        __props__.__dict__["inputs"] = None
        __props__.__dict__["job_id"] = None
        __props__.__dict__["job_state"] = None
        __props__.__dict__["last_output_event_time"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["output_error_policy"] = None
        __props__.__dict__["output_start_mode"] = None
        __props__.__dict__["output_start_time"] = None
        __props__.__dict__["outputs"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["transformation"] = None
        __props__.__dict__["type"] = None
        return StreamingJob(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> pulumi.Output[Optional[str]]:
        """
        Controls certain runtime behaviors of the streaming job.
        """
        return pulumi.get(self, "compatibility_level")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        Value is an ISO-8601 formatted UTC timestamp indicating when the streaming job was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="dataLocale")
    def data_locale(self) -> pulumi.Output[Optional[str]]:
        """
        The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        """
        return pulumi.get(self, "data_locale")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The current entity tag for the streaming job. This is an opaque string. You can use it to detect whether the resource has changed between requests. You can also use it in the If-Match or If-None-Match headers for write operations for optimistic concurrency.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="eventsLateArrivalMaxDelayInSeconds")
    def events_late_arrival_max_delay_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        """
        return pulumi.get(self, "events_late_arrival_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderMaxDelayInSeconds")
    def events_out_of_order_max_delay_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        """
        return pulumi.get(self, "events_out_of_order_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderPolicy")
    def events_out_of_order_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the policy to apply to events that arrive out of order in the input event stream.
        """
        return pulumi.get(self, "events_out_of_order_policy")

    @property
    @pulumi.getter
    def functions(self) -> pulumi.Output[Optional[Sequence['outputs.FunctionResponse']]]:
        """
        A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "functions")

    @property
    @pulumi.getter
    def inputs(self) -> pulumi.Output[Optional[Sequence['outputs.InputResponse']]]:
        """
        A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        """
        return pulumi.get(self, "inputs")

    @property
    @pulumi.getter(name="jobId")
    def job_id(self) -> pulumi.Output[str]:
        """
        A GUID uniquely identifying the streaming job. This GUID is generated upon creation of the streaming job.
        """
        return pulumi.get(self, "job_id")

    @property
    @pulumi.getter(name="jobState")
    def job_state(self) -> pulumi.Output[str]:
        """
        Describes the state of the streaming job.
        """
        return pulumi.get(self, "job_state")

    @property
    @pulumi.getter(name="lastOutputEventTime")
    def last_output_event_time(self) -> pulumi.Output[str]:
        """
        Value is either an ISO-8601 formatted timestamp indicating the last output event time of the streaming job or null indicating that output has not yet been produced. In case of multiple outputs or multiple streams, this shows the latest value in that set.
        """
        return pulumi.get(self, "last_output_event_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputErrorPolicy")
    def output_error_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        """
        return pulumi.get(self, "output_error_policy")

    @property
    @pulumi.getter(name="outputStartMode")
    def output_start_mode(self) -> pulumi.Output[Optional[str]]:
        """
        This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        """
        return pulumi.get(self, "output_start_mode")

    @property
    @pulumi.getter(name="outputStartTime")
    def output_start_time(self) -> pulumi.Output[Optional[str]]:
        """
        Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        """
        return pulumi.get(self, "output_start_time")

    @property
    @pulumi.getter
    def outputs(self) -> pulumi.Output[Optional[Sequence['outputs.OutputResponse']]]:
        """
        A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        """
        return pulumi.get(self, "outputs")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Describes the provisioning status of the streaming job.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def transformation(self) -> pulumi.Output[Optional['outputs.TransformationResponse']]:
        """
        Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "transformation")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

