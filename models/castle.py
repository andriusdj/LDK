from odoo import models, fields, api

class ChestValue(models.Model):
    _name = 'ldk.castle'
    _description = 'Castle'
    _rec_name = 'name'

    name = fields.Char(string="Castle Name", store=True)
    capitol_level = fields.Integer(string="Capitol Level", store=True)
    guards_level = fields.Integer(string="Guards Level", store=True)
    
    chest_ids = fields.One2many('ldk.chest', 'castle_id', string="Chests", store=True)
    
    partner_id = fields.Many2one('res.partner', string='Owner', store=True)

    def init(self):
        res = super().init()
        self._auto_init()
        return res
