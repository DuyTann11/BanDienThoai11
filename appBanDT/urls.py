from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trangchu, name='trangchu'),
    path('sanpham/', views.sanpham, name='sanpham'),
    path('sanpham/<int:masp>/', views.sanpham, name='chi_tiet_sanpham'),
    path('dat-hang/', views.dat_hang, name='dat_hang'),
    path('quanlysp/', views.quanlysp, name='quanlysp'),
    path('sanpham/cap-nhat-trang-thai/<int:masp>/', views.capnhattrangthai, name='cap_nhat_trang_thai'),
    path('quanlydathang/', views.dat_hang, name='quanlydathang'),
    path('dathang/cap-nhat-trang-thai/<int:madonhang>/', views.capnhattrangthaidonhang, name='cap_nhat_trang_thai_don_hang'),
    path('quanlyanh/', views.quanlyanh, name='quanlyanh'),
    path('timkiem/', views.timsanpham, name='timsanpham'),
    path('lienhe/', views.lienhe, name='lienhe'),

]
