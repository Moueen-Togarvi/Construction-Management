# Construction-Management

Here is a `README.md` for your Django project, explaining its structure and functionality:

```markdown
# Django Project Management System

This project is a Django-based application designed for managing projects and materials. It includes features such as CRUD operations for projects and materials, importing/exporting data from Excel and PDF, and role-based access control for various user types.

## Features

1. **Project Management**:
   - Add, update, delete, and view projects.
   - Restore soft-deleted projects.
   - Copy projects along with associated materials.

2. **Material Management**:
   - Add, update, delete, and view materials for specific projects.
   - Calculate the total cost of materials dynamically.

3. **Excel Import/Export**:
   - Import materials from an Excel file.
   - Export project data and materials to Excel or PDF for reporting.

4. **Graphical Analysis**:
   - Visualize total costs per material with bar charts using Matplotlib.

5. **User Authentication and Authorization**:
   - Register and login users.
   - Role-based permissions for actions like viewing and editing projects.

6. **Soft Deletion**:
   - Projects can be soft-deleted and later restored.

## Models

### Project
```python
class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.number}"
```

### Material
```python
class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    gwp = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    penrt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unit})"
```

## Views

- `ProjectListView`: Display a list of projects along with material costs.
- `MaterialCreateView`: Add new materials to a project.
- `MaterialUpdateView`: Update details of existing materials.
- `MaterialDeleteView`: Remove materials from a project.
- `ExcelImportView`: Import materials from Excel files.
- `export_to_pdf`: Generate a PDF report for project materials.
- `export_to_excel`: Generate an Excel report for project materials.

## Templates

All templates are located in the `core/templates/core/` directory and include:
- `project_list.html`
- `project_form.html`
- `material_list.html`
- `material_form.html`
- `excel_import.html`

## Requirements

- Python 3.8+
- Django 4.0+
- Pandas
- Openpyxl
- Matplotlib
- ReportLab

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000`.

## Usage

- Create a new project.
- Add materials to the project.
- Import material data from an Excel file.
- Export project and material data as Excel or PDF.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


