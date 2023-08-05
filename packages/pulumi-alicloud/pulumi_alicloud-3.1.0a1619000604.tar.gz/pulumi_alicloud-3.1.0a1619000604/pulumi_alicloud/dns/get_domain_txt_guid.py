# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetDomainTxtGuidResult',
    'AwaitableGetDomainTxtGuidResult',
    'get_domain_txt_guid',
]

@pulumi.output_type
class GetDomainTxtGuidResult:
    """
    A collection of values returned by getDomainTxtGuid.
    """
    def __init__(__self__, domain_name=None, id=None, lang=None, output_file=None, rr=None, type=None, value=None):
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lang and not isinstance(lang, str):
            raise TypeError("Expected argument 'lang' to be a str")
        pulumi.set(__self__, "lang", lang)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if rr and not isinstance(rr, str):
            raise TypeError("Expected argument 'rr' to be a str")
        pulumi.set(__self__, "rr", rr)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> str:
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def lang(self) -> Optional[str]:
        return pulumi.get(self, "lang")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def rr(self) -> str:
        """
        Host record.
        """
        return pulumi.get(self, "rr")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Record the value.
        """
        return pulumi.get(self, "value")


class AwaitableGetDomainTxtGuidResult(GetDomainTxtGuidResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainTxtGuidResult(
            domain_name=self.domain_name,
            id=self.id,
            lang=self.lang,
            output_file=self.output_file,
            rr=self.rr,
            type=self.type,
            value=self.value)


def get_domain_txt_guid(domain_name: Optional[str] = None,
                        lang: Optional[str] = None,
                        output_file: Optional[str] = None,
                        type: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainTxtGuidResult:
    """
    Provides the generation of txt records to realize the retrieval and verification of domain names.

    > **NOTE:** Available in v1.80.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    this = alicloud.dns.get_domain_txt_guid(domain_name="test111.abc",
        type="ADD_SUB_DOMAIN")
    pulumi.export("rr", this.rr)
    pulumi.export("value", this.value)
    ```


    :param str domain_name: Verified domain name.
    :param str lang: User language.
    :param str type: Txt verification function. Value:`ADD_SUB_DOMAIN`, `RETRIEVAL`.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['lang'] = lang
    __args__['outputFile'] = output_file
    __args__['type'] = type
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:dns/getDomainTxtGuid:getDomainTxtGuid', __args__, opts=opts, typ=GetDomainTxtGuidResult).value

    return AwaitableGetDomainTxtGuidResult(
        domain_name=__ret__.domain_name,
        id=__ret__.id,
        lang=__ret__.lang,
        output_file=__ret__.output_file,
        rr=__ret__.rr,
        type=__ret__.type,
        value=__ret__.value)
