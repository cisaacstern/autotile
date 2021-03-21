#!/bin/sh

rm _notmatched.sqlite \
&& echo Removed _notmached.sqlite \
&& terracotta optimize-rasters --overwrite $TOA/*.tif -o $NOT_MATCHED 
