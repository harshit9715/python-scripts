from __future__ import print_function
import boto3, pymysql
import os, sys, logging, uuid, csv

from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

# Use environment variables for loading configurations
# https://pypi.org/project/python-dotenv/


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def connect_to_rds(rds_host, db_name, name, password):
	try:
		conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
		logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
		return conn
	except Exception as e:
		logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
		logger.error(e)
		sys.exit()


def data_to_rds(csv_data, conn):
	with conn.cursor() as cur:
		for idx, row in enumerate(csv_data):

			logger.info(row)
			try:
				cur.execute('INSERT INTO target_table(column1, column2, column3)' \
								'VALUES("%s", "%s", "%s")'
								, row)
			except Exception as e:
				logger.error(e)

			if idx % 100 == 0:
				conn.commit()

		conn.commit()

	logger.info('File loaded into RDS:' + str(download_path))


if __name__ == "__main__":

	# RDS CONFIG 
	rds_host  = os.getenv("rds_host")
	name = os.getenv("db_username")
	password = os.getenv("db_password")
	db_name = os.getenv("db_name")

	# S3 CONFIG
	bucket = os.getenv("bucket_name")
	key = os.getenv("key")

	# Create DB connection
	conn = connect_to_rds(rds_host, db_name, name, password)

	# temporary storage refrence
	download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)


	s3_client = boto3.client('s3')
	s3_client.download_file(bucket, key, download_path)

	csv_data = csv.reader(file(download_path))

	data_to_rds(csv_data, conn)


