'''
# AWS CloudFormation Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
'''
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
class CfnCustomResource(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnCustomResource",
):
    '''A CloudFormation ``AWS::CloudFormation::CustomResource``.

    :cloudformationResource: AWS::CloudFormation::CustomResource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        service_token: builtins.str,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::CustomResource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.
        '''
        props = CfnCustomResourceProps(service_token=service_token)

        jsii.create(CfnCustomResource, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''``AWS::CloudFormation::CustomResource.ServiceToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(self, value: builtins.str) -> None:
        jsii.set(self, "serviceToken", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={"service_token": "serviceToken"},
)
class CfnCustomResourceProps:
    def __init__(self, *, service_token: builtins.str) -> None:
        '''Properties for defining a ``AWS::CloudFormation::CustomResource``.

        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "service_token": service_token,
        }

    @builtins.property
    def service_token(self) -> builtins.str:
        '''``AWS::CloudFormation::CustomResource.ServiceToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        '''
        result = self._values.get("service_token")
        assert result is not None, "Required property 'service_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnMacro(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnMacro",
):
    '''A CloudFormation ``AWS::CloudFormation::Macro``.

    :cloudformationResource: AWS::CloudFormation::Macro
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::Macro``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.
        '''
        props = CfnMacroProps(
            function_name=function_name,
            name=name,
            description=description,
            log_group_name=log_group_name,
            log_role_arn=log_role_arn,
        )

        jsii.create(CfnMacro, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''``AWS::CloudFormation::Macro.FunctionName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::CloudFormation::Macro.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logRoleArn")
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.LogRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logRoleArn"))

    @log_role_arn.setter
    def log_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logRoleArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnMacroProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "name": "name",
        "description": "description",
        "log_group_name": "logGroupName",
        "log_role_arn": "logRoleArn",
    },
)
class CfnMacroProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::Macro``.

        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "function_name": function_name,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_role_arn is not None:
            self._values["log_role_arn"] = log_role_arn

    @builtins.property
    def function_name(self) -> builtins.str:
        '''``AWS::CloudFormation::Macro.FunctionName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::CloudFormation::Macro.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::Macro.LogRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        '''
        result = self._values.get("log_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMacroProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnModuleDefaultVersion(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnModuleDefaultVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ModuleDefaultVersion``.

    :cloudformationResource: AWS::CloudFormation::ModuleDefaultVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        arn: typing.Optional[builtins.str] = None,
        module_name: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ModuleDefaultVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param arn: ``AWS::CloudFormation::ModuleDefaultVersion.Arn``.
        :param module_name: ``AWS::CloudFormation::ModuleDefaultVersion.ModuleName``.
        :param version_id: ``AWS::CloudFormation::ModuleDefaultVersion.VersionId``.
        '''
        props = CfnModuleDefaultVersionProps(
            arn=arn, module_name=module_name, version_id=version_id
        )

        jsii.create(CfnModuleDefaultVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.Arn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-arn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "arn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.ModuleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-modulename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "moduleName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnModuleDefaultVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "module_name": "moduleName",
        "version_id": "versionId",
    },
)
class CfnModuleDefaultVersionProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        module_name: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::ModuleDefaultVersion``.

        :param arn: ``AWS::CloudFormation::ModuleDefaultVersion.Arn``.
        :param module_name: ``AWS::CloudFormation::ModuleDefaultVersion.ModuleName``.
        :param version_id: ``AWS::CloudFormation::ModuleDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if module_name is not None:
            self._values["module_name"] = module_name
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.Arn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.ModuleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-modulename
        '''
        result = self._values.get("module_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ModuleDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleDefaultVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnModuleVersion(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnModuleVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ModuleVersion``.

    :cloudformationResource: AWS::CloudFormation::ModuleVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        module_name: builtins.str,
        module_package: builtins.str,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ModuleVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param module_name: ``AWS::CloudFormation::ModuleVersion.ModuleName``.
        :param module_package: ``AWS::CloudFormation::ModuleVersion.ModulePackage``.
        '''
        props = CfnModuleVersionProps(
            module_name=module_name, module_package=module_package
        )

        jsii.create(CfnModuleVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''
        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDocumentationUrl")
    def attr_documentation_url(self) -> builtins.str:
        '''
        :cloudformationAttribute: DocumentationUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDocumentationUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrIsDefaultVersion")
    def attr_is_default_version(self) -> _IResolvable_da3f097b:
        '''
        :cloudformationAttribute: IsDefaultVersion
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrIsDefaultVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSchema")
    def attr_schema(self) -> builtins.str:
        '''
        :cloudformationAttribute: Schema
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchema"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrTimeCreated")
    def attr_time_created(self) -> builtins.str:
        '''
        :cloudformationAttribute: TimeCreated
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTimeCreated"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVisibility")
    def attr_visibility(self) -> builtins.str:
        '''
        :cloudformationAttribute: Visibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVisibility"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> builtins.str:
        '''``AWS::CloudFormation::ModuleVersion.ModuleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulename
        '''
        return typing.cast(builtins.str, jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: builtins.str) -> None:
        jsii.set(self, "moduleName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="modulePackage")
    def module_package(self) -> builtins.str:
        '''``AWS::CloudFormation::ModuleVersion.ModulePackage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulepackage
        '''
        return typing.cast(builtins.str, jsii.get(self, "modulePackage"))

    @module_package.setter
    def module_package(self, value: builtins.str) -> None:
        jsii.set(self, "modulePackage", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnModuleVersionProps",
    jsii_struct_bases=[],
    name_mapping={"module_name": "moduleName", "module_package": "modulePackage"},
)
class CfnModuleVersionProps:
    def __init__(
        self,
        *,
        module_name: builtins.str,
        module_package: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::ModuleVersion``.

        :param module_name: ``AWS::CloudFormation::ModuleVersion.ModuleName``.
        :param module_package: ``AWS::CloudFormation::ModuleVersion.ModulePackage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "module_name": module_name,
            "module_package": module_package,
        }

    @builtins.property
    def module_name(self) -> builtins.str:
        '''``AWS::CloudFormation::ModuleVersion.ModuleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulename
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def module_package(self) -> builtins.str:
        '''``AWS::CloudFormation::ModuleVersion.ModulePackage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulepackage
        '''
        result = self._values.get("module_package")
        assert result is not None, "Required property 'module_package' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnResourceDefaultVersion(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnResourceDefaultVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ResourceDefaultVersion``.

    :cloudformationResource: AWS::CloudFormation::ResourceDefaultVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ResourceDefaultVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type_name: ``AWS::CloudFormation::ResourceDefaultVersion.TypeName``.
        :param type_version_arn: ``AWS::CloudFormation::ResourceDefaultVersion.TypeVersionArn``.
        :param version_id: ``AWS::CloudFormation::ResourceDefaultVersion.VersionId``.
        '''
        props = CfnResourceDefaultVersionProps(
            type_name=type_name,
            type_version_arn=type_version_arn,
            version_id=version_id,
        )

        jsii.create(CfnResourceDefaultVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.TypeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "typeName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeVersionArn")
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.TypeVersionArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typeversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeVersionArn"))

    @type_version_arn.setter
    def type_version_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "typeVersionArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnResourceDefaultVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "type_name": "typeName",
        "type_version_arn": "typeVersionArn",
        "version_id": "versionId",
    },
)
class CfnResourceDefaultVersionProps:
    def __init__(
        self,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::ResourceDefaultVersion``.

        :param type_name: ``AWS::CloudFormation::ResourceDefaultVersion.TypeName``.
        :param type_version_arn: ``AWS::CloudFormation::ResourceDefaultVersion.TypeVersionArn``.
        :param version_id: ``AWS::CloudFormation::ResourceDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_version_arn is not None:
            self._values["type_version_arn"] = type_version_arn
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.TypeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.TypeVersionArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typeversionarn
        '''
        result = self._values.get("type_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceDefaultVersion.VersionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefaultVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnResourceVersion(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnResourceVersion",
):
    '''A CloudFormation ``AWS::CloudFormation::ResourceVersion``.

    :cloudformationResource: AWS::CloudFormation::ResourceVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["CfnResourceVersion.LoggingConfigProperty", _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::ResourceVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param schema_handler_package: ``AWS::CloudFormation::ResourceVersion.SchemaHandlerPackage``.
        :param type_name: ``AWS::CloudFormation::ResourceVersion.TypeName``.
        :param execution_role_arn: ``AWS::CloudFormation::ResourceVersion.ExecutionRoleArn``.
        :param logging_config: ``AWS::CloudFormation::ResourceVersion.LoggingConfig``.
        '''
        props = CfnResourceVersionProps(
            schema_handler_package=schema_handler_package,
            type_name=type_name,
            execution_role_arn=execution_role_arn,
            logging_config=logging_config,
        )

        jsii.create(CfnResourceVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrIsDefaultVersion")
    def attr_is_default_version(self) -> _IResolvable_da3f097b:
        '''
        :cloudformationAttribute: IsDefaultVersion
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrIsDefaultVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrProvisioningType")
    def attr_provisioning_type(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProvisioningType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProvisioningType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrTypeArn")
    def attr_type_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: TypeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTypeArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVisibility")
    def attr_visibility(self) -> builtins.str:
        '''
        :cloudformationAttribute: Visibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVisibility"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schemaHandlerPackage")
    def schema_handler_package(self) -> builtins.str:
        '''``AWS::CloudFormation::ResourceVersion.SchemaHandlerPackage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-schemahandlerpackage
        '''
        return typing.cast(builtins.str, jsii.get(self, "schemaHandlerPackage"))

    @schema_handler_package.setter
    def schema_handler_package(self, value: builtins.str) -> None:
        jsii.set(self, "schemaHandlerPackage", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        '''``AWS::CloudFormation::ResourceVersion.TypeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-typename
        '''
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        jsii.set(self, "typeName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceVersion.ExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-executionrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union["CfnResourceVersion.LoggingConfigProperty", _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::ResourceVersion.LoggingConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-loggingconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnResourceVersion.LoggingConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "loggingConfig"))

    @logging_config.setter
    def logging_config(
        self,
        value: typing.Optional[typing.Union["CfnResourceVersion.LoggingConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "loggingConfig", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnResourceVersion.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param log_group_name: ``CfnResourceVersion.LoggingConfigProperty.LogGroupName``.
            :param log_role_arn: ``CfnResourceVersion.LoggingConfigProperty.LogRoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''``CfnResourceVersion.LoggingConfigProperty.LogGroupName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnResourceVersion.LoggingConfigProperty.LogRoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnResourceVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_handler_package": "schemaHandlerPackage",
        "type_name": "typeName",
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
    },
)
class CfnResourceVersionProps:
    def __init__(
        self,
        *,
        schema_handler_package: builtins.str,
        type_name: builtins.str,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[CfnResourceVersion.LoggingConfigProperty, _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::ResourceVersion``.

        :param schema_handler_package: ``AWS::CloudFormation::ResourceVersion.SchemaHandlerPackage``.
        :param type_name: ``AWS::CloudFormation::ResourceVersion.TypeName``.
        :param execution_role_arn: ``AWS::CloudFormation::ResourceVersion.ExecutionRoleArn``.
        :param logging_config: ``AWS::CloudFormation::ResourceVersion.LoggingConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "schema_handler_package": schema_handler_package,
            "type_name": type_name,
        }
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def schema_handler_package(self) -> builtins.str:
        '''``AWS::CloudFormation::ResourceVersion.SchemaHandlerPackage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-schemahandlerpackage
        '''
        result = self._values.get("schema_handler_package")
        assert result is not None, "Required property 'schema_handler_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''``AWS::CloudFormation::ResourceVersion.TypeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-typename
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::ResourceVersion.ExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[CfnResourceVersion.LoggingConfigProperty, _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::ResourceVersion.LoggingConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[CfnResourceVersion.LoggingConfigProperty, _IResolvable_da3f097b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnStack(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnStack",
):
    '''A CloudFormation ``AWS::CloudFormation::Stack``.

    :cloudformationResource: AWS::CloudFormation::Stack
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.
        '''
        props = CfnStackProps(
            template_url=template_url,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(CfnStack, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::CloudFormation::Stack.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> builtins.str:
        '''``AWS::CloudFormation::Stack.TemplateURL``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateUrl"))

    @template_url.setter
    def template_url(self, value: builtins.str) -> None:
        jsii.set(self, "templateUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CloudFormation::Stack.NotificationARNs``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "notificationArns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::CloudFormation::Stack.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_url": "templateUrl",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::Stack``.

        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "template_url": template_url,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def template_url(self) -> builtins.str:
        '''``AWS::CloudFormation::Stack.TemplateURL``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        '''
        result = self._values.get("template_url")
        assert result is not None, "Required property 'template_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CloudFormation::Stack.NotificationARNs``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::CloudFormation::Stack.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''``AWS::CloudFormation::Stack.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnStackSet(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet",
):
    '''A CloudFormation ``AWS::CloudFormation::StackSet``.

    :cloudformationResource: AWS::CloudFormation::StackSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        permission_model: builtins.str,
        stack_set_name: builtins.str,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", _IResolvable_da3f097b]] = None,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union["CfnStackSet.OperationPreferencesProperty", _IResolvable_da3f097b]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]] = None,
        stack_instances_group: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnStackSet.StackInstancesProperty", _IResolvable_da3f097b]]]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::StackSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param permission_model: ``AWS::CloudFormation::StackSet.PermissionModel``.
        :param stack_set_name: ``AWS::CloudFormation::StackSet.StackSetName``.
        :param administration_role_arn: ``AWS::CloudFormation::StackSet.AdministrationRoleARN``.
        :param auto_deployment: ``AWS::CloudFormation::StackSet.AutoDeployment``.
        :param capabilities: ``AWS::CloudFormation::StackSet.Capabilities``.
        :param description: ``AWS::CloudFormation::StackSet.Description``.
        :param execution_role_name: ``AWS::CloudFormation::StackSet.ExecutionRoleName``.
        :param operation_preferences: ``AWS::CloudFormation::StackSet.OperationPreferences``.
        :param parameters: ``AWS::CloudFormation::StackSet.Parameters``.
        :param stack_instances_group: ``AWS::CloudFormation::StackSet.StackInstancesGroup``.
        :param tags: ``AWS::CloudFormation::StackSet.Tags``.
        :param template_body: ``AWS::CloudFormation::StackSet.TemplateBody``.
        :param template_url: ``AWS::CloudFormation::StackSet.TemplateURL``.
        '''
        props = CfnStackSetProps(
            permission_model=permission_model,
            stack_set_name=stack_set_name,
            administration_role_arn=administration_role_arn,
            auto_deployment=auto_deployment,
            capabilities=capabilities,
            description=description,
            execution_role_name=execution_role_name,
            operation_preferences=operation_preferences,
            parameters=parameters,
            stack_instances_group=stack_instances_group,
            tags=tags,
            template_body=template_body,
            template_url=template_url,
        )

        jsii.create(CfnStackSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrStackSetId")
    def attr_stack_set_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: StackSetId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStackSetId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::CloudFormation::StackSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="permissionModel")
    def permission_model(self) -> builtins.str:
        '''``AWS::CloudFormation::StackSet.PermissionModel``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        '''
        return typing.cast(builtins.str, jsii.get(self, "permissionModel"))

    @permission_model.setter
    def permission_model(self, value: builtins.str) -> None:
        jsii.set(self, "permissionModel", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackSetName")
    def stack_set_name(self) -> builtins.str:
        '''``AWS::CloudFormation::StackSet.StackSetName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackSetName"))

    @stack_set_name.setter
    def stack_set_name(self, value: builtins.str) -> None:
        jsii.set(self, "stackSetName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="administrationRoleArn")
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.AdministrationRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administrationRoleArn"))

    @administration_role_arn.setter
    def administration_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "administrationRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoDeployment")
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::StackSet.AutoDeployment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", _IResolvable_da3f097b]], jsii.get(self, "autoDeployment"))

    @auto_deployment.setter
    def auto_deployment(
        self,
        value: typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "autoDeployment", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CloudFormation::StackSet.Capabilities``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "capabilities", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRoleName")
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.ExecutionRoleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleName"))

    @execution_role_name.setter
    def execution_role_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "executionRoleName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="operationPreferences")
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union["CfnStackSet.OperationPreferencesProperty", _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::StackSet.OperationPreferences``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStackSet.OperationPreferencesProperty", _IResolvable_da3f097b]], jsii.get(self, "operationPreferences"))

    @operation_preferences.setter
    def operation_preferences(
        self,
        value: typing.Optional[typing.Union["CfnStackSet.OperationPreferencesProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "operationPreferences", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::CloudFormation::StackSet.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackInstancesGroup")
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.StackInstancesProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::CloudFormation::StackSet.StackInstancesGroup``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.StackInstancesProperty", _IResolvable_da3f097b]]]], jsii.get(self, "stackInstancesGroup"))

    @stack_instances_group.setter
    def stack_instances_group(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.StackInstancesProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "stackInstancesGroup", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.TemplateBody``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateBody"))

    @template_body.setter
    def template_body(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateBody", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.TemplateURL``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateUrl"))

    @template_url.setter
    def template_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateUrl", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet.AutoDeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "retain_stacks_on_account_removal": "retainStacksOnAccountRemoval",
        },
    )
    class AutoDeploymentProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            retain_stacks_on_account_removal: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnStackSet.AutoDeploymentProperty.Enabled``.
            :param retain_stacks_on_account_removal: ``CfnStackSet.AutoDeploymentProperty.RetainStacksOnAccountRemoval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if retain_stacks_on_account_removal is not None:
                self._values["retain_stacks_on_account_removal"] = retain_stacks_on_account_removal

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnStackSet.AutoDeploymentProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def retain_stacks_on_account_removal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnStackSet.AutoDeploymentProperty.RetainStacksOnAccountRemoval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-retainstacksonaccountremoval
            '''
            result = self._values.get("retain_stacks_on_account_removal")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoDeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet.DeploymentTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accounts": "accounts",
            "organizational_unit_ids": "organizationalUnitIds",
        },
    )
    class DeploymentTargetsProperty:
        def __init__(
            self,
            *,
            accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param accounts: ``CfnStackSet.DeploymentTargetsProperty.Accounts``.
            :param organizational_unit_ids: ``CfnStackSet.DeploymentTargetsProperty.OrganizationalUnitIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if accounts is not None:
                self._values["accounts"] = accounts
            if organizational_unit_ids is not None:
                self._values["organizational_unit_ids"] = organizational_unit_ids

        @builtins.property
        def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnStackSet.DeploymentTargetsProperty.Accounts``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accounts
            '''
            result = self._values.get("accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def organizational_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnStackSet.DeploymentTargetsProperty.OrganizationalUnitIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-organizationalunitids
            '''
            result = self._values.get("organizational_unit_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet.OperationPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_tolerance_count": "failureToleranceCount",
            "failure_tolerance_percentage": "failureTolerancePercentage",
            "max_concurrent_count": "maxConcurrentCount",
            "max_concurrent_percentage": "maxConcurrentPercentage",
            "region_order": "regionOrder",
        },
    )
    class OperationPreferencesProperty:
        def __init__(
            self,
            *,
            failure_tolerance_count: typing.Optional[jsii.Number] = None,
            failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            max_concurrent_count: typing.Optional[jsii.Number] = None,
            max_concurrent_percentage: typing.Optional[jsii.Number] = None,
            region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param failure_tolerance_count: ``CfnStackSet.OperationPreferencesProperty.FailureToleranceCount``.
            :param failure_tolerance_percentage: ``CfnStackSet.OperationPreferencesProperty.FailureTolerancePercentage``.
            :param max_concurrent_count: ``CfnStackSet.OperationPreferencesProperty.MaxConcurrentCount``.
            :param max_concurrent_percentage: ``CfnStackSet.OperationPreferencesProperty.MaxConcurrentPercentage``.
            :param region_order: ``CfnStackSet.OperationPreferencesProperty.RegionOrder``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if failure_tolerance_count is not None:
                self._values["failure_tolerance_count"] = failure_tolerance_count
            if failure_tolerance_percentage is not None:
                self._values["failure_tolerance_percentage"] = failure_tolerance_percentage
            if max_concurrent_count is not None:
                self._values["max_concurrent_count"] = max_concurrent_count
            if max_concurrent_percentage is not None:
                self._values["max_concurrent_percentage"] = max_concurrent_percentage
            if region_order is not None:
                self._values["region_order"] = region_order

        @builtins.property
        def failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnStackSet.OperationPreferencesProperty.FailureToleranceCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancecount
            '''
            result = self._values.get("failure_tolerance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def failure_tolerance_percentage(self) -> typing.Optional[jsii.Number]:
            '''``CfnStackSet.OperationPreferencesProperty.FailureTolerancePercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancepercentage
            '''
            result = self._values.get("failure_tolerance_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnStackSet.OperationPreferencesProperty.MaxConcurrentCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentcount
            '''
            result = self._values.get("max_concurrent_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_percentage(self) -> typing.Optional[jsii.Number]:
            '''``CfnStackSet.OperationPreferencesProperty.MaxConcurrentPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentpercentage
            '''
            result = self._values.get("max_concurrent_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def region_order(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnStackSet.OperationPreferencesProperty.RegionOrder``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionorder
            '''
            result = self._values.get("region_order")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OperationPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_key": "parameterKey",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_key: builtins.str,
            parameter_value: builtins.str,
        ) -> None:
            '''
            :param parameter_key: ``CfnStackSet.ParameterProperty.ParameterKey``.
            :param parameter_value: ``CfnStackSet.ParameterProperty.ParameterValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "parameter_key": parameter_key,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_key(self) -> builtins.str:
            '''``CfnStackSet.ParameterProperty.ParameterKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parameterkey
            '''
            result = self._values.get("parameter_key")
            assert result is not None, "Required property 'parameter_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameter_value(self) -> builtins.str:
            '''``CfnStackSet.ParameterProperty.ParameterValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            assert result is not None, "Required property 'parameter_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSet.StackInstancesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_targets": "deploymentTargets",
            "regions": "regions",
            "parameter_overrides": "parameterOverrides",
        },
    )
    class StackInstancesProperty:
        def __init__(
            self,
            *,
            deployment_targets: typing.Union["CfnStackSet.DeploymentTargetsProperty", _IResolvable_da3f097b],
            regions: typing.Sequence[builtins.str],
            parameter_overrides: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''
            :param deployment_targets: ``CfnStackSet.StackInstancesProperty.DeploymentTargets``.
            :param regions: ``CfnStackSet.StackInstancesProperty.Regions``.
            :param parameter_overrides: ``CfnStackSet.StackInstancesProperty.ParameterOverrides``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "deployment_targets": deployment_targets,
                "regions": regions,
            }
            if parameter_overrides is not None:
                self._values["parameter_overrides"] = parameter_overrides

        @builtins.property
        def deployment_targets(
            self,
        ) -> typing.Union["CfnStackSet.DeploymentTargetsProperty", _IResolvable_da3f097b]:
            '''``CfnStackSet.StackInstancesProperty.DeploymentTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets
            '''
            result = self._values.get("deployment_targets")
            assert result is not None, "Required property 'deployment_targets' is missing"
            return typing.cast(typing.Union["CfnStackSet.DeploymentTargetsProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def regions(self) -> typing.List[builtins.str]:
            '''``CfnStackSet.StackInstancesProperty.Regions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-regions
            '''
            result = self._values.get("regions")
            assert result is not None, "Required property 'regions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def parameter_overrides(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]]:
            '''``CfnStackSet.StackInstancesProperty.ParameterOverrides``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-parameteroverrides
            '''
            result = self._values.get("parameter_overrides")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStackSet.ParameterProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackInstancesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnStackSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "permission_model": "permissionModel",
        "stack_set_name": "stackSetName",
        "administration_role_arn": "administrationRoleArn",
        "auto_deployment": "autoDeployment",
        "capabilities": "capabilities",
        "description": "description",
        "execution_role_name": "executionRoleName",
        "operation_preferences": "operationPreferences",
        "parameters": "parameters",
        "stack_instances_group": "stackInstancesGroup",
        "tags": "tags",
        "template_body": "templateBody",
        "template_url": "templateUrl",
    },
)
class CfnStackSetProps:
    def __init__(
        self,
        *,
        permission_model: builtins.str,
        stack_set_name: builtins.str,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union[CfnStackSet.AutoDeploymentProperty, _IResolvable_da3f097b]] = None,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union[CfnStackSet.OperationPreferencesProperty, _IResolvable_da3f097b]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnStackSet.ParameterProperty, _IResolvable_da3f097b]]]] = None,
        stack_instances_group: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnStackSet.StackInstancesProperty, _IResolvable_da3f097b]]]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::StackSet``.

        :param permission_model: ``AWS::CloudFormation::StackSet.PermissionModel``.
        :param stack_set_name: ``AWS::CloudFormation::StackSet.StackSetName``.
        :param administration_role_arn: ``AWS::CloudFormation::StackSet.AdministrationRoleARN``.
        :param auto_deployment: ``AWS::CloudFormation::StackSet.AutoDeployment``.
        :param capabilities: ``AWS::CloudFormation::StackSet.Capabilities``.
        :param description: ``AWS::CloudFormation::StackSet.Description``.
        :param execution_role_name: ``AWS::CloudFormation::StackSet.ExecutionRoleName``.
        :param operation_preferences: ``AWS::CloudFormation::StackSet.OperationPreferences``.
        :param parameters: ``AWS::CloudFormation::StackSet.Parameters``.
        :param stack_instances_group: ``AWS::CloudFormation::StackSet.StackInstancesGroup``.
        :param tags: ``AWS::CloudFormation::StackSet.Tags``.
        :param template_body: ``AWS::CloudFormation::StackSet.TemplateBody``.
        :param template_url: ``AWS::CloudFormation::StackSet.TemplateURL``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "permission_model": permission_model,
            "stack_set_name": stack_set_name,
        }
        if administration_role_arn is not None:
            self._values["administration_role_arn"] = administration_role_arn
        if auto_deployment is not None:
            self._values["auto_deployment"] = auto_deployment
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if execution_role_name is not None:
            self._values["execution_role_name"] = execution_role_name
        if operation_preferences is not None:
            self._values["operation_preferences"] = operation_preferences
        if parameters is not None:
            self._values["parameters"] = parameters
        if stack_instances_group is not None:
            self._values["stack_instances_group"] = stack_instances_group
        if tags is not None:
            self._values["tags"] = tags
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_url is not None:
            self._values["template_url"] = template_url

    @builtins.property
    def permission_model(self) -> builtins.str:
        '''``AWS::CloudFormation::StackSet.PermissionModel``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        '''
        result = self._values.get("permission_model")
        assert result is not None, "Required property 'permission_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_set_name(self) -> builtins.str:
        '''``AWS::CloudFormation::StackSet.StackSetName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        '''
        result = self._values.get("stack_set_name")
        assert result is not None, "Required property 'stack_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.AdministrationRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        '''
        result = self._values.get("administration_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union[CfnStackSet.AutoDeploymentProperty, _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::StackSet.AutoDeployment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        '''
        result = self._values.get("auto_deployment")
        return typing.cast(typing.Optional[typing.Union[CfnStackSet.AutoDeploymentProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CloudFormation::StackSet.Capabilities``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.ExecutionRoleName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        '''
        result = self._values.get("execution_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[CfnStackSet.OperationPreferencesProperty, _IResolvable_da3f097b]]:
        '''``AWS::CloudFormation::StackSet.OperationPreferences``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        '''
        result = self._values.get("operation_preferences")
        return typing.cast(typing.Optional[typing.Union[CfnStackSet.OperationPreferencesProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnStackSet.ParameterProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::CloudFormation::StackSet.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnStackSet.ParameterProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnStackSet.StackInstancesProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::CloudFormation::StackSet.StackInstancesGroup``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        '''
        result = self._values.get("stack_instances_group")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnStackSet.StackInstancesProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''``AWS::CloudFormation::StackSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.TemplateBody``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        '''
        result = self._values.get("template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_url(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::StackSet.TemplateURL``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        '''
        result = self._values.get("template_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnWaitCondition(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnWaitCondition",
):
    '''A CloudFormation ``AWS::CloudFormation::WaitCondition``.

    :cloudformationResource: AWS::CloudFormation::WaitCondition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudFormation::WaitCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.
        '''
        props = CfnWaitConditionProps(count=count, handle=handle, timeout=timeout)

        jsii.create(CfnWaitCondition, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrData")
    def attr_data(self) -> _IResolvable_da3f097b:
        '''
        :cloudformationAttribute: Data
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrData"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::CloudFormation::WaitCondition.Count``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "count"))

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="handle")
    def handle(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::WaitCondition.Handle``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handle"))

    @handle.setter
    def handle(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "handle", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::WaitCondition.Timeout``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "timeout", value)


@jsii.implements(_IInspectable_c2943556)
class CfnWaitConditionHandle(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnWaitConditionHandle",
):
    '''A CloudFormation ``AWS::CloudFormation::WaitConditionHandle``.

    :cloudformationResource: AWS::CloudFormation::WaitConditionHandle
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''Create a new ``AWS::CloudFormation::WaitConditionHandle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        '''
        jsii.create(CfnWaitConditionHandle, self, [scope, id])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cloudformation.CfnWaitConditionProps",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "handle": "handle", "timeout": "timeout"},
)
class CfnWaitConditionProps:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CloudFormation::WaitCondition``.

        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if handle is not None:
            self._values["handle"] = handle
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::CloudFormation::WaitCondition.Count``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::WaitCondition.Handle``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        '''
        result = self._values.get("handle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''``AWS::CloudFormation::WaitCondition.Timeout``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaitConditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCustomResource",
    "CfnCustomResourceProps",
    "CfnMacro",
    "CfnMacroProps",
    "CfnModuleDefaultVersion",
    "CfnModuleDefaultVersionProps",
    "CfnModuleVersion",
    "CfnModuleVersionProps",
    "CfnResourceDefaultVersion",
    "CfnResourceDefaultVersionProps",
    "CfnResourceVersion",
    "CfnResourceVersionProps",
    "CfnStack",
    "CfnStackProps",
    "CfnStackSet",
    "CfnStackSetProps",
    "CfnWaitCondition",
    "CfnWaitConditionHandle",
    "CfnWaitConditionProps",
]

publication.publish()
