from odoo import models, fields, api
from odoo.exceptions import MissingError

class Clan(models.Model):
    _name = 'ldk.clan'
    _description = 'Clan'
    _rec_name = 'name'

    name = fields.Char(string="Name", store=True, required=True)
    short = fields.Char(string="Short Code", store=True, required=True)

    member_ids = fields.One2many(comodel_name='ldk.castle', inverse_name='clan_id', string='Members', store=True) 
    
    def init(self):
        res = super().init()
        self._auto_init()
        return res
