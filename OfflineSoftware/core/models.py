from django.db import models
# core/models.py

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_view_all_projects", "Can view all projects"),
            ("can_edit_projects", "Can edit projects"),
        ]

class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.number}"
    

#     def delete(self):
#         self.is_deleted = True
#         self.save()
# # core/forms.py




# core/models.py

# core/models.py

# core/models.py

from django.db import models

class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)  # Unit field to store the unit of the material
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    gwp = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # GWP value
    penrt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # PENRT value

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unit})"




    