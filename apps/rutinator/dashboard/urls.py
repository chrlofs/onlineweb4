from django.conf.urls import url
from apps.rutinator.dashboard.views import CreateTaskView, EditTaskView, TaskListView, DeleteTaskView


urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='task_view'),
    url(r'^create/$', CreateTaskView.as_view(), name='task_create'),
    url(r'^edit/(?P<pk>\d+)/$', EditTaskView.as_view(), name='task_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteTaskView.as_view(), name='task_delete'),
]


