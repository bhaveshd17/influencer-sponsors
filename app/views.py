import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import *
from .utils import *
from .send_email import sendMail
from app.decorators import unauthenticated_user, allowed_users
from app.forms import UserForm, InfluencerForm, InluencerPostForm

group_inf='Influencer'


def home(request):
    content = {}
    return render(request, 'home.html', content)

@login_required(login_url='login')
def viewinf(request,pk):
    content = {}
    try:
        view_obj = InfluencerPost.objects.filter(id=pk)
        content['view_obj'] = view_obj
    except Exception as e:
        print(e)
    return render(request, 'views_influencer.html',content)

    
@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def influencer_details(request):
    inf_form = InfluencerForm()
    if request.method == 'POST':
        inf_form = InfluencerForm(request.POST, request.FILES)
        if inf_form.is_valid():
            inf_form.save()
            social_media_list = json.loads(request.POST.get("social_media_list"))
            influencer = Influencer.objects.get(influencer_id=request.user.id)
            for i, data in social_media_list.items():
                inf_social = InfSocialMedia.objects.create(
                    influencer=influencer,
                    url=data['url'],
                    social_media=data['social_media'],
                    followers=data['follower']
                )
                inf_social.save()

            return redirect('home')
        else:
            return redirect('influencer_details')
    content = {'inf_form':inf_form, 'user':User.objects.get(username=request.user.username), 'for_loop':[1, 2, 3, 4, 5, 6]}
    return render(request, 'add_details.html', content)



@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def dashboardInf(request):
    posts = InfluencerPost.objects.all().order_by("-id")
    nav_field = [i.field for i in posts]
    saved_posts = InfSavePost.objects.filter(who_saved=Influencer.objects.get(influencer_id=request.user.id))
    saved_post_ls = [i.post.id for i in saved_posts]
    content = {
               'posts':posts,
               'nav_fields':list(set(nav_field)),
               'saved_post_ls':saved_post_ls
               }
    context_addition(request, content)
    return render(request, 'dashboard.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def dashboardFilter(request):
    data = request.GET.get('object')
    if data == 'ALL':
        posts = InfluencerPost.objects.all().order_by('-id')
    else:
        posts = InfluencerPost.objects.filter(field=data).order_by('-id')
    saved_posts = InfSavePost.objects.filter(who_saved=Influencer.objects.get(influencer_id=request.user.id))
    saved_post_ls = [i.post.id for i in saved_posts]
    content = {'posts':posts,
               'saved_post_ls':saved_post_ls,
               'id':request.user.id
               }
    template = render_to_string('ajax_temp/dashboard_filter.html', content)
    return JsonResponse({'data': template})


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def saved_post_view(request):
    saved_posts = InfSavePost.objects.filter(who_saved=Influencer.objects.get(influencer_id=request.user.id)).order_by("-id")
    saved_post_ls = [i.post.id for i in saved_posts]
    content = {'posts':saved_posts,
               'saved_post_ls':saved_post_ls,
               
               }
    context_addition(request, content)
    return render(request, 'saved_post_view.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def influencerPost(request):
    form = InluencerPostForm()
    if request.method == "POST":
        form = InluencerPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboardInf')
        else:
            return redirect('dashboardInf')

    content = {'form':form,'user':Influencer.objects.get(influencer_id=request.user.id),}
    context_addition(request, content)
    return render(request, 'influencer_post.html', content)

@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def save_post(request):
    data = json.loads(request.body)
    p_id = data['save_post_details']['post_id']
    post = InfluencerPost.objects.get(id=p_id)
    InfSavePost.objects.create(
        post=post,
        who_saved=Influencer.objects.get(influencer_id=request.user.id)
    )
    return JsonResponse('Done', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def remove_saved_post(request):
    data = json.loads(request.body)
    p_id = data['save_post_details']['post_id']
    post = InfluencerPost.objects.get(id=p_id)
    InfSavePost.objects.filter(
        post=post,
        who_saved=Influencer.objects.get(influencer_id=request.user.id)
    ).delete()
    return JsonResponse('Done', safe=False)



@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def profile(request):
    influencer = Influencer.objects.get(influencer_id=request.user.id)
    socialmedia = InfSocialMedia.objects.filter(influencer=influencer)
    content = {'socialmedia':socialmedia, 'influencer':influencer}
    return render(request, 'profile/profile.html', content)\

@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def edit_profile(request):
    influencer = Influencer.objects.get(influencer_id=request.user.id)
    influencer_form = InfluencerForm(instance=influencer)
    if request.method == 'POST':
        influencer_form = InfluencerForm(request.POST, request.FILES, instance=influencer)
        print(influencer_form)
        if influencer_form.is_valid():
            influencer_form.save()
            return redirect('profile')
    socialmedia = InfSocialMedia.objects.filter(influencer=influencer)
    content = {'socialmedia':socialmedia, 'influencer':influencer, 'influencer_form':influencer_form, 'user':User.objects.get(username=request.user.username)}
    return render(request, 'profile/edit_personal.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def personal_post(request):
    influencer = Influencer.objects.get(influencer_id=request.user.id)
    posts = InfluencerPost.objects.filter(influencer=influencer)
    content = {'influencer':influencer, 'posts':posts}
    return render(request, 'profile/post.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=[group_inf])
def delete_post(request, id):
    InfluencerPost.objects.get(id=id).delete()
    return redirect('personal_post')







@unauthenticated_user
def loginHandle(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 7)
            if user.is_staff:
                # messages.success(request, 'welcome back :)')
                return redirect('dashboardCmp')
            # messages.success(request, 'welcome back :)')
            return redirect('dashboardInf')

        else:
            messages.error(request, 'Wrong username or password')
            return redirect('login')
    content = {}
    return render(request, 'authentication/login.html', content)

@unauthenticated_user
def signupHandle(request):
    #influencer account creation
    if request.method == 'POST':
        email = request.POST.get("inf_email")
        password = request.POST.get("inf_pass")
        cpassword = request.POST.get("inf_cpass")
        first_name = request.POST.get("inf_name")
        username = request.POST.get("inf_username")
        if password == cpassword:
            if password_val(password):
                try:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name)
                    group = Group.objects.get(name='Influencer')
                    user.groups.add(group)
                    user.save()
                    login(request, user)
                    request.session.set_expiry(60 * 60 * 24 * 7)
                    messages.success(request, f"created")
                    sendMail(request, [user.email], {
						'p1': user.username,
						}, 'AddPAndWelcome', 'Welcome To Growspons')
                    return redirect('influencer_details')
                except:
                    messages.error(request, f"username already exist")
                    return redirect('signUp')
            else:
                messages.error(request, f"Password should contain atleast 6 digit, upper lower case and one symbol")
                return redirect('signUp')
        else:
            messages.error(request, f"Password and cpassword should be same")
            return redirect('signUp')
    content = {}
    return render(request, 'authentication/signup.html',content)

@unauthenticated_user
def companySignupHandle(request):
    email = request.POST.get("cmp_email")
    password = request.POST.get("cmp_pass")
    cpassword = request.POST.get("cmp_cpass")
    first_name = request.POST.get("cmp_name")
    if password == cpassword:
        if password_val(password):
            try:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name)
                group = Group.objects.get(name='Company')
                user.groups.add(group)
                user.is_staff=True
                user.save()
                login(request, user)
                request.session.set_expiry(60 * 60 * 24 * 7)
                messages.success(request, f"created")
                return redirect('dashboardCmp')
            except:
                messages.error(request, f"username already exist")
                return redirect('signUp')

        else:
            messages.error(request, f"Password should contain atleast 6 digit, upper lower case and one symbol")
            return redirect('signUp')
    else:
        messages.error(request, f"Password and confirm password should be same")
        return redirect('signUp')


def handleLogout(request):
    logout(request)
    return redirect('login')
