# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Red Hat, Inc.
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

from django.core.urlresolvers import reverse  # noqa

from openstack_dashboard.test import helpers as test


INDEX_URL = reverse("horizon:settings:user:index")


class UserSettingsTest(test.TestCase):

    def test_timezone_offset_is_displayed(self):
        res = self.client.get(INDEX_URL)

        self.assertContains(res, "Australia/Melbourne (UTC +11:00)")
        self.assertContains(res, "Europe/Moscow (UTC +04:00)")
        self.assertContains(res, "Atlantic/Stanley (UTC -03:00)")
        self.assertContains(res, "Pacific/Honolulu (UTC -10:00)")
