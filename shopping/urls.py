from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('add_item/<int:product_id>', views.add_item),
    path('review', views.review),
    path('clear_item', views.clear_item),
    path('remove_item/<int:product_id>', views.remove_item),
    path('change_item/<int:product_id>/<int:amount>', views.change_item),
    path('payment_form',views.payment_form),
    path('process',views.process),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)