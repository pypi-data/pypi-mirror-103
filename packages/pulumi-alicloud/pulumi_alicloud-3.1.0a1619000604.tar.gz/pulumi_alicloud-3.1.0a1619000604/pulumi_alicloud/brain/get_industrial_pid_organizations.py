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
    'GetIndustrialPidOrganizationsResult',
    'AwaitableGetIndustrialPidOrganizationsResult',
    'get_industrial_pid_organizations',
]

@pulumi.output_type
class GetIndustrialPidOrganizationsResult:
    """
    A collection of values returned by getIndustrialPidOrganizations.
    """
    def __init__(__self__, id=None, ids=None, name_regex=None, names=None, organizations=None, output_file=None, parent_organization_id=None):
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
        if organizations and not isinstance(organizations, list):
            raise TypeError("Expected argument 'organizations' to be a list")
        pulumi.set(__self__, "organizations", organizations)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if parent_organization_id and not isinstance(parent_organization_id, str):
            raise TypeError("Expected argument 'parent_organization_id' to be a str")
        pulumi.set(__self__, "parent_organization_id", parent_organization_id)

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
    @pulumi.getter
    def organizations(self) -> Sequence['outputs.GetIndustrialPidOrganizationsOrganizationResult']:
        return pulumi.get(self, "organizations")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="parentOrganizationId")
    def parent_organization_id(self) -> Optional[str]:
        return pulumi.get(self, "parent_organization_id")


class AwaitableGetIndustrialPidOrganizationsResult(GetIndustrialPidOrganizationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIndustrialPidOrganizationsResult(
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            organizations=self.organizations,
            output_file=self.output_file,
            parent_organization_id=self.parent_organization_id)


def get_industrial_pid_organizations(ids: Optional[Sequence[str]] = None,
                                     name_regex: Optional[str] = None,
                                     output_file: Optional[str] = None,
                                     parent_organization_id: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIndustrialPidOrganizationsResult:
    """
    This data source provides the Brain Industrial Pid Organizations of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.113.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.brain.get_industrial_pid_organizations(ids=["3e74e684-cbb5-xxxx"],
        name_regex="tf-testAcc")
    pulumi.export("firstBrainIndustrialPidOrganizationId", example.organizations[0].id)
    ```


    :param Sequence[str] ids: A list of Pid Organization IDs.
    :param str name_regex: A regex string to filter results by Pid Organization name.
    :param str parent_organization_id: The parent organization id.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['parentOrganizationId'] = parent_organization_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:brain/getIndustrialPidOrganizations:getIndustrialPidOrganizations', __args__, opts=opts, typ=GetIndustrialPidOrganizationsResult).value

    return AwaitableGetIndustrialPidOrganizationsResult(
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        organizations=__ret__.organizations,
        output_file=__ret__.output_file,
        parent_organization_id=__ret__.parent_organization_id)
