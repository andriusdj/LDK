from odoo import models, fields, api

class ChestValue(models.Model):
    _name = 'ldk.castle'
    _description = 'Castle'
    _rec_name = 'name'

    name = fields.Char(string="Castle Name", store=True)
    capitol_level = fields.Integer(string="Capitol Level", store=True)
    guards_level = fields.Integer(string="Guards Level", store=True)

    is_main = fields.Boolean(string="Is Main?", store=True)
        
    chest_ids = fields.One2many('ldk.chest', 'castle_id', string="Chests", store=True)
    
    partner_id = fields.Many2one('res.partner', string='Owner', store=True)

    chest_value_total = fields.Integer(string="Total value of chests", compute='_compute_chests')
    #chest_worth_week
    #chest_worth_day
    #chest_worth_2week

    @api.depends('chest_ids')
    def _compute_chests(self):
        for record in self:
            value = 0
            for chest in record.chest_ids:
                if chest.castle_id.id == record.id:
                    value += chest.value
            record.chest_value_total = value

    def init(self):
        res = super().init()
        self._auto_init()
        return res
