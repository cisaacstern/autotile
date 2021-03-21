#!/bin/sh

rm -r geotiffs \
&& echo removed geotiffs directory \
&& mkdir geotiffs \
&& mkdir geotiffs/0_raw \
&& mkdir geotiffs/1_toa \
&& mkdir geotiffs/2_hst \
&& mkdir geotiffs/3_cog \
&& mkdir geotiffs/3_cog/matched \
&& mkdir geotiffs/3_cog/notmatched \
&& echo created new geotiffs directory with subdirectories
