import os
import unittest
import json
import logging
from policy_sentry.command.query import query
from policy_sentry.command.write_policy import write_policy
from kinnaird_utils.shell import run_click_command
logger = logging.getLogger(__name__)


class ShellTestCase(unittest.TestCase):

    def test_run_click_command(self):
        results = run_click_command(query, args="action-table --service ram")
        print(results.output)
        # Expected results:
        """
ALL ram actions:
ram:AcceptResourceShareInvitation
ram:AssociateResourceShare
ram:AssociateResourceSharePermission
ram:CreateResourceShare
ram:DeleteResourceShare
ram:DisassociateResourceShare
ram:DisassociateResourceSharePermission
ram:EnableSharingWithAwsOrganization
ram:GetPermission
ram:GetResourcePolicies
ram:GetResourceShareAssociations
ram:GetResourceShareInvitations
ram:GetResourceShares
ram:ListPendingInvitationResources
ram:ListPermissions
ram:ListPrincipals
ram:ListResourceSharePermissions
ram:ListResourceTypes
ram:ListResources
ram:PromoteResourceShareCreatedFromPolicy
ram:RejectResourceShareInvitation
ram:TagResource
ram:UntagResource
ram:UpdateResourceShare

        """
        self.assertTrue("ram:GetPermission" in results.output)

    def test_run_click_command_fail(self):
        with self.assertRaises(FileNotFoundError):
            results = run_click_command(write_policy, args="--input-file doesnotexist.yml")
