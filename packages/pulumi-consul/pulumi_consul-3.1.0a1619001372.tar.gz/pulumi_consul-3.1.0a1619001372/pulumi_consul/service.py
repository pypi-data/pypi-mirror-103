# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ServiceArgs', 'Service']

@pulumi.input_type
class ServiceArgs:
    def __init__(__self__, *,
                 node: pulumi.Input[str],
                 address: Optional[pulumi.Input[str]] = None,
                 checks: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 enable_tag_override: Optional[pulumi.Input[bool]] = None,
                 external: Optional[pulumi.Input[bool]] = None,
                 meta: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Service resource.
        :param pulumi.Input[str] node: The name of the node the to register the service on.
        :param pulumi.Input[str] address: The address of the service. Defaults to the
               address of the node.
        :param pulumi.Input[str] datacenter: The datacenter to use. This overrides the
               agent's default datacenter and the datacenter in the provider setup.
        :param pulumi.Input[bool] enable_tag_override: Specifies to disable the
               anti-entropy feature for this service's tags. Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] meta: A map of arbitrary KV metadata linked to the service
               instance.
        :param pulumi.Input[str] name: The name of the health-check.
        :param pulumi.Input[str] namespace: The namespace to create the service within.
        :param pulumi.Input[int] port: The port of the service.
        :param pulumi.Input[str] service_id: - If the service ID is not provided, it will be defaulted to the value
               of the `name` attribute.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of values that are opaque to Consul,
               but can be used to distinguish between services or nodes.
        """
        pulumi.set(__self__, "node", node)
        if address is not None:
            pulumi.set(__self__, "address", address)
        if checks is not None:
            pulumi.set(__self__, "checks", checks)
        if datacenter is not None:
            pulumi.set(__self__, "datacenter", datacenter)
        if enable_tag_override is not None:
            pulumi.set(__self__, "enable_tag_override", enable_tag_override)
        if external is not None:
            warnings.warn("""The external field has been deprecated and does nothing.""", DeprecationWarning)
            pulumi.log.warn("""external is deprecated: The external field has been deprecated and does nothing.""")
        if external is not None:
            pulumi.set(__self__, "external", external)
        if meta is not None:
            pulumi.set(__self__, "meta", meta)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if service_id is not None:
            pulumi.set(__self__, "service_id", service_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def node(self) -> pulumi.Input[str]:
        """
        The name of the node the to register the service on.
        """
        return pulumi.get(self, "node")

    @node.setter
    def node(self, value: pulumi.Input[str]):
        pulumi.set(self, "node", value)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        The address of the service. Defaults to the
        address of the node.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def checks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]]:
        return pulumi.get(self, "checks")

    @checks.setter
    def checks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]]):
        pulumi.set(self, "checks", value)

    @property
    @pulumi.getter
    def datacenter(self) -> Optional[pulumi.Input[str]]:
        """
        The datacenter to use. This overrides the
        agent's default datacenter and the datacenter in the provider setup.
        """
        return pulumi.get(self, "datacenter")

    @datacenter.setter
    def datacenter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "datacenter", value)

    @property
    @pulumi.getter(name="enableTagOverride")
    def enable_tag_override(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies to disable the
        anti-entropy feature for this service's tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_tag_override")

    @enable_tag_override.setter
    def enable_tag_override(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_tag_override", value)

    @property
    @pulumi.getter
    def external(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "external")

    @external.setter
    def external(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "external", value)

    @property
    @pulumi.getter
    def meta(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of arbitrary KV metadata linked to the service
        instance.
        """
        return pulumi.get(self, "meta")

    @meta.setter
    def meta(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "meta", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the health-check.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to create the service within.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port of the service.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[pulumi.Input[str]]:
        """
        - If the service ID is not provided, it will be defaulted to the value
        of the `name` attribute.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that are opaque to Consul,
        but can be used to distinguish between services or nodes.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ServiceState:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 checks: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 enable_tag_override: Optional[pulumi.Input[bool]] = None,
                 external: Optional[pulumi.Input[bool]] = None,
                 meta: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Service resources.
        :param pulumi.Input[str] address: The address of the service. Defaults to the
               address of the node.
        :param pulumi.Input[str] datacenter: The datacenter to use. This overrides the
               agent's default datacenter and the datacenter in the provider setup.
        :param pulumi.Input[bool] enable_tag_override: Specifies to disable the
               anti-entropy feature for this service's tags. Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] meta: A map of arbitrary KV metadata linked to the service
               instance.
        :param pulumi.Input[str] name: The name of the health-check.
        :param pulumi.Input[str] namespace: The namespace to create the service within.
        :param pulumi.Input[str] node: The name of the node the to register the service on.
        :param pulumi.Input[int] port: The port of the service.
        :param pulumi.Input[str] service_id: - If the service ID is not provided, it will be defaulted to the value
               of the `name` attribute.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of values that are opaque to Consul,
               but can be used to distinguish between services or nodes.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if checks is not None:
            pulumi.set(__self__, "checks", checks)
        if datacenter is not None:
            pulumi.set(__self__, "datacenter", datacenter)
        if enable_tag_override is not None:
            pulumi.set(__self__, "enable_tag_override", enable_tag_override)
        if external is not None:
            warnings.warn("""The external field has been deprecated and does nothing.""", DeprecationWarning)
            pulumi.log.warn("""external is deprecated: The external field has been deprecated and does nothing.""")
        if external is not None:
            pulumi.set(__self__, "external", external)
        if meta is not None:
            pulumi.set(__self__, "meta", meta)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if node is not None:
            pulumi.set(__self__, "node", node)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if service_id is not None:
            pulumi.set(__self__, "service_id", service_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        The address of the service. Defaults to the
        address of the node.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def checks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]]:
        return pulumi.get(self, "checks")

    @checks.setter
    def checks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceCheckArgs']]]]):
        pulumi.set(self, "checks", value)

    @property
    @pulumi.getter
    def datacenter(self) -> Optional[pulumi.Input[str]]:
        """
        The datacenter to use. This overrides the
        agent's default datacenter and the datacenter in the provider setup.
        """
        return pulumi.get(self, "datacenter")

    @datacenter.setter
    def datacenter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "datacenter", value)

    @property
    @pulumi.getter(name="enableTagOverride")
    def enable_tag_override(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies to disable the
        anti-entropy feature for this service's tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_tag_override")

    @enable_tag_override.setter
    def enable_tag_override(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_tag_override", value)

    @property
    @pulumi.getter
    def external(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "external")

    @external.setter
    def external(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "external", value)

    @property
    @pulumi.getter
    def meta(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of arbitrary KV metadata linked to the service
        instance.
        """
        return pulumi.get(self, "meta")

    @meta.setter
    def meta(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "meta", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the health-check.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to create the service within.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def node(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the node the to register the service on.
        """
        return pulumi.get(self, "node")

    @node.setter
    def node(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port of the service.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[pulumi.Input[str]]:
        """
        - If the service ID is not provided, it will be defaulted to the value
        of the `name` attribute.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of values that are opaque to Consul,
        but can be used to distinguish between services or nodes.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Service(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 checks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceCheckArgs']]]]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 enable_tag_override: Optional[pulumi.Input[bool]] = None,
                 external: Optional[pulumi.Input[bool]] = None,
                 meta: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A high-level resource for creating a Service in Consul in the Consul catalog. This
        is appropriate for registering [external services](https://www.consul.io/docs/guides/external.html) and
        can be used to create services addressable by Consul that cannot be registered
        with a [local agent](https://www.consul.io/docs/agent/basics.html).

        > **NOTE:** If a Consul agent is running on the node where this service is
        registered, it is not recommended to use this resource as the service will be
        removed during the next [anti-entropy synchronisation](https://www.consul.io/docs/architecture/anti-entropy).

        ## Example Usage

        Creating a new node with the service:

        ```python
        import pulumi
        import pulumi_consul as consul

        compute = consul.Node("compute", address="www.google.com")
        google = consul.Service("google",
            node=compute.name,
            port=80,
            tags=["tag0"])
        ```

        Utilizing an existing known node:

        ```python
        import pulumi
        import pulumi_consul as consul

        google = consul.Service("google",
            node="google",
            port=443)
        ```

        Register a health-check:

        ```python
        import pulumi
        import pulumi_consul as consul

        redis = consul.Service("redis",
            checks=[consul.ServiceCheckArgs(
                check_id="service:redis1",
                deregister_critical_service_after="30s",
                headers=[
                    consul.ServiceCheckHeaderArgs(
                        name="foo",
                        value=["test"],
                    ),
                    consul.ServiceCheckHeaderArgs(
                        name="bar",
                        value=["test"],
                    ),
                ],
                http="https://www.hashicorptest.com",
                interval="5s",
                method="PUT",
                name="Redis health check",
                status="passing",
                timeout="1s",
                tls_skip_verify=False,
            )],
            node="redis",
            port=6379)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The address of the service. Defaults to the
               address of the node.
        :param pulumi.Input[str] datacenter: The datacenter to use. This overrides the
               agent's default datacenter and the datacenter in the provider setup.
        :param pulumi.Input[bool] enable_tag_override: Specifies to disable the
               anti-entropy feature for this service's tags. Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] meta: A map of arbitrary KV metadata linked to the service
               instance.
        :param pulumi.Input[str] name: The name of the health-check.
        :param pulumi.Input[str] namespace: The namespace to create the service within.
        :param pulumi.Input[str] node: The name of the node the to register the service on.
        :param pulumi.Input[int] port: The port of the service.
        :param pulumi.Input[str] service_id: - If the service ID is not provided, it will be defaulted to the value
               of the `name` attribute.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of values that are opaque to Consul,
               but can be used to distinguish between services or nodes.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A high-level resource for creating a Service in Consul in the Consul catalog. This
        is appropriate for registering [external services](https://www.consul.io/docs/guides/external.html) and
        can be used to create services addressable by Consul that cannot be registered
        with a [local agent](https://www.consul.io/docs/agent/basics.html).

        > **NOTE:** If a Consul agent is running on the node where this service is
        registered, it is not recommended to use this resource as the service will be
        removed during the next [anti-entropy synchronisation](https://www.consul.io/docs/architecture/anti-entropy).

        ## Example Usage

        Creating a new node with the service:

        ```python
        import pulumi
        import pulumi_consul as consul

        compute = consul.Node("compute", address="www.google.com")
        google = consul.Service("google",
            node=compute.name,
            port=80,
            tags=["tag0"])
        ```

        Utilizing an existing known node:

        ```python
        import pulumi
        import pulumi_consul as consul

        google = consul.Service("google",
            node="google",
            port=443)
        ```

        Register a health-check:

        ```python
        import pulumi
        import pulumi_consul as consul

        redis = consul.Service("redis",
            checks=[consul.ServiceCheckArgs(
                check_id="service:redis1",
                deregister_critical_service_after="30s",
                headers=[
                    consul.ServiceCheckHeaderArgs(
                        name="foo",
                        value=["test"],
                    ),
                    consul.ServiceCheckHeaderArgs(
                        name="bar",
                        value=["test"],
                    ),
                ],
                http="https://www.hashicorptest.com",
                interval="5s",
                method="PUT",
                name="Redis health check",
                status="passing",
                timeout="1s",
                tls_skip_verify=False,
            )],
            node="redis",
            port=6379)
        ```

        :param str resource_name: The name of the resource.
        :param ServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 checks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceCheckArgs']]]]] = None,
                 datacenter: Optional[pulumi.Input[str]] = None,
                 enable_tag_override: Optional[pulumi.Input[bool]] = None,
                 external: Optional[pulumi.Input[bool]] = None,
                 meta: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = ServiceArgs.__new__(ServiceArgs)

            __props__.__dict__["address"] = address
            __props__.__dict__["checks"] = checks
            __props__.__dict__["datacenter"] = datacenter
            __props__.__dict__["enable_tag_override"] = enable_tag_override
            if external is not None and not opts.urn:
                warnings.warn("""The external field has been deprecated and does nothing.""", DeprecationWarning)
                pulumi.log.warn("""external is deprecated: The external field has been deprecated and does nothing.""")
            __props__.__dict__["external"] = external
            __props__.__dict__["meta"] = meta
            __props__.__dict__["name"] = name
            __props__.__dict__["namespace"] = namespace
            if node is None and not opts.urn:
                raise TypeError("Missing required property 'node'")
            __props__.__dict__["node"] = node
            __props__.__dict__["port"] = port
            __props__.__dict__["service_id"] = service_id
            __props__.__dict__["tags"] = tags
        super(Service, __self__).__init__(
            'consul:index/service:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address: Optional[pulumi.Input[str]] = None,
            checks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceCheckArgs']]]]] = None,
            datacenter: Optional[pulumi.Input[str]] = None,
            enable_tag_override: Optional[pulumi.Input[bool]] = None,
            external: Optional[pulumi.Input[bool]] = None,
            meta: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            node: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            service_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Service':
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The address of the service. Defaults to the
               address of the node.
        :param pulumi.Input[str] datacenter: The datacenter to use. This overrides the
               agent's default datacenter and the datacenter in the provider setup.
        :param pulumi.Input[bool] enable_tag_override: Specifies to disable the
               anti-entropy feature for this service's tags. Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] meta: A map of arbitrary KV metadata linked to the service
               instance.
        :param pulumi.Input[str] name: The name of the health-check.
        :param pulumi.Input[str] namespace: The namespace to create the service within.
        :param pulumi.Input[str] node: The name of the node the to register the service on.
        :param pulumi.Input[int] port: The port of the service.
        :param pulumi.Input[str] service_id: - If the service ID is not provided, it will be defaulted to the value
               of the `name` attribute.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of values that are opaque to Consul,
               but can be used to distinguish between services or nodes.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceState.__new__(_ServiceState)

        __props__.__dict__["address"] = address
        __props__.__dict__["checks"] = checks
        __props__.__dict__["datacenter"] = datacenter
        __props__.__dict__["enable_tag_override"] = enable_tag_override
        __props__.__dict__["external"] = external
        __props__.__dict__["meta"] = meta
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["node"] = node
        __props__.__dict__["port"] = port
        __props__.__dict__["service_id"] = service_id
        __props__.__dict__["tags"] = tags
        return Service(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Output[str]:
        """
        The address of the service. Defaults to the
        address of the node.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def checks(self) -> pulumi.Output[Optional[Sequence['outputs.ServiceCheck']]]:
        return pulumi.get(self, "checks")

    @property
    @pulumi.getter
    def datacenter(self) -> pulumi.Output[str]:
        """
        The datacenter to use. This overrides the
        agent's default datacenter and the datacenter in the provider setup.
        """
        return pulumi.get(self, "datacenter")

    @property
    @pulumi.getter(name="enableTagOverride")
    def enable_tag_override(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies to disable the
        anti-entropy feature for this service's tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_tag_override")

    @property
    @pulumi.getter
    def external(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "external")

    @property
    @pulumi.getter
    def meta(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of arbitrary KV metadata linked to the service
        instance.
        """
        return pulumi.get(self, "meta")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the health-check.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to create the service within.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def node(self) -> pulumi.Output[str]:
        """
        The name of the node the to register the service on.
        """
        return pulumi.get(self, "node")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        The port of the service.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Output[str]:
        """
        - If the service ID is not provided, it will be defaulted to the value
        of the `name` attribute.
        """
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of values that are opaque to Consul,
        but can be used to distinguish between services or nodes.
        """
        return pulumi.get(self, "tags")

