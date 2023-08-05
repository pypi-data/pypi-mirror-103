import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_9df397a6,
    CfnTag as _CfnTag_f6864754,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnContainer(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mediastore.CfnContainer",
):
    '''A CloudFormation ``AWS::MediaStore::Container``.

    :cloudformationResource: AWS::MediaStore::Container
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        container_name: builtins.str,
        access_logging_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        cors_policy: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_da3f097b]]]] = None,
        lifecycle_policy: typing.Optional[builtins.str] = None,
        metric_policy: typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_da3f097b]] = None,
        policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaStore::Container``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param container_name: ``AWS::MediaStore::Container.ContainerName``.
        :param access_logging_enabled: ``AWS::MediaStore::Container.AccessLoggingEnabled``.
        :param cors_policy: ``AWS::MediaStore::Container.CorsPolicy``.
        :param lifecycle_policy: ``AWS::MediaStore::Container.LifecyclePolicy``.
        :param metric_policy: ``AWS::MediaStore::Container.MetricPolicy``.
        :param policy: ``AWS::MediaStore::Container.Policy``.
        :param tags: ``AWS::MediaStore::Container.Tags``.
        '''
        props = CfnContainerProps(
            container_name=container_name,
            access_logging_enabled=access_logging_enabled,
            cors_policy=cors_policy,
            lifecycle_policy=lifecycle_policy,
            metric_policy=metric_policy,
            policy=policy,
            tags=tags,
        )

        jsii.create(CfnContainer, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::MediaStore::Container.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        '''``AWS::MediaStore::Container.ContainerName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-containername
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        jsii.set(self, "containerName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessLoggingEnabled")
    def access_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::MediaStore::Container.AccessLoggingEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-accessloggingenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "accessLoggingEnabled"))

    @access_logging_enabled.setter
    def access_logging_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "accessLoggingEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="corsPolicy")
    def cors_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::MediaStore::Container.CorsPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-corspolicy
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_da3f097b]]]], jsii.get(self, "corsPolicy"))

    @cors_policy.setter
    def cors_policy(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "corsPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaStore::Container.LifecyclePolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-lifecyclepolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecyclePolicy"))

    @lifecycle_policy.setter
    def lifecycle_policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "lifecyclePolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metricPolicy")
    def metric_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_da3f097b]]:
        '''``AWS::MediaStore::Container.MetricPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-metricpolicy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_da3f097b]], jsii.get(self, "metricPolicy"))

    @metric_policy.setter
    def metric_policy(
        self,
        value: typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "metricPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaStore::Container.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-policy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policy", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mediastore.CfnContainer.CorsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_headers": "allowedHeaders",
            "allowed_methods": "allowedMethods",
            "allowed_origins": "allowedOrigins",
            "expose_headers": "exposeHeaders",
            "max_age_seconds": "maxAgeSeconds",
        },
    )
    class CorsRuleProperty:
        def __init__(
            self,
            *,
            allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allowed_headers: ``CfnContainer.CorsRuleProperty.AllowedHeaders``.
            :param allowed_methods: ``CfnContainer.CorsRuleProperty.AllowedMethods``.
            :param allowed_origins: ``CfnContainer.CorsRuleProperty.AllowedOrigins``.
            :param expose_headers: ``CfnContainer.CorsRuleProperty.ExposeHeaders``.
            :param max_age_seconds: ``CfnContainer.CorsRuleProperty.MaxAgeSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allowed_headers is not None:
                self._values["allowed_headers"] = allowed_headers
            if allowed_methods is not None:
                self._values["allowed_methods"] = allowed_methods
            if allowed_origins is not None:
                self._values["allowed_origins"] = allowed_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age_seconds is not None:
                self._values["max_age_seconds"] = max_age_seconds

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnContainer.CorsRuleProperty.AllowedHeaders``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedheaders
            '''
            result = self._values.get("allowed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnContainer.CorsRuleProperty.AllowedMethods``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedmethods
            '''
            result = self._values.get("allowed_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnContainer.CorsRuleProperty.AllowedOrigins``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedorigins
            '''
            result = self._values.get("allowed_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnContainer.CorsRuleProperty.ExposeHeaders``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-exposeheaders
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnContainer.CorsRuleProperty.MaxAgeSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-maxageseconds
            '''
            result = self._values.get("max_age_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mediastore.CfnContainer.MetricPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_level_metrics": "containerLevelMetrics",
            "metric_policy_rules": "metricPolicyRules",
        },
    )
    class MetricPolicyProperty:
        def __init__(
            self,
            *,
            container_level_metrics: builtins.str,
            metric_policy_rules: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnContainer.MetricPolicyRuleProperty", _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''
            :param container_level_metrics: ``CfnContainer.MetricPolicyProperty.ContainerLevelMetrics``.
            :param metric_policy_rules: ``CfnContainer.MetricPolicyProperty.MetricPolicyRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "container_level_metrics": container_level_metrics,
            }
            if metric_policy_rules is not None:
                self._values["metric_policy_rules"] = metric_policy_rules

        @builtins.property
        def container_level_metrics(self) -> builtins.str:
            '''``CfnContainer.MetricPolicyProperty.ContainerLevelMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-containerlevelmetrics
            '''
            result = self._values.get("container_level_metrics")
            assert result is not None, "Required property 'container_level_metrics' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_policy_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnContainer.MetricPolicyRuleProperty", _IResolvable_da3f097b]]]]:
            '''``CfnContainer.MetricPolicyProperty.MetricPolicyRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-metricpolicyrules
            '''
            result = self._values.get("metric_policy_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnContainer.MetricPolicyRuleProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mediastore.CfnContainer.MetricPolicyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_group": "objectGroup",
            "object_group_name": "objectGroupName",
        },
    )
    class MetricPolicyRuleProperty:
        def __init__(
            self,
            *,
            object_group: builtins.str,
            object_group_name: builtins.str,
        ) -> None:
            '''
            :param object_group: ``CfnContainer.MetricPolicyRuleProperty.ObjectGroup``.
            :param object_group_name: ``CfnContainer.MetricPolicyRuleProperty.ObjectGroupName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object_group": object_group,
                "object_group_name": object_group_name,
            }

        @builtins.property
        def object_group(self) -> builtins.str:
            '''``CfnContainer.MetricPolicyRuleProperty.ObjectGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroup
            '''
            result = self._values.get("object_group")
            assert result is not None, "Required property 'object_group' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_group_name(self) -> builtins.str:
            '''``CfnContainer.MetricPolicyRuleProperty.ObjectGroupName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroupname
            '''
            result = self._values.get("object_group_name")
            assert result is not None, "Required property 'object_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricPolicyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mediastore.CfnContainerProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "access_logging_enabled": "accessLoggingEnabled",
        "cors_policy": "corsPolicy",
        "lifecycle_policy": "lifecyclePolicy",
        "metric_policy": "metricPolicy",
        "policy": "policy",
        "tags": "tags",
    },
)
class CfnContainerProps:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        access_logging_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        cors_policy: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnContainer.CorsRuleProperty, _IResolvable_da3f097b]]]] = None,
        lifecycle_policy: typing.Optional[builtins.str] = None,
        metric_policy: typing.Optional[typing.Union[CfnContainer.MetricPolicyProperty, _IResolvable_da3f097b]] = None,
        policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::MediaStore::Container``.

        :param container_name: ``AWS::MediaStore::Container.ContainerName``.
        :param access_logging_enabled: ``AWS::MediaStore::Container.AccessLoggingEnabled``.
        :param cors_policy: ``AWS::MediaStore::Container.CorsPolicy``.
        :param lifecycle_policy: ``AWS::MediaStore::Container.LifecyclePolicy``.
        :param metric_policy: ``AWS::MediaStore::Container.MetricPolicy``.
        :param policy: ``AWS::MediaStore::Container.Policy``.
        :param tags: ``AWS::MediaStore::Container.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
        }
        if access_logging_enabled is not None:
            self._values["access_logging_enabled"] = access_logging_enabled
        if cors_policy is not None:
            self._values["cors_policy"] = cors_policy
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if metric_policy is not None:
            self._values["metric_policy"] = metric_policy
        if policy is not None:
            self._values["policy"] = policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def container_name(self) -> builtins.str:
        '''``AWS::MediaStore::Container.ContainerName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-containername
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::MediaStore::Container.AccessLoggingEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-accessloggingenabled
        '''
        result = self._values.get("access_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def cors_policy(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnContainer.CorsRuleProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::MediaStore::Container.CorsPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-corspolicy
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnContainer.CorsRuleProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaStore::Container.LifecyclePolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-lifecyclepolicy
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnContainer.MetricPolicyProperty, _IResolvable_da3f097b]]:
        '''``AWS::MediaStore::Container.MetricPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-metricpolicy
        '''
        result = self._values.get("metric_policy")
        return typing.cast(typing.Optional[typing.Union[CfnContainer.MetricPolicyProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::MediaStore::Container.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''``AWS::MediaStore::Container.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnContainer",
    "CfnContainerProps",
]

publication.publish()
