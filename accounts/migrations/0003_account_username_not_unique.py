from django.db import migrations, models
import django.contrib.auth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(
                error_messages={
                    'unique': 'A user with that username already exists.',
                },
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                unique=False,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='username',
            ),
        ),
    ]
