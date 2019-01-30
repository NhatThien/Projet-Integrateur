# Projet Integrateur

## Prerequisites
minio
spark
elasticsearch
kibana
elasticsearch-spark-20_2.11-x.x.x.jar: jars file for spark and elasticsearch integration (x.x.x: your elasticsearch version)
tensorflow

## Running the test

Launch mini
docker-compose up

Launch elasticsearch (always before launch kibana)
cd elasticsearch-6.5.4/bin
./elasticsearch

Launch kibana
cd kibana/bin
./kibana

Connect to kibana on port 5601 (http://localhost:5601)

Lauch ElasticPy
python3 ElasticPy.py




