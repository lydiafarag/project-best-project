#!/bin/bash
curl --request POST http://localhost:8000/api/timeline_post -d 'name=randompost&email=random@random.com&content=Making a random post for testing purposes'
curl --request GET http://localhost:8000/api/timeline_post | jq --raw-output '.timeline_posts | .[] |"\(.content)\(.email)\(.name)"'

