# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .cloud_connector import *
from .cost_allocation_rule import *
from .export import *
from .get_cloud_connector import *
from .get_cost_allocation_rule import *
from .get_export import *
from .get_report import *
from .get_report_by_billing_account import *
from .get_report_by_department import *
from .get_report_by_resource_group_name import *
from .get_setting import *
from .get_view import *
from .get_view_by_scope import *
from .report import *
from .report_by_billing_account import *
from .report_by_department import *
from .report_by_resource_group_name import *
from .setting import *
from .view import *
from .view_by_scope import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20180531,
    v20180801preview,
    v20190101,
    v20190301preview,
    v20190401preview,
    v20190901,
    v20191001,
    v20191101,
    v20200301preview,
    v20200601,
    v20201201preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:costmanagement:CloudConnector":
                return CloudConnector(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:CostAllocationRule":
                return CostAllocationRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:Export":
                return Export(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:Report":
                return Report(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:ReportByBillingAccount":
                return ReportByBillingAccount(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:ReportByDepartment":
                return ReportByDepartment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:ReportByResourceGroupName":
                return ReportByResourceGroupName(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:Setting":
                return Setting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:View":
                return View(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:costmanagement:ViewByScope":
                return ViewByScope(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "costmanagement", _module_instance)

_register_module()
