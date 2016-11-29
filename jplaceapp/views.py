from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.db.models import Q
from datetime import datetime, timedelta
from .forms import *


def home(request):
    title="Welcome to Jplace"
    shared_testimonies = SharedTestimonies.objects.order_by('-date')[:10]
    context={
        "title":title,
        "shared_testimonies": shared_testimonies
    }
    return render(request,"home.html",context)



def testimony_detail(request, id=None):
    instance=get_object_or_404(Testimonies,id=id)
    #if instance.draft or instance.publish > timezone.now().date():
       # if not request.user.is_staff or not request.user.is_superuser:
            #raise Http404
    context={
        "title":instance.title,
        "instance":instance,
    }
    return render(request,"testimony_detail.html",context)




@login_required(login_url='/')
def testimony_vote_page(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            shared_testimonies = SharedTestimonies.objects.get(id=id)
            user_voted = shared_testimonies.users_voted.filter(username=request.user.username)
            if not user_voted:
                shared_testimonies.votes += 1
                shared_testimonies.users_voted.add(request.user)
                shared_testimonies.save()
        except ObjectDoesNotExist:
            raise Http404('Testimony not found.')
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')



def user_page(request, username):
    user = get_object_or_404(User, username=username)
    testimony = user.testimonies_set.order_by('-id')
    is_friend = Friendship.objects.filter(from_friend=request.user,to_friend=user )

    context={
        'testimony': testimony,
        'username': username,
         'show_tags': True,
        'show_edit': username == request.user.username,
         'is_friend': is_friend,
        }
    return render(request,"user_page.html",context)




def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    testimony = tag.testimony.order_by('-id')
    context={
        'testimony': testimony,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True,
    }
    return render(request,'tag_page.html', context)



def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].testimony.count()
    for tag in tags:
        tag.count = tag.testimony.count()
        if tag.count < min_count:
            min_count = tag.count
            if max_count < tag.count:
                max_count = tag.count
     # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
        # Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range)
    context= {
        'tags': tags
    }
    return render(request,'tag_cloud_page.html', context)

'''

def _testimonies_save(request, form):
    testimony, dummy = My_testimony.objects.get_or_create(
        testimony=form.cleaned_data['testimony']
    )
    # Create or get bookmark.
    testimonies, created = Testimonies.objects.get_or_create(
        user=request.user,
        testimonies=testimony,
    )
    # Update bookmark title.
    testimonies.title = form.cleaned_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        testimonies.tag_set.clear()
    # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        testimonies.tag_set.add(tag)

     # Share on the main page if requested.
    if form.cleaned_data['share']:
        shared_testimony, created = SharedTestimonies.objects.get_or_create(testimony=testimony)
        if created:
            shared_testimony.users_voted.add(request.user)
            shared_testimony.save()
    # Save bookmark to database.
    testimonies.save()
    return testimonies

'''



def _testimonies_save(request, form):
    testimony, dummy = My_testimony.objects.get_or_create(
        testimony=form.cleaned_data['testimony']
    )
    # Create or get testimonies.
    testimonies, created = Testimonies.objects.get_or_create(
        user=request.user,
        testimonies=testimony,
    )
    # Update bookmark title.
    testimonies.title = form.cleaned_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        testimonies.tag_set.clear()
    # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        testimonies.tag_set.add(tag)

     # Share on the main page if requested.
    if form.cleaned_data['share']:
        shared_testimony, created = SharedTestimonies.objects.get_or_create(testimony=testimony)
        if created:
            shared_testimony.users_voted.add(request.user)
            shared_testimony.save()
    # Save bookmark to database.
    testimonies.save()
    return testimonies




@csrf_exempt
@login_required(login_url='/')
def testimonies_save_page(request):
    if request.method == 'POST':
        form = TestimonySaveForm(request.POST)
        if form.is_valid():
            testimonies = _testimonies_save(request, form)
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    elif request.GET.has_key('url'):
        url = request.GET['url']
        title = ''
        tags = ''
        try:
            my_testimony = My_testimony.objects.get(url=url)
            testimonies = Testimonies.objects.get(
                my_testimony=my_testimony,
                user=request.user
            )
            title = Testimonies.title
            tags = ' '.join(
                tag.name for tag in Testimonies.tag_set.all()
            )
        except:
            pass
        form = TestimonySaveForm({
            'url': url,
            'title': title,
            'tags': tags
        })
    else:
        form =TestimonySaveForm()
    context={
            'form': form
        }
    return render(request, 'testimonies_save.html', context)

def testimonies_page(request, testimonies_id):
    shared_testimonies = get_object_or_404(SharedTestimonies, id=testimonies_id)
    context={
        'shared_testimonies': shared_testimonies,
    }
    return render(request, 'testimonies_page.html', context)

'''
@csrf_exempt
@login_required(login_url='/')
def testimonies_save_page(request):
    if request.method == 'POST':
        form = TestimonySaveForm(request.POST)
        if form.is_valid():
            testimony, dummy = My_testimony.objects.get_or_create(
                testimony=form.cleaned_data['testimony']
            )
            # Create or get bookmark.
            testimonies, created = Testimonies.objects.get_or_create(
                user=request.user,
                testimonies=testimony,
            )
            # Update bookmark title.
            testimonies.title = form.cleaned_data['title']
            # If the bookmark is being updated, clear old tag list.
            if not created:
                testimonies.tag_set.clear()
             # Create new tag list.
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                testimonies.tag_set.add(tag)
                # Save bookmark to database.
            testimonies.save()
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
        form =TestimonySaveForm()
    variables = RequestContext(request, {
            'form': form
        })
    return render_to_response('testimonies_save.html', variables)
'''






def search_page(request):
    form = SearchForm()
    testimony = []
    show_results = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
                form = SearchForm({'query': query})
                testimony = Testimonies.objects.filter(q)[:10]
    context = {
        'form': form,
        'testimony': testimony,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True,
               }

    if request.GET.has_key('ajax'):
        return render(request, 'testimony_list.html', context)
    else:
        return render(request, 'search.html', context)



def popular_page(request):
    today = datetime.today()
    yesterday = today - timedelta(1)
    shared_testimonies = SharedTestimonies.objects.filter(date__gt=yesterday )
    shared_testimonies = shared_testimonies.order_by('-votes')[:10]
    context= {
        'shared_testimonies': shared_testimonies
    }
    return render(request, 'popular_page.html', context)


def friends_page(request, username):
    user = get_object_or_404(User, username=username)
    friends =[friendship.to_friend for friendship in user.friend_set.all()]
    friend_testimonies = Testimonies.objects.filter(user__in=friends).order_by('-id')
    context={
        'username': username,
        'friends': friends,
        'testimonies': friend_testimonies[:10],
        'show_tags': True,
        'show_user': True
    }
    return render(request, 'friends_page.html', context)


@login_required
def friend_add(request):
    if request.GET.has_key('username'):
        friend =get_object_or_404(User, username=request.GET['username'])
        friendship = Friendship(from_friend=request.user,to_friend=friend)
        friendship.save()
        return HttpResponseRedirect('/bookmarks/friends/%s/' % request.user.username)
    else:
        raise Http404

@csrf_exempt
@login_required
def friend_invite(request):
    if request.method == 'POST':
        form = FriendInviteForm(request.POST)
        if form.is_valid():
            invitation = Invitation(name = form.cleaned_data['name'],
                                    email = form.cleaned_data['email'],
                                    code = User.objects.make_random_password(20),
                                    sender = request.user
                                    )
            invitation.save()
            invitation.send()
            return HttpResponseRedirect('friend/invite/')
    else:
        form = FriendInviteForm()
    context={
                'form': form
    }
    return render(request,'friend_invite.html', context)


def friend_accept(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('register/')