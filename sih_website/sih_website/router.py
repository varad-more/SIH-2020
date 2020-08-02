# from dashboard.viewsets import corpactiondata_viewset,filedownload_viewset
from dashboard.viewsets import *
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('corpaction',corpactiondata_viewset )
router.register('filedownload',filedownload_viewset )
router.register('articles',articles_viewset )
router.register('dashboard',dashboard_viewset )
router.register('securities',securities_viewset )
