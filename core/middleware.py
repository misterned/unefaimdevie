"""
Middleware pour mesurer le temps de réponse des fichiers médias (images/vidéos)
et envoyer la métrique à Application Insights via OpenCensus.
"""
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

try:
    from opencensus.ext.azure.metrics_exporter import new_metrics_exporter
    from opencensus.metrics.transport import get_exporter_thread
    from opencensus.metrics import label_key, label_value, metric, metric_utils
    from opencensus.stats import aggregation as aggregation_module
    from opencensus.stats import measure as measure_module
    from opencensus.stats import stats as stats_module
    from opencensus.stats import view as view_module
    from opencensus.tags import tag_map as tag_map_module
except ImportError:
    new_metrics_exporter = None


class MediaTimingMiddleware(MiddlewareMixin):
    """
    Middleware qui mesure le temps de réponse des requêtes médias (images/vidéos)
    et envoie la métrique à Application Insights si configuré.
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enabled = bool(getattr(settings, "APPLICATIONINSIGHTS_CONNECTION_STRING", None)) and new_metrics_exporter
        if self.enabled:
            self.exporter = new_metrics_exporter(connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING)
            self.stats = stats_module.stats
            self.view_manager = self.stats.view_manager
            self.stats_recorder = self.stats.stats_recorder
            self.measure = measure_module.MeasureFloat(
                "media_response_time_ms",
                "Temps de réponse des médias (ms)",
                "ms"
            )
            self.view = view_module.View(
                "media_response_time_view",
                "Temps de réponse des médias (ms)",
                [label_key.LabelKey("path", "Chemin du média")],
                self.measure,
                aggregation_module.DistributionAggregation([0, 100, 300, 500, 1000, 2000, 5000, 10000])
            )
            self.view_manager.register_view(self.view)
            get_exporter_thread(self.exporter)

    def process_request(self, request):
        if self.enabled and request.path.startswith(settings.MEDIA_URL):
            request._media_start_time = time.perf_counter()

    def process_response(self, request, response):
        if self.enabled and hasattr(request, "_media_start_time"):
            elapsed = (time.perf_counter() - request._media_start_time) * 1000  # ms
            mmap = self.stats_recorder.new_measurement_map()
            tmap = tag_map_module.TagMap()
            tmap.insert("path", request.path)
            mmap.measure_float_put(self.measure, elapsed)
            mmap.record(tmap)
        return response
