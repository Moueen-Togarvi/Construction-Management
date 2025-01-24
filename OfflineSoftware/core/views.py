from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Project, Material
from .forms import ProjectForm
from django.views.generic.edit import FormView
from .forms import MaterialForm, ExcelImportForm
from django.forms import modelformset_factory
from django.contrib import messages
import pandas as pd
from django.http import JsonResponse
import matplotlib.pyplot as plt
import io
import base64
from django.views import View
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import DeleteView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from .models import Project
from .forms import ExcelImportForm
from django.views.generic import UpdateView
from .models import Material, Project

from django.views.generic import DeleteView



# core/views.py

import pandas as pd
from django.http import JsonResponse

def load_materials(request):
    # Load the Excel file (ensure the path is correct)
    excel_file_path = 'path_to_your_excel_file.xlsx'
    df = pd.read_excel(excel_file_path)

    # Assuming your Excel file has columns 'Material Name' and 'Unit'
    materials = df[['Material Name', 'Unit']].to_dict(orient='records')

    return JsonResponse(materials, safe=False)




# core/views.py

# core/views.py

# core/views.py

from django.shortcuts import render, get_object_or_404
from .models import Project, Material

def project_materials_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    materials = project.materials.all()

    material_contributions = []
    gwp_total = 0
    penrt_total = 0

    for material in materials:
        gwp_contribution = material.gwp * material.quantity if material.gwp and material.quantity else 0
        penrt_contribution = material.penrt * material.quantity if material.penrt and material.quantity else 0
        
        material_contributions.append({
            'name': material.name,
            'gwp_contribution': gwp_contribution,
            'penrt_contribution': penrt_contribution,
        })
        
        gwp_total += gwp_contribution
        penrt_total += penrt_contribution

    context = {
        'project': project,
        'material_contributions': material_contributions,
        'gwp_total': gwp_total,
        'penrt_total': penrt_total,
    }

    return render(request, 'core/project_materials.html', context)












class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'core/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')






class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'number']
    template_name = 'core/project_form.html'

    def get_success_url(self):
        return reverse_lazy('project_list')



class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        projects = Project.objects.all()

        for project in projects:
            # Calculate the total cost of materials for each project
            project.total_materials_cost = sum(
                material.total_cost for material in project.materials.all()
            )

        return projects
# core/views.py

class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_deleted=False)


class ProjectRestoreView(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, is_deleted=True)
        project.is_deleted = False
        project.save()
        messages.success(request, f"Project '{project.name}' restored successfully!")
        return redirect('project_list')


class MaterialListView(ListView):
    model = Material
    template_name = 'core/material_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return Material.objects.filter(project_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'core/material_form.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('material_list', pk=self.kwargs['pk'])

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'core/material_form.html'

    def get_success_url(self):
        return redirect('material_list', pk=self.object.project.pk)

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'core/material_confirm_delete.html'

    def get_success_url(self):
        return redirect('material_list', pk=self.object.project.pk)



# core/views.py



class ProjectCopyView(View):
    def post(self, request, pk):
        original_project = get_object_or_404(Project, pk=pk)
        # Create a new project with a modified name and number to indicate it's a copy
        copied_project = Project.objects.create(
            name=f"Copy of {original_project.name}",
            number=f"{original_project.number}-copy",
        )
        # Copy materials associated with the original project
        for material in original_project.materials.all():
            Material.objects.create(
                project=copied_project,
                name=material.name,
                quantity=material.quantity,
                unit_price=material.unit_price,
                total_cost=material.total_cost,
            )
        messages.success(request, f"Project '{original_project.name}' copied successfully!")
        return redirect('project_list')

    


class HomePageView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects_with_materials'] = [
            {
                'project': project,
                'materials': project.materials.all()
            }
            for project in Project.objects.all()
        ]
        context['excel_form'] = ExcelImportForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            try:
                df = pd.read_excel(excel_file)
                project_id = request.POST.get('project_id')
                project = get_object_or_404(Project, id=project_id)

                for _, row in df.iterrows():
                    Material.objects.create(
                        project=project,
                        name=row['Material Name'],
                        quantity=row['Quantity'],
                        unit_price=row['Unit Price']
                    )

                messages.success(request, 'Materials imported successfully!')
            except Exception as e:
                messages.error(request, f'Error processing file: {e}')

        return redirect('project_list')



#######^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# core/views.py

class ProjectListView(PermissionRequiredMixin, ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    permission_required = 'core.can_view_all_projects'




def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin)
def admin_only_view(request):
    # View code here
    return render(request, 'core/admin_only.html')





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})



@login_required
def form_valid(self, form):
    try:
        excel_file = form.cleaned_data['excel_file']
        df = pd.read_excel(excel_file)
        ...
        messages.success(self.request, "Materials imported successfully!")
    except Exception as e:
        messages.error(self.request, f"Error importing materials: {str(e)}")
    return redirect('material_list', pk=self.kwargs['pk'])




@login_required
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Project created successfully!")
        return response



@login_required
def export_to_pdf(request, pk):
    project = get_object_or_404(Project, pk=pk)
    materials = Material.objects.filter(project=project)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Project_{project.name}_Results.pdf'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph(f"Project {project.name} - Calculation Results", styles['Title'])
    elements.append(title)

    data = [['Material Name', 'Quantity', 'Unit Price', 'Total Cost']]
    for material in materials:
        data.append([material.name, material.quantity, material.unit_price, material.total_cost])

    total_project_cost = sum(material.total_cost for material in materials)
    data.append(['', '', 'Total Project Cost', total_project_cost])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    return response



@login_required
def export_to_excel(request, pk):
    project = get_object_or_404(Project, pk=pk)
    materials = Material.objects.filter(project=project)

    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f"Project {project.name} Results"

    # Add headers to the worksheet
    headers = ['Material Name', 'Quantity', 'Unit Price', 'Total Cost']
    worksheet.append(headers)

    # Add material data to the worksheet
    for material in materials:
        worksheet.append([material.name, material.quantity, material.unit_price, material.total_cost])

    # Add total project cost at the bottom
    total_project_cost = sum(material.total_cost for material in materials)
    worksheet.append(['', '', 'Total Project Cost', total_project_cost])

    # Prepare the response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Project_{project.name}_Results.xlsx'

    workbook.save(response)
    return response




class CalculationResultView(View):
    template_name = 'core/calculation_results.html'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, self.template_name, {'project': project})



@login_required
def calculate_results(request, pk):
    project = get_object_or_404(Project, pk=pk)
    materials = Material.objects.filter(project=project)

    # Example calculation: total cost per material and total project cost
    total_project_cost = sum(material.total_cost for material in materials)

    # Prepare data for table display
    table_data = [
        {'name': material.name, 'quantity': material.quantity, 'total_cost': material.total_cost}
        for material in materials
    ]

    # Generate a simple bar chart for graphical display
    fig, ax = plt.subplots()
    ax.bar([material.name for material in materials], [material.total_cost for material in materials])
    ax.set_title(f'Total Cost per Material for Project {project.name}')
    ax.set_xlabel('Materials')
    ax.set_ylabel('Total Cost')

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Return the calculation results as JSON
    return JsonResponse({
        'total_project_cost': total_project_cost,
        'table_data': table_data,
        'chart_image': image_base64,
    })






class ExcelImportView(FormView):
    template_name = 'core/excel_import.html'
    form_class = ExcelImportForm

    def form_valid(self, form):
        excel_file = form.cleaned_data['excel_file']
        df = pd.read_excel(excel_file)

        project = get_object_or_404(Project, pk=self.kwargs['pk'])

        for _, row in df.iterrows():
            Material.objects.create(
                project=project,
                name=row['Material Name'],
                quantity=row['Quantity'],
                unit_price=row['Unit Price'],
            )

        messages.success(self.request, "Materials imported successfully!")
        return redirect('material_list', pk=self.kwargs['pk'])






class MaterialListView(ListView):
    model = Material
    template_name = 'core/material_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return Material.objects.filter(project_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'core/material_form.html'

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('material_list', kwargs={'pk': self.kwargs['pk']})

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'core/material_form.html'

    def get_success_url(self):
        return reverse_lazy('material_list', kwargs={'pk': self.object.project.pk})

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'core/material_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('material_list', kwargs={'pk': self.object.project.pk})



class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'core/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')



def export_to_excel(request, project_id):
    project = Project.objects.get(id=project_id)
    materials = Material.objects.filter(project=project)
    df = pd.DataFrame(list(materials.values('name', 'quantity')))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{project.name}_report.xlsx"'
    df.to_excel(response, index=False)
    return response