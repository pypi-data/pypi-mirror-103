from odoo import api, fields, models, _
import logging
from datetime import date
_logger = logging.getLogger(__name__)


class ContractEmailChangeWizard(models.TransientModel):
    _name = 'contract.email.change.wizard'
    partner_id = fields.Many2one('res.partner')
    summary = fields.Char(required=True, default=_('Email change'))
    done = fields.Boolean(default=True)
    location = fields.Char()
    note = fields.Char()
    start_date = fields.Date('Start Date', required=True)
    available_email_ids = fields.Many2many(
        'res.partner',
        string="Available Emails",
        compute="_load_available_email_ids"
    )
    contract_ids = fields.Many2many('contract.contract', string='Contracts')
    email_ids = fields.Many2many(
        'res.partner',
        string='Emails',
        required=True,
    )

    @api.multi
    @api.depends("partner_id")
    def _load_available_email_ids(self):
        if self.partner_id:
            self.available_email_ids = [
                (6, 0, self.partner_id.get_available_email_ids())
            ]

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        defaults['start_date'] = self._get_first_day_of_next_month(date.today())
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        for contract in self.contract_ids:
            message_partner = _("Email changed ({} --> {}) in partner's contract '{}'")
            self.partner_id.message_post(
                message_partner.format(
                    ', '.join([email.email for email in contract.email_ids]),
                    ', '.join([email.email for email in self.email_ids]),
                    contract.name
                )
            )
            message_contract = _("Contract email changed ({} --> {})")
            contract.message_post(
                message_contract.format(
                    ', '.join([email.email for email in contract.email_ids]),
                    ', '.join([email.email for email in self.email_ids]),
                )
            )

            contract.write(
                {'email_ids': [(6, 0, [email.id for email in self.email_ids])]}
            )
            self._create_activity(contract.id)

        self.enqueue_OC_email_update()

        return True

    def _get_first_day_of_next_month(self, request_date):
        if request_date.month == 12:
            return date(request_date.year+1, 1, 1)
        else:
            return date(request_date.year, request_date.month+1, 1)

    def _create_activity(self, contract_id):
        self.env['mail.activity'].create({
            'summary': self.summary,
            'res_id': contract_id,
            'res_model_id': self.env.ref('contract.model_contract_contract').id,
            'user_id': self.env.user.id,
            'activity_type_id': self.env.ref('somconnexio.mail_activity_type_contract_data_change').id, # noqa
            'done': self.done,
            'date_done': date.today(),
            'date_deadline': date.today(),
            'location': self.location,
            'note': self.note,
        })

    def enqueue_OC_email_update(self):
        self.env['contract.contract'].with_delay(
            priority=50,
        ).update_subscription(
            self.contract_ids,
            "email"
        )
