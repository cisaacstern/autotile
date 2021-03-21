#!/bin/sh

terracotta serve -d _notmatched.sqlite \
& sleep 2 \
&& streamlit run _rendered_view.py
