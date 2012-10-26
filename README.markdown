bokbok
======

An experimental graphite-web alternative.

Prerequisites
=============

* redis for caching metric names and configs for ephemeral graph links
* An S3 bucket for storage for persistent graph images

Running
=======

1. pip install -r requirements.txt
2. Set up local_settings.py (see below)
3. ./store_metrics.py
4. env FLASK_DEBUG=true ./manage.py runserver

Your local_settings.py
======================

    CARBON_SHARDS = ["localhost"]         # Typically you'll just list your Graphite server unless you have a cluster of carbon-caches. Then list them all here as hostname:port pairs.
    GRAPHITE_HOST = "localhost"           # This should be obvious.
    AWS_ACCESS_KEY_ID = "CHANGE_THIS"     # Your S3 access key
    AWS_SECRET_ACCESS_KEY = "CHANGE_THIS" # Your S3 secret key
    AWS_BUCKET_NAME = "your-bucket-name"  # S3 bucket name
    
    # Don't change the dimensions but feel free to add other graphite rendering options such as colors, etc. Most can be set in the web interface, though.
    GRAPHITE_OPTIONS = {
      "width": 1170,
      "height": 500
    }
