from odoo import models, fields, api
from odoo.exceptions import MissingError

class ChestValue(models.Model):
    _name = 'ldk.chest.value'
    _description = 'Chest Value'
    _rec_name = 'chest_name'

    chest_name = fields.Char(string="Chest Name", store=True, required=True)
    chest_type = fields.Char(string="Chest Type", store=True, required=True)
    value = fields.Integer(string='Value', store=True)

    @api.model
    def get_value(self, cname, ctype):
        for records in self:
            if record.chest_name == cname and record.chest_type == ctype:
                return record.value
        raise MissingError('Value unavailable')
    
    def init(self):
        res = super().init()
        self._auto_init()
        return res
