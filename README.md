# containerizing-python-microservice
Containerizing a Python Microservice, Multi-Container Orchestration with Docker Compose, Live Web UI &amp; Bind Mounts, Troubleshooting Skills

Step 1 Create folder name microservice
mkdir microservice
cd microservice

Step 2 Create folder name server
mkdir server
cd server

Step 3 Create Dockerfile and server.py and index.html file in server folder
vim Dockerfile

vim server.py

vim index.html

Verify all created file
ls

Step 5 Create folder name client
mkdir client
cd client

Step 6 Create Dockerfile and client.py and template.html file in client folder
vim Dockerfile

vim client.py

vim template.html

Verify all created file
ls
 
Step 7 Create docker-compose.yml file
vim docker-compose.yml

Step 8 Create docker-stack.yml for Docker Swarm
vim docker-stack.yml 

Step 9 Build image using compose file
docker-compose build

Verify images created
docker images

Step 10 Tag the images and push remote Docker Hub
Tag images

Verify

Step 11 Push images
Before push create Docker Hub account login.docker.com

Type docker login in terminal and authenticate.
docker login 

Push image to Docker Hub
Syntax : docker push your-username/imagename
docker push akmi/microservice-server:v1

Syntax : docker push your-username/imagename
docker push akmi/microservice-client:v1

Verify on Docker Hub portal

Step 12 Start containers
docker compose up -d 

Verify containers
docker ps

Step 13 Check http://localhost:8091/ on browser

OR

Run curl command in terminal
curl http://localhost:8091 

Deploy and inspect the stack on your Swarm Manager node:

Step 14 Start Docker Swarm 
docker swarm init

Step Deploy Stack
docker stack deploy -c docker-stack.yml docker-microservice

Verify stack

Step 15 Create worker node for distribute workload
docker run -d --privileged --name manager1 docker:dind
docker run -d --privileged --name manager2 docker:dind
docker run -d --privileged --name manager3 docker:dind

Note : docker:dind image is not available in local repository, hence it download from remote  and store locally.

Step 16 Join node to Docker Swarm
docker exec -it manager1 docker swarm join --token SWMTKN-1-0wmrxdurs7p9xqa6h85g2jr71a3gs89arpxst0htyoisxdylqi-1wkgipzhk720m2d5komkb11x9 192.168.65.3:2377

docker exec -it manager2 docker swarm join --token SWMTKN-1-0wmrxdurs7p9xqa6h85g2jr71a3gs89arpxst0htyoisxdylqi-1wkgipzhk720m2d5komkb11x9 192.168.65.3:2377

Verify
docker node ls

Step 17  Promote node as swarm manager 
docker node promote 198a75bb8809
docker node promote 86890d48cf14


Verify Check Manager Status changed to reachable
docker node ls

Step 18 Create worker node 
docker run -d --privileged --name workernode1 docker:dind
docker run -d --privileged --name workernode2 docker:dind

Verify 
docker node ls

Step 19 Join node to Docker Swarm

docker exec -it workernode1 docker swarm join --token SWMTKN-1-0wmrxdurs7p9xqa6h85g2jr71a3gs89arpxst0htyoisxdylqi-1wkgipzhk720m2d5komkb11x9 192.168.65.3:2377
docker exec -it workernode2 docker swarm join --token SWMTKN-1-0wmrxdurs7p9xqa6h85g2jr71a3gs89arpxst0htyoisxdylqi-1wkgipzhk720m2d5komkb11x9 192.168.65.3:2377


Verify
docker node ls
Column Manager Status Blank are docker worker nodes.

Step 20 Rebalance both services
docker service update --force docker-microservice_client


Verify
docker service ps --filter "desired-state=running" docker-microservice_client


Service docker-microservice_client is distributed between node 198a75bb8809
and 86890d48cf14.

docker service update --force docker-microservice_server

Verify
docker service ps --filter "desired-state=running" docker-microservice_server


Check website on browser
http://localhost:8091

OR

curl http://localhost:8091


Monitor and logs

# 1. Check container exit code, error message, and active command
docker inspect --format 'Status: {{.State.Status}} | ExitCode: {{.State.ExitCode}} | Error: {{.State.Error}} | Cmd: {{.Config.Cmd}}' <container>

# 2. Check container networks, IP addresses, and DNS aliases
docker inspect --format '{{json .NetworkSettings.Networks}}' <container>

# 3. Check container bind mounts and volumes
docker inspect --format '{{json .Mounts}}' <container>

# 4. Check Swarm service ports and placement constraints
docker service inspect --format 'Ports: {{json .Spec.EndpointSpec.Ports}} | Constraints: {{json .Spec.TaskTemplate.Placement.Constraints}}' <service>

# 5.Check the webpage is working on containers.
docker service logs --tail 25 docker-microservice_client
