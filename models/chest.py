from odoo import models, fields, api
from odoo.exceptions import MissingError

class Chest(models.Model):
    _name = 'ldk.chest'
    _description = 'Chest'
    _rec_name = 'chest_name'

    chest_name = fields.Char(string="Chest Name", store=True, required=True)
    chest_type = fields.Char(string="Chest Type", store=True, required=True)

    recorded = fields.Char(string='Recorded Timestamp', store=True)
    recorded_date = fields.Datetime(string="Recorded", compute='_compute_recorded', store=True)

    expiring_in = fields.Char(string='Expiring in', store=True)

    collected = fields.Datettime(string='Collected', compute='_compute_collected', store=True)

    value = fields.Integer(string="Value", compute='_compute_value')
            
    castle_id = fields.Many2one('ldk.castle', string="Castle", store=True, required=True)

    @api.depends('recorded')
    def _compute_recorded(self):
        for record in self:
            if record.recorded:
                try:
                    timestamp_float = float(record.recorded)
                    record.recorded_date = datetime.fromtimestamp(timestamp_float)
                except ValueError:
                    record.recorded_date = False
            else:
                record.recorded_date = False

    @api.depends('chest_name', 'chest_type')
    def _compute_value(self):
        chest_value = self.env['ldk.chest.value'].search(domain=[('chest_name', '=', self.chest_name), ('chest_type', '=', self.chest_type)], limit=1)
        if not chest_value:
            chest_value = self.env['ldk.chest.value'].create({
                'chest_name': self.chest_name,
                'chest_type': self.chest_type,
                'value': 0
            })
        self.value = chest_value.value

    def init(self):
        res = super().init()
        self._auto_init()
        return res
