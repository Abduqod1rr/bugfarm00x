from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.landing, name="landing"),
    path("feed/", views.Home.as_view(), name="feed"),
    path("scoreboard/", views.scoreboard, name="scoreboard"),
    path("scoreboard/mark/<str:bug_id>/", views.mark_found, name="mark_found"),
    path("hints/", views.hints, name="hints"),
    path("solutions/", views.solutions, name="solutions"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin, name="login"),
    path("logout/", views.userlogout.as_view(), name="logout"),
    path("createprofile", views.CreateProfile.as_view(), name="createprofile"),
    path("addpoc/", views.AddPoc.as_view(), name="addpoc"),
    path("mypocs/", views.MyPocs.as_view(), name="mypocs"),
    path("delete_poc/<int:pk>", views.DeletePoc.as_view(), name="delete_poc"),
    path("update_poc/<int:pk>",views.UpdatePoc.as_view(), name='update_poc'),
    path("myprofile/", views.MyProfile.as_view(), name="myprofile"),
    path("edit_profile/", views.EditProfile.as_view(), name="edit_profile"),
    path("profile/<int:pk>/", views.UserProfile.as_view(), name="user_profile"),
    path("toggle_like/<int:pk>", views.toggle_like, name="toggle_like"),
    path("add_comment/<int:pk>", views.CommentPoc.as_view(), name="add_comment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
