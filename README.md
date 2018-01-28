# Music recommendation service
This project is intended to help users to find new interesting music bands based on their vk.com profile.

It's simple: send your user_id and get a recommendation of 10 music bands which will likely meet your taste.

## Under the hood system has 4 main parts:
- UI:
Django based web server.
- Telegram bot:
just start chat with @Muzender_bot
- recommendation model:
We use Implicit ALS implementation it's blazing fast and support online recommendation without recalculation of the whole user-item matrix. After some optimizations, recommendation for new user takes less than 0.5 seconds.
- vk.com user page parser:
We use vk_api implementation but it's quite limited and took about 15 seconds to parse all user music data, so it's main delay point and we work to implement the faster multiprocess solution.
- message queue:
RabbitMQ as queue manager. Really easy to work with and functional, it supports RPC which is crucial for this project.

All services run in Docker containers and we use docker compose for orchestration. This allows to deploy and run all services with a single command, test different solutions in parallel and balance loads in future. Also as a big plus, all the package and service settings are in the text format so it's easy to configure and keep configurations in version control system.

## Super quick start:
- download [model.pkl](https://drive.google.com/open?id=1DfQoraube1tpEtvjUmq9Ue-pBXHJiiih) (250MB) to recommedation_service/data/

- download [dataset.pkl](https://drive.google.com/open?id=1O9dLiuV873pm-MjChUKl_KNQGoFHm1yo) (360MB) to recommedation_service/data/

- download [artist_names.pkl](https://drive.google.com/open?id=1O9dLiuV873pm-MjChUKl_KNQGoFHm1yo) (1MB) to recommedation_service/data/

- setup vk account for parser:
create dictionary with 'login' and 'password' keys and enter your values and dump it to pickle version 3 to parser/secret.pkl

- start service:
cd to root folder of the project and run: docker-compose up --build .

- get your recommendation:
just open http://localhost:8000 in your browser and enter vk.com user id (only numbers)

## Quick start (build dataset and train model from scratch):
- get data:
We use Million Song Dataset and Echo Nest user-music rating dataset. 
Download these tables to  Vk_user_analyzer/data/ (you will find links in dataset_sources.txt file of this folder).

- preprocess data:
Run Vk_user_analyzer/model_creation/dataset_assembly.ipynb to reformat data to apropriate format.

- train model:
Run Vk_user_analyzer/model_creation/basic_recommender.ipynb model will be stored in recommedation_service/data/model.pkl file.

- setup vk account for parser:
create dictionary with 'login' and 'password' keys and enter your values and dump it to pickle version 3 to parser/secret.pkl

- start service:
cd to root folder of the project and run: docker-compose up --build .

- get your recommendation:
just open http://localhost:8000 in your browser and enter vk.com user id (only numbers)
