# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .cluster import *
from .experiment import *
from .file_server import *
from .get_cluster import *
from .get_experiment import *
from .get_file_server import *
from .get_job import *
from .get_workspace import *
from .job import *
from .list_cluster_remote_login_information import *
from .list_job_output_files import *
from .list_job_remote_login_information import *
from .workspace import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20170901preview,
    v20180301,
    v20180501,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:batchai:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai:Experiment":
                return Experiment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai:FileServer":
                return FileServer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai:Job":
                return Job(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai:Workspace":
                return Workspace(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "batchai", _module_instance)

_register_module()
