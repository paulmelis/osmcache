Simple tile caching server for OpenStreetMap tiles.
Allows faster retrieval of OSM tiles for HoloLens
and other applications.

- Stores each retrieved OSM tile PNG image on disk
- Serves tiles in cache directly
- Respects the OSM [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)

PM 2019-03-13

## Usage

$ ./serve.py

Serves tiles on port 12347 under URL /tile/<zoom>/<x>/<y>
(see https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)

## Dependencies

- flask
- gevent
- requests
