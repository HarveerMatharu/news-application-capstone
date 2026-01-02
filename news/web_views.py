"""
Web views for article management with templates.

These views provide a web interface for editors to review and approve articles,
alongside the existing API views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from .models import Article, Publisher, Newsletter, User
from django.db import models


def is_editor(user):
    """Check if user is an editor."""
    return user.is_authenticated and user.role == 'EDITOR'


def is_journalist(user):
    """Check if user is a journalist."""
    return user.is_authenticated and user.role == 'JOURNALIST'


def is_editor_or_journalist(user):
    """Check if user is editor or journalist."""
    return (
        user.is_authenticated and
        user.role in ['EDITOR', 'JOURNALIST']
    )


def logout_view(request):
    """Custom logout view that handles both GET and POST requests."""
    logout(request)
    return redirect('news:article_list')


@login_required
def article_list(request):
    """
    Display list of articles.

    Readers see only approved articles.
    Editors and Journalists see all articles.
    """
    if request.user.role == 'READER':
        articles = Article.objects.filter(approved=True)
    else:
        articles = Article.objects.all()

    return render(request, 'news/article_list.html', {
        'articles': articles
    })


@login_required
@user_passes_test(is_editor)
def pending_articles(request):
    """Display articles pending approval (editors only)."""
    articles = Article.objects.filter(approved=False)

    return render(request, 'news/pending_articles.html', {
        'articles': articles
    })


@login_required
def article_detail(request, pk):
    """Display article detail."""
    article = get_object_or_404(Article, pk=pk)

    # Readers can only view approved articles
    if request.user.role == 'READER' and not article.approved:
        messages.error(
            request,
            'You do not have permission to view this article.'
        )
        return redirect('news:article_list')

    return render(request, 'news/article_detail.html', {
        'article': article
    })


@login_required
@user_passes_test(is_editor)
def approve_article(request, pk):
    """
    Approve an article (editors only).

    This triggers the post_save signal which sends emails and posts to Twitter.
    """
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)

        if article.approved:
            messages.warning(request, 'Article is already approved.')
        else:
            article.approved = True
            article.save()  # This triggers the post_save signal
            messages.success(
                request,
                f'Article "{article.title}" has been approved. '
                f'Notifications sent to subscribers.'
            )

        return redirect('news:article_detail', pk=pk)

    return redirect('news:article_list')


@login_required
@user_passes_test(is_journalist)
def article_create(request):
    """Create a new article (journalists only)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        publisher_id = request.POST.get('publisher')

        # Validate input
        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return redirect('news:article_create')

        # Create article
        article = Article(
            title=title,
            content=content,
            author=request.user,
            approved=False
        )

        # Add publisher if selected
        if publisher_id:
            try:
                publisher = Publisher.objects.get(pk=publisher_id)
                article.publisher = publisher
            except Publisher.DoesNotExist:
                pass

        article.save()

        messages.success(
            request,
            f'Article "{article.title}" created successfully. '
            f'Waiting for editor approval.'
        )
        return redirect('news:article_detail', pk=article.id)

    # GET request - show form
    publishers = Publisher.objects.all()
    return render(request, 'news/article_form.html', {
        'publishers': publishers
    })


@login_required
@user_passes_test(is_editor_or_journalist)
def article_edit(request, pk):
    """Edit an article (editors and article author only)."""
    article = get_object_or_404(Article, pk=pk)

    # Check permission - editors or article author
    if request.user.role != 'EDITOR' and request.user != article.author:
        messages.error(
            request,
            'You do not have permission to edit this article.'
        )
        return redirect('news:article_detail', pk=pk)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        publisher_id = request.POST.get('publisher')

        # Update publisher
        if publisher_id:
            try:
                article.publisher = Publisher.objects.get(pk=publisher_id)
            except Publisher.DoesNotExist:
                article.publisher = None
        else:
            article.publisher = None

        article.save()

        messages.success(
            request,
            f'Article "{article.title}" updated successfully.'
        )
        return redirect('news:article_detail', pk=pk)

    # GET request - show form
    publishers = Publisher.objects.all()
    return render(request, 'news/article_form.html', {
        'article': article,
        'publishers': publishers
    })


@login_required
@user_passes_test(is_editor_or_journalist)
def article_delete(request, pk):
    """Delete an article (editors and article author only)."""
    article = get_object_or_404(Article, pk=pk)

    # Check permission - editors or article author
    if request.user.role != 'EDITOR' and request.user != article.author:
        messages.error(
            request,
            'You do not have permission to delete this article.'
        )
        return redirect('news:article_detail', pk=pk)

    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'Article "{title}" deleted successfully.')
        return redirect('news:article_list')

    return redirect('news:article_detail', pk=pk)


"""
Newsletter view functions.

"""


@login_required
def newsletter_list(request):
    """Display list of all newsletters."""
    newsletters = Newsletter.objects.all().order_by('-created_at')

    return render(request, 'news/newsletter_list.html', {
        'newsletters': newsletters
    })


@login_required
def newsletter_detail(request, pk):
    """Display newsletter detail with all articles."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    return render(request, 'news/newsletter_detail.html', {
        'newsletter': newsletter
    })


@login_required
@user_passes_test(is_editor_or_journalist)
def newsletter_create(request):
    """Create a new newsletter (journalists and editors only)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        article_ids = request.POST.getlist('articles')

        # Validate input
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('news:newsletter_create')

        # Create newsletter
        newsletter = Newsletter(
            title=title,
            description=description,
            author=request.user
        )
        newsletter.save()

        # Add selected articles
        if article_ids:
            articles = Article.objects.filter(id__in=article_ids)
            newsletter.articles.set(articles)

        messages.success(
            request,
            f'Newsletter "{newsletter.title}" created successfully.'
        )
        return redirect('news:newsletter_detail', pk=newsletter.id)

    # GET request - show form
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/newsletter_form.html', {
        'articles': articles
    })


@login_required
@user_passes_test(is_editor_or_journalist)
def newsletter_edit(request, pk):
    """Edit a newsletter (editors and newsletter author only)."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # Check permission - editors or newsletter author
    if request.user.role != 'EDITOR' and request.user != newsletter.author:
        messages.error(
            request,
            'You do not have permission to edit this newsletter.'
        )
        return redirect('news:newsletter_detail', pk=pk)

    if request.method == 'POST':
        newsletter.title = request.POST.get('title')
        newsletter.description = request.POST.get('description')
        article_ids = request.POST.getlist('articles')

        newsletter.save()

        # Update articles
        if article_ids:
            articles = Article.objects.filter(id__in=article_ids)
            newsletter.articles.set(articles)
        else:
            newsletter.articles.clear()

        messages.success(
            request,
            f'Newsletter "{newsletter.title}" updated successfully.'
        )
        return redirect('news:newsletter_detail', pk=pk)

    # GET request - show form
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/newsletter_form.html', {
        'newsletter': newsletter,
        'articles': articles
    })


@login_required
@user_passes_test(is_editor_or_journalist)
def newsletter_delete(request, pk):
    """Delete a newsletter (editors and newsletter author only)."""
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # Check permission - editors or newsletter author
    if request.user.role != 'EDITOR' and request.user != newsletter.author:
        messages.error(
            request,
            'You do not have permission to delete this newsletter.'
        )
        return redirect('news:newsletter_detail', pk=pk)

    if request.method == 'POST':
        title = newsletter.title
        newsletter.delete()
        messages.success(
            request,
            f'Newsletter "{title}" deleted successfully.'
        )
        return redirect('news:newsletter_list')

    return redirect('news:newsletter_detail', pk=pk)


"""
Subscription and Publisher view functions

"""


def is_reader(user):
    """Check if user is a reader."""
    return user.is_authenticated and user.role == 'READER'


@login_required
def publisher_list(request):
    """Display list of all publishers."""
    publishers = Publisher.objects.all().order_by('name')

    return render(request, 'news/publisher_list.html', {
        'publishers': publishers
    })


@login_required
def publisher_detail(request, pk):
    """Display publisher detail with articles and subscribe button."""
    publisher = get_object_or_404(Publisher, pk=pk)

    # Get articles from this publisher
    if request.user.role == 'READER':
        articles = Article.objects.filter(
            publisher=publisher,
            approved=True
        ).order_by('-created_at')[:10]
    else:
        articles = Article.objects.filter(
            publisher=publisher
        ).order_by('-created_at')[:10]

    # Check if user is subscribed
    is_subscribed = False
    if request.user.role == 'READER':
        is_subscribed = publisher in request.user.subscribed_publishers.all()

    return render(request, 'news/publisher_detail.html', {
        'publisher': publisher,
        'articles': articles,
        'is_subscribed': is_subscribed
    })


@login_required
@user_passes_test(is_reader)
def subscribe_publisher(request, pk):
    """Subscribe to a publisher (readers only)."""
    if request.method == 'POST':
        publisher = get_object_or_404(Publisher, pk=pk)

        if publisher not in request.user.subscribed_publishers.all():
            request.user.subscribed_publishers.add(publisher)
            messages.success(
                request,
                f'You are now subscribed to {publisher.name}.'
            )
        else:
            messages.info(
                request,
                f'You are already subscribed to {publisher.name}.'
            )

        return redirect('news:publisher_detail', pk=pk)

    return redirect('news:publisher_list')


@login_required
@user_passes_test(is_reader)
def unsubscribe_publisher(request, pk):
    """Unsubscribe from a publisher (readers only)."""
    if request.method == 'POST':
        publisher = get_object_or_404(Publisher, pk=pk)

        if publisher in request.user.subscribed_publishers.all():
            request.user.subscribed_publishers.remove(publisher)
            messages.success(
                request,
                f'You have unsubscribed from {publisher.name}.'
            )
        else:
            messages.info(
                request,
                f'You were not subscribed to {publisher.name}.'
            )

        # Check if redirecting from subscriptions page or publisher page
        next_url = request.POST.get('next', 'news:publisher_detail')
        if next_url == 'subscriptions':
            return redirect('news:my_subscriptions')
        else:
            return redirect('news:publisher_detail', pk=pk)

    return redirect('news:publisher_list')


@login_required
@user_passes_test(is_reader)
def subscribe_journalist(request, pk):
    """Subscribe to a journalist (readers only)."""
    if request.method == 'POST':
        journalist = get_object_or_404(User, pk=pk, role='JOURNALIST')

        if journalist not in request.user.subscribed_journalists.all():
            request.user.subscribed_journalists.add(journalist)
            messages.success(
                request,
                f'You are now following {journalist.get_full_name() or journalist.username}.'
            )
        else:
            messages.info(
                request,
                f'You are already following {journalist.get_full_name() or journalist.username}.'
            )

        # Redirect back to article or subscriptions page
        next_url = request.POST.get('next', 'article')
        if next_url == 'subscriptions':
            return redirect('news:my_subscriptions')
        else:
            # Redirect to referring page or article list
            return redirect(request.META.get('HTTP_REFERER', 'news:article_list'))

    return redirect('news:article_list')


@login_required
@user_passes_test(is_reader)
def unsubscribe_journalist(request, pk):
    """Unsubscribe from a journalist (readers only)."""
    if request.method == 'POST':
        journalist = get_object_or_404(User, pk=pk, role='JOURNALIST')

        if journalist in request.user.subscribed_journalists.all():
            request.user.subscribed_journalists.remove(journalist)
            messages.success(
                request,
                f'You have unfollowed {journalist.get_full_name() or journalist.username}.'
            )
        else:
            messages.info(
                request,
                f'You were not following {journalist.get_full_name() or journalist.username}.'
            )

        return redirect('news:my_subscriptions')

    return redirect('news:article_list')


@login_required
@user_passes_test(is_reader)
def my_subscriptions(request):
    """Display user's subscriptions (readers only)."""
    subscribed_publishers = request.user.subscribed_publishers.all()
    subscribed_journalists = request.user.subscribed_journalists.all()

    return render(request, 'news/my_subscriptions.html', {
        'subscribed_publishers': subscribed_publishers,
        'subscribed_journalists': subscribed_journalists
    })


@login_required
@user_passes_test(is_reader)
def subscribed_articles(request):
    """Display articles from user's subscriptions (readers only)."""
    # Get subscribed publishers and journalists
    subscribed_publishers = request.user.subscribed_publishers.all()
    subscribed_journalists = request.user.subscribed_journalists.all()

    # Get articles from subscribed publishers or journalists
    articles = Article.objects.filter(
        approved=True
    ).filter(
        models.Q(publisher__in=subscribed_publishers) |
        models.Q(author__in=subscribed_journalists)
    ).distinct().order_by('-created_at')

    return render(request, 'news/subscribed_articles.html', {
        'articles': articles,
        'subscribed_publishers': subscribed_publishers,
        'subscribed_journalists': subscribed_journalists
    })
