from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post
from .forms import PostForm


def _to_int_safe(str_obj):
    try:
        res = int(str_obj)
    except Exception:
        res = str_obj
    return res


def post_list(request):
    # posts = Post.objects.filter(publish__lte=timezone.now()).order_by('publish')
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page_num = _to_int_safe(request.GET.get('page'))
    if page_num is None or not isinstance(page_num, (int,)):
        # if page is not an integer deliver the first page
        page_num = 1
    try:
        posts = paginator.page(page_num)
    except EmptyPage:
        # if page is out of range deliver last page of results
        page_num = paginator.num_pages
        posts = paginator.page(page_num)
    if posts.has_next():
        sb_title = "Also see:"
    else:
        sb_title = "My Blog"

    return render(request, 'blog/post/list.html', {'sb_title': sb_title,
                                                   'page_num': page_num,
                                                   'posts': posts})


# def post_detail(request, pk):
def post_detail(request, year, month, day, post):
    # Post.objects.get(pk=pk)
    # post = get_object_or_404(Post, pk=pk)
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # return render(request, 'blog/post_detail.html', {'post':post})
    return render(request, 'blog/post/detail.html', {'post': post})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    # posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    posts = Post.objects.filter(publish__isnull=True).order_by('created')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post._publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
