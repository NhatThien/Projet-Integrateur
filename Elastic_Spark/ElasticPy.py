# es_spark_test.py
from tempfile import TemporaryFile
from pyspark import SparkContext, SparkConf
from minio import Minio 
from minio.error import (ResponseError,
                         BucketAlreadyExists)

import json
import numpy as np

if __name__ == "__main__":

	conf = SparkConf().setAppName("ProjetIntegrateur")
	sc = SparkContext(conf=conf)

	path_to_images = "/home/xin/Documents/Projet_integrateur/data/test_RGB_0_10_25.npy"
	path_to_labels = "/home/xin/Documents/Projet_integrateur/data/test_labels_0_10_25.npy"
	bucket_name = 'data'

	def format_data(x):
		return (x['doc_id'], json.dumps(x))


	def write_in_elastic(label,index):
		es_write_conf = {
			# specify the node that we are sending data to (this should be the master)
			"es.nodes" : 'localhost',
			# specify the port in case it is not the default port
			"es.port" : '9200',
			# specify a resource in the form 'index/doc-type'
			"es.resource" : '{}/{}'.format(label,label),#index, label
			# is the input JSON?
			"es.input.json" : "yes",
			# is there a field in the mapping that should be used to specify the ES document ID
			"es.mapping.id": "doc_id" #TODO pareil qe index ? 
		}

		data = [
			{'bucket': bucket_name, 'doc_id': index}
		]

		rdd = sc.parallelize(data)

		rdd = rdd.map(lambda x: format_data(x))

		rdd.saveAsNewAPIHadoopFile(
			path='-',
			outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
			keyClass="org.apache.hadoop.io.NullWritable",
			valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",

			# critically, we must specify our `es_write_conf`
			conf=es_write_conf
		)

	outfile = TemporaryFile()

	client1 = Minio("172.18.0.5:9000",access_key="minio",secret_key="minio123",secure=False) 
	client2 = Minio("172.18.0.4:9000",access_key="minio",secret_key="minio123",secure=False) 
	client3 = Minio("172.18.0.3:9000",access_key="minio",secret_key="minio123",secure=False) 
	client4 = Minio("172.18.0.2:9000",access_key="minio",secret_key="minio123",secure=False) 

	data = np.load(path_to_images)
	label = np.load(path_to_labels)

	print("\ndata chargee\n")

	try:
		client1.make_bucket(bucket_name)
	except BucketAlreadyExists as err:
		   pass
	except ResponseError as err:
		   raise
	print("\nbucket cree\n")

	nb_image = data.shape[0]

	print ("\nl'imporation des donnees commence\n")
	for i in range (0,nb_image):
		np.save(str(i),data[i])
		file_name = '{}.npy'.format(i)

		if (i <= nb_image/4):
			try:
				client1.fput_object(bucket_name, str(i), file_name)
			except ResponseError as err:
				   raise
		elif (i <= nb_image/2):
			try:
				client2.fput_object(bucket_name, str(i), file_name)
			except ResponseError as err:
				   raise
		elif (i <= nb_image*0,75):
			try:
				client3.fput_object(bucket_name, str(i), file_name)
			except ResponseError as err:
				   raise
		else:
			try:
				client4.fput_object(bucket_name, str(i), file_name)
			except ResponseError as err:
				   raise

		if (np.array_equal(label[i], [1,0,0,0,0])):
			write_in_elastic("forest",i)
		elif (np.array_equal(label[i], [0,1,0,0,0])):
			write_in_elastic("sea",i)
		elif (np.array_equal(label[i], [0,0,1,0,0])):
			write_in_elastic("city",i)
		elif (np.array_equal(label[i], [0,0,0,1,0])):
			write_in_elastic("mountain",i)
		elif (np.array_equal(label[i], [0,0,0,0,1])):
			write_in_elastic("plan",i)

	print("\nDONE\n")
