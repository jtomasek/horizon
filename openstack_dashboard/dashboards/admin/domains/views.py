# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings  # noqa
from django.utils import simplejson as json
from django.core.urlresolvers import reverse  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import View
from djangular.views.mixins import JSONResponseMixin

from horizon import exceptions
from horizon import tables
from horizon import workflows

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.domains import constants
from openstack_dashboard.dashboards.admin.domains \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.domains \
    import workflows as project_workflows


class IndexView(tables.DataTableView):
    table_class = project_tables.DomainsTable
    template_name = constants.DOMAINS_INDEX_VIEW_TEMPLATE

    def get_data(self):
        domains = []
        domain_context = self.request.session.get('domain_context', None)
        try:
            if domain_context:
                domain = api.keystone.domain_get(self.request,
                                                 domain_context)
                domains.append(domain)
            else:
                domains = api.keystone.domain_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve domain list.'))
        return domains


class CreateDomainView(workflows.WorkflowView):
    workflow_class = project_workflows.CreateDomain


class UpdateDomainView(workflows.WorkflowView):
    workflow_class = project_workflows.UpdateDomain

    def get_initial(self):
        initial = super(UpdateDomainView, self).get_initial()

        domain_id = self.kwargs['domain_id']
        initial['domain_id'] = domain_id

        initial['json_data_url'] = reverse('horizon:admin:domains:update_json', args=(domain_id,))

        try:
            # get initial domain info
            domain_info = api.keystone.domain_get(self.request,
                                                  domain_id)
            for field in constants.DOMAIN_INFO_FIELDS:
                initial[field] = getattr(domain_info, field, None)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve domain details.'),
                              redirect=reverse(constants.DOMAINS_INDEX_URL))
        return initial

class UpdateDomainJSONDataView(JSONResponseMixin, View):
    def get_data(self):
        data = {}
        err_msg = _('Unable to retrieve group list. Please try again later.')
        domain_id = self.kwargs['domain_id']

        # Get the default role
        try:
            default_role = api.keystone.get_default_role(self.request)
            # Default role is necessary to add members to a domain
            if default_role is None:
                default = getattr(settings,
                                  "OPENSTACK_KEYSTONE_DEFAULT_ROLE", None)
                msg = _('Could not find default role "%s" in Keystone') % \
                        default
                raise exceptions.NotFound(msg)
        except Exception:
            exceptions.handle(self.request,
                              err_msg,
                              redirect=reverse(constants.DOMAINS_INDEX_URL))
        # default_role_name = self.get_default_role_field_name()
        # self.fields[default_role_name] = forms.CharField(required=False)
        # self.fields[default_role_name].initial = default_role.id
        data['default_role_id'] = default_role.id

        # Get list of available groups
        all_groups = []
        try:
            all_groups = api.keystone.group_list(self.request,
                                                 domain=domain_id)
        except Exception:
            exceptions.handle(self.request, err_msg)
        # groups_list = [(group.id, group.name) for group in all_groups]
        data['groups'] = [{'id': group.id, 'name': group.name} for group in all_groups]

        # Get list of roles
        role_list = []
        try:
            role_list = api.keystone.role_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                              err_msg,
                              redirect=reverse(constants.DOMAINS_INDEX_URL))
        # for role in role_list:
            # field_name = self.get_member_field_name(role.id)
            # label = role.name
            # self.fields[field_name] = forms.MultipleChoiceField(required=False,
            #                                                     label=label)
            # self.fields[field_name].choices = groups_list
            # self.fields[field_name].initial = []
        data['roles'] = [{'id': role.id, 'name': role.name, 'selected_groups': []} for role in role_list]

        # Figure out groups & roles
        if domain_id:
            for group in all_groups:
                try:
                    roles = api.keystone.roles_for_group(self.request,
                                                         group=group.id,
                                                         domain=domain_id)
                except Exception:
                    exceptions.handle(self.request,
                                      err_msg,
                                      redirect=reverse(
                                          constants.DOMAINS_INDEX_URL))

                for role in roles:
                    next((r['selected_groups'].append(group.id) for r in data['roles'] if r['id'] == role.id), None)
                    # field_name = self.get_member_field_name(role.id)
                    # r['selected_groups'].append(group.id)
                    # self.fields[field_name].initial.append(group.id)


        # data = {
        #     'default_role_id': 'a1908c795d9b46d781af8682f0b9d266',
        #     'groups': [
        #         {
        #             'id': 'd6bf6cc53db54f1baf16c05464ccfbb7',
        #             'name': 'mygroup1',
        #         },
        #         {
        #             'id': 'd817f3b6aa7a4462bbf8de1e7c6909cf',
        #             'name': 'mygroup2',
        #         }
        #     ],
        #     'roles': [
        #         {
        #             'id': '9fe2ff9ee4384b1894a90878d3e92bab',
        #             'name': '_member_',
        #             'selected_groups': []
        #         },
        #         {
        #             'id': '139092b4b20048e6ad45b59d96309212',
        #             'name': 'admin',
        #             'selected_groups': ['d6bf6cc53db54f1baf16c05464ccfbb7']
        #         },
        #         {
        #             'id': 'a1908c795d9b46d781af8682f0b9d266',
        #             'name': 'Member',
        #             'selected_groups': ['d6bf6cc53db54f1baf16c05464ccfbb7']
        #         },
        #         {
        #             'id': 'f0b734b0ea4a4fe1926cff4756b1a5f7',
        #             'name': 'anotherrole',
        #             'selected_groups': []
        #         },
        #         {
        #             'id': '26bbda95f78f4320ac2f6ed488dff740',
        #             'name': 'ResellerAdmin',
        #             'selected_groups': []
        #         },
        #         {
        #             'id': '529ed653a0684981bc0dafffb21de25c',
        #             'name': 'service',
        #             'selected_groups': []
        #         },
        #     ]
        # }
        # return json.dumps(data)
        return data
