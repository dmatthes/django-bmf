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
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
# from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseFormView
from django.views.generic.dates import BaseDateListView
from django.views.generic.dates import YearMixin
from django.views.generic.dates import MonthMixin
from django.views.generic.dates import WeekMixin
from django.views.generic.dates import DayMixin
from django.views.generic.dates import _date_from_string
from django.views.generic.dates import _get_next_prev
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.template.loader import get_template
from django.template.loader import select_template
from django.template import TemplateDoesNotExist
from django.utils.encoding import force_text
from django.utils.formats import get_format
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from djangobmf.document.forms import UploadDocument
from djangobmf.document.models import Document
# from djangobmf.document.views import DocumentCreateView
from djangobmf.models import Report
from djangobmf.notification.forms import HistoryCommentForm
from djangobmf.notification.models import Activity
from djangobmf.notification.models import Notification
from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
# from .signals import activity_workflow
from djangobmf.utils import form_class_factory
from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning
from djangobmf.viewmixins import ModuleClonePermissionMixin
from djangobmf.viewmixins import ModuleCreatePermissionMixin
from djangobmf.viewmixins import ModuleDeletePermissionMixin
from djangobmf.viewmixins import ModuleUpdatePermissionMixin
from djangobmf.viewmixins import ModuleViewPermissionMixin
from djangobmf.viewmixins import ModuleAjaxMixin
from djangobmf.viewmixins import ModuleBaseMixin
from djangobmf.viewmixins import ModuleViewMixin
from djangobmf.viewmixins import NextMixin
from djangobmf.viewmixins import ViewMixin

import copy
import datetime
import operator
import re
import types
import warnings
from functools import reduce
from django_filters.views import FilterView


# --- list views --------------------------------------------------------------


class ModuleGenericBaseView(ModuleViewPermissionMixin, ModuleViewMixin):
    """
    """
    model = None  # set by workspace.views
    workspace = None  # set by workspace.views
    context_object_name = 'objects'
    template_name_suffix = None
    template_name = None
    allow_empty = True
    name = None
    slug = None
    paginate_by = None

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name:
            return [self.template_name]

        names = []
        if self.template_name_suffix:
            names.append("%s/%s_bmfgeneric_%s.html" % (
                self.model._meta.app_label,
                self.model._meta.model_name,
                self.template_name_suffix
            ))

        names.append("%s/%s_bmfgeneric.html" % (
            self.model._meta.app_label,
            self.model._meta.model_name
        ))
        if self.template_name_suffix:
            names.append("djangobmf/module_generic_%s.html" % self.template_name_suffix)

        names.append("djangobmf/module_generic_default.html")

        return names


class ModuleListView(ModuleGenericBaseView, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    """
    This view generates a simple parginated list
    """
    template_name_suffix = 'list'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class ModuleFilterView(ModuleGenericBaseView, FilterView):
    """
    """
    template_name_suffix = 'filter'

    def get_context_data(self, **kwargs):
        if self.filterset_class:
            kwargs.update({
                'has_filter': True,
            })
        else:
            kwargs.update({
                'has_filter': False,
            })
        return super(ModuleFilterView, self).get_context_data(**kwargs)


class ModuleTreeView(ModuleGenericBaseView, FilterView):
    """
    This view generates a parginated list and tree navigation
    """
    template_name_suffix = 'tree'


class ModuleCategoryView(ModuleGenericBaseView, FilterView):
    """
    TODO: Some mixin between Tree, List and Letter, probably with multiple categorie-items or workspace-states
    """
    template_name_suffix = 'category'


class ModuleArchiveView(ModuleGenericBaseView, YearMixin, MonthMixin, WeekMixin, DayMixin,
                        MultipleObjectTemplateResponseMixin, BaseDateListView):
    """
    This view generates a parginated list for a time intervall
    """
    template_name_suffix = 'archive'
    date_field = 'modified'
    date_resolution = 'year'
    allow_empty = True
    allow_future = False

    def get(self, request, *args, **kwargs):
        self.date_list, self.object_list, extra_context = self.get_dated_items()
        context = self.get_context_data(object_list=self.object_list, date_list=self.date_list)
        context.update(extra_context)
        return self.render_to_response(context)

    def get_week_format(self):
        return '%W' if get_format('FIRST_DAY_OF_WEEK') else '%U'

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """

        year = self.request.GET.get('year', None)
        month = self.request.GET.get('month', None)
        day = self.request.GET.get('day', None)
        week = self.request.GET.get('week', None)

        year_format = '%Y'
        month_format = '%m'
        day_format = '%d'
        week_format = self.get_week_format()

        date_now = now()

        if not year:
            year = date_now.strftime(year_format)

        if not month and not week and self.date_resolution in ["month", "day"]:
            month = date_now.strftime(month_format)

        if not week and not month and self.date_resolution in ["week"]:
            week = date_now.strftime(week_format)

        if not day and self.date_resolution in ["day"]:
            day = date_now.strftime(day_format)

        date_field = self.get_date_field()

        if month and not week:
            if day:
                date = _date_from_string(year, year_format, month, month_format, day, day_format)
                period = "day"
                until = self._make_date_lookup_arg(self._get_next_day(date))
            else:
                date = _date_from_string(year, year_format, month, month_format)
                period = "month"
                until = self._make_date_lookup_arg(self._get_next_month(date))
        elif week and not month:
            if week_format == '%W':
                date = _date_from_string(year, year_format, week, week_format, '1', '%w')
            else:
                date = _date_from_string(year, year_format, week, week_format, '0', '%w')
            period = "week"
            until = self._make_date_lookup_arg(self._get_next_week(date))
        else:
            date = _date_from_string(year, year_format)
            period = "year"
            until = self._make_date_lookup_arg(self._get_next_year(date))
        since = self._make_date_lookup_arg(date)

        lookup_kwargs = {
            '%s__gte' % date_field: since,
            '%s__lt' % date_field: until,
        }

        qs = self.get_dated_queryset(**lookup_kwargs)
        date_list = self.get_date_list(qs)

        return (date_list, qs, {
            'current_period': period,
            'current_period_start': date,
            'current_period_end': until - datetime.timedelta(1),
            'next_period': _get_next_prev(self, date, False, period),
            'previous_period': _get_next_prev(self, date, True, period),
            'dateformat': {
                'year': year_format[1:],
                'month': month_format[1:],
                'day': day_format[1:],
                'week': week_format[1:],
            }
        })


class ModuleLetterView(ModuleGenericBaseView, FilterView):
    """
    This view generates a parginated list and a "A-Z 0-9"
    navigation
    """
    template_name_suffix = 'letter'


# --- detail, forms and api ---------------------------------------------------


class ModuleActivityMixin(object):
    """
    Parse history to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        ct = ContentType.objects.get_for_model(self.object)

        try:
            watch = Notification.objects.get(
                user=self.request.user,
                watch_ct=ct,
                watch_id=self.object.pk
            )
            if watch.unread:
                watch.unread = False
                watch.save()
            notification = watch
            watching = watch.is_active()
        except Notification.DoesNotExist:
            notification = None
            watching = False

        kwargs.update({
            'bmfactivity': {
                'qs': Activity.objects.filter(parent_ct=ct, parent_id=self.object.pk),
                'enabled': (self.model._bmfmeta.has_comments or self.model._bmfmeta.has_history),
                'comments': self.model._bmfmeta.has_comments,
                'log': self.model._bmfmeta.has_history,
                'pk': self.object.pk,
                'ct': ct.pk,
                'notification': notification,
                'watch': watching,
                'log_data': None,
                'comment_form': None,
                'object_ct': ct,
                'object_pk': self.object.pk,
            },
        })
        if self.model._bmfmeta.has_history:
            kwargs['bmfactivity']['log_data'] = Activity.objects.select_related('user') \
                .filter(parent_ct=ct, parent_id=self.object.pk)
        if self.model._bmfmeta.has_comments:
            kwargs['bmfactivity']['comment_form'] = HistoryCommentForm()
        return super(ModuleActivityMixin, self).get_context_data(**kwargs)


class ModuleFilesMixin(object):
    """
    Parse files to view (as a context variable)
    """

    def get_context_data(self, **kwargs):
        if self.model._bmfmeta.has_files:
            ct = ContentType.objects.get_for_model(self.object)

            kwargs.update({
                'has_files': True,
                'history_file_form': UploadDocument,
                'files': Document.objects.filter(content_type=ct, content_id=self.object.pk),
            })
        return super(ModuleFilesMixin, self).get_context_data(**kwargs)


class ModuleFormMixin(object):
    """
    make an BMF-Form
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


class ModuleDetailView(
        ModuleViewPermissionMixin, ModuleFilesMixin, ModuleActivityMixin, ModuleViewMixin, DetailView):
    """
    show the details of an entry
    """
    context_object_name = 'object'
    template_name_suffix = '_bmfdetail'

    def get_related_views(self):
        # TODO: maybe cache this
        if hasattr(self, '_related_views'):
            return self._related_views
        open = self.request.GET.get("open", None)
        self._related_views = {}
        for rel in self.model._meta.get_all_related_objects():
            template = '%s/%s_bmfrelated_%s.html' % (
                rel.model._meta.app_label,
                rel.model._meta.model_name,
                self.model._meta.model_name,
            )
            qs = getattr(self.object, rel.get_accessor_name())
            qs_mod = getattr(rel.model, 'bmfrelated_%s_queryset' % self.model._meta.model_name, None)
            try:
                self._related_views[rel.model._meta.model_name] = {
                    'name': '%s' % rel.model._meta.verbose_name_plural,
                    'key': rel.model._meta.model_name,
                    'active': open == rel.model._meta.model_name,
                    'objects': qs if not isinstance(qs_mod, types.FunctionType) else qs_mod(qs),
                    'template': get_template(template),
                }
            except TemplateDoesNotExist:
                continue
        return self._related_views

    def get_context_data(self, **kwargs):
        kwargs.update({
            'related_views': self.get_related_views(),
            'parent_template': select_template(self.get_template_names(related=False)),
            'related_objects': self.get_related_objects(),  # TODO add pagination
        })
        return super(ModuleDetailView, self).get_context_data(**kwargs)

    def get_related_objects(self):
        if "open" in self.request.GET.keys() and self.request.GET["open"] in self.get_related_views().keys():
            return self.get_related_views()[self.request.GET["open"]]["objects"]

    def get_template_names(self, related=True):
        self.update_notification()
        if related and "open" in self.request.GET.keys() and \
                self.request.GET["open"] in self.get_related_views().keys():
            return self.get_related_views()[self.request.GET["open"]]["template"]
        return super(ModuleDetailView, self).get_template_names() \
            + ["djangobmf/module_detail_default.html"]


class ModuleAutoDetailView(ModuleFormMixin, ModuleDetailView):
    """
    show the details of an entry
    """
    form_class = None

    def get_form(self, **kwargs):
        if self.form_class is None:
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
        return ["djangobmf/module_report.html"]

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
    template_name_suffix = '_bmfclone'
    fields = []

    def get_template_names(self):
        return super(ModuleCloneView, self).get_template_names() \
            + ["djangobmf/module_clone_default.html"]

    def clone_object(self, formdata, instance):
        pass

    def clone_related_objects(self, formdata, old_object, new_object):
        pass

    def form_valid(self, form):
        # messages.success(self.request, 'Object cloned')
        old_object = copy.copy(self.object)
        self.clone_object(form.cleaned_data, form.instance)
        form.instance.pk = None
        if form.instance._bmfmeta.workflow_field:
            setattr(
                form.instance,
                form.instance._bmfmeta.workflow_field,
                form.instance._bmfmeta.workflow._default_state_key
            )
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
    """
    context_object_name = 'object'
    template_name_suffix = '_bmfupdate'
    exclude = []

    def get_template_names(self):
        return super(ModuleUpdateView, self).get_template_names() \
            + ["djangobmf/module_update_default.html"]

    def form_valid(self, form):
        # messages.success(self.request, 'Object updated')
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
    template_name_suffix = '_bmfcreate'

    def get_initial(self):
        for key in self.request.GET.keys():
            match = 'data\[(\w+)\]'
            if re.match(match, key):
                field = re.match(match, key).groups()[0]
                self.initial.update({field: self.request.GET.get(key)})
        return super(ModuleCreateView, self).get_initial()

    def get_template_names(self):
        return super(ModuleCreateView, self).get_template_names() \
            + ["djangobmf/module_create_default.html"]

    def form_valid(self, form):
        # messages.success(self.request, 'Object created')
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
    template_name_suffix = '_bmfdelete'

    def get_template_names(self):
        return super(ModuleDeleteView, self).get_template_names() \
            + ["djangobmf/module_delete_default.html"]

    def get_success_url(self):
        messages.info(self.request, 'Object deleted')
        return self.redirect_next()


class ModuleWorkflowView(ModuleViewMixin, NextMixin, DetailView):
    """
    update the state of a workflow
    """
    context_object_name = 'object'
    success_url = None

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.change_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleWorkflowView, self).get_permissions(perms)

    def get_success_url(self):
        return self.redirect_next()

    def get(self, request, transition='', *args, **kwargs):
        self.object = self.get_object()

        try:
            # TODO also change modelbase.py, when updating to use ajax
            self.success_url = self.object.bmfworkflow_transition(transition, self.request.user)
        except ValidationError as e:
            # the objects gets checks with full_clean
            # if a validation error is raised, show an error page and don't save the object
            return self.response_class(
                request=self.request,
                template=['djangobmf/module_workflow.html'],
                context=self.get_context_data(error=e),
            )

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
            raise Http404(_("No %(verbose_name)s found matching the query") % {
                'verbose_name': queryset.model._meta.verbose_name
            })
        return obj

    def get(self, request, *args, **kwargs):
        # dont react on get requests
        raise Http404

    def post(self, request, *args, **kwargs):
        form_class = self.form_view(model=self.model, object=self.get_object()).get_form_class()
        form = form_class(
            prefix=self.get_prefix(),
            data=QueryDict(self.request.POST['form']),
            instance=self.get_object())

        if "search" in self.request.GET:
            # do form validation to fill form.instance with data
            valid = form.is_valid()

            field = form.get_field(self.request.POST['field'])
            if not field:
                # TODO ADD LOGGING
                raise Http404
            qs = field.field.queryset

            if hasattr(field.field.queryset.model, 'has_permissions'):
                qs = field.field.queryset.model.has_permissions(qs, self.request.user)

            func = getattr(form.instance, 'get_%s_queryset' % field.name, None)
            if func:
                qs = func(qs)

            if self.request.POST['string']:
                for bit in self.normalize_query(self.request.POST['string']):
                    lookups = [self.construct_search(str(f)) for f in qs.model._bmfmeta.search_fields]
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

    def normalize_query(
            self, query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
            normspace=re.compile(r'\s{2,}').sub):
        '''
        Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.

        Example:
        > self.normalize_query('  some random  words "with   quotes  " and   spaces')
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


# --- misc --------------------------------------------------------------------


class ModuleOverviewView(ViewMixin, TemplateView):
    template_name = "djangobmf/modules.html"

    def get_context_data(self, **kwargs):
        from .sites import site

        modules = []
        for ct, model in site.models.items():
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if self.request.user.has_perms([perm, ]):
                key = force_text(model._bmfmeta.category)
                modules.append({
                    'category': key,
                    'model': model,
                    'name': model._meta.verbose_name_plural,
                    'url': model._bmfmeta.url_namespace + ':index',
                })

        context = super(ModuleOverviewView, self).get_context_data(**kwargs)
        context['modules'] = modules
        return context


# --- old ---------------------------------------------------------------------


class ModuleIndexView(ModuleListView):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "ModuleIndexView is is deprecated - use ModuleListView",
            RemovedInNextBMFVersionWarning, stacklevel=2)
        super(ModuleIndexView, self).__init__(*args, **kwargs)


class ModuleGenericListView(ModuleListView):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "ModuleGenericListView is is deprecated - use ModuleListView",
            RemovedInNextBMFVersionWarning, stacklevel=2)
        super(ModuleGenericListView, self).__init__(*args, **kwargs)
