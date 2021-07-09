: '
Use this script to build docker iamges and push it to default dockerhub repo
1) Frontend
./script/build_n_push_images.sh -f f -v 0.3
2) Backend
./script/build_n_push_images.sh -f b -v 0.3
3) All
./script/build_n_push_images.sh -f a -v 0.3
'
while getopts f:v: flag
do
    case "${flag}" in
        b) FLAG=${OPTARG};;
        v) VERSION=${OPTARG};;
    esac
done

if [ "$FLAG" == "b" ]
then
  docker build -t mozhi-ui-cpu:latest -f ops/docker/ui/Dockerfile .
  docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:$VERSION
  docker push mageswaran1989/mozhi-ui-cpu:$VERSION
elif [ "$FLAG" == "f" ]; then
  docker build -t mozhi-api-cpu:latest -f ops/docker/api/cpu/multistage/Dockerfile .
  docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:$VERSION
  docker push mageswaran1989/mozhi-api-cpu:$VERSION
else
  docker build -t mozhi-ui-cpu:latest -f ops/docker/ui/Dockerfile .
  docker tag mozhi-ui-cpu:latest mageswaran1989/mozhi-ui-cpu:$VERSION
  docker push mageswaran1989/mozhi-ui-cpu:$VERSION
  docker build -t mozhi-api-cpu:latest -f ops/docker/api/cpu/multistage/Dockerfile .
  docker tag mozhi-api-cpu:latest mageswaran1989/mozhi-api-cpu:$VERSION
  docker push mageswaran1989/mozhi-api-cpu:$VERSION
fi

