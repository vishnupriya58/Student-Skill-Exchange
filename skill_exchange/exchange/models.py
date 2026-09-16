from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    education = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Designing', 'Designing'),
        ('Languages', 'Languages'),
        ('Photography', 'Photography'),
        ('Music', 'Music'),
        ('Marketing', 'Marketing'),
        ('Academics', 'Academics'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)



class StudentSkill(models.Model):
    SKILL_TYPE_CHOICES = [
        ('teach', 'Can Teach'),
        ('learn', 'Want to Learn'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    skill_type = models.CharField(
        max_length=10,
        choices=SKILL_TYPE_CHOICES
    )



class ExchangeRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )

    receiver = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    

class Message(models.Model):

    sender = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )


class Session(models.Model):

  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

  sender = models.ForeignKey(
    StudentProfile,
    on_delete=models.CASCADE,
    related_name='sent_sessions'
)

  receiver = models.ForeignKey(
    StudentProfile,
    on_delete=models.CASCADE,
    related_name='received_sessions'
)

  title = models.CharField(
    max_length=200
)

  description = models.TextField(
    blank=True
)

  session_date = models.DateField()

  session_time = models.TimeField()

  duration = models.PositiveIntegerField(
    help_text="Duration in minutes"
)

  meeting_link = models.URLField(
    blank=True
)

  status = models.CharField(
    max_length=10,
    choices=STATUS_CHOICES,
    default='pending'
)

  created_at = models.DateTimeField(
    auto_now_add=True
)



class Rating(models.Model):
    reviewer = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )
    receiver = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='received_ratings'
    )
    rating = models.PositiveIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    
class Block(models.Model):
    blocker = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='blocked_students'
    )
    blocked = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.blocker.user.username} blocked {self.blocked.user.username}"
class Report(models.Model):
    reporter = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    reported = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='reports_received'
    )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    

    

