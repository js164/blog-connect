from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView
from blogapp.models import Post,Comment,PostLike
from blogapp.forms import PostForm,UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your views here.

class AboutView(TemplateView):
    template_name='blogapp/about.html'

class UserSignUp(CreateView):
    form_class=UserCreateForm
    template_name='blogapp/signup.html'
    success_url=reverse_lazy('login')

class PostListView(ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class MyPost(LoginRequiredMixin,ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_date')


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
        return Post.objects.filter(author=self.request.user,published_date__isnull=True).order_by('created_date')


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


def comment_create(request,pk):
    if request.method=='POST':
        post=Post.objects.get(id=pk)
        description = request.POST['textcomment']
        comment=Comment.objects.create(post=post,author=request.user.username,text=description)
        comment.save()
        return redirect('post_detail',pk=pk)
    else:
        return HttpResponse("Error")