#!/bin/bash

TOKEN=$1

http :5000/api/me 'Authorization:Bearer '$TOKEN -v