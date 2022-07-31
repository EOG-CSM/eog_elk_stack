## Start the ELK containers

Change password to desired password in .env file.

```
$ cd path/to/cloned/repository
$ cd main_elk_compose
$ sudo docker-compose up -d
```

### Copy the ca.crt

The docker containers should have generated a certificate authority in `certs/`. This folder should also be owned by root. Copy the ca.crt to the base repo dir and change it so you have access rights.

```
$ cd path/to/repo/
# cp certs/ca/ca.crt 
# chown <your-username> ca.crt # or appropriate chmod
```

## Filebeat setup

### Get the API key

Run the python script `python3 elk_setup.py api`. This should print the API key. Copy it and paste it in the API key section of `filebeat/filebeat.yml` (need root access).

### Run Filebeat Setup

```
$ cd path/to/cloned/repo
$ cd filebeat
$ which docker-compose # eogdata server docker-compose is in /usr/bin/local
/path/to/docker-compose
$ sudo /path/to/docker-compose run filebeat filebeat setup -e
```

## Creating the user-list index, enrich policy, and ingest pipelines.  

The below script handles all of this. Just make sure the elastic username:password in the script is correct if you change it (Default is elastic:elasticpassword).

`python3 elk_setup.py setup <name of user_list file.json>`

## Start the filebeat container

```
$ cd /path/to/repo
$ cd filebeat
$ sudo /path/to/docker-compose up -d
```
Note: if this doesn't work, omit the `-d` to see what the container is printing to stdout.

## Ranking Users and Countries

See [rank_users.md](rank_users.md) and [rank_countries.md](rank_countries.md).
