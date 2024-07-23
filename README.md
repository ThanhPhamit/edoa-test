# agent

## frontend(agent) setting

Run the following command

```sh
npm install -g pnpm
pnpm install
pnpm run setup
pnpm run dev
```

## backend setting

Run the following command

```sh
docker-compose exec backend bash
python manage.py makemigrations api
python manage.py migrate
```

```sh
docker-compose build --no-cache
docker-compose up
```

Build image for deployment
```sh
docker build -f ./docker/python/Dockerfile --force-rm -t pocket-assistant-api  .
```