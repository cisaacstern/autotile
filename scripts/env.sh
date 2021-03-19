#!/bin/bash

alias autotile='python autotile.py' \
&& export TOA=geotiffs/1_toa \
&& export HISTOGRAM=geotiffs/2_hst \
&& export MATCHED=geotiffs/3_cog/matched \
&& export NOT_MATCHED=geotiffs/3_cog/notmatched
