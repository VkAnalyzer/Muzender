# Music recommendation service
This project is intended to help users to find new interesting music bands based on their vk.com profile.

It's simple: send your user_id and get a recommendation of 5 music bands which will likely meet your taste. 
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
We use vk_api implementation but it's quite limited and took about 15 seconds to parse all user music data. 
So we run multiple parsers at the same time.
- Redis to cache parser results for fast recommendation recalculation when user changes settings.
- message queue:
RabbitMQ as queue manager. Really easy to work with and functional.
- vk.com crawler: it runs through user's friends and friends of friends, send their pages to parser to collect dataset. 

All services run in Docker containers and we use docker compose for orchestration. This allows to deploy and run all 
services with a single command, test different solutions in parallel and balance loads. 

## Super quick start:
- download [model_w2v.pkl](https://drive.google.com/open?id=1LXEJsFOAl0TX51sNY-s5BOHknInc6Wku) (22MB) to /data/

- download [dataset.pkl](https://drive.google.com/open?id=1BiMqy4YLuBIF2RWMqUbgK5OyJr7Nfw2t) (1MB) to /data/

- setup vk account for parser:
create dictionary with 'login' and 'password' keys and enter your values and dump it to pickle version 3 
to parser/secret.pkl and crawler/secret.pkl

- setup telegram bot token:
pickle string with bot token and dump it to tg_bot/token.pkl 

- start service:
cd to root folder of the project and run: `docker-compose up --build .`

- get your recommendation:
just open http://localhost:8000 in your browser and enter vk.com user id

## Build dataset and train model from scratch:
- get data:
We use Million Song Dataset and Echo Nest user-music rating dataset. 
Download these tables /data/ (you will find links in dataset_sources.txt file of this folder).

- preprocess data:
Run /model_creation/dataset_assembly.ipynb to reformat data to apropriate format.

- train model:
Run /model_creation/w2v_recommender.ipynb to generate model and band popularity index.
