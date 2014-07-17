#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, Http404, QueryDict
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic.edit import BaseFormView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .activity.models import Activity
from .watch.models import Watch
from .models import Report
from .activity.forms import HistoryCommentForm
from .signals import activity_create
from .signals import activity_update
from .signals import activity_workflow
from .signals import djangoerp_post_save
from .utils import get_model_from_cfg
from .utils import form_class_factory
from .utils.deprecation import RemovedInNextVersionWarning
from .viewmixins import ModuleClonePermissionMixin
from .viewmixins import ModuleCreatePermissionMixin
from .viewmixins import ModuleDeletePermissionMixin
from .viewmixins import ModuleUpdatePermissionMixin
from .viewmixins import ModuleViewPermissionMixin
from .viewmixins import ModuleAjaxMixin
from .viewmixins import ModuleBaseMixin
from .viewmixins import ModuleViewMixin
from .viewmixins import NextMixin

import re
import operator
import warnings
import copy
from functools import reduce
from django_filters.views import FilterView


class ModuleActivityMixin(object):
    """
    Parse history to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        ct = ContentType.objects.get_for_model(self.object)

        watch = Watch.objects.filter(user=self.request.user, watch_ct=ct, watch_id__in=[self.object.pk, 0]).order_by('-watch_id').first()
        if watch:
            watching = watch.active
        else:
            watching = False

        kwargs.update({
            'erpactivity': {
                'qs': Activity.objects.filter(parent_ct=ct, parent_id=self.object.pk),
                'enabled': (self.model._erpmeta.has_comments or self.model._erpmeta.has_history),
                'comments': self.model._erpmeta.has_comments,
                'log': self.model._erpmeta.has_history,
                'pk': self.object.pk,
                'ct': ct.pk,
                'watch': watching,
                'log_data': None,
                'comment_form': None,
                'object_ct': ct,
                'object_pk': self.object.pk,
            },
        })
        if self.model._erpmeta.has_history:
            kwargs['erpactivity']['log_data'] = Activity.objects.select_related('user').filter(parent_ct=ct, parent_id=self.object.pk)
        if self.model._erpmeta.has_comments:
            kwargs['erpactivity']['comment_form'] = HistoryCommentForm()
        return super(ModuleActivityMixin, self).get_context_data(**kwargs)


class ModuleFilesMixin(object):
    """
    Parse files to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        if self.model._erpmeta.has_files:
            from .file.views import FileAddView
            Document = get_model_from_cfg('DOCUMENT')

            ct = ContentType.objects.get_for_model(self.object)

            kwargs.update({
                'has_files': True,
                'history_file_form': FileAddView.form_class(),
                'files': Document.objects.filter(content_type=ct, content_id=self.object.pk),
            })
        return super(ModuleFilesMixin, self).get_context_data(**kwargs)


class ModuleFormMixin(object):
    """
    make an ERP-Form
    """
    fields = None
    exclude = []

    def get_form_class(self, *args, **kwargs):
        """
        Returns the form class to use in this view.
        """
        if not self.form_class:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_queryset().model

            if isinstance(self.fields, list):
                self.form_class = modelform_factory(model, fields=self.fields)
            else:
                self.form_class = modelform_factory(model, exclude=self.exclude)
        return form_class_factory(self.form_class)


class ModuleIndexView(ModuleViewPermissionMixin, ModuleViewMixin, FilterView):
    """
    """
    context_object_name = 'objects'
    template_name_suffix = '_erpindex'
    allow_empty = True

    def get_template_names(self):
        return super(ModuleIndexView, self).get_template_names() + ["djangoerp/module_index_default.html"]

    def get_context_data(self, **kwargs):
        if self.filterset_class:
            kwargs.update({
                'has_filter': True,
            })
        else:
            kwargs.update({
                'has_filter': False,
            })
        return super(ModuleIndexView, self).get_context_data(**kwargs)


class ModuleDetailView(ModuleViewPermissionMixin, ModuleFilesMixin, ModuleActivityMixin, ModuleViewMixin, DetailView):
    """
    show the details of an entry
    """
    context_object_name = 'object'
    template_name_suffix = '_erpdetail'

    def get_template_names(self):
        self.update_notification()
        return super(ModuleDetailView, self).get_template_names() + ["djangoerp/module_detail_default.html"]

class ModuleAutoDetailView(ModuleFormMixin, ModuleDetailView):
    """
    show the details of an entry
    """
    form_class = None

    def get_form(self, **kwargs):
        if self.form_class == None:
            self.get_form_class()
        form = self.form_class(instance=self.object)
        return form

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form()
        })
        return super(ModuleAutoDetailView, self).get_context_data(**kwargs)


class ModuleReportView(ModuleViewPermissionMixin, ModuleBaseMixin, DetailView):
    """
    render a report
    """
    context_object_name = 'object'

    def get_template_names(self):
        return ["djangoerp/module_report.html"]

    def get(self, request, *args, **kwargs):
        response = super(ModuleReportView, self).get(request, *args, **kwargs)

        ct = ContentType.objects.get_for_model(self.get_object())
        try:
            report = Report.objects.get(contenttype=ct)
            return report.render(self.request, self.get_context_data())
        except Report.DoesNotExist:
            # return "no view configured" page
            return response

    def get_context_data(self, **kwargs):
        context = super(ModuleReportView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class ModuleCloneView(ModuleFormMixin, ModuleClonePermissionMixin, ModuleAjaxMixin, UpdateView):
    """
    clone a object
    """
    context_object_name = 'object'
    template_name_suffix = '_erpclone'
    fields = []

    def get_template_names(self):
        return super(ModuleCloneView, self).get_template_names() + ["djangoerp/module_clone_default.html"]

    def clone_object(self, formdata, instance):
        pass

    def clone_related_objects(self, formdata, old_object, new_object):
        pass

    def form_valid(self, form):
        # messages.success(self.request, 'Object cloned')
        old_object = copy.copy(self.object)
        self.clone_object(form.cleaned_data, form.instance)
        form.instance.pk = None
        if form.instance._erpmeta.workflow_field:
            setattr(form.instance, form.instance._erpmeta.workflow_field, form.instance._erpmeta.workflow._default_state_key)
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        self.object = form.save()
        self.clone_related_objects(form.cleaned_data, old_object, self.object)
        activity_create.send(sender=self.object.__class__, instance=self.object)
        return self.render_valid_form({
            'object_pk': self.object.pk,
            'redirect': self.object.get_absolute_url(),
            'message': ugettext('Object copied'),
        })


class ModuleUpdateView(ModuleFormMixin, ModuleUpdatePermissionMixin, ModuleAjaxMixin, UpdateView):
    """
    update an update
    """
    context_object_name = 'object'
    template_name_suffix = '_erpupdate'
    exclude=[]

    def get_template_names(self):
        return super(ModuleUpdateView, self).get_template_names() + ["djangoerp/module_update_default.html"]

    def form_valid(self, form):
       #messages.success(self.request, 'Object updated')
        form.instance.modified_by = self.request.user
        self.object = form.save()
        activity_update.send(sender=self.object.__class__, instance=self.object)
        return self.render_valid_form({
            'object_pk': self.object.pk,
            'message': ugettext('Object updated'),
        })


class ModuleCreateView(ModuleFormMixin, ModuleCreatePermissionMixin, ModuleAjaxMixin, CreateView):
    """
    create a new instance
    """
    context_object_name = 'object'
    template_name_suffix = '_erpcreate'

    def get_initial(self):
        for key in self.request.GET.keys():
            match = 'data\[(\w+)\]'
            if re.match(match, key):
                field = re.match(match, key).groups()[0]
                self.initial.update({field: self.request.GET.get(key)})
        return super(ModuleCreateView, self).get_initial()

    def get_template_names(self):
        return super(ModuleCreateView, self).get_template_names() + ["djangoerp/module_create_default.html"]

    def form_valid(self, form):
        #messages.success(self.request, 'Object created')
        form.instance.modified_by = self.request.user
        form.instance.created_by = self.request.user
        self.object = form.save()
        activity_create.send(sender=self.object.__class__, instance=self.object)
        return self.render_valid_form({
            'object_pk': self.object.pk,
            'message': ugettext('Object created'),
        })


class ModuleDeleteView(ModuleDeletePermissionMixin, NextMixin, ModuleViewMixin, DeleteView):
    """
    delete an instance
    """
    context_object_name = 'object'
    template_name_suffix = '_erpdelete'

    def get_template_names(self):
        return super(ModuleDeleteView, self).get_template_names() + ["djangoerp/module_delete_default.html"]

    def get_success_url(self):
        messages.info(self.request, 'Object deleted')
        return self.redirect_next('%s:index' % self.model._erpmeta.url_namespace)


class ModuleWorkflowView(ModuleViewMixin, NextMixin, DetailView):
    """
    update the state of a workflow
    """
    context_object_name = 'object'
    success_url = None

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.update_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleWorkflowView, self).get_permissions(perms)

    def get_success_url(self):
        return self.redirect_next('%s:index' % self.model._erpmeta.url_namespace)

    def get(self, request, transition='', *args, **kwargs):
        self.object = self.get_object()

        transitions = dict(self.object._erpworkflow._from_here())
        if not transition in transitions:
            raise Http404

        try:
            self.success_url = self.object._erpworkflow._call(transition, self.object, self.request.user)
        except ValidationError as e:
            # the objects gets checks with full_clean
            # if a validation error is raised, show an error page and don't save the object
            return self.response_class(
                request=self.request,
                template=['djangoerp/module_workflow.html'],
                context=self.get_context_data(error=e),
            )
        self.object = self.object._erpworkflow.instance
        self.object.save()

        # generate a history object and signal
        activity_workflow.send(sender=self.object.__class__, instance=self.object)
        djangoerp_post_save.send(sender=self.object.__class__, instance=self.object, new=False)
        messages.success(self.request, 'Workflow-State changed')
        return HttpResponseRedirect(self.get_success_url())


class ModuleFormAPI(ModuleFormMixin, ModuleAjaxMixin, SingleObjectMixin, BaseFormView):
    """
    """
    model = None
    queryset = None
    form_view = None

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        if hasattr(self, 'object'):
            return self.object
        # Use a custom queryset if provided; this is required for subclasses
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        if pk is None:
            return None
        try:
            obj = queryset.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get(self, request, *args, **kwargs):
        # dont react on get requests
        raise Http404

    def post(self, request, *args, **kwargs):
        form_class = self.form_view(model=self.model, object=self.get_object()).get_form_class()
        form = form_class(prefix=self.get_prefix(), data=QueryDict(self.request.POST['form']), instance=self.get_object())

        if "search" in self.request.GET:
            # do form validation to fill form.instance with data
            valid = form.is_valid()

            field = form.get_field(self.request.POST['field'])
            if not field:
                # TODO ADD LOGGING
                raise Http404
            qs = field.field.choices.queryset

            func = getattr(form.instance, 'get_%s_queryset' % field.name, None)
            if func:
                qs = func(qs)

            if self.request.POST['string']:
                for bit in self.normalize_query(self.request.POST['string']):
                    lookups = [self.construct_search(str(f)) for f in qs.model._erpmeta.search_fields]
                    queries = [Q(**{l: bit}) for l in lookups]
                    qs = qs.filter(reduce(operator.or_, queries))
            data = []
            for item in qs:
                data.append({'pk': item.pk, 'value': str(item)})
            return self.render_to_json_response(data)

        if "changed" in self.request.GET:
            """
            validate one form and compare it to an new form created with the validated instance
            """
            valid, data = form.get_changes()
            return self.render_to_json_response(data)
        raise Http404

    def get_form_kwargs(self):
        kwargs = super(ModuleFormAPI, self).get_form_kwargs()
        kwargs.update({
            'instance': self.get_object(),
        })
        return kwargs

    def normalize_query(self, query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        '''
        Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.

        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    # Apply keyword searches.
    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name
