'''
# AWS CDK Docker Image Assets

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module allows bundling Docker images as assets.

Images are built from a local Docker context directory (with a `Dockerfile`),
uploaded to ECR by the CDK toolkit and/or your app's CI-CD pipeline, and can be
naturally referenced in your CDK app.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ecr_assets import DockerImageAsset


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image")
)
```

The directory `my-image` must include a `Dockerfile`.

This will instruct the toolkit to build a Docker image from `my-image`, push it
to an AWS ECR repository and wire the name of the repository as CloudFormation
parameters to your stack.

By default, all files in the given directory will be copied into the docker
*build context*. If there is a large directory that you know you definitely
don't need in the build context you can improve the performance by adding the
names of files and directories to ignore to a file called `.dockerignore`, or
pass them via the `exclude` property. If both are available, the patterns
found in `exclude` are appended to the patterns found in `.dockerignore`.

The `ignoreMode` property controls how the set of ignore patterns is
interpreted. The recommended setting for Docker image assets is
`IgnoreMode.DOCKER`. If the context flag
`@aws-cdk/aws-ecr-assets:dockerIgnoreSupport` is set to `true` in your
`cdk.json` (this is by default for new projects, but must be set manually for
old projects) then `IgnoreMode.DOCKER` is the default and you don't need to
configure it on the asset itself.

Use `asset.imageUri` to reference the image (it includes both the ECR image URL
and tag.

You can optionally pass build args to the `docker build` command by specifying
the `buildArgs` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    build_args={
        "HTTP_PROXY": "http://10.20.30.2:1234"
    }
)
```

You can optionally pass a target to the `docker build` command by specifying
the `target` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    target="a-target"
)
```

## Pull Permissions

Depending on the consumer of your image asset, you will need to make sure
the principal has permissions to pull the image.

In most cases, you should use the `asset.repository.grantPull(principal)`
method. This will modify the IAM policy of the principal to allow it to
pull images from this repository.

If the pulling principal is not in the same account or is an AWS service that
doesn't assume a role in your account (e.g. AWS CodeBuild), pull permissions
must be granted on the **resource policy** (and not on the principal's policy).
To do that, you can use `asset.repository.addToResourcePolicy(statement)` to
grant the desired principal the following permissions: "ecr:GetDownloadUrlForLayer",
"ecr:BatchGetImage" and "ecr:BatchCheckLayerAvailability".
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
    FileFingerprintOptions as _FileFingerprintOptions_115b8b51,
    IgnoreMode as _IgnoreMode_655a98e8,
    SymlinkFollowMode as _SymlinkFollowMode_047ec1f6,
)
from ..aws_ecr import IRepository as _IRepository_e6004aa6


class DockerImageAsset(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAsset",
):
    '''(experimental) An asset that represents a Docker image.

    The image will be created in build time and uploaded to an ECR repository.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_SymlinkFollowMode_047ec1f6] = None,
        ignore_mode: typing.Optional[_IgnoreMode_655a98e8] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param directory: (experimental) The directory where the Dockerfile is stored.
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param target: (experimental) Docker target to build to. Default: - no target
        :param extra_hash: (experimental) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (experimental) Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow_symlinks: (experimental) A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: (experimental) The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        props = DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        jsii.create(DockerImageAsset, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> builtins.str:
        '''(experimental) A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetHash"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        '''(experimental) The full URI of the image (including a tag).

        Use this reference to pull
        the asset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        jsii.set(self, "imageUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repository")
    def repository(self) -> _IRepository_e6004aa6:
        '''(experimental) Repository where the image is stored.

        :stability: experimental
        '''
        return typing.cast(_IRepository_e6004aa6, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: _IRepository_e6004aa6) -> None:
        jsii.set(self, "repository", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAssetOptions",
    jsii_struct_bases=[_FileFingerprintOptions_115b8b51],
    name_mapping={
        "exclude": "exclude",
        "follow_symlinks": "followSymlinks",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "build_args": "buildArgs",
        "file": "file",
        "target": "target",
    },
)
class DockerImageAssetOptions(_FileFingerprintOptions_115b8b51):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_SymlinkFollowMode_047ec1f6] = None,
        ignore_mode: typing.Optional[_IgnoreMode_655a98e8] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for DockerImageAsset.

        :param exclude: (experimental) Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow_symlinks: (experimental) A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: (experimental) The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param extra_hash: (experimental) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param target: (experimental) Docker target to build to. Default: - no target

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from the copy.

        :default: - nothing is excluded

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_symlinks(self) -> typing.Optional[_SymlinkFollowMode_047ec1f6]:
        '''(experimental) A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER

        :stability: experimental
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_SymlinkFollowMode_047ec1f6], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_IgnoreMode_655a98e8]:
        '''(experimental) The ignore behavior to use for exclude patterns.

        :default: IgnoreMode.GLOB

        :stability: experimental
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_IgnoreMode_655a98e8], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: experimental
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker target to build to.

        :default: - no target

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAssetProps",
    jsii_struct_bases=[DockerImageAssetOptions],
    name_mapping={
        "exclude": "exclude",
        "follow_symlinks": "followSymlinks",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "build_args": "buildArgs",
        "file": "file",
        "target": "target",
        "directory": "directory",
    },
)
class DockerImageAssetProps(DockerImageAssetOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_SymlinkFollowMode_047ec1f6] = None,
        ignore_mode: typing.Optional[_IgnoreMode_655a98e8] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        directory: builtins.str,
    ) -> None:
        '''(experimental) Props for DockerImageAssets.

        :param exclude: (experimental) Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow_symlinks: (experimental) A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: (experimental) The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param extra_hash: (experimental) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param target: (experimental) Docker target to build to. Default: - no target
        :param directory: (experimental) The directory where the Dockerfile is stored.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "directory": directory,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Glob patterns to exclude from the copy.

        :default: - nothing is excluded

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_symlinks(self) -> typing.Optional[_SymlinkFollowMode_047ec1f6]:
        '''(experimental) A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER

        :stability: experimental
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_SymlinkFollowMode_047ec1f6], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_IgnoreMode_655a98e8]:
        '''(experimental) The ignore behavior to use for exclude patterns.

        :default: IgnoreMode.GLOB

        :stability: experimental
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_IgnoreMode_655a98e8], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(experimental) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: experimental
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker target to build to.

        :default: - no target

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''(experimental) The directory where the Dockerfile is stored.

        :stability: experimental
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerImageAsset",
    "DockerImageAssetOptions",
    "DockerImageAssetProps",
]

publication.publish()
