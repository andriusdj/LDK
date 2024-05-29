from odoo import models, fields

class CastleOwner(models.Model):
    _inherit = 'res.partner'

    castle_ids = fields.One2many('ldk.castle', 'partner_id', string="Owned Castles", store=True)
