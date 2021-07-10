: '
Use this script to build docker images and push it to default dockerhub repo
1) Frontend
./scripts/build-and-push-images.sh -f f -v 0.4
2) Backend
./scripts/build-and-push-images.sh -f b -v 0.4
3) All
./scripts/build-and-push-images.sh -f a -v 0.4
'
while getopts f:v: flag
do
    case "${flag}" in
        b) FLAG=${OPTARG};;
        v) VERSION=${OPTARG};;
    esac
done

ui_image() {
  docker build -t mozhi-ui-cpu:latest -f ops/docker/ui/Dockerfile .
  docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:$VERSION
  docker push mageswaran1989/mozhi-ui-cpu:$VERSION
}

api_image() {
  docker build -t mozhi-api-cpu:latest -f ops/docker/api/cpu/multistage/Dockerfile .
  docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:$VERSION
  docker push mageswaran1989/mozhi-api-cpu:$VERSION
}

if [ "$FLAG" == "b" ]
then
  ui_image
elif [ "$FLAG" == "f" ]; then
  api_images
else
  ui_image
  api_image
fi

