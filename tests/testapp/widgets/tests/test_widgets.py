import json

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import reload_module
from django.contrib.gis.geos import Point
from mapwidgets import widgets as mw_widgets

from mapwidgets import GooglePointFieldWidget


GOOGLE_MAP_API_KEY = "AIzaSyC6BeCYCBSWDdC3snYRFKWw18bd9MA-uu4"


class GooglePointWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test the widget with default map options in the django project settings file
        """
        zoom = 15
        default_map_center = [51.5073509, -0.12775829999]
        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", default_map_center),
            )
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = GooglePointFieldWidget()
            self.assertEqual(hasattr(widget, "settings"), True)
            self.assertEqual(hasattr(widget, "settings_namespace"), True)

            # test `map_options` method
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), zoom)
            self.assertEqual(options.get("mapCenterLocation"), default_map_center)

            # test render
            point = Point(-104.9903, 39.7392)
            widget_html_elem_id = "id_location"
            result = widget.render(name="location", value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            self.assertIn(widget_html_elem_id, result)
