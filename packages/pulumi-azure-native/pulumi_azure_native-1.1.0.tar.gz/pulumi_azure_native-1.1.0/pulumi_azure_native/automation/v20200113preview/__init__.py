# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .automation_account import *
from .certificate import *
from .connection import *
from .connection_type import *
from .credential import *
from .dsc_node_configuration import *
from .get_automation_account import *
from .get_certificate import *
from .get_connection import *
from .get_connection_type import *
from .get_credential import *
from .get_dsc_node_configuration import *
from .get_job_schedule import *
from .get_module import *
from .get_private_endpoint_connection import *
from .get_python2_package import *
from .get_schedule import *
from .get_source_control import *
from .get_variable import *
from .get_watcher import *
from .job_schedule import *
from .list_key_by_automation_account import *
from .module import *
from .private_endpoint_connection import *
from .python2_package import *
from .schedule import *
from .source_control import *
from .variable import *
from .watcher import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:automation/v20200113preview:AutomationAccount":
                return AutomationAccount(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Connection":
                return Connection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:ConnectionType":
                return ConnectionType(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Credential":
                return Credential(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:DscNodeConfiguration":
                return DscNodeConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:JobSchedule":
                return JobSchedule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Module":
                return Module(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:PrivateEndpointConnection":
                return PrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Python2Package":
                return Python2Package(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Schedule":
                return Schedule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:SourceControl":
                return SourceControl(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Variable":
                return Variable(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:automation/v20200113preview:Watcher":
                return Watcher(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "automation/v20200113preview", _module_instance)

_register_module()
