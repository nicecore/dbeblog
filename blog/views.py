from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
from .forms import CommentForm
from .models import Post, Comment


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    ### Comments
    # Get all comments associated with post grabbed above
    comments = post.comments.filter(active=True)
    # If a comment has been posted
    if request.method == 'POST':
        # Populate CommentForm() with data from POST request
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign current post to the comment
            new_comment.post = post
            # Save comment
            new_comment.save()
    # If a GET request and we need an empty form
    else:
        comment_form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {'post': post, 'comments': comments, 'comment_form': comment_form},
    )




def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'page': page, 'posts': posts, 'tag': tag}
    )
