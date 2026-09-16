from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import StudentProfile,Skill,StudentSkill,ExchangeRequest,Message,Session,Rating,Block,Report,Notification

#home#

def home(request):
    return render(request, "home.html")

#register#

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and email and password:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            StudentProfile.objects.create(user=user)
            return redirect("login")
        return render(request, "register.html")
    return render(request, "register.html")

#login_view#

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html")
    return render(request, "login.html")

#dashboard#

def dashboard(request):
 if not request.user.is_authenticated:
    return redirect("login")
 student_profile = StudentProfile.objects.get(user=request.user)
 skills_offered = StudentSkill.objects.filter(student=student_profile,skill_type="teach").count()
 skills_wanted = StudentSkill.objects.filter(
    student=student_profile,
    skill_type="learn").count()
 pending_requests = ExchangeRequest.objects.filter(
    receiver=student_profile,
    status="pending").count()
 accepted_requests = ExchangeRequest.objects.filter(
    receiver=student_profile,
    status="accepted").count()
 unread_messages = Message.objects.filter(
    receiver=student_profile,
    is_read=False).count()
 unread_notifications = Notification.objects.filter(
    student=student_profile,
    is_read=False).count()
 return render(
    request,
    "dashboard.html",
    {
        "skills_offered": skills_offered,
        "skills_wanted": skills_wanted,
        "pending_requests": pending_requests,
        "accepted_requests": accepted_requests,
        "unread_messages": unread_messages,
        "unread_notifications": unread_notifications,
    }
)


#profile#

def profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(
        request,
        "profile.html",
        {"student_profile": student_profile}
    )


#edit_profile#

def edit_profile(request):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        student_profile.phone = request.POST.get("phone")
        student_profile.bio = request.POST.get("bio")
        student_profile.education = request.POST.get("education")
        student_profile.location = request.POST.get("location")

        # Profile picture
        if request.FILES.get("profile_picture"):
            student_profile.profile_picture = request.FILES.get("profile_picture")

        student_profile.save()

        return redirect("profile")

    return render(
        request,
        "edit_profile.html",
        {
            "student_profile": student_profile
        }
    )


#skills#

def skills(request):
    if not request.user.is_authenticated:
        return redirect("login")
    student_profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )
    teaching_skills = StudentSkill.objects.filter(
        student=student_profile,
        skill_type="teach"
    ).select_related("skill")
    learning_skills = StudentSkill.objects.filter(
        student=student_profile,
        skill_type="learn"
    ).select_related("skill")
    teach_count = teaching_skills.count()
    learn_count = learning_skills.count()
    return render(
        request,
        "skills.html",
        {
            "student_profile": student_profile,
            "teaching_skills": teaching_skills,
            "learning_skills": learning_skills,
            "teach_count": teach_count,
            "learn_count": learn_count,
        }
    )


#add_skill#

def add_skill(request):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    all_skills = Skill.objects.all()

    if request.method == "POST":

        skill_id = request.POST.get("skill")
        skill_type = request.POST.get("skill_type")

        if skill_id and skill_type:

            skill = Skill.objects.get(
                id=skill_id
            )

            StudentSkill.objects.create(
                student=student_profile,
                skill=skill,
                skill_type=skill_type
            )

            return redirect("skills")

    return render(
        request,
        "add_skill.html",
        {
            "all_skills": all_skills
        }
    )


def find_students(request):
    if not request.user.is_authenticated:
        return redirect("login")

    current_student = StudentProfile.objects.get(
        user=request.user
    )

    blocked_by_me = Block.objects.filter(
        blocker=current_student
    ).values_list(
        "blocked_id",
        flat=True
    )

    blocked_me = Block.objects.filter(
        blocked=current_student
    ).values_list(
        "blocker_id",
        flat=True
    )
    students = StudentProfile.objects.select_related(
        "user"
    ).exclude(
        id=current_student.id
    ).exclude(
        id__in=blocked_by_me
    ).exclude(
        id__in=blocked_me
    )

    return render(
        request,
        "find_students.html",
        {
            "students": students
        }
    )


def send_exchange_request(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    sender = StudentProfile.objects.get(
        user=request.user
    )

    receiver = StudentProfile.objects.get(
        id=student_id
    )

    if sender == receiver:
        return redirect(
            "student_profile",
            student_id=student_id
        )

    skills = StudentSkill.objects.filter(
        student=receiver,
        skill_type="teach"
    ).select_related("skill")

    if request.method == "POST":

        skill_id = request.POST.get("skill")
        message = request.POST.get("message")

        if skill_id:

            skill = Skill.objects.get(
                id=skill_id
            )

            already_sent = ExchangeRequest.objects.filter(
                sender=sender,
                receiver=receiver,
                skill=skill,
                status="pending"
            ).exists()

            if not already_sent:

                ExchangeRequest.objects.create(
                    sender=sender,
                    receiver=receiver,
                    skill=skill,
                    message=message
                )

                Notification.objects.create(
                    student=receiver,
                    message=f"{sender.user.username} sent you an exchange request for {skill.name}."
                )

            return redirect("exchange_requests")

    return render(
        request,
        "send_exchange_request.html",
        {
            "receiver": receiver,
            "skills": skills
        }
    )


def student_profile(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")

    student = StudentProfile.objects.get(
        id=student_id
    )

    skills = StudentSkill.objects.filter(
        student=student
    )

    ratings = Rating.objects.filter(
        receiver=student
    ).select_related(
        "reviewer__user"
    ).order_by("-created_at")

    return render(
        request,
        "student_profile.html",
        {
            "student": student,
            "skills": skills,
            "ratings": ratings,
        }
    )





def exchange_requests(request):
    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )
    received_requests = ExchangeRequest.objects.filter(
        receiver=student_profile
    ).select_related(
        "sender__user",
        "skill"
    ).order_by("-created_at")

    return render(
        request,
        "exchange_requests.html",
        {
            "received_requests": received_requests
        }
    )




def logout_view(request):
    logout(request)
    return redirect("home")



def accept_exchange_request(request, request_id):
    if not request.user.is_authenticated:
        return redirect("login")
    student_profile = StudentProfile.objects.get(
        user=request.user
    )
    exchange_request = ExchangeRequest.objects.get(
        id=request_id,
        receiver=student_profile
    )
    exchange_request.status = "accepted"
    exchange_request.save()
    Notification.objects.create(
        student=exchange_request.sender,
        message=f"{student_profile.user.username} accepted your exchange request for {exchange_request.skill.name}."
    )
    return redirect("exchange_requests")




def reject_exchange_request(request, request_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    exchange_request = ExchangeRequest.objects.get(
        id=request_id,
        receiver=student_profile
    )

    exchange_request.status = "rejected"
    exchange_request.save()

    return redirect("exchange_requests")


def messages_view(request, student_id):

    if not request.user.is_authenticated:
        return redirect("login")

    current_student = StudentProfile.objects.get(
        user=request.user
    )

    other_student = StudentProfile.objects.get(
        id=student_id
    )

    messages = Message.objects.filter(
        sender=current_student,
        receiver=other_student
    ) | Message.objects.filter(
        sender=other_student,
        receiver=current_student
    )

    messages = messages.order_by("created_at")

    Message.objects.filter(
        sender=other_student,
        receiver=current_student,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        "messages.html",
        {
            "other_student": other_student,
            "messages": messages
        }
    )

def messages_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    current_student = StudentProfile.objects.get(
        user=request.user
    )

    messages = Message.objects.filter(
        sender=current_student
    ) | Message.objects.filter(
        receiver=current_student
    )

    students = StudentProfile.objects.filter(
        id__in=messages.values_list("sender_id", flat=True)
    ) | StudentProfile.objects.filter(
        id__in=messages.values_list("receiver_id", flat=True)
    )

    students = students.exclude(
        id=current_student.id
    ).distinct().select_related("user")

    return render(
        request,
        "messages_list.html",
        {
            "students": students
        }
    )


def send_message(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        sender = StudentProfile.objects.get(
            user=request.user
        )
        receiver = StudentProfile.objects.get(
            id=student_id
        )
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content
            )
    return redirect(
        "messages",
        student_id=student_id
    )



def learning_sessions(request):
    if not request.user.is_authenticated:
        return redirect("login")
    student_profile = StudentProfile.objects.get(
        user=request.user
    )
    sessions = ( Session.objects.filter(sender=student_profile)| Session.objects.filter(receiver=student_profile) )
    sessions = sessions.select_related(
        "sender__user",
        "receiver__user"
    ).order_by(
        "-session_date",
        "-session_time"
    )
    return render(
        request,
        "learning_sessions.html",
        {
            "sessions": sessions
        }
    )



def create_session(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")
    sender = StudentProfile.objects.get(
        user=request.user
    )
    receiver = StudentProfile.objects.get(
        id=student_id
    )
    if sender == receiver:
        return redirect(
            "student_profile",
            student_id=student_id
        )
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        session_date = request.POST.get("session_date")
        session_time = request.POST.get("session_time")
        duration = request.POST.get("duration")
        meeting_link = request.POST.get("meeting_link")
        if title and session_date and session_time and duration:
            Session.objects.create(
                sender=sender,
                receiver=receiver,
                title=title,
                description=description,
                session_date=session_date,
                session_time=session_time,
                duration=duration,
                meeting_link=meeting_link
            )
            return redirect("learning_sessions")
    return render(
        request,
        "create_session.html",
        {
            "receiver": receiver
        }
    )

def accept_session(request, session_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    session = Session.objects.get(
        id=session_id,
        receiver=student_profile
    )

    session.status = "accepted"
    session.save()

    return redirect("learning_sessions")


def reject_session(request, session_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    session = Session.objects.get(
        id=session_id,
        receiver=student_profile
    )

    session.status = "rejected"
    session.save()

    return redirect("learning_sessions")


def block_student(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")
    blocker = StudentProfile.objects.get(
        user=request.user
    )
    blocked = StudentProfile.objects.get(
        id=student_id
    )

    if blocker == blocked:
        return redirect(
            "student_profile",
            student_id=student_id
        )
    Block.objects.get_or_create(
        blocker=blocker,
        blocked=blocked
    )
    return redirect("find_students")



def report_student(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")

    reporter = StudentProfile.objects.get(
        user=request.user
    )
    reported = StudentProfile.objects.get(
        id=student_id
    )
    if reporter == reported:
        return redirect(
            "student_profile",
            student_id=student_id
        )
    if request.method == "POST":
        reason = request.POST.get("reason")
        if reason:
            Report.objects.create(
                reporter=reporter,
                reported=reported,
                reason=reason
            )
            return redirect("student_profile", student_id=student_id)
    return render(
        request,
        "report_student.html",
        {
            "student": reported
        }
    )

def notifications(request):
    if not request.user.is_authenticated:
        return redirect("login")
    student_profile = StudentProfile.objects.get(user=request.user)
    notifications = Notification.objects.filter(
        student=student_profile
    ).order_by("-created_at")
    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )


def add_rating(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")
    reviewer = StudentProfile.objects.get(
        user=request.user
    )
    receiver = StudentProfile.objects.get(
        id=student_id
    )
    if reviewer == receiver:
        return redirect(
            "student_profile",
            student_id=student_id
        )
    already_rated = Rating.objects.filter(
        reviewer=reviewer,
        receiver=receiver
    ).exists()

    if request.method == "POST":

        if already_rated:
            return redirect(
                "student_profile",
                student_id=student_id
            )

        rating = request.POST.get("rating")
        review = request.POST.get("review")

        if rating:
            Rating.objects.create(
                reviewer=reviewer,
                receiver=receiver,
                rating=rating,
                review=review
            )

            return redirect(
                "student_profile",
                student_id=student_id
            )

    return render(
        request,
        "add_rating.html",
        {
            "receiver": receiver,
            "already_rated": already_rated
        }
    )


def my_reviews(request):
    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    ratings = Rating.objects.filter(
        receiver=student_profile
    ).select_related(
        "reviewer__user"
    ).order_by("-created_at")

    return render(
        request,
        "my_reviews.html",
        {
            "ratings": ratings
        }
    )

def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        return redirect("dashboard")

    students_count = StudentProfile.objects.count()
    skills_count = Skill.objects.count()
    requests_count = ExchangeRequest.objects.count()
    messages_count = Message.objects.count()
    sessions_count = Session.objects.count()
    reports_count = Report.objects.count()

    return render(
        request,
        "admin_dashboard.html",
        {
            "students_count": students_count,
            "skills_count": skills_count,
            "requests_count": requests_count,
            "messages_count": messages_count,
            "sessions_count": sessions_count,
            "reports_count": reports_count,
        }
    )


def cancel_session(request, session_id):

    if not request.user.is_authenticated:
        return redirect("login")

    student_profile = StudentProfile.objects.get(
        user=request.user
    )

    session = Session.objects.get(
        id=session_id
    )

    if session.sender != student_profile and session.receiver != student_profile:
        return redirect("learning_sessions")

    session.status = "cancelled"
    session.save()

    return redirect("learning_sessions")