#!/bin/sh

terracotta serve -d _matched.sqlite geotiffs/4_cog/matched \
&& terracotta serve -d geotiffs/4_cog/notmatched \
&& streamlit run _dash
