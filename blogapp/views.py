from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView,RedirectView,View
from blogapp.models import Post,Comment,PostLike,Requestsend,Friends,UserProfile
from blogapp.forms import PostForm,UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.text import slugify

User=get_user_model()
# Create your views here.


class UserSignUp(CreateView):
    form_class=UserCreateForm
    template_name='blogapp/signup.html'
    success_url=reverse_lazy('login')

class PostListView(LoginRequiredMixin,ListView):
    model=Post
    login_url='/login/'

    def get_queryset(self):
        queryset= super().get_queryset().filter(published_date__lte=timezone.now()).order_by('-published_date')
        following_list=Friends.objects.filter(following=self.request.user)
        new_following=[]
        for i in following_list:
            new_following.append(i.followers)
        return queryset.filter(author__in=new_following)

class MyPost(LoginRequiredMixin,ListView):
    model=Post
    login_url='/login/'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user).order_by('-created_date')


class PostDetailView(LoginRequiredMixin,DetailView):
    login_url='/login/'
    model=Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blogapp/post_detail.html'
    form_class=PostForm
    model=Post

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.author=User.objects.get(id=self.request.user.id)
        if '_publish' in self.request.POST:
            self.object.publish()
        self.object.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blogapp/post_detail.html'
    form_class=PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')


class PostDraftView(LoginRequiredMixin,ListView):
    login_url='/login/'
    template_name='blogapp/post_draft_list.html'
    model=Post

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user,published_date__isnull=True).order_by('-created_date')


@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def like_post(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        post=get_object_or_404(Post,pk=pk)
        try:
            likeobj=PostLike.objects.get(post=post,like_by=request.user)
            likeobj.delete()
        except:
            like=PostLike.objects.create(post=post,like_by=request.user)
            like.save()
        
        count=PostLike.objects.filter(post=post).count()
        return HttpResponse(count)
    else:
        return HttpResponse('Error')


class comment_create(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        post=Post.objects.get(id=pk)
        description = self.request.POST['textcomment']
        comment=Comment.objects.create(post=post,author=request.user.username,text=description)
        comment.save()
        return redirect('post_detail',pk=pk)


class SendRequest(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        sendby=self.request.user
        sendto=User.objects.get(pk=pk)
        frd_request=Requestsend.objects.create(sendby=sendby,sendto=sendto)
        frd_request.save()
        return redirect('profile',pk=pk)

class ConfirmRequest(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        following=User.objects.get(pk=pk)
        followers=self.request.user
        frds=Friends.objects.create(following=following,followers=followers)
        frds.save()
        frd_request=Requestsend.objects.get(sendby=following,sendto=followers)
        frd_request.req_confirmed=True
        frd_request.save()
        return redirect('requests')

class DeleteRequestByReciver(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        sendby=User.objects.get(pk=pk)
        sendto=self.request.user
        frd_request=Requestsend.objects.get(sendby=sendby,sendto=sendto)
        frd_request.delete()
        return redirect('requests')

class DeleteRequestBySender(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        sendto=User.objects.get(pk=pk)
        sendby=self.request.user
        frd_request=Requestsend.objects.get(sendby=sendby,sendto=sendto)
        frd_request.delete()
        return redirect('profile',pk=pk)

class Unfollow(LoginRequiredMixin,RedirectView):
    login_url='/login/'
    def get(self,request,pk):
        user1=self.request.user
        user2=User.objects.get(pk=pk)
        frd_request=Requestsend.objects.get(sendby=user1,sendto=user2)
        frd_request.delete()
        frds=Friends.objects.get(following=user1,followers=user2)
        frds.delete()
        return redirect('profile',pk=pk)


class UserProfileView(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=Post
    template_name='blogapp/profile.html'

    def get_queryset(self):
        userpost=User.objects.get(pk=self.kwargs['pk'])
        return super().get_queryset().filter(author=userpost,published_date__lte=timezone.now()).order_by('-published_date')

    def get_context_data(self):
        userpost=User.objects.get(pk=self.kwargs['pk'])
        context=super().get_context_data()
        context['username']=userpost.username
        context['email']=userpost.email
        context['postuserpk']=userpost.pk
        context['followes']=Friends.objects.filter(followers=userpost).count()
        context['following']=Friends.objects.filter(following=userpost).count()
        try:
            context['userprofile']=UserProfile.objects.get(user=userpost)
        except:
            context['userprofile']={'photo':'user.jpg','private_account':False}
        if userpost==self.request.user:
            context['requests']=Requestsend.objects.filter(sendto=self.request.user,req_confirmed=False).count()
        return context
    

class Profile(LoginRequiredMixin,RedirectView):
    def get(self,request,pk):
        pk=int(pk)
        if pk==self.request.user.pk:
            try:
                user=UserProfile.objects.get(user=User.objects.get(pk=pk))
                return redirect('userprofile',pk=pk)
            except:
                # return redirect('complateprofile',pk=pk)
                context=dict()
                context['img']='user.jpg'
                context['is_private']=False
                return render(request,'blogapp/profile_complate.html',context=context)
        return redirect('userprofile',pk=pk)

class AllRequests(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=Requestsend

    def get_queryset(self,*args,**kwargs):
        queryset=super().get_queryset(*args,**kwargs)
        return queryset.filter(sendto=self.request.user,req_confirmed=False)

class UpdateProfile(LoginRequiredMixin,RedirectView):

    def get(self,request,pk):
        photo=request.FILES['profile']
        is_private=request.POST.get('private')
        try:
            UserProfile.objects.get(user=self.request.user).delete()
            userprofile=UserProfile.objects.create(user=self.request.user,photo=photo,private_account=is_private)
            userprofile.save()
        except:
            if is_private:
                userprofile=UserProfile.objects.create(user=self.request.user,photo=photo,private_account=True)
                userprofile.save()
            else:
                userprofile=UserProfile.objects.create(user=self.request.user,photo=photo,private_account=False)
                userprofile.save()
        return redirect('userprofile',pk=self.request.user.pk)

class Showfollowers(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=Friends
    template_name='blogapp/showfollowers.html'

    def get_queryset(self,*args,**kwargs):
        queryset=super().get_queryset(*args,**kwargs)
        return queryset.filter(followers=self.request.user)

class Showfollowing(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=Friends
    template_name='blogapp/showfollowing.html'

    def get_queryset(self,*args,**kwargs):
        queryset=super().get_queryset(*args,**kwargs)
        return queryset.filter(following=self.request.user)

class EditProfile(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self,request):
        userprofile=UserProfile.objects.get(user=self.request.user)
        context=dict()
        context['img']=userprofile.photo
        context['is_private']=userprofile.private_account
        return render(request,'blogapp/profile_complate.html',context=context)

class Explore(ListView):
    model=Post
    template_name='blogapp/explore.html'
    
    def get_queryset(self,*args,**kwargs):
        queryset=super().get_queryset(*args,**kwargs).filter(published_date__lte=timezone.now()).order_by('-published_date')
        public_users=UserProfile.objects.filter(private_account=False)
        user_list=set()
        for i in public_users:
            user_list.add(User.objects.get(pk=i.user.pk))
        return queryset.filter(author__in=user_list)

class FindUser(RedirectView):
    def get(self,request):
        searchuser=slugify(str(self.request.GET.get('search')))
        all_users=User.objects.all()
        for i in all_users:
            if slugify(i.username)==searchuser:
                return redirect('userprofile',pk=i.pk)
        return HttpResponse("No User Found!")