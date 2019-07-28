from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


# using class based views instead of function, going to be detail view
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


# create a view to user's specificposts
class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


# view for individual post, going to be detail view
class PostDetailView(DetailView):
    model = Post


# view to create a new post,provides fields for form
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# view to update a users post,provides fields for form
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# delete post,
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):

    return render(request, "blog/about.html", {"title": "About"})


# '''create a home function that defines our home route that takes a
#     request argument and returns a HttpResponse'''

# '''create an about function that handles the logic for our about page that takes
#     request argument and returns a HttpResponse'''

# After modifying our routes to return render, we can delete the HttpResponse import since we are no longer using it.
# The render function also returns a HttpResponse
