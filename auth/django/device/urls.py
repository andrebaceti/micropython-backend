"""Set urls for registration."""
from pumpwood_djangoviews.routers import PumpWoodRouter
from django.conf.urls import url
from device import rest

pumpwoodrouter = PumpWoodRouter()
pumpwoodrouter.register(viewset=rest.RestMicropythonDescriptionGeoarea)
pumpwoodrouter.register(viewset=rest.RestMicropythonDescriptionDevice)
pumpwoodrouter.register(viewset=rest.RestMicropythonDeviceCode)

urlpatterns = [
]

urlpatterns += pumpwoodrouter.urls
