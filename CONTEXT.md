# Problem

This project began when I encountered difficulty in interactively exploring full-resolution GeoTIFFs. In working with LiDAR pointcloud data over the last year (see https://cstern.io/projects/albedo), I'd become accustomed to using [Panel](http://panel.holoviz.org) for interactive data visualization. I find that exploring the data in this way imparts a uniquely valuable intuitive grasp over its characteristics.

The LiDAR pointclouds (and resulting interpolations) I've historically worked with are generally NumPy `ndarray`s comprised of fewer than 50,000 points. In-memory arrays of this size are handled easily and quickly by Panel and Matplotlib on my laptop.

When I began to get curious about Landsat8 GeoTIFFs, however, I quickly found that these arrays were too large for my prior techniques. I needed a new approach.

# Techniques

Researching visualization methods brought me to the [Terracotta](https://github.com/DHI-GRAS/terracotta) tileserver, which attracted me for its basis in Rasterio and Flask, two libraries I was already familiar with and enjoy using. While this was a major breakthrough in my understanding of the processes and infrastructure required to serve COG tiles, I found myself wanting a few more bells-and-whistles; specifically:

1. A reproducible and robust way to request raw GeoTiffs for a specific geographic location.
2. A method to programmatically and/or interactively adjust the color-balance of these images using arbitrary Python methods.
3. A minimalist and aesthetically-pleasing way to view the served tiles.

Working one-by-one, I determined that [this Dask + Rasterio tutorial](https://examples.dask.org/applications/satellite-imagery-geotiff.html) provided helpful methods for implementing #1; that Panel's parameterized class would provide a useful solution for #2; and finally, that Streamlit's Folium extension was an ideal and simple way to solve #3.

While all of these services could be run independently, bringing them all together "under one CLI roof" made immediate intuitive sense to me. I'm a big believer in keeping it simple during the prototyping phase of any engineering effort. As such, a reached for `sys.argv` to implement this CLI. This approach is not necessarily the most user-friendly for outside users (for that, something like Click would be much better). But at the very beginning of the development process, it offers a "no fuss" way to get a proof-of-concept running.

The actual execution of the steps in this pipeline ended up being a mix of calls to Python methods, shell commands executed by static `.sh` scripts, and perhaps most exotic of all, shell commands run by Python methods (to simplify variable subsitution). This diversity of execution styles is reflective of the range of tasks which needed to be accomplished to bring this Frankenstein to life.

# Takeaways

This project opened so many new avenues of learning and curiosity for me. Already it is clear that the biggest bottleneck in this pipeline is the optimization of the GeoTIFFs into COGs, and the ingestion of the COGs into the sqlite databases. Currently these processes are dispatched to Terracotta. I'm keen to study the internal workings of these processes as a basis for optimizing them, either by adjusting my use of Terracotta somehow, or swapping it out for another COG conversion engine.