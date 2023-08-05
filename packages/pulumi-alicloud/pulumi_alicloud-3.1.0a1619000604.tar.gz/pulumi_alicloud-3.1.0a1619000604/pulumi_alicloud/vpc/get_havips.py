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
    'GetHavipsResult',
    'AwaitableGetHavipsResult',
    'get_havips',
]

@pulumi.output_type
class GetHavipsResult:
    """
    A collection of values returned by getHavips.
    """
    def __init__(__self__, havips=None, id=None, ids=None, name_regex=None, names=None, output_file=None, status=None):
        if havips and not isinstance(havips, list):
            raise TypeError("Expected argument 'havips' to be a list")
        pulumi.set(__self__, "havips", havips)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def havips(self) -> Sequence['outputs.GetHavipsHavipResult']:
        return pulumi.get(self, "havips")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetHavipsResult(GetHavipsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHavipsResult(
            havips=self.havips,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            status=self.status)


def get_havips(ids: Optional[Sequence[str]] = None,
               name_regex: Optional[str] = None,
               output_file: Optional[str] = None,
               status: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHavipsResult:
    """
    This data source provides the Havips of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.120.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.vpc.get_havips(ids=["example_value"],
        name_regex="the_resource_name")
    pulumi.export("firstHavipId", example.havips[0].id)
    ```


    :param Sequence[str] ids: A list of Ha Vip IDs.
    :param str name_regex: A regex string to filter results by Ha Vip name.
    :param str status: The status.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:vpc/getHavips:getHavips', __args__, opts=opts, typ=GetHavipsResult).value

    return AwaitableGetHavipsResult(
        havips=__ret__.havips,
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        status=__ret__.status)
