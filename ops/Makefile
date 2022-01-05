# https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
# https://aws.amazon.com/premiumsupport/knowledge-center/eks-access-kubernetes-services/
# https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
delete_cloud_foramtion_stack:
	aws cloudformation delete-stack --stack-name  eksctl-mozhi-eks-cluster

create_cluster:
	eksctl create cluster -f aws/cluster.yaml

delete_cluster:
	eksctl delete cluster -f aws/cluster.yaml

describe_cluster:
	eksctl utils describe-stacks --region=${AWS_DEFAULT_REGION} --cluster=mozhi-eks

aws_identity:
	aws sts get-caller-identity

set_context:
	eksctl utils write-kubeconfig --cluster=mozhi-eks --set-kubeconfig-context=true

enable_iam_sa_provider:
	eksctl utils associate-iam-oidc-provider --cluster=mozhi-eks --approve

create_cluster_role:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/rbac-role.yaml

delete_iam_policy:
	aws iam delete-policy --policy-arn arn:aws:iam::344890062315:policy/AWSLoadBalancerControllerIAMPolicy

create_iam_policy:
	curl -o aws/iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy.json
	aws iam create-policy \
		--policy-name AWSLoadBalancerControllerIAMPolicy \
		--policy-document file://aws/iam_policy.json


create_service_account:
	eksctl create iamserviceaccount \
      --cluster=mozhi-eks \
      --namespace=kube-system \
      --name=aws-load-balancer-controller \
      --attach-policy-arn=arn:aws:iam::344890062315:policy/AWSLoadBalancerControllerIAMPolicy \
      --override-existing-serviceaccounts \
      --approve

create_controller_policy:
	curl -o aws/iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy_v1_to_v2_additional.json
	aws iam create-policy \
  		--policy-name AWSLoadBalancerControllerAdditionalIAMPolicy \
  		--policy-document file://aws/iam_policy_v1_to_v2_additional.json

	export ROLE_NAME=`aws iam list-roles | grep -i addon | grep -i "RoleName" | cut -d ':' -f 2 | sed 's/",//' | sed 's/ "//'`
	aws iam attach-role-policy \
  		--role-name ${ROLE_NAME} \
  		--policy-arn arn:aws:iam::344890062315:policy/AWSLoadBalancerControllerAdditionalIAMPolicy

# aws iam get-role --role-name eksctl-mozhi-eks-addon-iamserviceaccount-kube-system-aws-load-balancer-controlle

deploy_cert_manager:
	kubectl apply \
		--validate=false \
		-f https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.yaml
	sleep 10

# https://kubernetes.github.io/ingress-nginx/deploy/#aws
k8s_ingress_controller:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.0/deploy/static/provider/aws/deploy.yaml

deploy_ingress_controller:
	kubectl apply -f aws/v2_3_1_full.yaml
	sleep 10

deploy_application:
	kustomize build ./k8s/mozhi/ | kubectl apply -f -

delete_application:
	kustomize build ./k8s/mozhi/ | kubectl delete -f -

# https://aws.amazon.com/premiumsupport/knowledge-center/eks-load-balancers-troubleshooting/

# 1. Delete IAM Policies (AWSLoadBalancerController*)
# 2. Delete IAM Roles (eksctl-mozhi-eks*)
# 3. Delete Cloud Formation templates
# 4. Delete EKS cluster
# 5. Delete EC2 Instances
# 6. Delete Load Balancers
# 7. Delete NAT Gateways
# 8. Release Elastic IP
# 9. Delete VPC