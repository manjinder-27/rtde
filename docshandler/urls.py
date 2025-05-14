from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.createDoc,name='create_doc'),
    path('editor/<str:docID>/',views.openEditor,name='doc_editor_view'),
    path('download/<str:docID>/',views.downloadFile,name='doc_download_view'),
    path('connect/',views.connectView,name='connect_view')
]