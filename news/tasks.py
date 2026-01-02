"""
Tasks module for handling email notifications and X (Twitter) posting.

These functions are called by the Article post_save signal when an article
is approved by an editor.
"""

import requests
from django.core.mail import send_mass_mail
from django.conf import settings


def send_article_notifications(article):
    """
    Send email notifications to all subscribers when article is approved.

    Args:
        article: Approved Article instance

    Returns:
        None
    """
    from .models import User

    subscribers = get_article_subscribers(article)

    if not subscribers:
        return

    # Prepare email content
    subject = f"New Article: {article.title}"

    # Create plain text message
    author_name = article.author.get_full_name() or article.author.username
    content_preview = article.content[:200]
    article_url = f"{settings.SITE_URL}/articles/{article.id}/"

    if article.publisher:
        subscription_info = f"the {article.publisher.name}"
    else:
        subscription_info = article.author.username

    message = f"""
New Article Published!

Title: {article.title}
Author: {author_name}

{content_preview}...

Read the full article at: {article_url}

---
You received this email because you subscribed to {subscription_info}.
    """

    # Create list of email tuples
    # Format: (subject, message, from_email, recipient_list)
    emails = []
    for subscriber in subscribers:
        if subscriber.email:
            emails.append((
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            ))

    # Send all emails
    try:
        send_mass_mail(tuple(emails), fail_silently=False)
        print(f"Sent {len(emails)} notification emails for: {article.title}")
    except Exception as e:
        print(f"Error sending emails: {str(e)}")


def get_article_subscribers(article):
    """
    Get all subscribers for an article based on publisher or author.

    Args:
        article: Article instance

    Returns:
        QuerySet of User objects who are subscribed to this article's
        publisher or journalist author
    """
    from .models import User

    subscribers = User.objects.none()

    # If article has a publisher, get publisher subscribers
    if article.publisher:
        subscribers = article.publisher.subscribers.filter(role='READER')

    # Get subscribers to the journalist/author
    journalist_subscribers = User.objects.filter(
        subscribed_journalists=article.author,
        role='READER'
    )

    # Combine and remove duplicates
    subscribers = (subscribers | journalist_subscribers).distinct()

    return subscribers


def post_to_twitter(article):
    """
    Post article to X (formerly Twitter) when approved.

    Args:
        article: Approved Article instance

    Returns:
        dict: Response from Twitter API if successful, None otherwise
    """
    # Check if Twitter credentials are configured
    if not hasattr(settings, 'TWITTER_BEARER_TOKEN'):
        print("Twitter API credentials not configured. Skipping tweet.")
        return None

    if not settings.TWITTER_BEARER_TOKEN:
        print("Twitter API credentials not configured. Skipping tweet.")
        return None

    # Prepare tweet content (X has 280 character limit)
    author_name = article.author.get_full_name() or article.author.username
    article_url = f"{settings.SITE_URL}/articles/{article.id}/"

    tweet_text = f"""
NEW: {article.title}

By {author_name}

Read more: {article_url}
"""

    # Truncate if too long
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."

    # X API v2 endpoint
    url = "https://api.twitter.com/2/tweets"

    # Prepare headers with Bearer token
    headers = {
        "Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    # Prepare payload
    payload = {
        "text": tweet_text
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 201:
            print(f"Successfully posted to X (Twitter): {article.title}")
            return response.json()
        else:
            print(f"Failed to post to X. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error posting to X (Twitter): {str(e)}")
        return None


def post_to_twitter_mock(article):
    """
    Mock version of post_to_twitter for testing.

    Use this in tests or when Twitter API is not available.

    Args:
        article: Approved Article instance

    Returns:
        dict: Mock response data
    """
    tweet_text = f"NEW: {article.title} by {article.author.username}"
    print(f"[MOCK TWEET] {tweet_text}")
    return {"mock": True, "text": tweet_text}
