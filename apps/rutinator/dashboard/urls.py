from django.conf.urls import url
from apps.rutinator.dashboard.views import CreateTaskView, EditTaskView, TaskListView


urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='task_view'),
    url(r'^create/$', CreateTaskView.as_view(), name='task_create'),
    url(r'^edit/(?P<pk>\d+)/$', EditTaskView.as_view(), name='task_edit')
]

