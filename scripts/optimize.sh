#!/bin/sh

rm _notmatched.sqlite \
&& rm _matched.sqlite \
&& echo Removed _notmached.sqlite and _matched.sqlite \
&& terracotta optimize-rasters --overwrite $TOA/*.tif -o $NOT_MATCHED \
&& terracotta optimize-rasters --overwrite $HISTOGRAM/*.tif -o $MATCHED \
&& exit 0
