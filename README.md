# Library Microservices (Assignment 2)

Multi-container version of the Assignment 1 Library API. Three Flask services (books, staff, readers) sit behind an Nginx reverse proxy, and a MySQL container is set up for the database work in a later assignment. The APIs read from text files for now and don't query MySQL yet.

## Layout

```
services/
  books_api/     app.py, Dockerfile, requirements.txt, books.txt
  staff_api/     app.py, Dockerfile, requirements.txt, staff.txt
  readers_api/   app.py, Dockerfile, requirements.txt, readers.txt
nginx/nginx.conf
docker-compose.yml
.env.example
```

## Setup

1. Copy the example env file and set your own values:

```
cp .env.example .env
```

2. Build and start everything:

```
docker compose up -d --build
```

3. Check the containers. The three APIs show "starting" for 10 to 20 seconds, then "healthy". Nginx starts last, once they are healthy:

```
docker compose ps
```

## Endpoints

Everything goes through Nginx on port 80.

| URL | What it returns |
|---|---|
| /health | "healthy" (answered by Nginx itself) |
| /api/books | all books |
| /api/books/{id} | one book, or 404 |
| /api/staff | all staff |
| /api/staff/{id} | one staff member, or 404 |
| /api/readers | all readers |
| /api/readers/{id} | one reader, or 404 |

Each API also has its own `/` and `/health` routes. Those aren't published outside Docker, so check them from inside:

```
docker compose exec books-api python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read().decode())"
```

## How it's wired

- Two named networks: `app_frontend` and `app_backend`.
- Nginx is only on the frontend network. The database is only on the backend network. The three APIs are on both.
- Port 80 on Nginx is the only port published to the host.
- Containers find each other by service name (for example `books-api:5000` and `db`).
- Database data lives in the named volume `app_db_data`, so it survives `docker compose down`.

## Config choices

- The healthchecks use Python instead of curl, because the slim Python image doesn't include curl.
- Each `proxy_pass` in nginx.conf ends with the service's route (for example `http://books_api/books`), so `/api/books/3` reaches Flask as `/books/3`. Without that, Flask gets `/api/books/3` and returns 404.
- Nginx waits for the three APIs to be healthy before it starts (`condition: service_healthy`).
- Each container has a memory limit.
- Database credentials come from `.env`, which is not committed. `.env.example` lists the variables.

## Troubleshooting

- **502 Bad Gateway:** Nginx can't reach an API. Run `docker compose ps` and `docker compose logs <service>`.
- **404 through Nginx:** the proxy worked but the path is wrong. Check the `proxy_pass` lines.
- **A service shows unhealthy:** run `docker inspect --format '{{json .State.Health}}' <container>` to see the failed check output.
- **Port 80 already in use:** change `"80:80"` in docker-compose.yml to `"8080:80"` and use port 8080.
- **Changed the DB password in .env but the old one still works:** MySQL only reads those values on first start. Run `docker compose down -v` to wipe the volume, then start again.

## Stopping

```
docker compose down      # removes containers, keeps the database volume
docker compose down -v   # removes containers and the database volume
```

## AI Use Disclosure

AI was used to help me better understand the instructions and troubleshoot any errors along the way. I completed the commands myself and documented the results using my own screenshots.

It also assisted with formatting my 'readme.md' the way I wanted it.
