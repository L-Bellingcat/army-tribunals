docker build -t server:latest -f website/Dockerfile .
docker tag server:latest europe-west2-docker.pkg.dev/army-tribunals/server/server:latest
docker push europe-west2-docker.pkg.dev/army-tribunals/server/server:latest