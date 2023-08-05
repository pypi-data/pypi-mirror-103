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
    'GetAccountsResult',
    'AwaitableGetAccountsResult',
    'get_accounts',
]

@pulumi.output_type
class GetAccountsResult:
    """
    A collection of values returned by getAccounts.
    """
    def __init__(__self__, accounts=None, id=None, ids=None, output_file=None, status=None):
        if accounts and not isinstance(accounts, list):
            raise TypeError("Expected argument 'accounts' to be a list")
        pulumi.set(__self__, "accounts", accounts)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def accounts(self) -> Sequence['outputs.GetAccountsAccountResult']:
        """
        A list of accounts. Each element contains the following attributes:
        """
        return pulumi.get(self, "accounts")

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
        """
        A list of account IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the member account.
        """
        return pulumi.get(self, "status")


class AwaitableGetAccountsResult(GetAccountsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountsResult(
            accounts=self.accounts,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            status=self.status)


def get_accounts(ids: Optional[Sequence[str]] = None,
                 output_file: Optional[str] = None,
                 status: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountsResult:
    """
    This data source provides the Resource Manager Accounts of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.86.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.resourcemanager.get_accounts()
    pulumi.export("firstAccountId", default.accounts[0].id)
    ```


    :param Sequence[str] ids: A list of account IDs.
    :param str status: The status of account, valid values: `CreateCancelled`, `CreateExpired`, `CreateFailed`, `CreateSuccess`, `CreateVerifying`, `InviteSuccess`, `PromoteCancelled`, `PromoteExpired`, `PromoteFailed`, `PromoteSuccess`, and `PromoteVerifying`.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getAccounts:getAccounts', __args__, opts=opts, typ=GetAccountsResult).value

    return AwaitableGetAccountsResult(
        accounts=__ret__.accounts,
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        status=__ret__.status)
