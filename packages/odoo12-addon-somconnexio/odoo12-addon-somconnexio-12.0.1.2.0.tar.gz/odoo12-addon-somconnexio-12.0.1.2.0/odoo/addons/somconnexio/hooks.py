from odoo.addons.mail.models.mail_activity import MailActivity
from odoo import fields


def post_load_hook():

    def new_action_feedback(self, feedback=False):

        if 'done' not in self._fields:
            return self.action_feedback_original_sc(feedback=feedback)
        message = self.env['mail.message']
        if feedback:
            self.write(dict(feedback=feedback))
        for activity in self:
            record = self.env[activity.res_model].browse(activity.res_id)
            activity.done = True
            if not activity.date_done:
                activity.date_done = fields.Date.today()
            record.message_post_with_view(
                'mail.message_activity_done',
                values={'activity': activity},
                subtype_id=self.env.ref('mail.mt_activities').id,
                mail_activity_type_id=activity.activity_type_id.id,
            )
            message |= record.message_ids[0]
        return message.ids and message.ids[0] or False

    if not hasattr(MailActivity, 'action_feedback_original_sc'):
        MailActivity.action_feedback_original_sc = MailActivity.action_feedback
        MailActivity.action_feedback = new_action_feedback
