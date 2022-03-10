#!/bin/bash

TOKEN=$1
CLIENT_ID=my-client
CLIENT_SECRETE=secret

http --form :5000/oauth/token/introspection token=$TOKEN -a $CLIENT_ID:$CLIENT_SECRETE -v