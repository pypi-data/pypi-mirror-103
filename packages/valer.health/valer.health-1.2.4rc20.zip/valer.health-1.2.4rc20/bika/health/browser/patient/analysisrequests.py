# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.HEALTH.
#
# SENAITE.HEALTH is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.health import bikaMessageFactory as _
from bika.health.utils import is_internal_client
from bika.lims import api
from bika.lims.browser import BrowserView
from bika.lims.browser.analysisrequest import AnalysisRequestsView as BaseView

from bika.lims.utils import get_link
from plone.memoize import view as viewcache
import logging
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as _
from bika.health import logger


class AnalysisRequestsView(BaseView):

    def __init__(self, context, request):
        super(AnalysisRequestsView, self).__init__(context, request)
        self.contentFilter['getPatientUID'] = self.context.UID()
        self.show_all = True
        self.columns['BatchID']['title'] = _('Case ID')
        self.columns['getPatientFirstName'] =  {
                "title": _("First Name"),
        }
        self.columns['getPatientLastName'] =  {
                "title": _("Last Name"),
        }
        self.columns['getTestNames'] =  {
                "title": _("Test Names"),
        }
        self.columns['getPhysician'] =  {
                "title": _("Physician"),
        }

    def folderitems(self):
        pm = getToolByName(self.context, "portal_membership")
        member = pm.getAuthenticatedMember()
        # We will use this list for each element
        roles = member.getRoles()
        # delete roles user doesn't have permissions
        if 'Manager' not in roles \
            and 'LabManager' not in roles \
                and 'LabClerk' not in roles:
            self.remove_column('getPatientID')
            #self.remove_column('getClientPatientID')
            self.remove_column('getPatientTitle')
            self.remove_column('getDoctorTitle')
        # Otherwise show the columns in the list
        else:
            for rs in self.review_states:
                i = rs['columns'].index('BatchID') + 1
                rs['columns'].insert(i, 'getClientPatientID')
                rs['columns'].insert(i, 'getPatientID')
                rs['columns'].insert(i, 'getPatientTitle')
                rs['columns'].insert(i, 'getDoctorTitle')
                rs['columns'].insert(i, 'getPatientFirstName')
                rs['columns'].insert(i, 'getPatientLastName')
                rs['columns'].insert(i, 'getTestNames')
                rs['columns'].insert(i, 'getPhysician')

        return super(AnalysisRequestsView, self).folderitems()

    @viewcache.memoize
    def get_brain(self, uid, catalog):
        if not api.is_uid(uid):
            return None
        query = dict(UID=uid)
        brains = api.search(query, catalog)
        if brains and len(brains) == 1:
            return brains[0]
        return None

    def folderitem(self, obj, item, index):
        item = super(AnalysisRequestsView, self).folderitem(obj, item, index)

        logging.info("============================================================================================== folderitem called")
        url = '{}/analysisrequests'.format(obj.getPatientURL)
        item['getPatientID'] = obj.getPatientID
        item['getPatientTitle'] = obj.getPatientTitle

        patient_brain = self.get_brain(obj.getPatientUID,'bikahealth_catalog_patient_listing')

        item['getClientPatientID'] = obj.getClientPatientID
        item['getPatientFirstName'] = patient_brain.getObject().getFirstname()
        item['getPatientLastName']  = patient_brain.getObject().getSurname()

        analyses = obj.getObject().getAnalyses()
        logging.info(analyses)
        analyses_list = ""

        for an in analyses:
            analyses_list = an.Title + ", " + analyses_list
        item['getTestNames'] = analyses_list

        item['getPhysician'] = 'Physician Name'

        # Replace with Patient's URLs
        if obj.getClientPatientID:
            item['replace']['getClientPatientID'] = get_link(
                url, obj.getClientPatientID)

        if obj.getPatientTitle:
            item['replace']['getPatientTitle'] = get_link(
                url, obj.getPatientTitle)

        if obj.getPatientID:
            item['replace']['getPatientID'] = get_link(url, obj.getPatientID)

        # Doctor
        item['getDoctorTitle'] = obj.getDoctorTitle
        if obj.getDoctorURL:
            url = '{}/analysisrequests'.format(obj.getDoctorURL)
            item['replace']['getDoctorTitle'] = get_link(url, obj.getDoctorTitle)

        return item


class AnalysisRequestAddRedirectView(BrowserView):
    """Artifact to redirect the user to AR Add view when 'AR Add' button is
    clicked in Patient's Analysis Requests view
    """

    def __call__(self):
        client = self.context.getClient()
        if not client:
            # Patient from the laboratory (no client assigned)
            base_folder = api.get_portal().analysisrequests
        elif is_internal_client(client):
            # Patient from an internal client, shared
            base_folder = api.get_portal().analysisrequests
        else:
            # Patient from an external client, private
            base_folder = client

        url = "{}/{}".format(api.get_url(base_folder), "ar_add")
        url = "{}?Patient={}".format(url, api.get_uid(self.context))
        qs = self.request.getHeader("query_string")
        if qs:
            url = "{}&{}".format(url, qs)
        return self.request.response.redirect(url)
