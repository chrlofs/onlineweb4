from apps.dashboard.tools import DashboardMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from apps.rutinator.models import Task
from apps.rutinator.forms import NewTaskForm
from django.core.urlresolvers import reverse_lazy



class TaskListView(DashboardMixin, ListView):
    model = Task
    queryset = Task.objects.all()
    template_name = "rutinator/dashboard/index.html"
    context_object_name = "tasks"


class CreateTaskView(DashboardMixin, CreateView):
    model = Task
    form_class = NewTaskForm
    template_name = 'rutinator/dashboard/create.html'
    success_url = reverse_lazy('rutinator:task_view')

    def form_valid(self, form):
        if form.instance.choose_random:
            form.instance.user = form.instance.random_from_group()
        return super().form_valid(form)


class EditTaskView(DashboardMixin, UpdateView):
    model = Task
    form_class = NewTaskForm
    template_name = 'rutinator/dashboard/edit.html'
    success_url = reverse_lazy('rutinator:task_view')


# fix
class DeleteTaskView(DashboardMixin, DeleteView):
    model = Task
    form_class = NewTaskForm
    #pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('rutinator:task_view')
