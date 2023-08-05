# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetRecordSetResult',
    'AwaitableGetRecordSetResult',
    'get_record_set',
]

@pulumi.output_type
class GetRecordSetResult:
    """
    Describes a DNS record set (a collection of DNS records with the same name and type).
    """
    def __init__(__self__, a_aaa_records=None, a_records=None, c_name_record=None, etag=None, fqdn=None, id=None, m_x_records=None, n_s_records=None, name=None, p_tr_records=None, s_oa_record=None, s_rv_records=None, t_xt_records=None, ttl=None, type=None):
        if a_aaa_records and not isinstance(a_aaa_records, list):
            raise TypeError("Expected argument 'a_aaa_records' to be a list")
        pulumi.set(__self__, "a_aaa_records", a_aaa_records)
        if a_records and not isinstance(a_records, list):
            raise TypeError("Expected argument 'a_records' to be a list")
        pulumi.set(__self__, "a_records", a_records)
        if c_name_record and not isinstance(c_name_record, dict):
            raise TypeError("Expected argument 'c_name_record' to be a dict")
        pulumi.set(__self__, "c_name_record", c_name_record)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if m_x_records and not isinstance(m_x_records, list):
            raise TypeError("Expected argument 'm_x_records' to be a list")
        pulumi.set(__self__, "m_x_records", m_x_records)
        if n_s_records and not isinstance(n_s_records, list):
            raise TypeError("Expected argument 'n_s_records' to be a list")
        pulumi.set(__self__, "n_s_records", n_s_records)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if p_tr_records and not isinstance(p_tr_records, list):
            raise TypeError("Expected argument 'p_tr_records' to be a list")
        pulumi.set(__self__, "p_tr_records", p_tr_records)
        if s_oa_record and not isinstance(s_oa_record, dict):
            raise TypeError("Expected argument 's_oa_record' to be a dict")
        pulumi.set(__self__, "s_oa_record", s_oa_record)
        if s_rv_records and not isinstance(s_rv_records, list):
            raise TypeError("Expected argument 's_rv_records' to be a list")
        pulumi.set(__self__, "s_rv_records", s_rv_records)
        if t_xt_records and not isinstance(t_xt_records, list):
            raise TypeError("Expected argument 't_xt_records' to be a list")
        pulumi.set(__self__, "t_xt_records", t_xt_records)
        if ttl and not isinstance(ttl, float):
            raise TypeError("Expected argument 'ttl' to be a float")
        pulumi.set(__self__, "ttl", ttl)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="aAAARecords")
    def a_aaa_records(self) -> Optional[Sequence['outputs.AaaaRecordResponse']]:
        """
        Gets or sets the list of AAAA records in the RecordSet.
        """
        return pulumi.get(self, "a_aaa_records")

    @property
    @pulumi.getter(name="aRecords")
    def a_records(self) -> Optional[Sequence['outputs.ARecordResponse']]:
        """
        Gets or sets the list of A records in the RecordSet.
        """
        return pulumi.get(self, "a_records")

    @property
    @pulumi.getter(name="cNAMERecord")
    def c_name_record(self) -> Optional['outputs.CnameRecordResponse']:
        """
        Gets or sets the CNAME record in the RecordSet.
        """
        return pulumi.get(self, "c_name_record")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        The etag of the record set.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        Fully qualified domain name of the record set.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the record set.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="mXRecords")
    def m_x_records(self) -> Optional[Sequence['outputs.MxRecordResponse']]:
        """
        Gets or sets the list of MX records in the RecordSet.
        """
        return pulumi.get(self, "m_x_records")

    @property
    @pulumi.getter(name="nSRecords")
    def n_s_records(self) -> Optional[Sequence['outputs.NsRecordResponse']]:
        """
        Gets or sets the list of NS records in the RecordSet.
        """
        return pulumi.get(self, "n_s_records")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the record set.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pTRRecords")
    def p_tr_records(self) -> Optional[Sequence['outputs.PtrRecordResponse']]:
        """
        Gets or sets the list of PTR records in the RecordSet.
        """
        return pulumi.get(self, "p_tr_records")

    @property
    @pulumi.getter(name="sOARecord")
    def s_oa_record(self) -> Optional['outputs.SoaRecordResponse']:
        """
        Gets or sets the SOA record in the RecordSet.
        """
        return pulumi.get(self, "s_oa_record")

    @property
    @pulumi.getter(name="sRVRecords")
    def s_rv_records(self) -> Optional[Sequence['outputs.SrvRecordResponse']]:
        """
        Gets or sets the list of SRV records in the RecordSet.
        """
        return pulumi.get(self, "s_rv_records")

    @property
    @pulumi.getter(name="tXTRecords")
    def t_xt_records(self) -> Optional[Sequence['outputs.TxtRecordResponse']]:
        """
        Gets or sets the list of TXT records in the RecordSet.
        """
        return pulumi.get(self, "t_xt_records")

    @property
    @pulumi.getter
    def ttl(self) -> Optional[float]:
        """
        Gets or sets the TTL of the records in the RecordSet.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the record set.
        """
        return pulumi.get(self, "type")


class AwaitableGetRecordSetResult(GetRecordSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRecordSetResult(
            a_aaa_records=self.a_aaa_records,
            a_records=self.a_records,
            c_name_record=self.c_name_record,
            etag=self.etag,
            fqdn=self.fqdn,
            id=self.id,
            m_x_records=self.m_x_records,
            n_s_records=self.n_s_records,
            name=self.name,
            p_tr_records=self.p_tr_records,
            s_oa_record=self.s_oa_record,
            s_rv_records=self.s_rv_records,
            t_xt_records=self.t_xt_records,
            ttl=self.ttl,
            type=self.type)


def get_record_set(record_type: Optional[str] = None,
                   relative_record_set_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   zone_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRecordSetResult:
    """
    Describes a DNS record set (a collection of DNS records with the same name and type).


    :param str record_type: The type of DNS record.
    :param str relative_record_set_name: The name of the RecordSet, relative to the name of the zone.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str zone_name: The name of the zone without a terminating dot.
    """
    __args__ = dict()
    __args__['recordType'] = record_type
    __args__['relativeRecordSetName'] = relative_record_set_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['zoneName'] = zone_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20150504preview:getRecordSet', __args__, opts=opts, typ=GetRecordSetResult).value

    return AwaitableGetRecordSetResult(
        a_aaa_records=__ret__.a_aaa_records,
        a_records=__ret__.a_records,
        c_name_record=__ret__.c_name_record,
        etag=__ret__.etag,
        fqdn=__ret__.fqdn,
        id=__ret__.id,
        m_x_records=__ret__.m_x_records,
        n_s_records=__ret__.n_s_records,
        name=__ret__.name,
        p_tr_records=__ret__.p_tr_records,
        s_oa_record=__ret__.s_oa_record,
        s_rv_records=__ret__.s_rv_records,
        t_xt_records=__ret__.t_xt_records,
        ttl=__ret__.ttl,
        type=__ret__.type)
