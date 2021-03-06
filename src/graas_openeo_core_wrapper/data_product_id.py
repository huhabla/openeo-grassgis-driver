# -*- coding: utf-8 -*-
from openeo_core.data_product_id import DataProductId, GET_DATA_PRODUCT_ID_DOC
from openeo_core.definitions import SpatialExtent, DateTime, BandDescription
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


strds_example = {
    "aggregation_type": "None",
    "bottom": "0.0",
    "creation_time": "2016-08-11 16:44:29.756411",
    "creator": "soeren",
    "east": "75.5",
    "end_time": "2013-07-01 00:00:00",
    "ewres_max": "0.25",
    "ewres_min": "0.25",
    "granularity": "1 month",
    "id": "precipitation_1950_2013_monthly_mm@PERMANENT",
    "map_time": "interval",
    "mapset": "PERMANENT",
    "max_max": "1076.9",
    "max_min": "168.9",
    "min_max": "3.2",
    "min_min": "0.0",
    "modification_time": "2016-08-11 16:45:14.032432",
    "name": "precipitation_1950_2013_monthly_mm",
    "north": "75.5",
    "nsres_max": "0.25",
    "nsres_min": "0.25",
    "number_of_maps": "762",
    "raster_register": "raster_map_register_934719ed2b4841818386a6f9c5f11b09",
    "semantic_type": "mean",
    "south": "25.25",
    "start_time": "1950-01-01 00:00:00",
    "temporal_type": "absolute",
    "top": "0.0",
    "west": "-40.5"
}


raster_example = {
    "cells": "2025000",
    "cols": "1500",
    "comments": "\"r.proj input=\"ned03arcsec\" location=\"northcarolina_latlong\" mapset=\"\\helena\" output=\"elev_ned10m\" method=\"cubic\" resolution=10\"",
    "creator": "\"helena\"",
    "database": "/tmp/gisdbase_75bc0828",
    "datatype": "FCELL",
    "date": "\"Tue Nov  7 01:09:51 2006\"",
    "description": "\"generated by r.proj\"",
    "east": "645000",
    "ewres": "10",
    "location": "nc_spm_08",
    "map": "elevation",
    "mapset": "PERMANENT",
    "max": "156.3299",
    "min": "55.57879",
    "ncats": "255",
    "north": "228500",
    "nsres": "10",
    "rows": "1350",
    "source1": "\"\"",
    "source2": "\"\"",
    "south": "215000",
    "timestamp": "\"none\"",
    "title": "\"South-West Wake county: Elevation NED 10m\"",
    "units": "\"none\"",
    "vdatum": "\"none\"",
    "west": "630000"
}

class GRaaSDataProductId(DataProductId):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_DATA_PRODUCT_ID_DOC)
    def get(self, product_id):

        # List strds maps from the GRASS location

        location, mapset, datatype, layer = self.iface.layer_def_to_components(product_id)

        status_code, layer_data = self.iface.layer_info(layer_name=product_id)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching GRASS GIS layer information "
                                                         "for layer <%s>!\n Error: %s"
                                                         ""%(product_id, str(layer_data))}, 400))

        # Get the projection from the GRASS mapset
        status_code, mapset_info = self.iface.mapset_info(location=location, mapset=mapset)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching mapset info "
                                                         "for mapset <%s>!"%mapset}, 400))

        description = "Raster dataset"
        if datatype.lower() == "strds":
            description = "Space time raster dataset"
        if datatype.lower() == "vector":
            description = "Vector dataset"

        source = "GRASS GIS location/mapset path: /%s/%s" % (location, mapset)
        srs = mapset_info["projection"]
        extent = SpatialExtent(left=float(layer_data["west"]),
                               right=float(layer_data["east"]),
                               top=float(layer_data["north"]),
                               bottom=float(layer_data["south"]),
                               srs=srs)

        print(layer_data)

        if datatype.lower() == "strds":
            time = DateTime()
            time["from"] = layer_data["start_time"]
            time["to"] = layer_data["end_time"]

            bands = BandDescription(band_id=product_id)

            info = dict(product_id=product_id,
                        extent=extent,
                        source=source,
                        description=description,
                        time=time,
                        bands=bands,
                        temporal_type=layer_data["start_time"],
                        number_of_maps=layer_data["number_of_maps"],
                        min_min=layer_data["min_min"],
                        min_max=layer_data["min_max"],
                        max_min=layer_data["max_min"],
                        max_max=layer_data["max_max"],
                        ewres_max=layer_data["ewres_max"],
                        ewres_min=layer_data["ewres_min"],
                        nsres_max=layer_data["nsres_max"],
                        nsres_min=layer_data["nsres_min"],
                        map_time=layer_data["map_time"],
                        granularity=layer_data["granularity"],
                        aggregation_type=layer_data["aggregation_type"],
                        creation_time=layer_data["creation_time"],
                        modification_time=layer_data["modification_time"],
                        mapset=mapset,
                        location=location)
        else:
            info = dict(product_id=product_id,
                        extent=extent,
                        source=source,
                        description=description,
                        mapset=mapset,
                        location=location,
                        title=layer_data["title"],
                        comments=layer_data["comments"],
                        datatype=layer_data["datatype"],
                        cells=layer_data["cells"],
                        cols=layer_data["cols"],
                        rows=layer_data["rows"],
                        ewres=layer_data["ewres"],
                        nsres=layer_data["nsres"],)

        return make_response(jsonify(info), 200)
