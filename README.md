# OSMCache

Simple tile caching server for OpenStreetMap tiles.

- Stores each retrieved OSM tile PNG image on disk
- Serves tiles from cache, if available
- Respects the OSM [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)

A local cache can be faster in providing often-used tiles, especially
when doing development cycles that retrieve the same tiles repeatedly.

## Usage

```python
$ ./serve.py [port]
```

Serves tiles (by default on port 8888) under URL `/tile/<zoom>/<x>/<y>`.
See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames for meaning
of `zoom`, `x` and `y` parameters.

## Dependencies

- flask
- gevent
- requests
