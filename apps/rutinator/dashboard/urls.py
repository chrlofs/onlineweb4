<<<<<<< HEAD
from django.conf.urls import url
from apps.rutinator.dashboard.views import TaskListView, CreateTaskView, EditTaskView
=======
from django.conf.urls import patterns, url

from apps.rutinator.dashboard.views import CreateTaskView, EditTaskView, TaskListView
>>>>>>> 4679cfe7942eb181b8ce20f96cb201573d0e91f5

urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='task_view'),
    url(r'^create/$', CreateTaskView.as_view(), name='task_create'),
    url(r'^edit/(?P<pk>\d+)/$', EditTaskView.as_view(), name='task_edit')
<<<<<<< HEAD
]
=======
)
>>>>>>> 4679cfe7942eb181b8ce20f96cb201573d0e91f5
