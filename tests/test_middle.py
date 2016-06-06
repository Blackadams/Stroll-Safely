from copy import deepcopy
import unittest
from middle import generate_waypoint
from nose.tools import eq_


class TestMiddle(unittest.TestCase):
    def test_generate_waypoint(self):
        lowest_crime_index = 0.5
        points_data = [{'crime_index': 0.5,
                        'total_crimes': 115,
                        'geohash': 'hfugpsb',
                        'point': (40.8, -73.96)
                        }]
        segmented_points = [{'data':
                            {'start':
                                {'lat': 40.8, 'lng': -73.96},
                                'end': {'lat': 40.8131494, 'lng': -73.95032520000001},
                                'waypoints': []}},
                            {'is_high_crime': False,
                                'lat': 40.8,
                                'geohash': u'hfv528h',
                                'crime_index': 0.5,
                                'lng': -73.96,
                                'total_crimes': 45}]

        original = deepcopy(segmented_points)

        generate_waypoint(lowest_crime_index, points_data, segmented_points)

        expected = [{'data':
                            {'start':
                                {'lat': 40.8, 'lng': -73.96},
                                'end': {'lat': 40.8131494, 'lng': -73.95032520000001},
                                'waypoints': []}},
                            {'is_high_crime': False,
                                'lat': 40.8,
                                'geohash': u'hfv528h',
                                'crime_index': 0.5,
                                'lng': -73.96,
                                'total_crimes': 45}]

        assert segmented_points != original
        eq_(segmented_points, expected)