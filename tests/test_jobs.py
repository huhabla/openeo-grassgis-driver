# -*- coding: utf-8 -*-
import unittest
import time
import pprint
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase
from graas_openeo_core_wrapper import config

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


use_case_1_graph = {
    "process_graph": {
        "process_id": "min_time",
        "args": {
            "collections": [{
                "process_id": "NDVI",
                "args": {
                    "collections": [{
                        "process_id": "filter_daterange",
                        "args": {
                            "collections": [{
                                "process_id": "filter_bbox",
                                "args": {
                                    "collections": [{
                                        "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }],
                                    "left": -5.0,
                                    "right": -4.98,
                                    "top": 39.12,
                                    "bottom": 39.1,
                                    "ewres": 0.1,
                                    "nsres": 0.1,
                                    "srs": "EPSG:4326"
                                }
                            }],
                            "from": "2017-04-12 11:17:08",
                            "to": "2017-09-04 11:18:26"
                        }
                    },
                        {
                            "process_id": "filter_daterange",
                            "args": {
                                "collections": [{
                                    "process_id": "filter_bbox",
                                    "args": {
                                        "collections": [{
                                            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                        }],
                                        "left": -5.0,
                                        "right": -4.98,
                                        "top": 39.12,
                                        "bottom": 39.1,
                                        "ewres": 0.1,
                                        "nsres": 0.1,
                                        "srs": "EPSG:4326"
                                    }
                                }],
                                "from": "2017-04-12 11:17:08",
                                "to": "2017-09-04 11:18:26"
                            }
                        }],
                    "red": "S2A_B04",
                    "nir": "S2A_B08"
                }
            }]
        }
    }
}

use_case_1_graph_export = {
    "process_graph": {
        "process_id": "raster_exporter",
        "args": {
            "collections": [{
                "process_id": "min_time",
                "args": {
                    "collections": [{
                        "process_id": "NDVI",
                        "args": {
                            "collections": [{
                                "process_id": "filter_daterange",
                                "args": {
                                    "collections": [{
                                        "process_id": "filter_bbox",
                                        "args": {
                                            "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"},
                                                            {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"}],
                                            "left": -5.0,
                                            "right": -4.98,
                                            "top": 39.12,
                                            "bottom": 39.1,
                                            "ewres": 0.1,
                                            "nsres": 0.1,
                                            "srs": "EPSG:4326"
                                        }
                                    }],
                                    "from": "2017-04-12 11:17:08",
                                    "to": "2017-09-04 11:18:26"
                                }
                            }],
                            "red": "S2A_B04",
                            "nir": "S2A_B08"
                        }
                    }]
                }
            }]
        }
    }
}

use_case_2_graph = {
    "process_graph": {
        "process_id": "udf_reduce_time",
        "args": {
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [
                                {"product_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"},
                                {"product_id": "ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm"}],
                            "left": -5.0,
                            "right": -4.7,
                            "top": 39.3,
                            "bottom": 39.0,
                            "ewres": 0.1,
                            "nsres": 0.1,
                            "srs": "EPSG:4326"
                        }
                    }],
                    "from": "1980-01-01 00:00:00",
                    "to": "2010-01-01 00:00:00"
                }
            }],
            "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
        }
    }
}

use_case_2_graph_export = {
    "process_graph": {
        "process_id": "raster_exporter",
        "args": {
            "collections": [{
                "process_id": "udf_reduce_time",
                "args": {
                    "collections": [{
                        "process_id": "filter_daterange",
                        "args": {
                            "collections": [{
                                "process_id": "filter_bbox",
                                "args": {
                                    "collections": [
                                        {
                                            "product_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"},
                                        {"product_id": "ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm"}],
                                    "left": -5.0,
                                    "right": -4.7,
                                    "top": 39.3,
                                    "bottom": 39.0,
                                    "ewres": 0.1,
                                    "nsres": 0.1,
                                    "srs": "EPSG:4326"
                                }
                            }],
                            "from": "1980-01-01 00:00:00",
                            "to": "2010-01-01 00:00:00"
                        }
                    }],
                    "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
                }
            }]
        }
    }
}


use_case_3_graph = {
    "process_graph": {
        "process_id": "zonal_statistics",
        "args": {
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [
                                {"product_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"},
                                {"product_id": "ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm"}],
                            "left": -5.0,
                            "right": -4.7,
                            "top": 39.3,
                            "bottom": 39.0,
                            "ewres": 0.1,
                            "nsres": 0.1,
                            "srs": "EPSG:4326"
                        }
                    }],
                    "from": "1980-01-01 00:00:00",
                    "to": "2010-01-01 00:00:00"
                }
            }],
            "regions": "https://storage.googleapis.com/graas-geodata/rio.json"
        }
    }
}


date_range_filter = {
    "process_graph": {
        "process_id": "filter_daterange",
        "args": {
            "collections": [{
                "process_id": "filter_bbox",
                "args": {
                    "collections": [{
                        "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                    }],
                    "left": -5.0,
                    "right": -4.98,
                    "top": 39.12,
                    "bottom": 39.1,
                    "ewres": 0.1,
                    "nsres": 0.1,
                    "srs": "EPSG:4326"
                }
            }],
            "from": "2017-06-21 11:12:22",
            "to": "2017-08-20 11:12:21"
        }
    }
}

date_range_filter_long_run = {
    "process_graph": {
        "process_id": "filter_daterange",
        "args": {
            "collections": [{
                "process_id": "filter_bbox",
                "args": {
                    "collections": [{
                        "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                    }],
                    "left": -5.5,
                    "right": -4.5,
                    "top": 39.5,
                    "bottom": 38.5,
                    "ewres": 0.0001,
                    "nsres": 0.0001,
                    "srs": "EPSG:4326"
                }
            }],
            "from": "2017-06-21 11:12:22",
            "to": "2017-08-20 11:12:21"
        }
    }
}

date_range_filter_error_no_strds = {
    "process_graph": {
        "process_id": "filter_daterange",
        "args": {
            "collections": [{
                "process_id": "filter_bbox",
                "args": {
                    "collections": [{
                        "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04_nope"
                    }],
                    "left": -5.0,
                    "right": -4.99,
                    "top": 39.0,
                    "bottom": 38.99,
                    "ewres": 0.1,
                    "nsres": 0.1,
                    "srs": "EPSG:4326"
                }
            }],
            "from": "2017-06-21 11:12:22",
            "to": "2017-08-20 11:12:21"
        }
    }
}


class JobsTestCase(TestBase):

    def test_1_post_use_case_1_job_ephemeral(self):
        """Run the test in the ephemeral database
        """
        response = self.app.post('/jobs', data=json.dumps(use_case_1_graph), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_1_put_use_case_1_job_persistent(self):
        """Run the test in the persistent database
        """
        response = self.app.put('/jobs', data=json.dumps(use_case_1_graph), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_1_post_use_case_1_job_ephemeral_export(self):
        """Run the test in the ephemeral database with export support
        """
        response = self.app.post('/jobs', data=json.dumps(use_case_1_graph_export), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_2_post_use_case_2_job(self):
        response = self.app.post('/jobs', data=json.dumps(use_case_2_graph), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_2_post_use_case_2_job_export(self):
        response = self.app.post('/jobs', data=json.dumps(use_case_2_graph_export), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_3_post_use_case_3_job(self):
        response = self.app.post('/jobs', data=json.dumps(use_case_3_graph), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_3_post_data_range_filter_job(self):
        response = self.app.post('/jobs', data=json.dumps(date_range_filter), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def test_4_post_use_case_1_job_delete(self):
        response = self.app.post('/jobs', data=json.dumps(date_range_filter_long_run), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(response.status_code, 200)
        response = self.app.delete('/jobs/%s' % data["job_id"])
        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response=response, status="terminated")

    def test_4_error_no_strds(self):
        response = self.app.post('/jobs', data=json.dumps(date_range_filter_error_no_strds),
                                 content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response=response, status="error", http_status=400)

    def wait_until_finished(self, response, http_status=200, status="finished"):
        """Poll the status of a resource and assert its finished HTTP status

        The response will be checked if the resource was accepted. Hence it must always be HTTP 200 status.

        The status URL from the response is then polled until status: finished, error or terminated.
        The result of the poll can be checked against its HTTP status and its GRaaS status message.

        Args:
            response: The accept response
            http_status (int): The HTTP status that should be checked
            status (str): The return status of the response

        Returns: response

        """
        # Check if the resource was accepted
        self.assertEqual(response.status_code, 200, "HTML status code is wrong %i" % response.status_code)
        self.assertEqual(response.mimetype, "application/json", "Wrong mimetype %s" % response.mimetype)

        resp_data = json.loads(response.data.decode())

        while True:
            print("waiting for finished job")
            response = self.app.get('/jobs/%s' % resp_data["job_id"])
            resp_data = json.loads(response.data.decode())
            print(response)
            print(resp_data)

            if "status" not in resp_data:
                raise Exception("wrong return values %s" % str(resp_data))
            if resp_data["status"] == "finished" or \
                    resp_data["status"] == "error" or \
                    resp_data["status"] == "terminated":
                break
            time.sleep(0.2)

        self.assertEquals(resp_data["status"], status)
        self.assertEqual(response.status_code, http_status, "HTML status code is wrong %i" % response.status_code)

        time.sleep(0.4)
        pprint.pprint(resp_data)
        return resp_data


if __name__ == "__main__":
    unittest.main()
