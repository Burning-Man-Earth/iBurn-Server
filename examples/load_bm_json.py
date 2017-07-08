import json 
import requests
import yaml
from requests.auth import HTTPBasicAuth

with open('bm_api.yaml') as f:
    bm_api = yaml.safe_load(f)['bm_api']
#Getting Burning Man Data

def get_burning_man_api(cat,year):
    r = requests.get('http://api.burningman.org/api/v1/{}?year={}'.format(cat,year), 
                     auth=HTTPBasicAuth(bm_api, ''))
    return r.json()


def transform_data_for_fixture(bm_results):
    output_list = []
    for event in bm_results:
        output_dict = {}
        output_dict['pk']=event['event_id']
        output_dict['model']='blog.post'
        fields_dict = {}
        fields_dict['body']=event['description']
        #fields_dict['year']=event['year']
        fields_dict['title']=event['title']
        fields_dict['slug']=event['slug']
        #fields_dict['uid']=event['uid']
        output_dict['fields']=fields_dict
        output_list.append(output_dict)
    return output_list

def main():
    cat = 'event'
    year = 2016
    dir_to_fixtures_folder = '../iburn/fixtures'
    bm_results = get_burning_man_api(cat,year)
    output_list = transform_data_for_fixture(bm_results)
    with open(dir_to_fixtures_folder+'/2016_events.json','wb') as f:
        json.dump(output_list,f,indent=4)

if __name__ == '__main__':
    main()
