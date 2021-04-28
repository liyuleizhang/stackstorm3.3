cd /opt/stackstorm3.3/stackstorm
docker-compose down
docker rmi st2api:v1
docker rmi st2actionrunner:v1
docker volume rm stackstorm_stackstorm-keys stackstorm_stackstorm-mongodb stackstorm_stackstorm-packs stackstorm_stackstorm-packs-configs stackstorm_stackstorm-postgres stackstorm_stackstorm-rabbitmq stackstorm_stackstorm-redis stackstorm_stackstorm-ssh stackstorm_stackstorm-virtualenvs stackstorm_stackstorm-ansible
cd /opt/stackstorm3.3/build-stackstorm-image
docker build -f Dockerfile_st2api -t st2api:v1 ./
docker build -f Dockerfile_st2actionrunner -t st2actionrunner:v1 ./
cd /opt/stackstorm3.3/stackstorm
docker-compose up -d
