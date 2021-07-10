: '
Use this script to build docker images and push it to default dockerhub repo
1) Frontend
./scripts/k8s-helper.sh -f frontend -v 0.4
2) Backend
./scripts/k8s-helper.sh -f backend -v 0.4
3) All
./scripts/k8s-helper.sh -f all -v 0.4
4) Delete and reapply K8s objects
./scripts/k8s-helper.sh -f killnrestart
5) Update existing K8s objects
./scripts/k8s-helper.sh -f update
'
while getopts f:v: flag
do
    case "${flag}" in
        f) FLAG=${OPTARG};;
        v) VERSION=${OPTARG};;
    esac
done

ui_image() {
  docker build -t mozhi-ui-cpu:latest -f ops/docker/ui/Dockerfile .
  docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:$VERSION
  docker push mageswaran1989/mozhi-ui-cpu:$VERSION

  docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:latest
  docker push mageswaran1989/mozhi-ui-cpu:latest
}

api_image() {
  docker build -t mozhi-api-cpu:latest -f ops/docker/api/cpu/multistage/Dockerfile .
  docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:$VERSION
  docker push mageswaran1989/mozhi-api-cpu:$VERSION

  docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:latest
  docker push mageswaran1989/mozhi-api-cpu:latest
}

apply_mozhi_k8s() {
  kubectl apply -f ops/k8s/services/ --v=0
  kubectl get all
}

kill_and_restart() {
  # Deletes all K8s objects with label "mozhi"
  kubectl delete pods,services,deployments,ingress -l org=mozhi --v=0
  apply_mozhi_k8s
}

start_minikube() {
  export DRIVER=docker
  minikube start --vm-driver=$(DRIVER)
}

if [ "$FLAG" == "frontend" ]
then
  ui_image
elif [ "$FLAG" == "backend" ]; then
  api_images
elif [ "$FLAG" == "aall" ]; then
  ui_image
  api_image
elif [ "$FLAG" == "killandrestart" ]; then
  kill_and_restart
elif [ "$FLAG" == "update" ]; then
  apply_mozhi_k8s
else
  echo "Invalid choice"
fi