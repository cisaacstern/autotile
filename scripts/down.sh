#!/bin/sh

kill $(lsof -t -i:5000)
kill $(lsof -t -i:5001)
