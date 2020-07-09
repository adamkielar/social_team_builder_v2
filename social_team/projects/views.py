from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, \
    UpdateView, DeleteView, RedirectView

from accounts.models import User, UserProject, MainSkill
from projects.models import Project, Position, Applicant
from projects.forms import SearchForm, ProjectForm, PositionForm, \
    PositionFormSet
from projects.filters import ApplicantsFilter, PositionStatusFilter, \
    ProjectsFilter


class SearchView(ListView):
    """View to handle search requests"""
    queryset = Project.objects.all()
    template_name = 'projects/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        projects = Project.objects.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
        )
        positions = Position.objects.all()
        context['search_form'] = SearchForm(initial={'q': q})
        context['query'] = q
        context['projects'] = projects
        context['positions'] = positions
        return context


class ProjectAll(ListView):
    """Main view for all projects and positions"""
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super(ProjectAll, self).get_queryset()
        queryset = queryset.filter(
            project_status='OPEN',
            position__main_skills__in=User.objects.filter(
                id=self.request.user.id).values('main_skills__id'),
        ).prefetch_related(
            'position_set'
        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectAll, self).get_context_data()
        context['search_form'] = SearchForm()
        context['position_filter'] = PositionStatusFilter(
            self.request.GET,
            queryset=Position.objects.all()
        )
        context['projects_filter'] = ProjectsFilter(
            self.request.GET,
            queryset=Project.objects.all()
        )
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    """View to create new project"""
    model = Project
    form_class = ProjectForm
    search_form_class = SearchForm
    position_form_class = PositionFormSet
    template_name = 'projects/project_form.html'

    def get_success_url(self):
        return reverse_lazy('projects:projects_all')

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['search_form'] = self.search_form_class()
            context['project_form'] = self.form_class(self.request.POST)
            context['position_formset'] = self.position_form_class(
                self.request.POST)
        else:
            context['search_form'] = self.search_form_class()
            context['project_form'] = self.form_class()
            context['position_formset'] = self.position_form_class()
        return context

    def get_queryset(self):
        queryset = super(ProjectCreate, self).get_queryset()
        self.owner = self.request.user
        return queryset

    def form_valid(self, form):
        messages.success(self.request, "Project created !")
        context = self.get_context_data()
        project_form = context['project_form']
        position_formset = context['position_formset']
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = self.request.user
            project.project_status = 'OPEN'
            project.save()
        if position_formset.is_valid():
            for form in position_formset:
                position = form.save(commit=False)
                position.project = project
                position.status = 'APPLY'
                position.save()
        return super(ProjectCreate, self).form_valid(form)


class ProjectDetail(DetailView):
    """View to display Project details"""
    model = Project
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class ProjectEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update Project details"""
    form_class = ProjectForm
    search_form_class = SearchForm
    position_form_class = PositionFormSet
    model = Project
    template_name = 'projects/project_edit.html'

    def test_func(self):
        owner = self.get_object().owner
        user = self.request.user
        if owner == user:
            return True
        else:
            if user.is_authenticated():
                raise Http404(
                    "You can not edit this Project. You are not the Owner !")

    def get_success_url(self):
        return reverse_lazy('projects:project_detail',
                            kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        context = super(ProjectEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['search_form'] = self.search_form_class()
            context['project_form'] = self.form_class(
                self.request.POST,
                instance=self.get_object()
            )
            context['position_formset'] = self.position_form_class(
                self.request.POST, instance=self.get_object())
        else:
            context['search_form'] = self.search_form_class()
            context['project_form'] = self.form_class(
                instance=self.get_object())
            context['position_formset'] = self.position_form_class(
                instance=self.get_object())
        return context

    def form_valid(self, form):
        messages.success(self.request, "Project updated !")
        context = self.get_context_data()
        position_formset = context['position_formset']
        self.object = form.save()
        if position_formset.is_valid():
            for form in position_formset:
                position = form.save(commit=False)
                position.project = self.object
                position.save()
        return super(ProjectEdit, self).form_valid(form)


class ProjectDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete Project"""
    model = Project
    search_form_class = SearchForm
    success_url = reverse_lazy('projects:projects_all')
    template_name = 'projects/project_confirm_delete.html'
    success_message = "Project deleted !"

    def test_func(self):
        owner = self.get_object().owner
        user = self.request.user
        if owner == user:
            return True
        else:
            if user.is_authenticated():
                raise Http404(
                    "You can not delete this Project. You are not the Owner !")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectDelete, self).get_context_data(**kwargs)
        if self.request.POST:
            context['search_form'] = self.search_form_class()
        else:
            context['search_form'] = self.search_form_class()
        return context


class ApplicantList(LoginRequiredMixin, ListView):
    """
    View for all Applicant that apply for User Project
    and User applications for other projects.
    """
    model = Applicant
    search_form_class = SearchForm
    template_name = 'projects/applications.html'
    context_object_name = 'applicants'

    def get_context_data(self, **kwargs):
        context = super(ApplicantList, self).get_context_data(**kwargs)
        if self.request.POST:
            context['search_form'] = self.search_form_class()
        else:
            context['search_form'] = self.search_form_class()
            context['user'] = get_object_or_404(User, pk=self.request.user.id)
            context['projects'] = Project.objects.filter(
                owner=self.request.user)
            context['positions'] = Position.objects.all()
            context['applicants_filter'] = ApplicantsFilter(
                self.request.GET,
                queryset=Applicant.objects.filter(
                    project__owner=self.request.user).prefetch_related(
                    'project')
            )
        return context


class ApplicantCreate(LoginRequiredMixin, RedirectView):
    """View to create Applicant object after apply for position"""
    url = 'projects:projects_all'

    success_message = 'You applied for position successfully !'
    warning_message = 'You already applied for that position !'

    def get(self, request, *args, **kwargs):
        self.position = get_object_or_404(Position, pk=self.kwargs.get('pk'))
        self.project = get_object_or_404(Project, id=self.position.project.id)
        try:
            Applicant.objects.create(
                user_profile=self.request.user,
                project=self.project,
                position=self.position,
                applicant_status='UNDECIDED'
            )
        except IntegrityError:
            messages.warning(self.request, self.warning_message)

        else:
            messages.success(self.request, self.success_message)
            self.applicant = get_object_or_404(Applicant,
                                               position=self.position,
                                               user_profile=self.request.user)
            send_mail(
                'Application for ' + self.project.title,
                'You applied for ' + self.position.title + ' position in ' + self.project.title + ' project!',
                self.request.user.email,
                [self.applicant.user_profile.email],
                fail_silently=False,
            )
        return super(ApplicantCreate, self).get(request, *args, **kwargs)


class ApplicantStatus(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    """View to change Applicant status and send email about decision"""
    success_message = 'You changed applicant status successfully !'

    def test_func(self):
        self.position = get_object_or_404(Position,
                                          pk=self.kwargs.get('position_pk'))
        self.project = get_object_or_404(Project, id=self.position.project.id)
        self.applicant = get_object_or_404(Applicant,
                                           pk=self.kwargs.get('applicant_pk'))
        owner = self.project.owner
        user = self.request.user
        if owner == user:
            return True
        else:
            if user.is_authenticated():
                raise Http404(
                    "You are not the owner of this project !"
                )

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:applications',
                       kwargs={'pk': self.request.user.id})

    def get(self, request, *args, **kwargs):
        if request.POST.get('approve'):
            self.applicant.applicant_status = 'APPROVED'
            self.applicant.save()
            self.position.position_status = 'FILLED'
            self.position.save()
            messages.success(self.request, self.success_message)

            send_mail(
                'You are Accepted',
                'You are accepted for ' + self.position.title + ' position in ' + self.project.title + ' project!',
                self.request.user.email,
                [self.applicant.user_profile.email],
                fail_silently=False,
            )

        if request.POST.get('reject'):
            self.applicant.applicant_status = 'REJECTED'
            self.applicant.save()
            messages.success(self.request, self.success_message)

            send_mail(
                'You are not accepted',
                'You are not accepted for ' + self.position.title + ' position in ' + self.project.title + ' project!',
                self.request.user.email,
                [self.applicant.user_profile.email],
                fail_silently=False,
            )
        return super(ApplicantStatus, self).get(request, *args, **kwargs)
