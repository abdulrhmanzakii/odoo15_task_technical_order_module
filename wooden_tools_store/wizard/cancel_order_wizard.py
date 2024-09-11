import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class CancelOrderWizard(models.TransientModel):

    _name = "cancel.order.wizard"
    _description = "Cancel Order Wizard"

    @api.model
    def default_get(self,fields):
        res= super(CancelOrderWizard,self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['technical_order_id'] = self.env.context.get('active_id')
        return res


    technical_order_id = fields.Many2one('technical.order',string="Technical Order")
    reject = fields.Text(related="technical_order_id.reject",readonly=False)
    date_cancel = fields.Date(string="Date Cancel")

    def action_cancel(self):
        self.technical_order_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.constrains('reject')
    def cancel_reason(self):
        for rec in self:
            if not rec.reject:
                raise ValidationError(_(" Please Write The Reject Reason"))


