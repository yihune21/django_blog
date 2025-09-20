from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post

class LatestPostsFeed(Feed):
    title = "My Blog - Latest Posts"
    link = "/"
    description = "Updates on latest blog posts"

    def items(self):
        return Post.objects.filter(published=True).order_by('-created_on')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt if item.excerpt else item.body[:200]

    def item_link(self, item):
        return reverse('blog_detail', args=[item.pk])