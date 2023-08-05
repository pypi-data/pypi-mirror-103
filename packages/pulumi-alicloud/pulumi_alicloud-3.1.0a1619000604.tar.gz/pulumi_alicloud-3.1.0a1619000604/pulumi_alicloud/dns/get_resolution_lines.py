# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetResolutionLinesResult',
    'AwaitableGetResolutionLinesResult',
    'get_resolution_lines',
]

@pulumi.output_type
class GetResolutionLinesResult:
    """
    A collection of values returned by getResolutionLines.
    """
    def __init__(__self__, domain_name=None, id=None, lang=None, line_codes=None, line_display_names=None, line_names=None, lines=None, output_file=None, user_client_ip=None):
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lang and not isinstance(lang, str):
            raise TypeError("Expected argument 'lang' to be a str")
        pulumi.set(__self__, "lang", lang)
        if line_codes and not isinstance(line_codes, list):
            raise TypeError("Expected argument 'line_codes' to be a list")
        pulumi.set(__self__, "line_codes", line_codes)
        if line_display_names and not isinstance(line_display_names, list):
            raise TypeError("Expected argument 'line_display_names' to be a list")
        pulumi.set(__self__, "line_display_names", line_display_names)
        if line_names and not isinstance(line_names, list):
            raise TypeError("Expected argument 'line_names' to be a list")
        pulumi.set(__self__, "line_names", line_names)
        if lines and not isinstance(lines, list):
            raise TypeError("Expected argument 'lines' to be a list")
        pulumi.set(__self__, "lines", lines)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if user_client_ip and not isinstance(user_client_ip, str):
            raise TypeError("Expected argument 'user_client_ip' to be a str")
        pulumi.set(__self__, "user_client_ip", user_client_ip)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[str]:
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
    @pulumi.getter(name="lineCodes")
    def line_codes(self) -> Sequence[str]:
        """
        Line code.
        """
        return pulumi.get(self, "line_codes")

    @property
    @pulumi.getter(name="lineDisplayNames")
    def line_display_names(self) -> Sequence[str]:
        """
        A list of line display names.
        """
        return pulumi.get(self, "line_display_names")

    @property
    @pulumi.getter(name="lineNames")
    def line_names(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "line_names")

    @property
    @pulumi.getter
    def lines(self) -> Sequence['outputs.GetResolutionLinesLineResult']:
        """
        A list of cloud resolution line. Each element contains the following attributes:
        """
        return pulumi.get(self, "lines")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="userClientIp")
    def user_client_ip(self) -> Optional[str]:
        return pulumi.get(self, "user_client_ip")


class AwaitableGetResolutionLinesResult(GetResolutionLinesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResolutionLinesResult(
            domain_name=self.domain_name,
            id=self.id,
            lang=self.lang,
            line_codes=self.line_codes,
            line_display_names=self.line_display_names,
            line_names=self.line_names,
            lines=self.lines,
            output_file=self.output_file,
            user_client_ip=self.user_client_ip)


def get_resolution_lines(domain_name: Optional[str] = None,
                         lang: Optional[str] = None,
                         line_codes: Optional[Sequence[str]] = None,
                         line_display_names: Optional[Sequence[str]] = None,
                         line_names: Optional[Sequence[str]] = None,
                         output_file: Optional[str] = None,
                         user_client_ip: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResolutionLinesResult:
    """
    This data source provides a list of DNS Resolution Lines in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.60.0.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    resolution_lines_ds = alicloud.dns.get_resolution_lines(line_codes=["cn_unicom_shanxi"],
        output_file="support_lines.txt")
    pulumi.export("firstLineCode", resolution_lines_ds.lines[0].line_code)
    ```


    :param str domain_name: Domain Name.
    :param str lang: language.
    :param Sequence[str] line_codes: A list of lines codes.
    :param Sequence[str] line_display_names: A list of line display names.
    :param str user_client_ip: The ip of user client.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['lang'] = lang
    __args__['lineCodes'] = line_codes
    __args__['lineDisplayNames'] = line_display_names
    __args__['lineNames'] = line_names
    __args__['outputFile'] = output_file
    __args__['userClientIp'] = user_client_ip
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:dns/getResolutionLines:getResolutionLines', __args__, opts=opts, typ=GetResolutionLinesResult).value

    return AwaitableGetResolutionLinesResult(
        domain_name=__ret__.domain_name,
        id=__ret__.id,
        lang=__ret__.lang,
        line_codes=__ret__.line_codes,
        line_display_names=__ret__.line_display_names,
        line_names=__ret__.line_names,
        lines=__ret__.lines,
        output_file=__ret__.output_file,
        user_client_ip=__ret__.user_client_ip)
