#!/bin/bash

docker run --rm -v $(pwd)/data:/app/data --env-file .env crm_etl_pipeline
