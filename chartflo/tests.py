from django.test import TestCase
from .views import ChartsView

# Create your tests here.
class TestVegaLiteChartsView(TestCase):
    def setUpTestCase(self):
        # Create new ChartsView instance
        self.chart_view = ChartsView()

        # Set Vega Lite as template engine
        self.chart_view.engine = "vegalite"

    def test_vega_lite_template(self):
        # URL for Vega Lite chart URL
        vega_lite_template_url = "chartflo/vegalite/chart.html"

        # Get chart view template URL
        chart_view_template_url = self.chart_view._get_template_url()

        # Make sure Chart View URL matches Vega Lite chart URL
        self.assertEqual(chart_view_template_url, vega_lite_template_url)
