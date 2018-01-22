# Music recommendation service
This project is intended to help users to find new interesting music bands based on their vk.com profile.

It's simple: send your user_id and get a recommendation of 10 music bands which will likely meet your taste.

## Under the hood system has 4 main parts:
- UI:
Jango web server.
- recommendation model:
We use Implicit ALS implementation it's blazing fast and support online recommendation without recalculation of the whole user-item matrix. After some optimizations, recommendation for new user takes less than 0.5 seconds.
- vk.com user page parser:
We use vk_api implementation but it's quite limited and took about 15 seconds to parse all user music data, so it's main delay point and we work to implement the faster multiprocess solution.
- message queue:
RabbitMQ as queue manager. Really easy to work with and functional, it supports RPC which is crucial for this project.

All services run in Docker containers and we use docker compose for orchestration. This allows to deploy and run all services with a single command, test different solutions in parallel and balance loads in future. Also as a big plus, all the package and service settings are in the text format so it's easy to configure and keep configurations in version control system.
