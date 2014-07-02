#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

class ERPModule(object):
    index = None
    create = None
    delete = None
    update = None
    detail = None
    report = None
    urlpatterns = None

    def __init__(self, model):
        self.model = model

    def get_urls(self, **options):
        index = self.index or options.get('index', None)
        create = self.create or options.get('create', None)
        delete = self.delete or options.get('delete', None)
        update = self.update or options.get('update', None)
        detail = self.detail or options.get('detail', None)
        report = self.report or options.get('report', None)

        add_patterns = self.urlpatterns or options.get('urlpatterns', None)

        urlpatterns =  patterns('',
            url(
                r'^$',
                index.as_view(model=self.model),
                name='index',
            ),
            url(
                r'^(?P<pk>[0-9]+)/$',
                detail.as_view(model=self.model),
                name='detail',
            ),
            url(
                r'^(?P<pk>[0-9]+)/update/$',
                update.as_view(model=self.model),
                name='update',
            ),
            url(
                r'^(?P<pk>[0-9]+)/delete/$',
                delete.as_view(model=self.model),
                name='delete',
            ),
            url(
                r'^(?P<pk>[0-9]+)/update/form-api/$',
                PluginFormAPI.as_view(
                    model=self.model,
                    form_view=update,
                ),
                name='form-api',
            ),
        )

        # create view(s)
        if isinstance(create, dict):
            for label, view in six.iteritems(create):
                key = slugify(label)
                if isinstance(view, (list, tuple)):
                    label = view[0]
                    view = view[1]
                self.model._erpmeta.create_views.append((key, label))
                urlpatterns += patterns('',
                    url(
                        r'^create/(?P<key>%s)/$' % key,
                        view.as_view(model=self.model),
                        name='create',
                    ),
                    url(
                        r'^create/(?P<key>%s)/form-api/$' % key,
                        PluginFormAPI.as_view(
                            model=self.model,
                            form_view=view,
                        ),
                        name='form-api',
                    ),
                )
        else:
            urlpatterns += patterns('',
                url(
                    r'^create/$',
                    create.as_view(model=self.model),
                    name='create',
                ),
                url(
                    r'^create/form-api/$',
                    PluginFormAPI.as_view(
                        model=self.model,
                        form_view=create,
                    ),
                    name='form-api',
              ),
            )

        # workflow interactions
        if bool(len(self.model._erpworkflow._transitions)):
            urlpatterns += patterns('',
              url(
                  r'^(?P<pk>[0-9]+)/workflow/(?P<transition>\w+)/$',
                  PluginWorkflow.as_view(model=self.model),
                  name='workflow',
              ),
            )

        # model reports
        if report:
            self.model._erpmeta.has_report = True
            urlpatterns += patterns('',
                url(
                    r'^(?P<pk>[0-9]+)/report/$',
                    report.as_view(model=self.model),
                    name='report',
                ),
            )

        # url patterns
        if add_patterns:
            urlpatterns += add_patterns

        return urlpatterns


