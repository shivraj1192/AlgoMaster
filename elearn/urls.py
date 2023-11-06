
from django.urls import path,include
from elearn import views


urlpatterns = [
    path('', views.home , name='home'),
    path('north-west-method/', views.north_west_method, name='north_west_method'),
    path('least-cost-method/', views.least_cost_method, name='least_cost_method'),
    path('row-minima-method/', views.row_minima_method, name='row_minima_method'),
    path('column-minima-method/', views.column_minima_method, name='column_minima_method'),
    path('vogels-approximation-method/', views.vogels_approximation_method, name='vogels_approximation_method'),
]