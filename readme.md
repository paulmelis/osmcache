Simple tile caching server for OpenStreetMap tiles.

- Stores each retrieved OSM tile PNG image on disk
- Serves tiles from cache, if available
- Respects the OSM [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)

## Usage

```python
$ ./serve.py
```

Serves tiles on port 12347 under URL `/tile/<zoom>/<x>/<y>`
(see https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)

## Dependencies

- flask
- gevent
- requests
