# verbs-training

## Database

You can either install Postregres or use a Docker container

#### By installing Postgres

[PostgreSQL](https://www.postgresql.org/download/)

#### Using the Postgres Docker image

###### Create volume

    $ docker volume create <volume_name>

###### Run postgres container with volume

    $ docker run --name <container_name> -e POSTGRES_USER=<postgres_user> -e POSTGRES_PASSWORD=<postgres_password> --volume <volume_name>:/var/lib/postgresql/data -p 5432:5432 -d postgres