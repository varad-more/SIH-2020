from dashboard.viewsets import corpactiondata_viewset
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('corpaction',corpactiondata_viewset )