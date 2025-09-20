# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    """Generate unique slugs for existing posts"""
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        base_slug = slugify(post.title) if post.title else f'post-{post.id}'
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exclude(id=post.id).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        post.slug = slug
        post.save()

def reverse_slugs(apps, schema_editor):
    """Reverse migration"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False),
        ),
        # First add slug field without unique constraint
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=200, unique=False),
            preserve_default=False,
        ),
        # Generate unique slugs for existing posts
        migrations.RunPython(generate_unique_slugs, reverse_slugs),
        # Then alter the field to add unique constraint
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]