from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class TechnicalOrder(models.Model):
    _inherit = "technical.order"
    so_created =fields.Boolean(default=False,string="Sale Order Created")


    def action_create_so_new(self):
        self.state = 'so'
        self.so_created = True
        invoice_vals = self.prepare_so_vals()

        # show_so = self.show_so()
        if len(invoice_vals['order_line']) > 0:
            invoice = self.env['sale.order'].sudo().create(invoice_vals)
            print(invoice)
        else:
            raise ValidationError(_('Products Lines Cannot be Empty'))


    # This Code Make Sale Order Without Show Form View
    def prepare_so_vals(self):
        action = {
            'technical_order_id': self.id,
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'order_line': [(0, 0, {
                        'price_unit': line.price_unit,
                        'name': line.product_id.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.qty,
                    }) for line in self.technical_order_line_ids],



        }
        return action

    # This Code Show Sale Order Form And Prepare its Values

    # def show_so(self):
    #     prepare = self.env["ir.actions.actions"]._for_xml_id("wooden_sale.sale_action_wooden_new")
    #     prepare['context'] = {
    #         'default_technical_order_id': self.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_origin': self.name,
    #         'default_order_line': [(0, 0, {
    #             'price_unit': line.price_unit,
    #             'name': line.product_id.id,
    #             'product_id': line.product_id.id,
    #             'product_uom_qty': line.qty,
    #         }) for line in self.technical_order_line_ids],
    #
    #     }
    #     return prepare


