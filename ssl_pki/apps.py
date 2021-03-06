# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.apps import AppConfig


class SslPkiAppConfig(AppConfig):
    name = 'ssl_pki'
    label = 'ssl_pki'
    verbose_name = 'SSL/PKI'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals  # noqa
