# Setup

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


# Ranking Users

1. Click menu on the left (3 lines), then under Analytics, click dashboard.
2. Click create new visualization.
3. From the left, drag userinfo.email into the graph
4. Click the top 5 values, and change the number of values to whatever you want
5. Then follow the steps below depending on how you want to rank.

## Rank by number of accesses
1. Leave rank by as count of records.

## Rank by Volume Downloaded
1. Click on what is under the vertical axis section
2. Select the field `http.response.body.bytes`
3. Under functions, select sum
4. Now there should be a vertical axis section that says `Sum of http.response.body.bytes`.

## Export
1. Click download as CSV at the top


# Ranking Countries

1. Click menu on the left (3 lines), then under Analytics, click dashboard.
2. Click create new visualization.
3. From the left, drag `source.geo.country_name` into the graph
4. Click the top 5 values, and change the number of values to whatever you want
5. Then follow the steps below depending on how you want to rank.

## Rank by number of accesses
1. Leave rank by as count of records.

## Rank by Volume Downloaded
1. Click on what is under the vertical axis section
2. Select the field `http.response.body.bytes`
3. Under functions, select sum
4. Now there should be a vertical axis section that says `Sum of http.response.body.bytes`.

## Export
1. Click download as CSV at the top
