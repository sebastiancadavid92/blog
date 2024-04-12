# Generated by Django 5.0.3 on 2024-04-10 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0004_rename_permission_category_post_permissioncategorypost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryname',
            field=models.CharField(blank=True, choices=[('PUBLIC', 'Public'), ('AUTHENTICATED', 'Authenticated'), ('TEAM', 'Team'), ('AUTHOR', 'Author')], null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='permissionname',
            field=models.CharField(blank=True, choices=[('READ_ONLY', 'Read Only'), ('EDIT', 'Read and Edit'), ('NONE', 'None')], unique=True),
        ),
    ]
