# AWS EKS Clsuter


```

eksctl create cluster

https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/deploy/installation/#setup-iam-role-for-service-accounts


Ingress: https://aws.amazon.com/premiumsupport/knowledge-center/eks-alb-ingress-aws-waf/

https://aws.amazon.com/premiumsupport/knowledge-center/eks-access-kubernetes-services/

https://githubmemory.com/repo/kubernetes-sigs/aws-load-balancer-controller/issues/2013

curl -silent ade9f3f72abd64501b785996d1c230a0-85582002.ap-south-1.elb.amazonaws.com:8080 | grep title


kubectl -n mozhi get pods -l 'app=nginx' -o wide | awk {'print $1" " $3 " " $6'} | column -t


kubectl apply -f ops/k8s/mozhi/namespace.yaml 
kubectl apply -f ops/k8s/mozhi/ui.yaml
kubectl apply -f ops/k8s/mozhi/api.yaml
 kubectl apply -f ops/k8s/mozhi/nginx-deployment.yaml 

```


```
eksctl utils associate-iam-oidc-provider \
    --region ap-south-1 \
    --cluster ridiculous-hideout-1640086879 \
    --approve


curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.1/docs/install/iam_policy.json



(mozhi) m.c.dhandapani@AMAC02FF2J5MD6P mozhi % aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json
{
    "Policy": {
        "PolicyName": "AWSLoadBalancerControllerIAMPolicy",
        "PolicyId": "ANPAVATIMWXV4WEZSVQ6J",
        "Arn": "arn:aws:iam::344890062315:policy/AWSLoadBalancerControllerIAMPolicy",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
        "PermissionsBoundaryUsageCount": 0,
        "IsAttachable": true,
        "CreateDate": "2021-12-21T13:58:17Z",
        "UpdateDate": "2021-12-21T13:58:17Z"
    }
}



eksctl create iamserviceaccount \
--cluster=ridiculous-hideout-1640086879 \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--attach-policy-arn=arn:aws:iam::344890062315:policy/AWSLoadBalancerControllerIAMPolicy \
--override-existing-serviceaccounts \
--approve


```

