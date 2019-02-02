from django.db import models

# Create your models here.
LEVELS = (
    (BACHELOR, 'Bachelor'),
    (MASTER, 'Master'),
    (PHD, 'PHD'),
)

SEMESTER = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
)

YEARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField( max_length = 100, null = True )
    last_name = models.CharField( max_length = 100, null = True )
    picture = models.ImageField( null = True, blank = True, default = 'no-img.png' )
    website = models.URLField( max_length = 100, null = True, blank = True )
    email = models.EmailField( max_length = 100, null = True )
    phone = models.CharField( max_length = 100, null = True )
    program = models.CharField(max_length = 20, choices=LEVELS,default=BACHELOR, null = True )
    country = models.CharField( max_length = 100, null = True )
    city = models.CharField( max_length = 100, null = True )
    course_teacher = models.CharField( max_length = 100, related_name = 'course_teacher', blank = True )
    years = models.IntegerField( choices = YEARS, default = 1 )
    semester = models.IntegerField( choices = SEMESTER, default = 1 )
    level = models.CharField( max_length = 100, choices = LEVELS, default = 1 )


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    def get_website(self):
        if self.website[0:4] != 'http':
            return 'http://' + self.website
        else:
            return self.website

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Student'

