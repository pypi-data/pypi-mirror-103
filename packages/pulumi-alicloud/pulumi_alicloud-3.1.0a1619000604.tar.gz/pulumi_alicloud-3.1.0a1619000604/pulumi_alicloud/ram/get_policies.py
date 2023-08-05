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
    'GetPoliciesResult',
    'AwaitableGetPoliciesResult',
    'get_policies',
]

@pulumi.output_type
class GetPoliciesResult:
    """
    A collection of values returned by getPolicies.
    """
    def __init__(__self__, enable_details=None, group_name=None, id=None, ids=None, name_regex=None, names=None, output_file=None, policies=None, role_name=None, type=None, user_name=None):
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if group_name and not isinstance(group_name, str):
            raise TypeError("Expected argument 'group_name' to be a str")
        pulumi.set(__self__, "group_name", group_name)
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
        if policies and not isinstance(policies, list):
            raise TypeError("Expected argument 'policies' to be a list")
        pulumi.set(__self__, "policies", policies)
        if role_name and not isinstance(role_name, str):
            raise TypeError("Expected argument 'role_name' to be a str")
        pulumi.set(__self__, "role_name", role_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[str]:
        return pulumi.get(self, "group_name")

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
        """
        A list of ram group names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def policies(self) -> Sequence['outputs.GetPoliciesPolicyResult']:
        """
        A list of policies. Each element contains the following attributes:
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[str]:
        return pulumi.get(self, "role_name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Type of the policy.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[str]:
        return pulumi.get(self, "user_name")


class AwaitableGetPoliciesResult(GetPoliciesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPoliciesResult(
            enable_details=self.enable_details,
            group_name=self.group_name,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            policies=self.policies,
            role_name=self.role_name,
            type=self.type,
            user_name=self.user_name)


def get_policies(enable_details: Optional[bool] = None,
                 group_name: Optional[str] = None,
                 ids: Optional[Sequence[str]] = None,
                 name_regex: Optional[str] = None,
                 output_file: Optional[str] = None,
                 role_name: Optional[str] = None,
                 type: Optional[str] = None,
                 user_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPoliciesResult:
    """
    This data source provides a list of RAM policies in an Alibaba Cloud account according to the specified filters.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    policies_ds = alicloud.ram.get_policies(group_name="group1",
        output_file="policies.txt",
        type="System",
        user_name="user1")
    pulumi.export("firstPolicyName", policies_ds.policies[0].name)
    ```


    :param bool enable_details: Default to `true`. Set it to true can output more details.
    :param str group_name: Filter results by a specific group name. Returned policies are attached to the specified group.
    :param str name_regex: A regex string to filter resulting policies by name.
    :param str role_name: Filter results by a specific role name. Returned policies are attached to the specified role.
    :param str type: Filter results by a specific policy type. Valid values are `Custom` and `System`.
    :param str user_name: Filter results by a specific user name. Returned policies are attached to the specified user.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['groupName'] = group_name
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['roleName'] = role_name
    __args__['type'] = type
    __args__['userName'] = user_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:ram/getPolicies:getPolicies', __args__, opts=opts, typ=GetPoliciesResult).value

    return AwaitableGetPoliciesResult(
        enable_details=__ret__.enable_details,
        group_name=__ret__.group_name,
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        policies=__ret__.policies,
        role_name=__ret__.role_name,
        type=__ret__.type,
        user_name=__ret__.user_name)
