from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
import pandas as pd
from .models import CustomUser, ErrorFeedback1,centers,Project,Transaction
from django.http import JsonResponse,HttpResponse,HttpResponseServerError
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from io import BytesIO
import os
from .decorators import restrict_direct_access
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.db.models import Count
def password_reset(request):
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(Email=email)
            except CustomUser.DoesNotExist:
                user = None

            if user:
                # Generate a random password
                new_password = get_random_string(length=8)

                # Update user's password
                user.Password=new_password
                user.save()
                m1="We hope this email finds you well. We wanted to inform you that your password has been successfully reset."
                m2='''If you wish to change your password again, simply follow these steps:

Log in to your account.
Click on your profile icon located at the top-right corner of the page.
From the dropdown menu, select "Change Password."
Follow the prompts to update your password.
If you have any questions or concerns, feel free to reach out to our support team.

Thank you for being a valued member of our community.'''
                message=f'''Dear {user.Username},
{m1}
Your new password is: {new_password}
 {m2}



'''
                # Send email with new password
                send_mail(
                    'Password Reset',
                    f'{message}',
                    'afreeenbano811@gmail.com',
                    [email],
                    fail_silently=False,
                )

                return render(request, 'ErrorFeedbackApp/done.html')
    else:
        form = PasswordResetForm()

    return render(request, 'ErrorFeedbackApp/password_reset_email.html', {'form': form})

def image_view(request, image_name):
    # Assuming images are stored in a directory named 'images' within your media directory
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)
    #print("Image Path:", image_path)
    

    with open(image_path, 'rb') as f:
            return HttpResponse(f.read())  # Adjust content type as needed
    
def login_view(request):
    if request.method == 'POST':
        Email = request.POST.get('username')
        password = request.POST.get('password')
        
        if Email and password:
            user = CustomUser.objects.filter(Email=Email, Password=password).first()
             
         
            if user:
                request.session['Email'] = Email
                request.session['center'] = user.Center
                request.session['role'] = user.Role
                request.session['username']=user.Username
                if user.Role.lower() == 'superadmin':
                    return redirect('SuperAdmin_home')
                elif user.Role.lower() == 'admin':
                   
                    return redirect('Admin_home')
                elif user.Role.lower() in ['editor', 'maker']:  
                    return render(request, 'ErrorFeedbackApp/default.html',{'role': user.Role, 'username': user.Username,'center':user.Center,'email':Email})
                else:
                     return redirect('database_view')
                
            else:
                # Authentication failed
                 return JsonResponse({'error': 'Invalid username or password'}, status=400)
        else:
            messages.error(request, 'Username and password are required')
    
    return render(request, 'ErrorFeedbackApp/login_view.html')
def change_password(request):
    if request.method == 'POST':
        Email= request.session.get('Email')
        password = request.POST.get('password')
        newPassword=request.POST.get('new')
        print(Email)
        print(password)
        print(newPassword)
        try:
                user = CustomUser.objects.filter(Email=Email, Password=password).first()
                
        except CustomUser.DoesNotExist:
                user = None
                
                
        if user:
            user.Password=newPassword
            user.save()
            return JsonResponse({'Success': 'password changed!'}, status=200)
        else:
            return JsonResponse({'error': 'Email and password do not match for any user'}, status=400)

    return render(request,'ErrorFeedbackApp/change_password.html')

@restrict_direct_access
def Admin_home(request):
    username = request.session.get('username', None) 
    center = request.session.get('center', None)
    role = request.session.get('role', None) 
    Email = request.session.get('Email', None)
    
    # Filter project list based on the admin's center
    project_list = Project.objects.filter(Location=center)
    project_count=Project.objects.filter(Location=center).count()
    user_count=CustomUser.objects.filter(Center=center).count()
    table_data = []
    for project_data in project_list:
        Pro_id = project_data.id
        project_name = project_data.ProjectName
        customer = project_data.Customer
        CreatedDate=project_data.CreatedDate
        # Fetch transaction data for the current project
        project_transactions = Transaction.objects.filter(Project_Id=Pro_id)
        
        # Calculate counts
        feedback_count = project_transactions.count()
        accepted_count = project_transactions.filter(Acknowledged='Accepted').count()
        rejected_count = project_transactions.filter(Acknowledged='Rejected').count()
        
        table_data.append({
            'Customer': customer,
            'Project_Name': project_name,
            'Total_Feedback_Count': feedback_count,
            'Accepted': accepted_count,
            'Rejected': rejected_count,
            'CreatedDate':CreatedDate
        })

    return render(request, 'ErrorFeedbackApp/Admin_home.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'project_count':project_count,
        'user_count':user_count,
        'table_data': table_data
    })
@restrict_direct_access
def Admin_user(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    user_list=CustomUser.objects.filter(Center=center)
    return render(request, 'ErrorFeedbackApp/Admin_user.html',{'role': role, 'username': username,'center':center,'email':Email,'user_list':user_list})
@restrict_direct_access
def Admin_download(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    project_list = Project.objects.filter(Location=center)
    table_data = []
    for project_data in project_list:
        project_name = project_data.ProjectName
        customer = project_data.Customer
        FieldCount=project_data.FieldCount
        CreatedDate=project_data.CreatedDate
        table_data.append({
            'Customer': customer,
            'Project_Name': project_name,
             'FieldCount': FieldCount,
             'CreatedDate':CreatedDate
        })
    return render(request, 'ErrorFeedbackApp/Admin_download.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'table_data': table_data
    })
@restrict_direct_access   
def view_screenshot(request, error_id):
	error = get_object_or_404(ErrorFeedback1, pk=error_id)
	response = HttpResponse(error.screenshot_path, content_type='image/png')  # Adjust content_type if necessary
	return response
def SuperAdmin_home(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    user_count=CustomUser.objects.count()
    project_count=Project.objects.count()
    project_list = Project.objects.all() 
    project_count_by_location = Project.objects.values('Location').annotate(num_projects=Count('Location'))
    transaction_data = Transaction.objects.values('Center', 'Project', 'Error_Type','Acknowledged','Project_Id').annotate(feedback_count=Count('id'))
    
    table_data = []
    for project_data in project_list:
        Pro_id=project_data.id
        project_name = project_data.ProjectName
        customer = project_data.Customer
        centers = project_data.Location
        
        project_transactions = [transaction for transaction in transaction_data if transaction['Project_Id'] == Pro_id]
        accepted_count = sum(1 for t in project_transactions if t['Acknowledged'] == 'Accepted')
        rejected_count = sum(1 for t in project_transactions if t['Acknowledged'] == 'Rejected')
        feedback_count = sum(t['feedback_count'] for t in project_transactions)
        table_data.append({
            'Center': centers,
            'Customer': customer,
            'Project_Name': project_name,
            'Feedback_Count': feedback_count,
            'Accepted': accepted_count,
            'Rejected': rejected_count
        })

    return render(request, 'ErrorFeedbackApp/SuperAdmin_home.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'user_count': user_count,
        'project_count': project_count,
        'project_count_by_location': project_count_by_location,
        'table_data': table_data
    })
@restrict_direct_access
def SuperAdmin_user(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    user_list = CustomUser.objects.all()  
    center_list = list(centers.objects.values_list('Centre', flat=True))
    context = {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'user_list': user_list,
        'center_list':center_list
    }
    
    return render(request, 'ErrorFeedbackApp/SuperAdmin_user.html', context)
    
@restrict_direct_access
def SuperAdmin_download(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    project_list = Project.objects.all() 
    table_data = []
    for project_data in project_list:
        project_name = project_data.ProjectName
        customer = project_data.Customer
        centers = project_data.Location
        FieldCount=project_data.FieldCount
        CreatedDate=project_data.CreatedDate
        table_data.append({
            'Center': centers,
            'Customer': customer,
            'Project_Name': project_name,
             'FieldCount': FieldCount,
             'CreatedDate':CreatedDate
        })
        
    return render(request, 'ErrorFeedbackApp/SuperAdmin_download.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'table_data': table_data
    })
@restrict_direct_access
def SuperAdmin_project(request):
    username = request.session.get('username', None) 
    center = request.session.get('center', None)
    role = request.session.get('role', None) 
    Email = request.session.get('Email', None)
    project_list = Project.objects.all()
    user_list = CustomUser.objects.all() 
    table_data = []
    
    for project_data in project_list:
        project_name = project_data.ProjectName
        customer = project_data.Customer
        centers = project_data.Location
        
        center_admins = [user.Email for user in user_list if user.Center == centers and user.Role == 'Admin']
        assigned_users = CustomUser.objects.filter(ProjectAssigned__icontains=project_name).count()
        
        table_data.append({
            'Center': centers,
            'Customer': customer,
            'Project_Name': project_name,
            'Admins': center_admins,
            'num_of_users':assigned_users
        })
    
    return render(request, 'ErrorFeedbackApp/SuperAdmin_project.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'table_data': table_data,
       
    })
    
@restrict_direct_access
def role(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/AddRoles.html',{'role': role, 'username': username,'center':center,'email':Email})
@restrict_direct_access
def Admin_project(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    project_list = Project.objects.filter(Location=center)
    user_list = CustomUser.objects.filter(Center=center) 
    table_data = []
    
    for project_data in project_list:
        project_name = project_data.ProjectName
      
        num_of_users = CustomUser.objects.filter(ProjectAssigned=project_name).count() 
        
        table_data.append({
            'Project_Name': project_name,
            'num_of_users':num_of_users
        })
    
    return render(request, 'ErrorFeedbackApp/Admin_project.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'table_data': table_data,
       
    })
@restrict_direct_access
def center(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    center_names = centers.objects.values_list('Centre', flat=True)
    return render(request, 'ErrorFeedbackApp/center_management.html', {
        'role': role,
        'username': username,
        'center': center,
        'email': Email,
        'Centers': center_names 
    })

def new_page_view(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/new_page.html',{'role': role, 'username': username,'center':center,'email':Email})

@restrict_direct_access
def default(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/default.html',{'role': role, 'username': username,'center':center,'email':Email})
@restrict_direct_access
def default_download(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/default_download.html',{'role': role, 'username': username,'center':center,'email':Email})
@restrict_direct_access
def create_project(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/create_project.html',{'role': role, 'username': username,'center':center,'email':Email})
@restrict_direct_access
def feedback(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/feedback.html',{'role': role, 'username': username,'center':center,'email':Email})
def acknowledge(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    return render(request, 'ErrorFeedbackApp/acknowledge.html',{'role': role, 'username': username,'center':center,'email':Email})
@restrict_direct_access
def download_error_data(request):
     if request.method == 'POST':
        # Get form data
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        # Check if the user is admin
        role = request.session.get('role')
        if role == 'Admin':
            # If admin, get center locations from form data
            center_location = request.POST.getlist('center_locations')
        else:
            # If not admin, get center location from session
            center_location = [request.session.get('center')]
        
        try:
            # Convert date strings to datetime objects
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
           
   
            error_data = ErrorFeedback1.objects.filter(
				Audited_date__range=[start_datetime, end_datetime],
    		    		center_location__in=center_location
		)
            
            # Convert data to DataFrame
            data = pd.DataFrame(list(error_data.values()))
            #error_data = ErrorFeedback1.objects.all()
            #data = pd.DataFrame(list(error_data.values()))
            
            # Convert audited_date to timezone-unaware datetimes
            if 'Audited_date' in data.columns:
                data['Audited_date'] = data['Audited_date'].apply(lambda x: x.replace(tzinfo=timezone.utc).astimezone(None) if x is not None else None)

            # Create Excel file in memory
            excel_file = BytesIO()
            data.to_excel(excel_file, index=False)
            excel_file.seek(0)
            
            # Prepare response
            response = HttpResponse(excel_file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="error_data.xlsx"'
            return response
        except Exception as e:
            # Handle any exceptions
            return HttpResponseServerError("An error occurred: {}".format(str(e)))
@restrict_direct_access      
def error_data_view(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        end_date += timedelta(days=1)
        # Retrieve unique center locations between the given dates
        unique_centers = ErrorFeedback1.objects.filter(
            Audited_date__range=(start_date, end_date)
        ).values_list('center_location', flat=True).distinct()
        
        # Calculate summary counts for each center
        summary_counts = {}
        for center in unique_centers:
            total_count = ErrorFeedback1.objects.filter(
                center_location=center,
                Audited_date__range=(start_date, end_date)
            ).count()
            accepted_count = ErrorFeedback1.objects.filter(
                center_location=center,
                Audited_date__range=(start_date, end_date),
                Acknowledged='Accepted'
            ).count()
            rejected_count = ErrorFeedback1.objects.filter(
                center_location=center,
                Audited_date__range=(start_date, end_date),
                Acknowledged='Rejected'
            ).count()
            not_acknowledged_count = total_count - accepted_count - rejected_count
            summary_counts[center] = {
                'Total': total_count,
                'Accepted': accepted_count,
                'Rejected': {
                    'Count': rejected_count,
                },
                'NotAcknowledged': not_acknowledged_count
                
            }
        
        
        return render(request, 'ErrorFeedbackApp/summary_view.html', {'summary_counts': summary_counts})
    else:
        return render(request, 'ErrorFeedbackApp/summary.html',{'username': username, 'center': center})
    
  

@restrict_direct_access
def update_status(request):
    if request.method == 'POST':
        error_id = request.POST.get('id')
        status = request.POST.get('status')

        if error_id and status:
            try:
                error = ErrorFeedback1.objects.get(id=error_id)
                error.Acknowledged = status
                error.save()
                return JsonResponse({'success': True})
            except ErrorFeedback1.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Error feedback not found'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data sent'})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})
@restrict_direct_access
def update_status_reject(request):
    if request.method == 'POST':
        error_id = request.POST.get('id')
        status = request.POST.get('status')
        reason = request.POST.get('reason')

        if error_id and status:
            try:
                error = ErrorFeedback1.objects.get(id=error_id)
                error.Acknowledged = status
                if status == "Rejected":
                    error.Reason_for_Rejection = reason
                error.save()
                # Redirect to success page
                return JsonResponse({'success': True})
            except ErrorFeedback1.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Error feedback not found'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data sent'})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})
@restrict_direct_access
def home(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    
    return render(request, 'ErrorFeedbackApp/home.html', {'username': username, 'center': center})
@restrict_direct_access
def database_view(request):
    # Fetch all ErrorFeedback1 objects from the database
    center_location = request.session.get('center')
    username = request.session.get('username', None) 
    role = request.session.get('role')
    if(role=="Maker"):
        error_feedback = ErrorFeedback1.objects.filter(
                 center_location=center_location,maker_name=username)
    else:
        error_feedback = ErrorFeedback1.objects.filter(
                 center_location=center_location)

    # Check if a search query is submitted
    if 'query' in request.GET and 'field' in request.GET:
        query = request.GET['query']
        field = request.GET['field']
        # Perform search based on the selected field
        if field == 'editor_id':
            error_feedback = error_feedback.filter(editor_id__icontains=query)
        elif field == 'job_id':
            error_feedback = error_feedback.filter(job_id__icontains=query)
        elif field == 'error_field':
            error_feedback = error_feedback.filter(error_field__icontains=query)
        elif field == 'error_type':
            error_feedback = error_feedback.filter(error_type__icontains=query)
        elif field == 'error_category':
            error_feedback = error_feedback.filter(error_category__icontains=query)
    # Pass the data to the template
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    if(role=="Maker"):
        return render(request, 'ErrorFeedbackApp/database_view.html', {'error_feedback': error_feedback,'username': username, 'center': center})
    return render(request, 'ErrorFeedbackApp/database_view_others.html', {'error_feedback': error_feedback,'username': username, 'center': center})

@restrict_direct_access

def registration(request):
    username = request.session.get('username', None) 
    center= request.session.get('center',None)
    role = request.session.get('role', None) 
    Email= request.session.get('Email',None)
    if request.method == 'POST':
        excel_file = request.FILES.get('excelFile')
        if excel_file:
            try:
                df = pd.read_excel(excel_file)  # Read the Excel file
                if df.empty:
                    messages.error(request, 'The Excel file is empty.')
                else:
                    # Check if column names match expected case
                    expected_columns = ['Username', 'Email', 'Password']
                    if not all(col in df.columns for col in expected_columns):
                        messages.error(request, 'Column headings do not match expected format.')
                    else:
                        for index, row in df.iterrows():
                            CustomUser.objects.create(
                                Username=row['Username'],
                                Email=row['Email'],
                                Password=row['Password'],
                                Center=center,
                                
                            )
                        messages.success(request, 'Users created successfully.')
            except Exception as e:
                print(f'An error occurred: {str(e)}')
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Please select an Excel file.')
    return render(request, 'ErrorFeedbackApp/Admin_user.html',{'role': role, 'username': username,'center':center,'email':Email})
def add_admin(request):
    if request.method == 'POST':
        # Assuming you have a form with fields: username, email, password, centerDropdown
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        center = request.POST.get('centerDropdown')
    
        
        # Create the admin user
        admin_user = CustomUser.objects.create(
            Username=username,
            Email=email,
            Password=password,
            Role='Admin',
            Center=center
        )
        return redirect('SuperAdmin_user/') 
    else:
        pass
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        center= request.session.get('center')
        

        user = CustomUser.objects.create(
            Username=username,
            Email=email,
            Password=password,
            Center=center
        )
        
        return redirect('Admin_user/') 
        
    else:
        pass
def delete_user(request):
    if request.method == 'POST':
        email = request.POST.get('Email')  # Assuming username is used as the identifier
        try:
            user = CustomUser.objects.get(Email=email)
            user.delete()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})        
    else:
    
        return JsonResponse({'success': False, 'error': 'Invalid request method'})