from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'conditions', views.ConditionViewSet)
router.register(r'entries', views.EntryViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
]