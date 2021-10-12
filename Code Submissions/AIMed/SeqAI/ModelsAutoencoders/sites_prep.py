import pandas as pd


def create_dict():
    data=pd.read_csv('SeqAI/data/sites_of_restriction.csv')
    sites=data['sites'].to_list()
    names=data['name'].to_list()
    names=[i.lower() for i in names]

    site_dict=dict(zip(names, sites))
    print(site_dict)
    return site_dict