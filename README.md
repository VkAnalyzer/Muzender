# Music recommendation service
This project is intended to help users to find new interesting music bands based on their vk.com profile.

It's simple: send your user_id and get recommendation of 5 music bands which will likely meet your taste. 

Adjust settings and try again.

## Under the hood system has 7 main parts:
- UI:
Django based web server.
- Telegram bot:
just start chat with @Muzender_bot
- recommendation model:
We use Word2Vec, it supports online recommendation without recalculation, it takes about 25ms for to generate 
recomendations for new user. It also have tiny memory footprint which allows to host whole system on 1 CPU, 
1GB RAM server.
- vk.com user page parser:
We use vk_api implementation to parse all user music data. We run multiple parsers at the same time to work 
with several users simultaneously.
- Redis to cache parser results for fast recommendation recalculation when user changes settings.
- message queue:
RabbitMQ as queue manager. Really easy to work with and functional.
- vk.com crawler: it runs through user's friends and friends of friends, send their pages to parser to collect dataset. 

All services run in Docker containers and we use docker swarm for orchestration in production 
and docker-compose for development. This allows to deploy and run all 
services with a single command, test different solutions in parallel and balance loads. 

## Super quick start:
- run `python quickstart.py` in console and follow instructions to setup environment

- start service:
cd to root folder of the project and run: `docker stack up -c docker-compose.yml muzender`

- get your recommendation:
just open http://localhost:8000 in your browser and enter vk.com user id
or start chat with your own Telegram bot

- for development it's convenient to use docker-compose with local build:
`docker-compose up docker-compose-dev.yml --build` 

## Build dataset and train model from scratch:
- get data:
You can use Million Song Dataset and Echo Nest user-music rating dataset. 
Download these tables to ./data/ (you will find links in dataset_sources.txt file of this folder).

Alternatively you can use our own dataset which includes 950K of music playlists (links also in dataset_sources.txt file of this folder)

- preprocess data:
Run /model_creation/dataset_assembly.ipynb to reformat data to apropriate format.

- train model:
Run /model_creation/w2v_recommender.ipynb to generate model and band popularity index.
