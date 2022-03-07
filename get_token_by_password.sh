#!/bin/bash

USERNAME=green_pea88@likelion.net
PASSWORD=1234
CLIENT_ID=my-client
CLIENT_SECRET=secret

http --form :5000/oauth/token username=$USERNAME password=$PASSWORD grant_type=password scope="openid profile" -a $CLIENT_ID:$CLIENT_SECRET -v
