
# docker-compose -d
# -d : detached mode
docker-compose up


# docker-compose stop

# container name : web
# run python manage.py migrate
# --rm : Automatically remove the container when it exits
# docker-compose run --rm web python manage.py migrate


# stop the services - for detached mode (up -d)
# docker compose stop

# remove data in volumes as well
# docker compose down --volumes