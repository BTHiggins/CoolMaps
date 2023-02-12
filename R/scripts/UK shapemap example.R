library(tidyverse)

#ggplot has some map data which is pretty handy. The package "maps" needs to be installed to make use of ggplot2::map_data().

# Example of using the data to create a 
italy <- map_data("italy")
ggplot(italy, aes(long, lat, group = group)) +
  geom_polygon(fill = "white", colour = "grey50") +
  coord_quickmap()

# To get the UK map, we can use the world map and select UK as a region. Inspect the dataset for map_data("world")

world_map = map_data("world")
world_map2 = map_data("world2")

regions <- sort(unique(world_map$region))
subregions <- sort(unique(world_map$subregion))

"UK" %in% world_map$region

# Filter by region to get the UK shapemap
# uk_map = world_map %>% filter(region == "UK")
uk_map = map_data(map = "world", region = "UK")

ggplot(uk_map, aes(long, lat, group = group)) +
  geom_polygon(fill = "white", colour = "grey50") +
  coord_quickmap()


# TO DO:
# Get shapemap data for counties/local authorities
# Work out how to fill them differently
# Work out how to isolate London only 

