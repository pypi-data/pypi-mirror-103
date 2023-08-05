# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AlidnsRecordArgs', 'AlidnsRecord']

@pulumi.input_type
class AlidnsRecordArgs:
    def __init__(__self__, *,
                 domain_name: pulumi.Input[str],
                 rr: pulumi.Input[str],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str],
                 lang: Optional[pulumi.Input[str]] = None,
                 line: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 user_client_ip: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AlidnsRecord resource.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] rr: Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        :param pulumi.Input[str] type: The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        :param pulumi.Input[str] value: The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] line: The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        :param pulumi.Input[int] priority: The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        :param pulumi.Input[str] remark: The remark of the domain record.
        :param pulumi.Input[str] status: The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        :param pulumi.Input[int] ttl: The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        :param pulumi.Input[str] user_client_ip: The IP address of the client.
        """
        pulumi.set(__self__, "domain_name", domain_name)
        pulumi.set(__self__, "rr", rr)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)
        if lang is not None:
            pulumi.set(__self__, "lang", lang)
        if line is not None:
            pulumi.set(__self__, "line", line)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if remark is not None:
            pulumi.set(__self__, "remark", remark)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if user_client_ip is not None:
            pulumi.set(__self__, "user_client_ip", user_client_ip)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def rr(self) -> pulumi.Input[str]:
        """
        Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        """
        return pulumi.get(self, "rr")

    @rr.setter
    def rr(self, value: pulumi.Input[str]):
        pulumi.set(self, "rr", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter
    def lang(self) -> Optional[pulumi.Input[str]]:
        """
        User language.
        """
        return pulumi.get(self, "lang")

    @lang.setter
    def lang(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lang", value)

    @property
    @pulumi.getter
    def line(self) -> Optional[pulumi.Input[str]]:
        """
        The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        """
        return pulumi.get(self, "line")

    @line.setter
    def line(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "line", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def remark(self) -> Optional[pulumi.Input[str]]:
        """
        The remark of the domain record.
        """
        return pulumi.get(self, "remark")

    @remark.setter
    def remark(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "remark", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter(name="userClientIp")
    def user_client_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the client.
        """
        return pulumi.get(self, "user_client_ip")

    @user_client_ip.setter
    def user_client_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_client_ip", value)


@pulumi.input_type
class _AlidnsRecordState:
    def __init__(__self__, *,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 lang: Optional[pulumi.Input[str]] = None,
                 line: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 rr: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 user_client_ip: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AlidnsRecord resources.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] line: The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        :param pulumi.Input[int] priority: The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        :param pulumi.Input[str] remark: The remark of the domain record.
        :param pulumi.Input[str] rr: Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        :param pulumi.Input[str] status: The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        :param pulumi.Input[int] ttl: The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        :param pulumi.Input[str] type: The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        :param pulumi.Input[str] user_client_ip: The IP address of the client.
        :param pulumi.Input[str] value: The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if lang is not None:
            pulumi.set(__self__, "lang", lang)
        if line is not None:
            pulumi.set(__self__, "line", line)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if remark is not None:
            pulumi.set(__self__, "remark", remark)
        if rr is not None:
            pulumi.set(__self__, "rr", rr)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_client_ip is not None:
            pulumi.set(__self__, "user_client_ip", user_client_ip)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def lang(self) -> Optional[pulumi.Input[str]]:
        """
        User language.
        """
        return pulumi.get(self, "lang")

    @lang.setter
    def lang(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lang", value)

    @property
    @pulumi.getter
    def line(self) -> Optional[pulumi.Input[str]]:
        """
        The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        """
        return pulumi.get(self, "line")

    @line.setter
    def line(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "line", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def remark(self) -> Optional[pulumi.Input[str]]:
        """
        The remark of the domain record.
        """
        return pulumi.get(self, "remark")

    @remark.setter
    def remark(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "remark", value)

    @property
    @pulumi.getter
    def rr(self) -> Optional[pulumi.Input[str]]:
        """
        Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        """
        return pulumi.get(self, "rr")

    @rr.setter
    def rr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rr", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userClientIp")
    def user_client_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the client.
        """
        return pulumi.get(self, "user_client_ip")

    @user_client_ip.setter
    def user_client_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_client_ip", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class AlidnsRecord(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 lang: Optional[pulumi.Input[str]] = None,
                 line: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 rr: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 user_client_ip: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Alidns Record resource. For information about Alidns Domain Record and how to use it, see [What is Resource Alidns Record](https://www.alibabacloud.com/help/en/doc-detail/29772.htm).

        > **NOTE:** Available in v1.85.0+.

        > **NOTE:** When the site is an international site, the `type` neither supports `REDIRECT_URL` nor `REDIRECT_URL`

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new Domain Record
        record = alicloud.dns.AlidnsRecord("record",
            domain_name="domainname",
            remark="Test new alidns record.",
            rr="@",
            status="ENABLE",
            type="A",
            value="192.168.99.99")
        ```

        ## Import

        Alidns Domain Record can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:dns/alidnsRecord:AlidnsRecord example abc123456
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] line: The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        :param pulumi.Input[int] priority: The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        :param pulumi.Input[str] remark: The remark of the domain record.
        :param pulumi.Input[str] rr: Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        :param pulumi.Input[str] status: The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        :param pulumi.Input[int] ttl: The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        :param pulumi.Input[str] type: The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        :param pulumi.Input[str] user_client_ip: The IP address of the client.
        :param pulumi.Input[str] value: The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AlidnsRecordArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Alidns Record resource. For information about Alidns Domain Record and how to use it, see [What is Resource Alidns Record](https://www.alibabacloud.com/help/en/doc-detail/29772.htm).

        > **NOTE:** Available in v1.85.0+.

        > **NOTE:** When the site is an international site, the `type` neither supports `REDIRECT_URL` nor `REDIRECT_URL`

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new Domain Record
        record = alicloud.dns.AlidnsRecord("record",
            domain_name="domainname",
            remark="Test new alidns record.",
            rr="@",
            status="ENABLE",
            type="A",
            value="192.168.99.99")
        ```

        ## Import

        Alidns Domain Record can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:dns/alidnsRecord:AlidnsRecord example abc123456
        ```

        :param str resource_name: The name of the resource.
        :param AlidnsRecordArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AlidnsRecordArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 lang: Optional[pulumi.Input[str]] = None,
                 line: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 rr: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 user_client_ip: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AlidnsRecordArgs.__new__(AlidnsRecordArgs)

            if domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_name'")
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["lang"] = lang
            __props__.__dict__["line"] = line
            __props__.__dict__["priority"] = priority
            __props__.__dict__["remark"] = remark
            if rr is None and not opts.urn:
                raise TypeError("Missing required property 'rr'")
            __props__.__dict__["rr"] = rr
            __props__.__dict__["status"] = status
            __props__.__dict__["ttl"] = ttl
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["user_client_ip"] = user_client_ip
            if value is None and not opts.urn:
                raise TypeError("Missing required property 'value'")
            __props__.__dict__["value"] = value
        super(AlidnsRecord, __self__).__init__(
            'alicloud:dns/alidnsRecord:AlidnsRecord',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            lang: Optional[pulumi.Input[str]] = None,
            line: Optional[pulumi.Input[str]] = None,
            priority: Optional[pulumi.Input[int]] = None,
            remark: Optional[pulumi.Input[str]] = None,
            rr: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            ttl: Optional[pulumi.Input[int]] = None,
            type: Optional[pulumi.Input[str]] = None,
            user_client_ip: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[str]] = None) -> 'AlidnsRecord':
        """
        Get an existing AlidnsRecord resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] line: The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        :param pulumi.Input[int] priority: The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        :param pulumi.Input[str] remark: The remark of the domain record.
        :param pulumi.Input[str] rr: Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        :param pulumi.Input[str] status: The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        :param pulumi.Input[int] ttl: The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        :param pulumi.Input[str] type: The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        :param pulumi.Input[str] user_client_ip: The IP address of the client.
        :param pulumi.Input[str] value: The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AlidnsRecordState.__new__(_AlidnsRecordState)

        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["lang"] = lang
        __props__.__dict__["line"] = line
        __props__.__dict__["priority"] = priority
        __props__.__dict__["remark"] = remark
        __props__.__dict__["rr"] = rr
        __props__.__dict__["status"] = status
        __props__.__dict__["ttl"] = ttl
        __props__.__dict__["type"] = type
        __props__.__dict__["user_client_ip"] = user_client_ip
        __props__.__dict__["value"] = value
        return AlidnsRecord(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        Name of the domain. This name without suffix can have a string of 1 to 63 characters, must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def lang(self) -> pulumi.Output[Optional[str]]:
        """
        User language.
        """
        return pulumi.get(self, "lang")

    @property
    @pulumi.getter
    def line(self) -> pulumi.Output[Optional[str]]:
        """
        The resolution line of domain record. When the `type` is `FORWORD_URL`, this parameter must be `default`. Default value is `default`. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/doc-detail/34339.htm) or using dns.getResolutionLines in data source to get the value.
        """
        return pulumi.get(self, "line")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[int]]:
        """
        The priority of domain record. Valid values: `[1-10]`. When the `type` is `MX`, this parameter is required.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def remark(self) -> pulumi.Output[Optional[str]]:
        """
        The remark of the domain record.
        """
        return pulumi.get(self, "remark")

    @property
    @pulumi.getter
    def rr(self) -> pulumi.Output[str]:
        """
        Host record for the domain record. This host_record can have at most 253 characters, and each part split with `.` can have at most 63 characters, and must contain only alphanumeric characters or hyphens, such as `-`, `.`, `*`, `@`, and must not begin or end with `-`.
        """
        return pulumi.get(self, "rr")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        The status of the domain record. Valid values: `ENABLE`,`DISABLE`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The effective time of domain record. Its scope depends on the edition of the cloud resolution. Free is `[600, 86400]`, Basic is `[120, 86400]`, Standard is `[60, 86400]`, Ultimate is `[10, 86400]`, Exclusive is `[1, 86400]`. Default value is `600`.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of domain record. Valid values: `A`,`NS`,`MX`,`TXT`,`CNAME`,`SRV`,`AAAA`,`CAA`, `REDIRECT_URL` and `FORWORD_URL`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userClientIp")
    def user_client_ip(self) -> pulumi.Output[Optional[str]]:
        """
        The IP address of the client.
        """
        return pulumi.get(self, "user_client_ip")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[str]:
        """
        The value of domain record, When the `type` is `MX`,`NS`,`CNAME`,`SRV`, the server will treat the `value` as a fully qualified domain name, so it's no need to add a `.` at the end.
        """
        return pulumi.get(self, "value")

