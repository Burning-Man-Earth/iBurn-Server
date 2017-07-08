### Commands for loading this example
First put in the bm api key and rename the yaml file bm_api.yaml

    python examples/load_bm_json.py
    python iburn/manage.py flush
    python iburn/manage.py loaddata fixtures/*
    python iburn/manage.py createsuperuser
    python iburn/manage.py runserver
    python examples/send_comment.py
