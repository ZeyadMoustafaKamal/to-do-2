from django.shortcuts import redirect
from tasks.models import Task
from django.views import generic

class Index(generic.TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['tasks'] = Task.objects.filter(user=self.request.user)
        return context
    def get(self, request, *args, **kwargs):
        if 'add-task' in request.GET:
            task_to_add = Task(name=request.GET.get('task-to-add'),user=request.user)
            task_to_add.save()
        return super().get(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        if 'btndelete' in request.POST:
            Task.objects.get(id = request.POST.get('btndelete')).delete()
        elif 'submit-tasks' in request.POST:
            states = request.POST.getlist('check')
            tasks = Task.objects.filter(user=self.request.user).all()
            for task in tasks:
                if str(task.id) in states:
                    task.is_done = True
                else:
                    task.is_done = False
                task.save()
        return redirect('index')

class WhoAMI(generic.TemplateView):
    template_name = 'whoami.html'

