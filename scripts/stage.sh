#!/bin/sh

rio-hist match $TOA -o $HISTOGRAM \
&& terracotta optimize $TOA -o  $NOT_MATCHED \
&& terracotta optimize $HISTOGRAM -o $MATCHED \
&& terracotta ingest $MATCHED _matched.sqlite \
&& terracotta ingest $NOT_MATCHED _notmatched.sqlite