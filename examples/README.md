### Commands for loading this example
First put in the bm api key and rename the yaml file bm_api.yaml. Make the superuser burner@iburn.com with password burningman for this example.

    python examples/load_bm_json.py
    source env/bin/activate
    cd iburn
    python manage.py flush
    python manage.py loaddata fixtures/*
    python manage.py createsuperuser
    python manage.py runserver
    cd ..
    deactivate
    python examples/send_comment.py
