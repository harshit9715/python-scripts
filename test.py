import requests
import pandas as pd
import numpy as np
import json


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)


def iterate_all_hosts():

	s = requests.session()

	s.params = {

		'api_key': '##################################',

		'application_key': '########################################',

		'start': 0

	}

	infra_link = 'https://app.datadoghq.com/api/v1/hosts'

	while True:

		response = s.request(method='GET', url=infra_link, params=s.params).json()

		for host in response['host_list']:

				yield host

		if response['total_returned'] == 0:

				return

		s.params['start'] += response['total_returned']


li = []
for host in iterate_all_hosts():
	if len([i for i in host['tags_by_source']['Datadog'] if i.split(':')[0] == 'team']) > 0:
			team = [ i.split(':')[1] for i in host['tags_by_source']['Datadog'] if 'team' in i][0]
			if team != 'pe':
				#   print(host)
					env = [ i.split(':')[1] for i in host['tags_by_source']['Datadog'] if 'environment' in i]
					environment = env[0] if env else None
			else:
					if 'Chef' in host['tags_by_source']:
							environment = [ i.split(':')[1] for i in host['tags_by_source']['Chef'] if 'env' in i][0]
					elif 'Users' in host['tags_by_source']:
							environment = [ i.split(':')[1] for i in host['tags_by_source']['Users'] if 'env' in i][0]
					else:
							environment = None
			
			di = dict([ (k,pd.Series(v)) for k,v in host.items() if k in ['tags_by_source', 'host_name', 'id'] ])
			di['environment'] = environment
			di['team'] = team
			di['tags_by_source'] = np.array((di['tags_by_source']))
			li.append(di)


df = pd.DataFrame.from_records(li)
# df.to_html('temp.html')

print()
print(df[df['team'] == 'ess'])
print()
print(df[df['team'] == 'jose'])
print()
print(df[df['team'] == 'jira'])
print()
print(df[df['team'] == 'pe'])
print()