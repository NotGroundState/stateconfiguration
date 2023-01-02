from django.contrib.gis.geoip2 import GeoIP2

def location_finder(request):
    return GeoIP2().country(request)