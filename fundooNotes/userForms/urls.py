from django.urls import path
from .views import registerForm,loginForm,forgotPasswordForm,resetPasswordForm,createNoteList,CreateNoteForm,activate,logout

urlpatterns = [
    path('register/',registerForm.as_view(),name="register"),
    path('login/',loginForm.as_view(),name='login'),
    path('forgot/',forgotPasswordForm.as_view(),name='forgot'),
    path('activate/<slug:surl>', activate, name='activate'),
    path('resetPassword/',resetPasswordForm.as_view(),name='resetPassword'),
    path('createNoteList/',createNoteList.as_view(),name='createNoteList'),
    path('createNoteList/<int:pk>',CreateNoteForm.as_view(),name='createNote'),
    path('logout',logout)
]