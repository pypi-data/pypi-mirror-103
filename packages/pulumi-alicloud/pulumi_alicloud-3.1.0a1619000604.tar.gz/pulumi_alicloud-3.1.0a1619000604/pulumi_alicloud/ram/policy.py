# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 document: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 rotate_strategy: Optional[pulumi.Input[str]] = None,
                 statements: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] description: Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        :param pulumi.Input[str] document: It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        :param pulumi.Input[bool] force: This parameter is used for resource destroy. Default value is `false`.
        :param pulumi.Input[str] name: It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        :param pulumi.Input[str] policy_document: Document of the RAM policy. It is required when the `statement` is not specified.
        :param pulumi.Input[str] policy_name: Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        :param pulumi.Input[str] rotate_strategy: The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]] statements: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        :param pulumi.Input[str] version: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if document is not None:
            warnings.warn("""Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""", DeprecationWarning)
            pulumi.log.warn("""document is deprecated: Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""")
        if document is not None:
            pulumi.set(__self__, "document", document)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if name is not None:
            warnings.warn("""Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_document is not None:
            pulumi.set(__self__, "policy_document", policy_document)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if rotate_strategy is not None:
            pulumi.set(__self__, "rotate_strategy", rotate_strategy)
        if statements is not None:
            warnings.warn("""Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
            pulumi.log.warn("""statements is deprecated: Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
        if statements is not None:
            pulumi.set(__self__, "statements", statements)
        if version is not None:
            warnings.warn("""Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
            pulumi.log.warn("""version is deprecated: Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def document(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        """
        return pulumi.get(self, "document")

    @document.setter
    def document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "document", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        This parameter is used for resource destroy. Default value is `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[pulumi.Input[str]]:
        """
        Document of the RAM policy. It is required when the `statement` is not specified.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter(name="rotateStrategy")
    def rotate_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        """
        return pulumi.get(self, "rotate_strategy")

    @rotate_strategy.setter
    def rotate_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rotate_strategy", value)

    @property
    @pulumi.getter
    def statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        """
        return pulumi.get(self, "statements")

    @statements.setter
    def statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]]):
        pulumi.set(self, "statements", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class _PolicyState:
    def __init__(__self__, *,
                 attachment_count: Optional[pulumi.Input[int]] = None,
                 default_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 document: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 rotate_strategy: Optional[pulumi.Input[str]] = None,
                 statements: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input[int] attachment_count: The policy attachment count.
        :param pulumi.Input[str] default_version: The default version of policy.
        :param pulumi.Input[str] description: Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        :param pulumi.Input[str] document: It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        :param pulumi.Input[bool] force: This parameter is used for resource destroy. Default value is `false`.
        :param pulumi.Input[str] name: It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        :param pulumi.Input[str] policy_document: Document of the RAM policy. It is required when the `statement` is not specified.
        :param pulumi.Input[str] policy_name: Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        :param pulumi.Input[str] rotate_strategy: The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]] statements: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        :param pulumi.Input[str] type: The policy type.
        :param pulumi.Input[str] version: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        :param pulumi.Input[str] version_id: The ID of default version policy.
        """
        if attachment_count is not None:
            pulumi.set(__self__, "attachment_count", attachment_count)
        if default_version is not None:
            pulumi.set(__self__, "default_version", default_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if document is not None:
            warnings.warn("""Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""", DeprecationWarning)
            pulumi.log.warn("""document is deprecated: Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""")
        if document is not None:
            pulumi.set(__self__, "document", document)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if name is not None:
            warnings.warn("""Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_document is not None:
            pulumi.set(__self__, "policy_document", policy_document)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if rotate_strategy is not None:
            pulumi.set(__self__, "rotate_strategy", rotate_strategy)
        if statements is not None:
            warnings.warn("""Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
            pulumi.log.warn("""statements is deprecated: Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
        if statements is not None:
            pulumi.set(__self__, "statements", statements)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if version is not None:
            warnings.warn("""Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
            pulumi.log.warn("""version is deprecated: Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
        if version is not None:
            pulumi.set(__self__, "version", version)
        if version_id is not None:
            pulumi.set(__self__, "version_id", version_id)

    @property
    @pulumi.getter(name="attachmentCount")
    def attachment_count(self) -> Optional[pulumi.Input[int]]:
        """
        The policy attachment count.
        """
        return pulumi.get(self, "attachment_count")

    @attachment_count.setter
    def attachment_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "attachment_count", value)

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> Optional[pulumi.Input[str]]:
        """
        The default version of policy.
        """
        return pulumi.get(self, "default_version")

    @default_version.setter
    def default_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def document(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        """
        return pulumi.get(self, "document")

    @document.setter
    def document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "document", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        This parameter is used for resource destroy. Default value is `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[pulumi.Input[str]]:
        """
        Document of the RAM policy. It is required when the `statement` is not specified.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter(name="rotateStrategy")
    def rotate_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        """
        return pulumi.get(self, "rotate_strategy")

    @rotate_strategy.setter
    def rotate_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rotate_strategy", value)

    @property
    @pulumi.getter
    def statements(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        """
        return pulumi.get(self, "statements")

    @statements.setter
    def statements(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyStatementArgs']]]]):
        pulumi.set(self, "statements", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The policy type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of default version policy.
        """
        return pulumi.get(self, "version_id")

    @version_id.setter
    def version_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version_id", value)


class Policy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 document: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 rotate_strategy: Optional[pulumi.Input[str]] = None,
                 statements: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyStatementArgs']]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        RAM policy can be imported using the id or name, e.g.

        ```sh
         $ pulumi import alicloud:ram/policy:Policy example my-policy
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        :param pulumi.Input[str] document: It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        :param pulumi.Input[bool] force: This parameter is used for resource destroy. Default value is `false`.
        :param pulumi.Input[str] name: It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        :param pulumi.Input[str] policy_document: Document of the RAM policy. It is required when the `statement` is not specified.
        :param pulumi.Input[str] policy_name: Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        :param pulumi.Input[str] rotate_strategy: The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyStatementArgs']]]] statements: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        :param pulumi.Input[str] version: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[PolicyArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        RAM policy can be imported using the id or name, e.g.

        ```sh
         $ pulumi import alicloud:ram/policy:Policy example my-policy
        ```

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 document: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_document: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 rotate_strategy: Optional[pulumi.Input[str]] = None,
                 statements: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyStatementArgs']]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
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
            __props__ = PolicyArgs.__new__(PolicyArgs)

            __props__.__dict__["description"] = description
            if document is not None and not opts.urn:
                warnings.warn("""Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""", DeprecationWarning)
                pulumi.log.warn("""document is deprecated: Field 'document' has been deprecated from provider version 1.114.0. New field 'policy_document' instead.""")
            __props__.__dict__["document"] = document
            __props__.__dict__["force"] = force
            if name is not None and not opts.urn:
                warnings.warn("""Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""", DeprecationWarning)
                pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.114.0. New field 'policy_name' instead.""")
            __props__.__dict__["name"] = name
            __props__.__dict__["policy_document"] = policy_document
            __props__.__dict__["policy_name"] = policy_name
            __props__.__dict__["rotate_strategy"] = rotate_strategy
            if statements is not None and not opts.urn:
                warnings.warn("""Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
                pulumi.log.warn("""statements is deprecated: Field 'statement' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
            __props__.__dict__["statements"] = statements
            if version is not None and not opts.urn:
                warnings.warn("""Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """, DeprecationWarning)
                pulumi.log.warn("""version is deprecated: Field 'version' has been deprecated from version 1.49.0, and use field 'document' to replace. """)
            __props__.__dict__["version"] = version
            __props__.__dict__["attachment_count"] = None
            __props__.__dict__["default_version"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["version_id"] = None
        super(Policy, __self__).__init__(
            'alicloud:ram/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attachment_count: Optional[pulumi.Input[int]] = None,
            default_version: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            document: Optional[pulumi.Input[str]] = None,
            force: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy_document: Optional[pulumi.Input[str]] = None,
            policy_name: Optional[pulumi.Input[str]] = None,
            rotate_strategy: Optional[pulumi.Input[str]] = None,
            statements: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyStatementArgs']]]]] = None,
            type: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[str]] = None,
            version_id: Optional[pulumi.Input[str]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] attachment_count: The policy attachment count.
        :param pulumi.Input[str] default_version: The default version of policy.
        :param pulumi.Input[str] description: Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        :param pulumi.Input[str] document: It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        :param pulumi.Input[bool] force: This parameter is used for resource destroy. Default value is `false`.
        :param pulumi.Input[str] name: It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        :param pulumi.Input[str] policy_document: Document of the RAM policy. It is required when the `statement` is not specified.
        :param pulumi.Input[str] policy_name: Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        :param pulumi.Input[str] rotate_strategy: The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyStatementArgs']]]] statements: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        :param pulumi.Input[str] type: The policy type.
        :param pulumi.Input[str] version: (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        :param pulumi.Input[str] version_id: The ID of default version policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyState.__new__(_PolicyState)

        __props__.__dict__["attachment_count"] = attachment_count
        __props__.__dict__["default_version"] = default_version
        __props__.__dict__["description"] = description
        __props__.__dict__["document"] = document
        __props__.__dict__["force"] = force
        __props__.__dict__["name"] = name
        __props__.__dict__["policy_document"] = policy_document
        __props__.__dict__["policy_name"] = policy_name
        __props__.__dict__["rotate_strategy"] = rotate_strategy
        __props__.__dict__["statements"] = statements
        __props__.__dict__["type"] = type
        __props__.__dict__["version"] = version
        __props__.__dict__["version_id"] = version_id
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachmentCount")
    def attachment_count(self) -> pulumi.Output[int]:
        """
        The policy attachment count.
        """
        return pulumi.get(self, "attachment_count")

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> pulumi.Output[str]:
        """
        The default version of policy.
        """
        return pulumi.get(self, "default_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the RAM policy. This name can have a string of 1 to 1024 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def document(self) -> pulumi.Output[str]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_document` instead.
        """
        return pulumi.get(self, "document")

    @property
    @pulumi.getter
    def force(self) -> pulumi.Output[Optional[bool]]:
        """
        This parameter is used for resource destroy. Default value is `false`.
        """
        return pulumi.get(self, "force")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        It has been deprecated from provider version 1.114.0 and `policy_name` instead.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> pulumi.Output[str]:
        """
        Document of the RAM policy. It is required when the `statement` is not specified.
        """
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Output[str]:
        """
        Name of the RAM policy. This name can have a string of 1 to 128 characters, must contain only alphanumeric characters or hyphen "-", and must not begin with a hyphen.
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter(name="rotateStrategy")
    def rotate_strategy(self) -> pulumi.Output[Optional[str]]:
        """
        The rotation strategy of the policy. You can use this parameter to delete an early policy version. Valid Values: `None`, `DeleteOldestNonDefaultVersionWhenLimitExceeded`. Default to `None`.
        """
        return pulumi.get(self, "rotate_strategy")

    @property
    @pulumi.getter
    def statements(self) -> pulumi.Output[Sequence['outputs.PolicyStatement']]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Statements of the RAM policy document. It is required when the `document` is not specified.
        """
        return pulumi.get(self, "statements")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The policy type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        (It has been deprecated from version 1.49.0, and use field 'document' to replace.) Version of the RAM policy document. Valid value is `1`. Default value is `1`.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> pulumi.Output[str]:
        """
        The ID of default version policy.
        """
        return pulumi.get(self, "version_id")

