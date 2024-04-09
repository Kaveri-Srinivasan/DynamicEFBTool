from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
class CustomUser(models.Model):
    # Add additional fields here
    id = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)
    Center =models.CharField(max_length=50)
    ProjectAssigned = models.CharField(max_length=50)
    MobileNo= models.CharField(max_length=50)
      
    class Meta:
        db_table = 'User'
        
class ErrorFeedback1(models.Model):
    id = models.AutoField(primary_key=True)
    editor_id = models.TextField()
    job_id = models.TextField()
    maker_name = models.TextField()
    error_field = models.TextField()
    error_type = models.TextField()
    error_category = models.TextField()
    error_2d_count = models.IntegerField()
    error_3d_count = models.IntegerField()
    object_id = models.TextField()
    selected_class = models.TextField()  
    correct_class = models.TextField()  
    screenshot_path = models.BinaryField(null=True)  
    Audited_date = models.DateTimeField(auto_now_add=True)  
    center_location = models.TextField()
    Acknowledged = models.TextField()
    Reason_for_Rejection = models.TextField()

    class Meta:
        db_table = 'EFBMasterTable'
        

class centers(models.Model):
    id = models.AutoField(primary_key=True)
    Centre = models.CharField(max_length=50)
    class Meta:
        db_table = 'Location'
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    Customer = models.CharField(max_length=50)
    Location = models.CharField(max_length=50)
    ProjectName = models.CharField(max_length=50)
    FieldCount =models.IntegerField()
    FieldName = models.CharField(max_length=50)
    CreatedDate=models.DateTimeField(auto_now_add=True) 
    class Meta:
        db_table = 'Project'

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    Center = models.CharField(max_length=50)
    Project_Id = models.IntegerField()
    Project = models.CharField(max_length=255)
    Editor_Id = models.CharField(max_length=255)
    Maker_Id = models.CharField(max_length=255)
    Job_Id = models.CharField(max_length=255)
    Error_Field = models.CharField(max_length=255)
    Error_Type = models.CharField(max_length=255)
    Error_Category = models.CharField(max_length=255)
    Audited_Date = models.DateTimeField(auto_now_add=True, null=True)
    Acknowledged = models.CharField(max_length=50, null=True)
    Reason_for_Rejection = models.CharField(max_length=255, null=True)
    Screenshot_path = models.BinaryField(null=True)
    Field1 = models.CharField(max_length=255, null=True)
    Field2 = models.CharField(max_length=255, null=True)
    Field3 = models.CharField(max_length=255, null=True)
    Field4 = models.CharField(max_length=255, null=True)
    Field5 = models.CharField(max_length=255, null=True)
    Field6 = models.CharField(max_length=255, null=True)
    Field7 = models.CharField(max_length=255, null=True)
    Field8 = models.CharField(max_length=255, null=True)
    Field9 = models.CharField(max_length=255, null=True)
    Field10 = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Transaction'