'''
# Route53 Alias Record Targets for the CDK Route53 Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains Route53 Alias Record targets for:

* API Gateway custom domains

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ApiGateway(rest_api))
  )
  ```
* API Gateway V2 custom domains

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ApiGatewayv2DomainProperties(domain_name.regional_domain_name, domain_name.regional_hosted_zone_id))
  )
  ```
* CloudFront distributions

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.CloudFrontTarget(distribution))
  )
  ```
* ELBv2 load balancers

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.LoadBalancerTarget(elbv2))
  )
  ```
* Classic load balancers

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ClassicLoadBalancerTarget(elb))
  )
  ```

**Important:** Based on [AWS documentation](https://aws.amazon.com/de/premiumsupport/knowledge-center/alias-resource-record-set-route53-cli/), all alias record in Route 53 that points to a Elastic Load Balancer will always include *dualstack* for the DNSName to resolve IPv4/IPv6 addresses (without *dualstack* IPv6 will not resolve).

For example, if the Amazon-provided DNS for the load balancer is `ALB-xxxxxxx.us-west-2.elb.amazonaws.com`, CDK will create alias target in Route 53 will be `dualstack.ALB-xxxxxxx.us-west-2.elb.amazonaws.com`.

* GlobalAccelerator

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(stack, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.GlobalAcceleratorTarget(accelerator))
  )
  ```

**Important:** If you use GlobalAcceleratorDomainTarget, passing a string rather than an instance of IAccelerator, ensure that the string is a valid domain name of an existing Global Accelerator instance.
See [the documentation on DNS addressing](https://docs.aws.amazon.com/global-accelerator/latest/dg/dns-addressing-custom-domains.dns-addressing.html) with Global Accelerator for more info.

* InterfaceVpcEndpoints

**Important:** Based on the CFN docs for VPCEndpoints - [see here](attrDnsEntries) - the attributes returned for DnsEntries in CloudFormation is a combination of the hosted zone ID and the DNS name. The entries are ordered as follows: regional public DNS, zonal public DNS, private DNS, and wildcard DNS. This order is not enforced for AWS Marketplace services, and therefore this CDK construct is ONLY guaranteed to work with non-marketplace services.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
route53.ARecord(stack, "AliasRecord",
    zone=zone,
    target=route53.RecordTarget.from_alias(alias.InterfaceVpcEndpointTarget(interface_vpc_endpoint))
)
```

* S3 Bucket Website:

**Important:** The Bucket name must strictly match the full DNS name.
See [the Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html) for more info.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
[recordName, domainName] = ["www", "example.com"]

bucket_website = Bucket(self, "BucketWebsite",
    bucket_name=[record_name, domain_name].join("."), # www.example.com
    public_read_access=True,
    website_index_document="index.html"
)

zone = HostedZone.from_lookup(self, "Zone", domain_name=domain_name)# example.com

route53.ARecord(self, "AliasRecord",
    zone=zone,
    record_name=record_name, # www
    target=route53.RecordTarget.from_alias(alias.BucketWebsiteTarget(bucket))
)
```

* User pool domain

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.UserPoolDomainTarget(domain))
  )
  ```

See the documentation of `@aws-cdk/aws-route53` for more information.
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
from ..aws_apigateway import (
    IDomainName as _IDomainName_6c4e4c80, RestApi as _RestApi_777c8238
)
from ..aws_cloudfront import IDistribution as _IDistribution_7ac752a4
from ..aws_cognito import UserPoolDomain as _UserPoolDomain_f402e168
from ..aws_ec2 import IInterfaceVpcEndpoint as _IInterfaceVpcEndpoint_7481aea1
from ..aws_elasticloadbalancing import LoadBalancer as _LoadBalancer_a894d40e
from ..aws_elasticloadbalancingv2 import ILoadBalancerV2 as _ILoadBalancerV2_4c5c0fbb
from ..aws_globalaccelerator import IAccelerator as _IAccelerator_88df59f2
from ..aws_route53 import (
    AliasRecordTargetConfig as _AliasRecordTargetConfig_588f62e9,
    IAliasRecordTarget as _IAliasRecordTarget_aae9327f,
    IRecordSet as _IRecordSet_7d446a82,
)
from ..aws_s3 import IBucket as _IBucket_42e086fd


@jsii.implements(_IAliasRecordTarget_aae9327f)
class ApiGatewayDomain(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGatewayDomain",
):
    '''(experimental) Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined through the ``RestApiProps.domainName`` prop.

    :stability: experimental
    '''

    def __init__(self, domain_name: _IDomainName_6c4e4c80) -> None:
        '''
        :param domain_name: -

        :stability: experimental
        '''
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class ApiGatewayv2DomainProperties(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGatewayv2DomainProperties",
):
    '''(experimental) Defines an API Gateway V2 domain name as the alias target.

    :stability: experimental
    '''

    def __init__(
        self,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> None:
        '''
        :param regional_domain_name: the region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.
        :param regional_hosted_zone_id: the domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        '''
        jsii.create(ApiGatewayv2DomainProperties, self, [regional_domain_name, regional_hosted_zone_id])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class BucketWebsiteTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.BucketWebsiteTarget",
):
    '''(experimental) Use a S3 as an alias record target.

    :stability: experimental
    '''

    def __init__(self, bucket: _IBucket_42e086fd) -> None:
        '''
        :param bucket: -

        :stability: experimental
        '''
        jsii.create(BucketWebsiteTarget, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class ClassicLoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ClassicLoadBalancerTarget",
):
    '''(experimental) Use a classic ELB as an alias record target.

    :stability: experimental
    '''

    def __init__(self, load_balancer: _LoadBalancer_a894d40e) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        jsii.create(ClassicLoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class CloudFrontTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.CloudFrontTarget",
):
    '''(experimental) Use a CloudFront Distribution as an alias record target.

    :stability: experimental
    '''

    def __init__(self, distribution: _IDistribution_7ac752a4) -> None:
        '''
        :param distribution: -

        :stability: experimental
        '''
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="getHostedZoneId") # type: ignore[misc]
    @builtins.classmethod
    def get_hosted_zone_id(cls, scope: constructs.IConstruct) -> builtins.str:
        '''(experimental) Get the hosted zone id for the current scope.

        :param scope: - scope in which this resource is defined.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getHostedZoneId", [scope]))

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CLOUDFRONT_ZONE_ID")
    def CLOUDFRONT_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone Id if using an alias record in Route53.

        This value never changes.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDFRONT_ZONE_ID"))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class GlobalAcceleratorDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.GlobalAcceleratorDomainTarget",
):
    '''(experimental) Use a Global Accelerator domain name as an alias record target.

    :stability: experimental
    '''

    def __init__(self, accelerator_domain_name: builtins.str) -> None:
        '''(experimental) Create an Alias Target for a Global Accelerator domain name.

        :param accelerator_domain_name: -

        :stability: experimental
        '''
        jsii.create(GlobalAcceleratorDomainTarget, self, [accelerator_domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GLOBAL_ACCELERATOR_ZONE_ID")
    def GLOBAL_ACCELERATOR_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone Id if using an alias record in Route53.

        This value never changes.
        Ref: https://docs.aws.amazon.com/general/latest/gr/global_accelerator.html

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "GLOBAL_ACCELERATOR_ZONE_ID"))


class GlobalAcceleratorTarget(
    GlobalAcceleratorDomainTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.GlobalAcceleratorTarget",
):
    '''(experimental) Use a Global Accelerator instance domain name as an alias record target.

    :stability: experimental
    '''

    def __init__(self, accelerator: _IAccelerator_88df59f2) -> None:
        '''(experimental) Create an Alias Target for a Global Accelerator instance.

        :param accelerator: -

        :stability: experimental
        '''
        jsii.create(GlobalAcceleratorTarget, self, [accelerator])


@jsii.implements(_IAliasRecordTarget_aae9327f)
class InterfaceVpcEndpointTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.InterfaceVpcEndpointTarget",
):
    '''(experimental) Set an InterfaceVpcEndpoint as a target for an ARecord.

    :stability: experimental
    '''

    def __init__(self, vpc_endpoint: _IInterfaceVpcEndpoint_7481aea1) -> None:
        '''
        :param vpc_endpoint: -

        :stability: experimental
        '''
        jsii.create(InterfaceVpcEndpointTarget, self, [vpc_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class LoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.LoadBalancerTarget",
):
    '''(experimental) Use an ELBv2 as an alias record target.

    :stability: experimental
    '''

    def __init__(self, load_balancer: _ILoadBalancerV2_4c5c0fbb) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_aae9327f)
class UserPoolDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.UserPoolDomainTarget",
):
    '''(experimental) Use a user pool domain as an alias record target.

    :stability: experimental
    '''

    def __init__(self, domain: _UserPoolDomain_f402e168) -> None:
        '''
        :param domain: -

        :stability: experimental
        '''
        jsii.create(UserPoolDomainTarget, self, [domain])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_7d446a82) -> _AliasRecordTargetConfig_588f62e9:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_588f62e9, jsii.invoke(self, "bind", [_record]))


class ApiGateway(
    ApiGatewayDomain,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGateway",
):
    '''(experimental) Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.

    :stability: experimental
    '''

    def __init__(self, api: _RestApi_777c8238) -> None:
        '''
        :param api: -

        :stability: experimental
        '''
        jsii.create(ApiGateway, self, [api])


__all__ = [
    "ApiGateway",
    "ApiGatewayDomain",
    "ApiGatewayv2DomainProperties",
    "BucketWebsiteTarget",
    "ClassicLoadBalancerTarget",
    "CloudFrontTarget",
    "GlobalAcceleratorDomainTarget",
    "GlobalAcceleratorTarget",
    "InterfaceVpcEndpointTarget",
    "LoadBalancerTarget",
    "UserPoolDomainTarget",
]

publication.publish()
