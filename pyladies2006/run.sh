#!/bin/bash

gunicorn app:app -w 1 -b 0.0.0.0:5000
