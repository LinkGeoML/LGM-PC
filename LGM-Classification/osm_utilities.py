import pandas as pd
import os
import re
import json
from shapely.geometry import LineString, Polygon

from config import config


def query_osm_data(query, fpath):
    url = f'https://www.overpass-api.de/api/interpreter?data={query}'
    os.system(f'wget -O {fpath} "{url}"')
    return


def parse_osm_streets(fpath):
    # Helper function
    def convert_to_wkt_geometry(row):
        lons = [p['lon'] for p in row['geometry']]
        lats = [p['lat'] for p in row['geometry']]
        return LineString(list(zip(lons, lats)))

    with open(fpath) as f:
        streets = json.load(f)['elements']

    data = [(street['id'], street['geometry']) for street in streets]
    cols = ['id', 'geometry']
    street_df = pd.DataFrame(data=data, columns=cols)
    street_df['geometry'] = street_df.apply(convert_to_wkt_geometry, axis=1)
    return street_df


def download_osm_streets(exp_path):
    bb_coords = config.osm_bbox
    fpath = exp_path + '/osm_streets.json'
    query = (
        '[out:json]'
        f'[bbox:{bb_coords[0]},{bb_coords[1]},{bb_coords[2]},{bb_coords[3]}];'
        'way["highway"];'
        'out geom;')
    query_osm_data(query, fpath)
    street_df = parse_osm_streets(fpath)
    fpath = exp_path + '/osm_streets.csv'
    street_df.to_csv(f'{fpath}', columns=['id', 'geometry'], index=False)
    return


def parse_osm_polys(fpath):
    # Helper function
    def extract_name_tags(row):
        names = [tag[1] for tag in row['tags'] if re.search('name', tag[0])]
        return names

    # Helper function
    def convert_to_wkt_geometry(row):
        lons = [p['lon'] for p in row['geometry']]
        lats = [p['lat'] for p in row['geometry']]
        return Polygon(list(zip(lons, lats)))

    with open(fpath) as f:
        polys = json.load(f)['elements']

    data = []
    for poly in polys:
        if 'tags' in poly:
            poly_tags = [(k, v) for k, v in poly['tags'].items()]
            data.append((poly['id'], poly_tags, poly['geometry']))

    cols = ['id', 'tags', 'geometry']
    poly_df = pd.DataFrame(data=data, columns=cols)
    poly_df['name'] = poly_df.apply(extract_name_tags, axis=1)
    poly_df['geometry'] = poly_df.apply(convert_to_wkt_geometry, axis=1)
    return poly_df


def download_osm_polygons(exp_path):
    bb_coords = config.osm_bbox
    fpath = exp_path + '/osm_polys.json'
    query = (
        '[out:json]'
        f'[bbox:{bb_coords[0]},{bb_coords[1]},{bb_coords[2]},{bb_coords[3]}];'
        'way(if:is_closed());'
        'out geom;')
    query_osm_data(query, fpath)
    poly_df = parse_osm_polys(fpath)
    fpath = exp_path + '/osm_polys.csv'
    cols = ['id', 'name', 'tags', 'geometry']
    poly_df.to_csv(f'{fpath}', columns=cols, index=False)
    return
