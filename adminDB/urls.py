from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mainTable', views.mainTable, name='mainTable'),
    path('searchOrder', views.searchOrder, name='searchOrder'),
    path('Log', views.FullLog,name='Log'),
    path('searchLog', views.searchLog, name='searchLog'),
    path('PaymentInfo', views.PaymentInfo, name='PaymentInfo'),
    path('OrderEdit', views.OrderEdit, name='OrderEdit'),
    path('delete/<int:order_id>', views.delete, name='delete'),
    path('update', views.update, name='update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)