from django.urls import path, include
from . import views

app_name ='surat_menyurat'

urlpatterns = [
  path('arsipsuratmasuk/', views.arsip_surat_masuk_list, name='arsip_surat_masuk_list'),
  path('arsipsuratmasukdelete/<int:id>', views.arsip_surat_masuk_delete, name='arsip_surat_masuk_delete'),
  path('arsipsuratkeluar/', views.arsip_surat_keluar_list, name='arsip_surat_keluar_list'),
  path('arsipsuratkeluardelete/<int:id>', views.arsip_surat_keluar_delete, name='arsip_surat_keluar_delete'),
  
  path('suratmasuk/', views.surat_masuk_list, name='surat_masuk_list'),
  path('suratmasukform/', views.surat_masuk_form, name='surat_masuk_form'),
  path('suratmasukdelete/<int:id>', views.surat_masuk_delete, name='surat_masuk_delete'),
  path('suratmasukedit/<int:id>', views.surat_masuk_edit, name='surat_masuk_edit'),

  path('suratkeluar/', views.surat_keluar_list, name='surat_keluar_list'),
  path('suratkeluarform/', views.surat_keluar_form, name='surat_keluar_form'),
  path('suratkeluardelete/<int:id>', views.surat_keluar_delete, name='surat_keluar_delete'),
  path('suratkeluaredit/<int:id>', views.surat_keluar_edit, name='surat_keluar_edit'),
]
