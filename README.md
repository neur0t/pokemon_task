# pokemon_task
Well, this is a python program that takes two pokemon names and simulates a fight against them.
All the data are fetched through pokeapi.co. The decition of the winner is based on the stats.change field

The repo contains also dockerfile 
These files define a  Docker setup for the application. 

Navigate to the cloned folder

# Docker container using the next command:
docker  build .
# Then to see the image that had been build run the following command:
docker images
# This would produce the ID of the image. And last step
docekr run -it (the image id)


