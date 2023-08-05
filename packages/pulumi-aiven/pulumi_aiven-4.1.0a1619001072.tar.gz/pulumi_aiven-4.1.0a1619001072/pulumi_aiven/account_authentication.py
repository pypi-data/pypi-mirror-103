# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AccountAuthenticationArgs', 'AccountAuthentication']

@pulumi.input_type
class AccountAuthenticationArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str],
                 type: pulumi.Input[str],
                 authentication_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_acs_url: Optional[pulumi.Input[str]] = None,
                 saml_certificate: Optional[pulumi.Input[str]] = None,
                 saml_entity_id: Optional[pulumi.Input[str]] = None,
                 saml_idp_url: Optional[pulumi.Input[str]] = None,
                 saml_metadata_url: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AccountAuthentication resource.
        :param pulumi.Input[str] account_id: is a unique account id.
        :param pulumi.Input[str] type: is an account authentication type, can be one of `internal` and `saml`.
        :param pulumi.Input[str] authentication_id: account authentication id.
        :param pulumi.Input[str] create_time: time of creation.
        :param pulumi.Input[bool] enabled: defines an authentication method enabled or not.
        :param pulumi.Input[str] name: is an account authentication name.
        :param pulumi.Input[str] saml_acs_url: is a SAML Assertion Consumer Service URL.
        :param pulumi.Input[str] saml_certificate: is a SAML Certificate.
        :param pulumi.Input[str] saml_entity_id: is a SAML Entity ID.
        :param pulumi.Input[str] saml_idp_url: is a SAML Idp URL.
        :param pulumi.Input[str] saml_metadata_url: is a SAML Metadata URL.
        :param pulumi.Input[str] update_time: time of last update.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "type", type)
        if authentication_id is not None:
            pulumi.set(__self__, "authentication_id", authentication_id)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if saml_acs_url is not None:
            pulumi.set(__self__, "saml_acs_url", saml_acs_url)
        if saml_certificate is not None:
            pulumi.set(__self__, "saml_certificate", saml_certificate)
        if saml_entity_id is not None:
            pulumi.set(__self__, "saml_entity_id", saml_entity_id)
        if saml_idp_url is not None:
            pulumi.set(__self__, "saml_idp_url", saml_idp_url)
        if saml_metadata_url is not None:
            pulumi.set(__self__, "saml_metadata_url", saml_metadata_url)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        """
        is a unique account id.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        is an account authentication type, can be one of `internal` and `saml`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="authenticationId")
    def authentication_id(self) -> Optional[pulumi.Input[str]]:
        """
        account authentication id.
        """
        return pulumi.get(self, "authentication_id")

    @authentication_id.setter
    def authentication_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_id", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        time of creation.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        defines an authentication method enabled or not.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        is an account authentication name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="samlAcsUrl")
    def saml_acs_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Assertion Consumer Service URL.
        """
        return pulumi.get(self, "saml_acs_url")

    @saml_acs_url.setter
    def saml_acs_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_acs_url", value)

    @property
    @pulumi.getter(name="samlCertificate")
    def saml_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Certificate.
        """
        return pulumi.get(self, "saml_certificate")

    @saml_certificate.setter
    def saml_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_certificate", value)

    @property
    @pulumi.getter(name="samlEntityId")
    def saml_entity_id(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Entity ID.
        """
        return pulumi.get(self, "saml_entity_id")

    @saml_entity_id.setter
    def saml_entity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_entity_id", value)

    @property
    @pulumi.getter(name="samlIdpUrl")
    def saml_idp_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Idp URL.
        """
        return pulumi.get(self, "saml_idp_url")

    @saml_idp_url.setter
    def saml_idp_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_idp_url", value)

    @property
    @pulumi.getter(name="samlMetadataUrl")
    def saml_metadata_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Metadata URL.
        """
        return pulumi.get(self, "saml_metadata_url")

    @saml_metadata_url.setter
    def saml_metadata_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_metadata_url", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        time of last update.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


@pulumi.input_type
class _AccountAuthenticationState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 authentication_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_acs_url: Optional[pulumi.Input[str]] = None,
                 saml_certificate: Optional[pulumi.Input[str]] = None,
                 saml_entity_id: Optional[pulumi.Input[str]] = None,
                 saml_idp_url: Optional[pulumi.Input[str]] = None,
                 saml_metadata_url: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccountAuthentication resources.
        :param pulumi.Input[str] account_id: is a unique account id.
        :param pulumi.Input[str] authentication_id: account authentication id.
        :param pulumi.Input[str] create_time: time of creation.
        :param pulumi.Input[bool] enabled: defines an authentication method enabled or not.
        :param pulumi.Input[str] name: is an account authentication name.
        :param pulumi.Input[str] saml_acs_url: is a SAML Assertion Consumer Service URL.
        :param pulumi.Input[str] saml_certificate: is a SAML Certificate.
        :param pulumi.Input[str] saml_entity_id: is a SAML Entity ID.
        :param pulumi.Input[str] saml_idp_url: is a SAML Idp URL.
        :param pulumi.Input[str] saml_metadata_url: is a SAML Metadata URL.
        :param pulumi.Input[str] type: is an account authentication type, can be one of `internal` and `saml`.
        :param pulumi.Input[str] update_time: time of last update.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if authentication_id is not None:
            pulumi.set(__self__, "authentication_id", authentication_id)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if saml_acs_url is not None:
            pulumi.set(__self__, "saml_acs_url", saml_acs_url)
        if saml_certificate is not None:
            pulumi.set(__self__, "saml_certificate", saml_certificate)
        if saml_entity_id is not None:
            pulumi.set(__self__, "saml_entity_id", saml_entity_id)
        if saml_idp_url is not None:
            pulumi.set(__self__, "saml_idp_url", saml_idp_url)
        if saml_metadata_url is not None:
            pulumi.set(__self__, "saml_metadata_url", saml_metadata_url)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        is a unique account id.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="authenticationId")
    def authentication_id(self) -> Optional[pulumi.Input[str]]:
        """
        account authentication id.
        """
        return pulumi.get(self, "authentication_id")

    @authentication_id.setter
    def authentication_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication_id", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        time of creation.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        defines an authentication method enabled or not.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        is an account authentication name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="samlAcsUrl")
    def saml_acs_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Assertion Consumer Service URL.
        """
        return pulumi.get(self, "saml_acs_url")

    @saml_acs_url.setter
    def saml_acs_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_acs_url", value)

    @property
    @pulumi.getter(name="samlCertificate")
    def saml_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Certificate.
        """
        return pulumi.get(self, "saml_certificate")

    @saml_certificate.setter
    def saml_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_certificate", value)

    @property
    @pulumi.getter(name="samlEntityId")
    def saml_entity_id(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Entity ID.
        """
        return pulumi.get(self, "saml_entity_id")

    @saml_entity_id.setter
    def saml_entity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_entity_id", value)

    @property
    @pulumi.getter(name="samlIdpUrl")
    def saml_idp_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Idp URL.
        """
        return pulumi.get(self, "saml_idp_url")

    @saml_idp_url.setter
    def saml_idp_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_idp_url", value)

    @property
    @pulumi.getter(name="samlMetadataUrl")
    def saml_metadata_url(self) -> Optional[pulumi.Input[str]]:
        """
        is a SAML Metadata URL.
        """
        return pulumi.get(self, "saml_metadata_url")

    @saml_metadata_url.setter
    def saml_metadata_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saml_metadata_url", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        is an account authentication type, can be one of `internal` and `saml`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        time of last update.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class AccountAuthentication(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 authentication_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_acs_url: Optional[pulumi.Input[str]] = None,
                 saml_certificate: Optional[pulumi.Input[str]] = None,
                 saml_entity_id: Optional[pulumi.Input[str]] = None,
                 saml_idp_url: Optional[pulumi.Input[str]] = None,
                 saml_metadata_url: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## # Account Authentication Resource

        The Account Authentication resource allows the creation and management of an Aiven Account Authentications.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: is a unique account id.
        :param pulumi.Input[str] authentication_id: account authentication id.
        :param pulumi.Input[str] create_time: time of creation.
        :param pulumi.Input[bool] enabled: defines an authentication method enabled or not.
        :param pulumi.Input[str] name: is an account authentication name.
        :param pulumi.Input[str] saml_acs_url: is a SAML Assertion Consumer Service URL.
        :param pulumi.Input[str] saml_certificate: is a SAML Certificate.
        :param pulumi.Input[str] saml_entity_id: is a SAML Entity ID.
        :param pulumi.Input[str] saml_idp_url: is a SAML Idp URL.
        :param pulumi.Input[str] saml_metadata_url: is a SAML Metadata URL.
        :param pulumi.Input[str] type: is an account authentication type, can be one of `internal` and `saml`.
        :param pulumi.Input[str] update_time: time of last update.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountAuthenticationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Account Authentication Resource

        The Account Authentication resource allows the creation and management of an Aiven Account Authentications.

        :param str resource_name: The name of the resource.
        :param AccountAuthenticationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountAuthenticationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 authentication_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 saml_acs_url: Optional[pulumi.Input[str]] = None,
                 saml_certificate: Optional[pulumi.Input[str]] = None,
                 saml_entity_id: Optional[pulumi.Input[str]] = None,
                 saml_idp_url: Optional[pulumi.Input[str]] = None,
                 saml_metadata_url: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None,
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
            __props__ = AccountAuthenticationArgs.__new__(AccountAuthenticationArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["authentication_id"] = authentication_id
            __props__.__dict__["create_time"] = create_time
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["name"] = name
            __props__.__dict__["saml_acs_url"] = saml_acs_url
            __props__.__dict__["saml_certificate"] = saml_certificate
            __props__.__dict__["saml_entity_id"] = saml_entity_id
            __props__.__dict__["saml_idp_url"] = saml_idp_url
            __props__.__dict__["saml_metadata_url"] = saml_metadata_url
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["update_time"] = update_time
        super(AccountAuthentication, __self__).__init__(
            'aiven:index/accountAuthentication:AccountAuthentication',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            authentication_id: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            saml_acs_url: Optional[pulumi.Input[str]] = None,
            saml_certificate: Optional[pulumi.Input[str]] = None,
            saml_entity_id: Optional[pulumi.Input[str]] = None,
            saml_idp_url: Optional[pulumi.Input[str]] = None,
            saml_metadata_url: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'AccountAuthentication':
        """
        Get an existing AccountAuthentication resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: is a unique account id.
        :param pulumi.Input[str] authentication_id: account authentication id.
        :param pulumi.Input[str] create_time: time of creation.
        :param pulumi.Input[bool] enabled: defines an authentication method enabled or not.
        :param pulumi.Input[str] name: is an account authentication name.
        :param pulumi.Input[str] saml_acs_url: is a SAML Assertion Consumer Service URL.
        :param pulumi.Input[str] saml_certificate: is a SAML Certificate.
        :param pulumi.Input[str] saml_entity_id: is a SAML Entity ID.
        :param pulumi.Input[str] saml_idp_url: is a SAML Idp URL.
        :param pulumi.Input[str] saml_metadata_url: is a SAML Metadata URL.
        :param pulumi.Input[str] type: is an account authentication type, can be one of `internal` and `saml`.
        :param pulumi.Input[str] update_time: time of last update.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountAuthenticationState.__new__(_AccountAuthenticationState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["authentication_id"] = authentication_id
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["saml_acs_url"] = saml_acs_url
        __props__.__dict__["saml_certificate"] = saml_certificate
        __props__.__dict__["saml_entity_id"] = saml_entity_id
        __props__.__dict__["saml_idp_url"] = saml_idp_url
        __props__.__dict__["saml_metadata_url"] = saml_metadata_url
        __props__.__dict__["type"] = type
        __props__.__dict__["update_time"] = update_time
        return AccountAuthentication(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        is a unique account id.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="authenticationId")
    def authentication_id(self) -> pulumi.Output[str]:
        """
        account authentication id.
        """
        return pulumi.get(self, "authentication_id")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        time of creation.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        defines an authentication method enabled or not.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        is an account authentication name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="samlAcsUrl")
    def saml_acs_url(self) -> pulumi.Output[str]:
        """
        is a SAML Assertion Consumer Service URL.
        """
        return pulumi.get(self, "saml_acs_url")

    @property
    @pulumi.getter(name="samlCertificate")
    def saml_certificate(self) -> pulumi.Output[Optional[str]]:
        """
        is a SAML Certificate.
        """
        return pulumi.get(self, "saml_certificate")

    @property
    @pulumi.getter(name="samlEntityId")
    def saml_entity_id(self) -> pulumi.Output[Optional[str]]:
        """
        is a SAML Entity ID.
        """
        return pulumi.get(self, "saml_entity_id")

    @property
    @pulumi.getter(name="samlIdpUrl")
    def saml_idp_url(self) -> pulumi.Output[Optional[str]]:
        """
        is a SAML Idp URL.
        """
        return pulumi.get(self, "saml_idp_url")

    @property
    @pulumi.getter(name="samlMetadataUrl")
    def saml_metadata_url(self) -> pulumi.Output[str]:
        """
        is a SAML Metadata URL.
        """
        return pulumi.get(self, "saml_metadata_url")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        is an account authentication type, can be one of `internal` and `saml`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        time of last update.
        """
        return pulumi.get(self, "update_time")

