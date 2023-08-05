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
    'GetInstanceAttachmentsResult',
    'AwaitableGetInstanceAttachmentsResult',
    'get_instance_attachments',
]

@pulumi.output_type
class GetInstanceAttachmentsResult:
    """
    A collection of values returned by getInstanceAttachments.
    """
    def __init__(__self__, attachments=None, id=None, instance_name=None, name_regex=None, names=None, output_file=None, vpc_ids=None):
        if attachments and not isinstance(attachments, list):
            raise TypeError("Expected argument 'attachments' to be a list")
        pulumi.set(__self__, "attachments", attachments)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_name and not isinstance(instance_name, str):
            raise TypeError("Expected argument 'instance_name' to be a str")
        pulumi.set(__self__, "instance_name", instance_name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if vpc_ids and not isinstance(vpc_ids, list):
            raise TypeError("Expected argument 'vpc_ids' to be a list")
        pulumi.set(__self__, "vpc_ids", vpc_ids)

    @property
    @pulumi.getter
    def attachments(self) -> Sequence['outputs.GetInstanceAttachmentsAttachmentResult']:
        """
        A list of instance attachments. Each element contains the following attributes:
        """
        return pulumi.get(self, "attachments")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> str:
        """
        The instance name.
        """
        return pulumi.get(self, "instance_name")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of vpc names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="vpcIds")
    def vpc_ids(self) -> Sequence[str]:
        """
        A list of vpc ids.
        """
        return pulumi.get(self, "vpc_ids")


class AwaitableGetInstanceAttachmentsResult(GetInstanceAttachmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceAttachmentsResult(
            attachments=self.attachments,
            id=self.id,
            instance_name=self.instance_name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            vpc_ids=self.vpc_ids)


def get_instance_attachments(instance_name: Optional[str] = None,
                             name_regex: Optional[str] = None,
                             output_file: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceAttachmentsResult:
    """
    This data source provides the ots instance attachments of the current Alibaba Cloud user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    attachments_ds = alicloud.ots.get_instance_attachments(instance_name="sample-instance",
        name_regex="testvpc",
        output_file="attachments.txt")
    pulumi.export("firstOtsAttachmentId", attachments_ds.attachments[0].id)
    ```


    :param str instance_name: The name of OTS instance.
    :param str name_regex: A regex string to filter results by vpc name.
    """
    __args__ = dict()
    __args__['instanceName'] = instance_name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:ots/getInstanceAttachments:getInstanceAttachments', __args__, opts=opts, typ=GetInstanceAttachmentsResult).value

    return AwaitableGetInstanceAttachmentsResult(
        attachments=__ret__.attachments,
        id=__ret__.id,
        instance_name=__ret__.instance_name,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        vpc_ids=__ret__.vpc_ids)
