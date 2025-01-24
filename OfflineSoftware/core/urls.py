from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectUpdateView
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView
from .views import ExcelImportView
from .views import CalculationResultView, calculate_results
from .views import export_to_excel
from .views import export_to_pdf
from .views import register
from django.contrib.auth import views as auth_views
from .views import HomePageView
# core/urls.py
from .views import ProjectCopyView
from .views import ProjectDeleteView
from .views import ProjectRestoreView
from .views import ProjectUpdateView


# core/urls.py






    
# core/urls.py




# core/urls.py


# from .views import load_materials



# core/urls
urlpatterns = [

    
    path('', ProjectListView.as_view(), name='project_list'),
    
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/copy/', ProjectCopyView.as_view(), name='project_copy'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:project_id>/export_excel/', export_to_excel, name='export_to_excel'),
    path('', HomePageView.as_view(), name='project_list'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('project/<int:pk>/materials/', MaterialListView.as_view(), name='material_list'),
    path('project/<int:pk>/materials/new/', MaterialCreateView.as_view(), name='material_create'),
    path('materials/<int:pk>/edit/', MaterialUpdateView.as_view(), name='material_edit'),
    path('materials/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material_delete'),
    path('project/<int:pk>/materials/import/', ExcelImportView.as_view(), name='excel_import'),
    path('project/<int:pk>/calculate/', CalculationResultView.as_view(), name='calculation_results'),
    path('project/<int:pk>/calculate/results/', calculate_results, name='calculate_results'),
    path('project/<int:pk>/calculate/export/excel/', export_to_excel, name='export_to_excel'),
    path('project/<int:pk>/calculate/export/pdf/', export_to_pdf, name='export_to_pdf'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('project/<int:pk>/materials/import/', ExcelImportView.as_view(), name='excel_import'),
    path('project/<int:pk>/restore/', ProjectRestoreView.as_view(), name='project_restore'),
    # path('project/<int:project_id>/load-materials/', load_materials, name='load_materials')
     path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]


# core/urls.py

from .views import load_materials

urlpatterns += [
    path('load-materials/', load_materials, name='load_materials'),
]


# core/urls.py

# urlpatterns += [
   
# ]













