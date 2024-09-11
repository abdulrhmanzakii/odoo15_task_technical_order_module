from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TechnicalOrder(models.Model):
    _name = "technical.order"
    _description = "Technical Order "
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'seq'
    _order = 'id desc'

    seq = fields.Char(string="Sequence")
    name= fields.Char(string="Name",required=True)
    confirm_user=fields.Many2one('res.users',string="Confirm User",required=True,default=lambda self: self.env.user)
    start_date=fields.Date(string="Start Date",default=fields.Datetime.now)
    end_date = fields.Date(string="End Date")
    reject = fields.Text(string="Rejection Reason")
    technical_order_line_ids=fields.One2many('technical.lines.ids','technical_order_id',string="Technical Orders")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',string="Currency",currency_field="currency_id",
                                related="company_id.currency_id")

    amount_total=fields.Monetary(String="Total Price",currency_field="currency_id",compute="_compute_amount_total")
    note=fields.Html(string="Note")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'To be Approved'),
        ('so', 'Sale Order'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancel')], string="Statues",required=True,default='draft',tracking=True)

    sale_id = fields.Many2one('sale.order',string="Sale Order")
    partner_id = fields.Many2one('res.partner',string="Customer")
    so_count=fields.Integer("# Sales",store=True,compute="_compute_so_count")
    sale_order_ids = fields.One2many(comodel_name='sale.order',inverse_name='technical_order_id'
                                     ,string="Sale for Count")
    technical_lines_id =fields.Many2one('technical.lines.ids',string="Technical orders")


    # @api.depends('sale_order_ids')
    # def _compute_so_count(self):
    #     for rec in self:
    #         rec.so_count= self.env['sale.order'].search_count([('technical_order_id','=',rec.id)])


    @api.depends('sale_order_ids')
    def _compute_so_count(self):
        technical_group= self.env['sale.order'].read_group(domain=[('technical_order_id','=',self.id)]
                                                                ,fields=['technical_order_id']
                                                                ,groupby=['technical_order_id'])
        for technical in technical_group:
            technical_order_id=technical.get('technical_order_id')[0]
            technical_rec=self.browse(technical_order_id)
            technical_rec.so_count = technical['technical_order_id_count']
            self -= technical_rec
        self.so_count = 0

    def action_view_sale_order(self):
        return {
            'name': _('Sales'),
            'res_model': 'sale.order',
            'view_mode': 'list,form,activity,calendar,graph,pivot',
            'domain': [('technical_order_id','=',self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {'default_technical_order_id':self.id},
        }



    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


    def action_submit(self):
        for rec in self:
            rec.state = 'submit'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    # def action_reject(self):
    #     for rec in self:
    #         rec.state = 'cancel'



    @api.depends('technical_order_line_ids')
    def _compute_amount_total(self):
        for rec in self:
            amount_total=0
            for line in rec.technical_order_line_ids:
                amount_total += line.price_sub_total
            rec.amount_total = amount_total










    @api.model
    def create(self,vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('technical.order')
        self = super(TechnicalOrder,self).create(vals)
        return self



    def write(self,vals):
        if not self.name and not vals.get('seq'):
            vals['seq'] = self.env['ir.sequence'].next_by_code('technical.order')
        return super(TechnicalOrder,self).write(vals)

class TechnicalOrderLines(models.Model):
    _name = "technical.lines.ids"
    _description = "Technical Order Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price', default=0.0)
    qty = fields.Float(string="Quantity", default=1)
    technical_order_id =fields.Many2one('technical.order',string="Technical Order")
    company_currency_id =fields.Many2one('res.currency',string="Currency",related='technical_order_id.currency_id')
    price_sub_total=fields.Monetary(string="Sub Total",currency_field="company_currency_id"
                                        ,compute="_compute_price_sub_total")
    order_line = fields.Many2one('sale.order.line')
    name = fields.Text(related='order_line.name')



    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.lst_price


    @api.depends('qty','price_unit')
    def _compute_price_sub_total(self):
        for rec in self:
            rec.price_sub_total = rec.price_unit * rec.qty




