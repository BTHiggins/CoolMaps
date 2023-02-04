# install sf package to unpack geo package files (filename.gpkg)
# tigris contains us states geo data for mapping
# rayshader is a 3d visualisation package
library(tidyverse)
library(sf)
library(tigris)
library(rayshader)

# load the map data ----
data <- st_read("data/kontur_population_US_20220630.gpkg")

# Get US states polygon data from the tigris package with "states()"
us_states <- states()

# We want to "intersect" the florida data with the total us data to make sure we're filtering the whole us data down to florida. To do this we need to make sure the CRSs are the same. CRS = coordinate reference system, different datasets will have varying CRSs. We can state this in the florida definition. We can compare the CRSs of datasets by uising st_crs(florida) and st_crs(data).

# filter all the states data to just florida, transform the CRS to match the CRS from the population dataset
florida <- us_states %>%
  filter(NAME == "Florida") %>%
  st_transform(crs = st_crs(data))

# basic plot using geom_sf() to check the geo looks correct
map <- florida %>%
  ggplot() +
  geom_sf()

# Filter the population data to florida by intersecting them. I.e. filtering the main dataset to only where florida overlaps it.
st_florida <- st_intersection(data, florida)

# Define aspect ratio based on the x-axis and y-axis bounds of the earlier florida plot
bb <- st_bbox(st_florida)

# We now have to convert the x and y bounds from numbers back to point coordinates as coordinates are the units on our chart.We'll start by getting the corners to get the width and height.
bb_bottom_left <- st_point(c(bb$xmin, bb$ymin)) %>%
  st_sfc(crs = st_crs(data))

bb_bottom_right <- st_point(c(bb$xmax, bb$ymin)) %>%
  st_sfc(crs = st_crs(data))

bb_top_left <- st_point(c(bb$xmin, bb$ymax)) %>%
  st_sfc(crs = st_crs(data))
  
# We can visually check what we have so far by plotting on the map
map + 
  geom_sf(data=bb_bottom_left, colour="red") +
  geom_sf(data=bb_bottom_right, colour="blue") +
  geom_sf(data=bb_top_left, colour = "purple")

# The distance calculation knows the units are in metres be cause it is defined within the CRS
bb_width <- st_distance(bb_bottom_left, bottom_right)
bb_height <- st_distance(bb_bottom_left, top_left)

# We now need to work out the height and width ratios.
if (bb_width > bb_height) {
  w_ratio <- 1
  h_ratio <- height / width
} else {
  w_ratio <- width / height
  h_ratio <- 1
}

