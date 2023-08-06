# -*- coding: utf-8 -*-
from mock import patch, Mock
from ..sc_test_case import SCTestCase


class TestContractEmailChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('base.partner_demo')
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.contract = self.env['contract.contract'].create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({
            'name': 'Test Contract Broadband B'
        })
        self.contract_same_partner = self.env['contract.contract'].with_context(
            tracking_disable=True
        ).create(
            vals_contract_same_partner
        )
        self.partner_email_b = self.env['res.partner'].create({
            'name': 'Email b',
            'email': 'email_b@example.org',
            'type': 'contract-email',
            'parent_id': self.partner.id
        })
        self.user_admin = self.browse_ref('base.user_admin')

    @patch(
        'odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService',  # noqa
        return_value=Mock(spec=["run"])
    )
    def test_wizard_one_email_change_ok(self, MockUpdateService):
        wizard = self.env['contract.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id, self.contract.id
            ])],
            'email_ids': [(6, 0, [self.partner_email_b.id])]
        })
        wizard.button_change()
        self.assertEquals(self.contract_same_partner.email_ids, self.partner_email_b)
        self.assertEquals(self.contract.email_ids, self.partner_email_b)

        MockUpdateService.assert_called_once_with(
            wizard.contract_ids,
            "email"
        )
        MockUpdateService.return_value.run.assert_called_once_with()

    @patch(
        'odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService',  # noqa
        return_value=Mock(spec=["run"])
    )
    def test_wizard_many_email_change_ok(self, MockUpdateService):
        wizard = self.env['contract.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id, self.contract.id
            ])],
            'email_ids': [(6, 0, [
                self.partner_email_b.id, self.partner.id
            ])]
        })
        wizard.button_change()
        self.assertIn(self.partner, self.contract.email_ids)
        self.assertIn(self.partner_email_b, self.contract.email_ids)
        self.assertIn(self.partner, self.contract_same_partner.email_ids)
        self.assertIn(self.partner_email_b, self.contract_same_partner.email_ids)

        MockUpdateService.assert_called_once_with(
            wizard.contract_ids,
            "email"
        )
        MockUpdateService.return_value.run.assert_called_once_with()

    @patch(
        'odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService',  # noqa
        return_value=Mock(spec=["run"])
    )
    def test_wizard_email_change_activity_register(self, MockUpdateService):
        wizard = self.env['contract.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id,
            ])],
            'email_ids': [(6, 0, [self.partner_email_b.id])]
        })

        mail_activities_before = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)]
        )

        wizard.button_change()

        mail_activities_after = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)]
        )

        self.assertEquals(len(mail_activities_after) - len(mail_activities_before), 1)

        email_change = mail_activities_after[-1]
        self.assertEquals(email_change.user_id, self.user_admin)
        self.assertEquals(email_change.summary, 'Email change')
        self.assertEquals(
            email_change.activity_type_id,
            self.browse_ref('somconnexio.mail_activity_type_contract_data_change')
        )
        self.assertEquals(email_change.done, True)
