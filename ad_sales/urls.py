from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^add_order', views.add_order, name='add_order'),
    url(r'^thx', views.thx, name='thx'),
    url(r'^view_orders/order_id=(?P<order_id>[0-9]+)/spots/free_spot?spot_id=(?P<spot_id>[0-9]+)', views.free_spot, name='free_spot'),
    url(r'^view_orders/order_id=(?P<order_id>[0-9]+)/prototypes', views.view_order_prototypes, name='view_order_prototypes'),
    url(r'^view_orders/order_id=(?P<order_id>[0-9]+)/spots', views.view_order_spots, name='view_order_spots'),
    url(r'^view_orders/order_id=(?P<order_id>[0-9]+)', views.view_order, name='view_order'),
    url(r'^view_orders/status=(?P<status>[a-z]+)', views.view_orders_filter, name='view_orders_filter'),
    url(r'^view_orders', views.view_orders, name='view_orders'),
    url(r'^delete_order/order_id=(?P<order_id>[0-9]+)', views.delete_order, name='delete_order'),
    url(r'^download/pr_id=(?P<pr_id>[0-9]+)', views.download, name='download'),
    url(r'^profile/username=(?P<username>[a-zA-Z0-9.-_]+)', views.profile, name='profile'),
    url(r'^view_spots/page=(?P<page>[0-9]+)', views.view_spots, name='view_spots'),
    url(r'^view_spots', views.view_spots_index, name='view_spots_index'),
    url(r'^add_spot', views.add_spot, name='add_spot'),
    url(r'^delete_spot/spot_id=(?P<spot_id>[0-9]+)', views.delete_spot, name='delete_spot'),
    url(r'^edit_spot/spot_id=(?P<spot_id>[0-9]+)', views.edit_spot, name='edit_spot'),
    url(r'^statistics', views.statistics, name='statistics')
]