# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['KafkaAclArgs', 'KafkaAcl']

@pulumi.input_type
class KafkaAclArgs:
    def __init__(__self__, *,
                 permission: pulumi.Input[str],
                 project: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 topic: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        The set of arguments for constructing a KafkaAcl resource.
        :param pulumi.Input[str] permission: is the level of permission the matching users are given to the matching
               topics (admin, read, readwrite, write).
        :param pulumi.Input[str] project: and `service_name` - (Required) define the project and service the ACL belongs to.
               They should be defined using reference as shown above to set up dependencies correctly.
               These properties cannot be changed once the service is created. Doing so will result in
               the topic being deleted and new one created instead.
        :param pulumi.Input[str] service_name: Service to link the Kafka ACL to
        :param pulumi.Input[str] topic: is a topic name pattern the ACL entry matches to.
        :param pulumi.Input[str] username: is a username pattern the ACL entry matches to.
        """
        pulumi.set(__self__, "permission", permission)
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "topic", topic)
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Input[str]:
        """
        is the level of permission the matching users are given to the matching
        topics (admin, read, readwrite, write).
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: pulumi.Input[str]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        and `service_name` - (Required) define the project and service the ACL belongs to.
        They should be defined using reference as shown above to set up dependencies correctly.
        These properties cannot be changed once the service is created. Doing so will result in
        the topic being deleted and new one created instead.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Service to link the Kafka ACL to
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Input[str]:
        """
        is a topic name pattern the ACL entry matches to.
        """
        return pulumi.get(self, "topic")

    @topic.setter
    def topic(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        is a username pattern the ACL entry matches to.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _KafkaAclState:
    def __init__(__self__, *,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 topic: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KafkaAcl resources.
        :param pulumi.Input[str] permission: is the level of permission the matching users are given to the matching
               topics (admin, read, readwrite, write).
        :param pulumi.Input[str] project: and `service_name` - (Required) define the project and service the ACL belongs to.
               They should be defined using reference as shown above to set up dependencies correctly.
               These properties cannot be changed once the service is created. Doing so will result in
               the topic being deleted and new one created instead.
        :param pulumi.Input[str] service_name: Service to link the Kafka ACL to
        :param pulumi.Input[str] topic: is a topic name pattern the ACL entry matches to.
        :param pulumi.Input[str] username: is a username pattern the ACL entry matches to.
        """
        if permission is not None:
            pulumi.set(__self__, "permission", permission)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)
        if topic is not None:
            pulumi.set(__self__, "topic", topic)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def permission(self) -> Optional[pulumi.Input[str]]:
        """
        is the level of permission the matching users are given to the matching
        topics (admin, read, readwrite, write).
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        and `service_name` - (Required) define the project and service the ACL belongs to.
        They should be defined using reference as shown above to set up dependencies correctly.
        These properties cannot be changed once the service is created. Doing so will result in
        the topic being deleted and new one created instead.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        Service to link the Kafka ACL to
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def topic(self) -> Optional[pulumi.Input[str]]:
        """
        is a topic name pattern the ACL entry matches to.
        """
        return pulumi.get(self, "topic")

    @topic.setter
    def topic(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "topic", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        is a username pattern the ACL entry matches to.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class KafkaAcl(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 topic: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## # Resource Kafka ACL Resource

        The Resource Kafka ACL resource allows the creation and management of ACLs for an Aiven Kafka service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        mytestacl = aiven.KafkaAcl("mytestacl",
            permission="admin",
            project=aiven_project["myproject"]["project"],
            service_name=aiven_service["myservice"]["service_name"],
            topic="<TOPIC_NAME_PATTERN>",
            username="<USERNAME_PATTERN>")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] permission: is the level of permission the matching users are given to the matching
               topics (admin, read, readwrite, write).
        :param pulumi.Input[str] project: and `service_name` - (Required) define the project and service the ACL belongs to.
               They should be defined using reference as shown above to set up dependencies correctly.
               These properties cannot be changed once the service is created. Doing so will result in
               the topic being deleted and new one created instead.
        :param pulumi.Input[str] service_name: Service to link the Kafka ACL to
        :param pulumi.Input[str] topic: is a topic name pattern the ACL entry matches to.
        :param pulumi.Input[str] username: is a username pattern the ACL entry matches to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KafkaAclArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## # Resource Kafka ACL Resource

        The Resource Kafka ACL resource allows the creation and management of ACLs for an Aiven Kafka service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        mytestacl = aiven.KafkaAcl("mytestacl",
            permission="admin",
            project=aiven_project["myproject"]["project"],
            service_name=aiven_service["myservice"]["service_name"],
            topic="<TOPIC_NAME_PATTERN>",
            username="<USERNAME_PATTERN>")
        ```

        :param str resource_name: The name of the resource.
        :param KafkaAclArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KafkaAclArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 topic: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
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
            __props__ = KafkaAclArgs.__new__(KafkaAclArgs)

            if permission is None and not opts.urn:
                raise TypeError("Missing required property 'permission'")
            __props__.__dict__["permission"] = permission
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            if topic is None and not opts.urn:
                raise TypeError("Missing required property 'topic'")
            __props__.__dict__["topic"] = topic
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        super(KafkaAcl, __self__).__init__(
            'aiven:index/kafkaAcl:KafkaAcl',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            permission: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service_name: Optional[pulumi.Input[str]] = None,
            topic: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'KafkaAcl':
        """
        Get an existing KafkaAcl resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] permission: is the level of permission the matching users are given to the matching
               topics (admin, read, readwrite, write).
        :param pulumi.Input[str] project: and `service_name` - (Required) define the project and service the ACL belongs to.
               They should be defined using reference as shown above to set up dependencies correctly.
               These properties cannot be changed once the service is created. Doing so will result in
               the topic being deleted and new one created instead.
        :param pulumi.Input[str] service_name: Service to link the Kafka ACL to
        :param pulumi.Input[str] topic: is a topic name pattern the ACL entry matches to.
        :param pulumi.Input[str] username: is a username pattern the ACL entry matches to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KafkaAclState.__new__(_KafkaAclState)

        __props__.__dict__["permission"] = permission
        __props__.__dict__["project"] = project
        __props__.__dict__["service_name"] = service_name
        __props__.__dict__["topic"] = topic
        __props__.__dict__["username"] = username
        return KafkaAcl(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Output[str]:
        """
        is the level of permission the matching users are given to the matching
        topics (admin, read, readwrite, write).
        """
        return pulumi.get(self, "permission")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        and `service_name` - (Required) define the project and service the ACL belongs to.
        They should be defined using reference as shown above to set up dependencies correctly.
        These properties cannot be changed once the service is created. Doing so will result in
        the topic being deleted and new one created instead.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Output[str]:
        """
        Service to link the Kafka ACL to
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Output[str]:
        """
        is a topic name pattern the ACL entry matches to.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        is a username pattern the ACL entry matches to.
        """
        return pulumi.get(self, "username")

