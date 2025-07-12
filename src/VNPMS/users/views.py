import datetime
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from VNPMS.database import bpm_database
from bases.views import index
from users.forms import CurrentCustomUserForm, CustomUser, UserInfoForm, Unit
from users.models import UserType, Plant, Group, Member
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext as
from django.views.decorators.http import require_POST
import json
from bases.utils import send_wecom_message
from django.utils.http import urlencode
from django.utils.translation import gettext as _


def add_permission(user, codename):
    perm = Permission.objects.get(codename=codename)
    user.user_permissions.add(perm)


def remove_permission(user, codename):
    perm = Permission.objects.get(codename=codename)
    user.user_permissions.remove(perm)


def register(request):
    '''
    Register a new user
    '''
    template = 'users/register.html'
    if request.method == 'GET':
        return render(request, template, {'userForm': CurrentCustomUserForm()})

    # POST
    userForm = CurrentCustomUserForm(request.POST)
    if not userForm.is_valid():
        return render(request, template, {'userForm': userForm})

    userForm.save()
    messages.success(request, _('Welcome to register'))
    return redirect('register')


@csrf_exempt
def login(request):
    if 'emp_no' in request.COOKIES:
        cookies_username = request.COOKIES['emp_no']

    if 'password' in request.COOKIES:
        cookies_password = request.COOKIES['password']

    '''
    Login an existing user
    '''
    template = 'users/login.html'
    if request.method == 'GET':
        next = request.GET.get('next')
        return render(request, template, locals())

    if request.method == 'POST':
        next_page = request.POST.get('next')
        if request.user.is_authenticated:
            if next_page != 'None':
                return HttpResponseRedirect(next_page)
            else:
                return index(request)
        else:
            # POST
            emp_no = request.POST.get('emp_no')
            password = request.POST.get('password')
            if not emp_no or not password:    # Server-side validation
                messages.error(request, _('User name or password is missing!'))
                return render(request, template)

            user = authenticate(username=emp_no, password=password)
            if not user:    # authentication fails
                messages.error(request, _('The username or password is incorrect!'))
                return render(request, template)

            custom_user = CustomUser.objects.get(emp_no=emp_no)
            if not custom_user or custom_user.user_type.type_name == 'Wait For Approve':    # check approved account
                messages.error(request, 'The user is waiting for approval')
                return render(request, template)

            response = redirect(reverse('pms_home'))
            if request.POST.get('remember') == "on":
                response.set_cookie("emp_no", emp_no, expires=timezone.now()+datetime.timedelta(days=30))
                response.set_cookie("password", password, expires=timezone.now()+datetime.timedelta(days=30))
            else:
                response.delete_cookie("emp_no")
                response.delete_cookie("password")
            # login success
            auth_login(request, user)

            # messages.success(request, '登入成功')

            return response


def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, 'Welcome back')
    return redirect('login')


# Create
@login_required
def create(request):
    template = 'users/create.html'
    if request.method == 'GET':
        form = CurrentCustomUserForm()
        form.fields['password1'].required = True
        form.fields['password2'].required = True
        if not request.user.is_superuser:
            form.fields["user_type"].queryset = UserType.objects.filter(type_name="一般使用者").all()

        return render(request, template, {'userForm': form})

    if request.method == 'POST':
        form = CurrentCustomUserForm(request.POST)
        form.fields['password1'].required = True
        form.fields['password2'].required = True
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["username"]
            user.create_by = request.user
            user.update_by = request.user
            user.set_password(form.cleaned_data["password1"])
            user.unit = Unit.objects.get(pk=request.POST.get('unit'))
            user.save()

            issue_owner_user_type = UserType.objects.filter(type_name__in=['Administrator', 'Normal'])
            user_type = form.cleaned_data["user_type"]

            if user_type in issue_owner_user_type:
                group_admin_user = CustomUser.objects.get(username='box_chang')

                issue_owner_group, _ = Group.objects.get_or_create(
                    group_name='Issue Owner',
                    group_description='This group includes all IT department members responsible for handling problems.',
                    defaults={'create_by': group_admin_user, 'update_by': group_admin_user}
                )

                if not Member.objects.filter(member=group_admin_user, group=issue_owner_group).exists():
                    Member.objects.create(
                        member=group_admin_user,
                        group=issue_owner_group,
                        isJoin=True,
                        create_by=group_admin_user
                    )

                if not Member.objects.filter(member=user, group=issue_owner_group).exists():
                    Member.objects.create(
                        member=user,
                        group=issue_owner_group,
                        isJoin=True,
                        create_by=request.user
                    )

            #messages.success(request, '歡迎註冊')
            return redirect('user_list')
        else:
            return render(request, template, {'userForm': form})


@login_required
def detail(request):
    template = 'users/edit.html'
    if request.method == 'POST':
        pk = request.POST.get('pk')
        member = CustomUser.objects.get(pk=pk)
        perm_pms = member.has_perm('users.perm_pms')
        perm_ams = member.has_perm('users.perm_ams')
        perm_workhour = member.has_perm('users.perm_workhour')
        perm_user_manage = member.has_perm('users.perm_user_manage')
        perm_misc_apply = member.has_perm('users.perm_misc_apply')
        perm_svr_monitor = member.has_perm('users.perm_svr_monitor')
        perm_stock = member.has_perm('users.perm_stock')

        if not request.user.is_superuser:
            form = CurrentCustomUserForm(instance=member, initial={'user_type': 2})
            form.fields["user_type"].queryset = UserType.objects.filter(type_name="一般使用者").all()
        else:
            form = CurrentCustomUserForm(instance=member)
        form.fields['emp_no'].widget.attrs['readonly'] = True
        form.fields["unit"].queryset = Unit.objects.filter(plant=member.unit.plant).all()
        form.fields['plant'].initial = member.unit.plant

        return render(request, template, locals())

# Edit
@login_required
def user_edit(request):
    template = 'users/edit.html'
    if request.method == 'POST':
        pk = request.POST.get('pk')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        member = CustomUser.objects.get(pk=pk)
        form = CurrentCustomUserForm(request.POST, instance=member)

        if form.is_valid():
            user = form.save(commit=False)
            user.create_by = request.user
            user.update_by = request.user
            user.unit = form.cleaned_data['unit']
            if password1 and password2:
                user.set_password(password1)
            user.save()
            return redirect('user_list')
    return render(request, template, locals())


# Edit
@login_required
def user_info(request):
    template = 'users/info.html'
    pk = request.user.pk
    member = CustomUser.objects.get(pk=pk)

    if request.method == 'POST':
        password = request.POST.get('password0')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        form = UserInfoForm(request.POST, instance=member)

        if form.is_valid():
            user = form.save(commit=False)
            user.update_by = request.user
            if password1 and password2:
                user.set_password(password1)
            user.save()
            messages.info(request, _('Modification successful!'))
    else:
        form = UserInfoForm(instance=member)
    return render(request, template, locals())


@login_required
def user_list(request):
    template = 'users/list.html'

    user_keyword = ""

    query = Q(user_type__isnull=False)  # 排除超級管理者
    members = CustomUser.objects.filter(query)

    member_all = members.count()

    admin_type = UserType.objects.filter(type_name__in=['Administrator'])
    admin_count = members.filter(user_type__in=admin_type, is_active=True).count()

    IT_type = UserType.objects.filter(type_name__in=['Normal'])
    IT_count = members.filter(user_type__in=IT_type, is_active=True).count()

    Request_type = UserType.objects.filter(type_name__in=['Requester'])
    requester_count = members.filter(user_type__in=Request_type, is_active=True).count()

    wait_approve_type = UserType.objects.filter(type_name__in=['Wait For Approve'])
    approval_members = members.filter(user_type__in=wait_approve_type)

    approved_type = UserType.objects.filter(type_name__in=['Administrator', 'Normal', 'Requester'])
    members = members.filter(user_type__in=approved_type)

    if request.method == 'POST':
        user_keyword = request.POST.get('user_keyword')
        request.session['user_keyword'] = user_keyword

    if request.method == 'GET':
        if 'user_keyword' in request.session:
            user_keyword = request.session['user_keyword']

    if user_keyword:
        query.add(Q(emp_no__icontains=user_keyword), Q.AND)
        query.add(Q(first_name__icontains=user_keyword), Q.OR)
        query.add(Q(last_name__icontains=user_keyword), Q.OR)
        query.add(Q(username__icontains=user_keyword), Q.OR)
        query.add(Q(email__icontains=user_keyword), Q.OR)
        members = CustomUser.objects.filter(query)

    for member in members:
        if member.is_active:
            member.is_active_text = "啟用"
            member.is_active_color = "bg-success"
        else:
            member.is_active_text = "停用"
            member.is_active_color = "bg-danger"

        if member.last_login:
            member.last_login_color = "bg-light"
        else:
            member.last_login_color = "bg-secondary"

    return render(request, template, locals())

# Ajax API
@login_required
def user_auth_api(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')

        user = CustomUser.objects.get(pk=pk)

        if request.POST.get('perm_pms'):
            add_permission(user, 'perm_pms')
        else:
            remove_permission(user, 'perm_pms')

        if request.POST.get('perm_ams'):
            add_permission(user, 'perm_ams')
        else:
            remove_permission(user, 'perm_ams')

        if request.POST.get('perm_workhour'):
            add_permission(user, 'perm_workhour')
        else:
            remove_permission(user, 'perm_workhour')

        if request.POST.get('perm_user_manage'):
            add_permission(user, 'perm_user_manage')
        else:
            remove_permission(user, 'perm_user_manage')

        if request.POST.get('perm_misc_apply'):
            add_permission(user, 'perm_misc_apply')
        else:
            remove_permission(user, 'perm_misc_apply')

        if request.POST.get('perm_svr_monitor'):
            add_permission(user, 'perm_svr_monitor')
        else:
            remove_permission(user, 'perm_svr_monitor')

        if request.POST.get('perm_stock'):
            add_permission(user, 'perm_stock')
        else:
            remove_permission(user, 'perm_stock')

        msg = "權限更新完成"
        return JsonResponse(msg, safe=False)


@login_required
def unit_list(request):
    template = 'users/unit_list.html'
    units = Unit.objects.all()
    return render(request, template, locals())


@login_required
def unit_sync(request):
    template = 'users/unit_list.html'

    if request.method == 'POST':
        sql = """SELECT OrganizationUnit.id AS unitId
                    ,Organization.id AS orgId
                    ,OrganizationUnit.organizationUnitName AS unitName
                    ,OrganizationUnit.organizationUnitType AS organizationUnitType
                    ,OrganizationUnitLevel.organizationUnitLevelName AS levelName
                    ,OrganizationUnit.validType AS isValid
                    ,Manager.id managerId
                    ,Manager.userName manager
                FROM OrganizationUnit
                INNER JOIN Organization ON OrganizationUnit.organizationOID = Organization.OID
                LEFT JOIN OrganizationUnitLevel ON OrganizationUnit.levelOID = OrganizationUnitLevel.OID
                LEFT JOIN Users Manager ON OrganizationUnit.managerOID = Manager.OID
                where OrganizationUnit.validType = 1
                ORDER BY unitId"""
        db = bpm_database()
        rows = db.select_sql_dict(sql)

        for row in rows:
            try:  # 更新
                if CustomUser.objects.filter(emp_no=row['managerId']).exists():
                    unit = Unit.objects.get(unitId=row['unitId'])
                    unit.unitName = row['unitName']
                    unit.manager = CustomUser.objects.get(emp_no=row['managerId'])
                    unit.isValid = row['isValid']
                    unit.update_by = request.user
                    unit.save()
                else:
                    print("{unitName} BPM尚未設定部門主管".format(unitName=row['unitName']))
            except:  # 新增
                unit = Unit(orgId=row['orgId'], unitId=row['unitId'], unitName=row['unitName'], isValid=row['isValid'])
                unit.manager = CustomUser.objects.get(emp_no=row['managerId'])
                unit.create_by = request.user
                unit.update_by = request.user
                unit.save()
        return redirect('unit_list')


@login_required
def user_sync(request):
    template = 'users/user_list.html'
    if request.method == 'POST':
        sql = """SELECT userId,main.userName,main.leaveDate,main.mailAddress,unitId,orgId,functionName,isMain,isnull(main.managerId,boss.id) managerId,levelName from (
                    SELECT Occupant.id AS userId
                                        ,Occupant.userName AS userName
                                        ,Occupant.leaveDate AS leaveDate
                                        ,Occupant.mailAddress
                                        ,OrganizationUnit.id AS unitId
                                        ,Organization.id AS orgId
                                        ,FunctionDefinition.functionDefinitionName AS functionName
                                        ,Functions.isMain AS isMain
                                        ,Manager.id AS managerId
                                        ,FunctionLevel.functionLevelName AS levelName
                                    FROM Functions
                                    INNER JOIN Users Occupant ON Functions.occupantOID = Occupant.OID
                                    INNER JOIN OrganizationUnit
                                    INNER JOIN Organization ON OrganizationUnit.organizationOID = Organization.OID ON Functions.organizationUnitOID = OrganizationUnit.OID INNER JOIN FunctionDefinition ON Functions.definitionOID = FunctionDefinition.OID LEFT JOIN FunctionLevel ON Functions.approvalLevelOID = FunctionLevel.OID LEFT JOIN Users Manager ON Functions.specifiedManagerOID = Manager.OID
                                    where isMain = 1 and OrganizationUnit.validType=1) main, OrganizationUnit unit, Users boss
                                    where main.unitId = unit.id and unit.managerOID = boss.OID
                                    order by userId"""
        db = bpm_database()
        rows = db.select_sql_dict(sql)

        for row in rows:
            try:
                # Noah有存在人員就更新資料
                if CustomUser.objects.filter(emp_no=row['userId']).exists():
                    user = CustomUser.objects.get(emp_no=row['userId'])
                    if row['leaveDate']:
                        user.is_active = False
                        user.save()
                    else:
                        user.unit = Unit.objects.get(unitId=row['unitId'])
                        if CustomUser.objects.filter(emp_no=row['managerId']).exists():
                            user.manager = CustomUser.objects.get(emp_no=row['managerId'])
                        user.update_by = request.user
                        user.email = row['mailAddress']
                        user.save()
                else:  # 不存在就新增
                    if not row['leaveDate']:
                        user = CustomUser(is_staff=1, is_active=1, user_type_id=2)
                        user.username = row['userName']
                        user.email = row['mailAddress']
                        user.emp_no = row['userId']
                        user.unit = Unit.objects.get(unitId=row['unitId'])
                        if CustomUser.objects.filter(emp_no=row['managerId']).exists():
                            user.manager = CustomUser.objects.get(emp_no=row['managerId'])
                        user.set_password(row['userId'])
                        user.create_by = request.user
                        user.update_by = request.user
                        user.save()
            except Exception as e:
                print(e)

        users = CustomUser.objects.filter(manager_id__isnull=True)
        for user in users:
            unit = Unit.objects.get(unitId=user.unit.unitId)
            user.manager = unit.manager
            user.create_by = request.user
            user.update_by = request.user
            user.save()
    return redirect('user_list')


def get_deptuser_api(request):
    if request.method == 'POST':
        unit = request.POST.get('unit')
        employees = CustomUser.objects.filter(unit=unit, is_active=True)
        html = """<option value="" selected>---------</option>"""

        for employee in employees:
            html += """<option value="{value}">{name}</option>""".format(value=employee.id, name=employee.username)
    return JsonResponse(html, safe=False)


def sign_up(request):
    plants = list(Plant.objects.values('id', 'plant_code', 'plant_name'))
    departments = list(Unit.objects.values('id', 'unitId', 'unitName', 'plant_id'))

    context = {
        'plants_json': json.dumps(plants),
        'departments_json': json.dumps(departments)
    }

    return render(request, 'users/signUp.html', context)


def sign_up_request(request):
    if request.method == 'POST':
        try:
            # Get form data
            dept_id = request.POST.get('dept_id')
            plant_id = request.POST.get('plant_id')
            emp_no = request.POST.get('empNo')
            name = request.POST.get('name')
            password = request.POST.get('password')

            # user_type = UserType.objects.get(type_id=3)
            user_type, created = UserType.objects.get_or_create(type_name="Wait For Approve",
                                                                defaults={"create_by_id": 1, "update_by_id": 1})

            # Check if user with same emp_no exists
            if CustomUser.objects.filter(emp_no=emp_no).exists():
                return JsonResponse({'status': 'error', 'message': 'Employee number already exists.'}, status=400)

            # Create new user
            new_user = CustomUser.objects.create_user(
                username=name,
                password=password,
                emp_no=emp_no,
                user_type=user_type,
                unit_id=dept_id
            )

            new_user.save()

            # Generate approval URL
            query_string = urlencode({'user_id': new_user.id, 'wecom': 'true'})
            approve_url = request.build_absolute_uri(f"{reverse('user_approving')}?{query_string}")

            dept = Unit.objects.get(pk=dept_id)
            plant = Plant.objects.get(pk=plant_id)

            # Construct message with approval link
            wecom_msg = f"""#### 📥 [NEW USER SIGN-UP REQUEST]
            **Name**: {name}  
            **Employee No**: {emp_no}
            **Plant**: {plant.plant_name}
            **Department**: {dept.unitName}  
            **Status**: ⏳ *Waiting for Approval*  

            👉 [Click here to Approve]({approve_url})
            """

            send_wecom_message(wecom_msg)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def signup_success(request):
    return render(request, 'users/signUp.html', {'show_success': True})


@login_required
def user_approving(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        is_wecom = request.GET.get('wecom') == 'true'
        try:
            user = CustomUser.objects.get(id=user_id)

            approve_type, _ = UserType.objects.get_or_create(
                type_name="Requester",
                defaults={"create_by_id": 1, "update_by_id": 1}
            )

            # Case for WeCom render
            if is_wecom:
                # Check if already approved
                if user.user_type == approve_type:
                    status_msg = "This account has already been approved."
                else:
                    # Approve the user
                    user.user_type = approve_type
                    user.is_staff = True
                    user.save()
                    status_msg = "Account approved successfully."
                return render(request, 'users/approveResponse.html', {'status_msg': status_msg})

            # Default non-WeCom logic
            user.user_type = approve_type
            user.is_staff = True
            user.save()
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


@login_required
def user_declining(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()  # Remove the user from the database

            return JsonResponse({'status': 'success'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


@login_required
def group_edit(request):
    group_id = request.GET.get('group_id')
    group_data = Group.objects.get(pk=group_id)

    is_membership = Member.objects.filter(group_id=group_id, member_id=request.user.pk)

    if not is_membership.exists():
        messages.error(request, "You are not in this group")
        return redirect('group_management')

    # Handle POST (form submission)
    if request.method == "POST":
        group_data.group_name = request.POST.get('group_name', '').strip()
        group_data.group_description = request.POST.get('group_desc', '').strip()
        group_data.visibility = bool(request.POST.get('visibility'))
        group_data.save()
        messages.success(request, "Group updated successfully.")

        return redirect(f'{request.path}?group_id={group_id}')

    group_member_ids = Member.objects.filter(group=group_data).values_list('member_id', flat=True)

    group_member_users = CustomUser.objects.filter(id__in=group_member_ids)
    users = CustomUser.objects.exclude(id__in=group_member_ids)

    plants = list(Plant.objects.values('id', 'plant_code', 'plant_name'))
    departments = list(Unit.objects.values('id', 'unitId', 'unitName', 'plant_id'))

    return render(request, 'group/edit.html', {
        **locals(),
        'plants_json': json.dumps(plants),
        'departments_json': json.dumps(departments)
    })


@login_required
def group_management(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group_description = request.POST.get('group_desc')
        visibility = request.POST.get('group_visibility') == 'on'
        group_image = request.FILES.get('group_image')

        # Save to DB (example)
        group = Group.objects.create(
            group_name=group_name,
            group_description=group_description,
            visibility=visibility,
            image=group_image,
            create_by=request.user,
            update_by=request.user
        )

        member = Member.objects.create(
            group=group,
            member=request.user,
            isJoin=True,
            create_by=request.user,
        )

        return redirect('group_management')

    group_ids = Member.objects.filter(member=request.user).values_list('group_id', flat=True)
    joined_groups = Group.objects.filter(id__in=group_ids).annotate(members=Count('member')).order_by('-create_at')
    public_groups = Group.objects.filter(visibility=True).exclude(id__in=group_ids).annotate(members=Count('member')).order_by('-create_at')
    all_groups = list(joined_groups) + list(public_groups)

    invitations = Member.objects.filter(
        member_id=request.user.pk,
        isJoin=False
    ).select_related('group', 'create_by')

    return render(request, 'group/management.html', {
        'all_groups': all_groups,
        'invitations': invitations
    })


@login_required
def send_invitation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group = Group.objects.get(pk=data['group_id'])
            user = CustomUser.objects.get(pk=data['user_id'])

            # Prevent duplicate invitations
            if Member.objects.filter(member=user, group=group).exists():
                return JsonResponse({'success': False, 'message': 'Already invited'})

            m = Member.objects.all()

            Member.objects.create(
                member=user,
                group=group,
                isJoin=True,
                create_by=request.user
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid method'})


@login_required
def respond_invitation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            invitation_id = data.get('invitation_id')
            action = data.get('action')  # 'accept' or 'decline'

            invitation = Member.objects.get(id=invitation_id, member=request.user)

            if action == 'accept':
                invitation.isJoin = True
                invitation.save()
            elif action == 'decline':
                invitation.delete()
            else:
                return JsonResponse({'success': False, 'message': 'Invalid action'})

            return JsonResponse({'success': True})
        except Member.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invitation not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def remove_member(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            member_id = data.get('member_id')
            group_id = data.get('group_id')

            membership = Member.objects.get(group_id=group_id, member_id=member_id)
            membership.delete()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def group_delete(request, group_id):
    group_qs = Group.objects.filter(id=group_id)

    if not group_qs.exists():
        messages.error(request, "Group not found.")
        return redirect('group_management')

    group = group_qs.first()

    if group.create_by != request.user:
        messages.error(request, "You are not authorized to delete this group.")
        return redirect('group_edit', group_id)

    if request.method == "POST":
        Member.objects.filter(group_id=group_id).delete()
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('group_management')

    return redirect('group_management')
