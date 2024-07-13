from odoo import models, fields, api
import datetime

class ChestValue(models.Model):
    _name = 'ldk.castle'
    _description = 'Castle'
    _rec_name = 'name'

    name = fields.Char(string="Castle Name", store=True)
    capitol_level = fields.Integer(string="Capitol Level", store=True)
    guards_level = fields.Integer(string="Guards Level", store=True)

    is_main = fields.Boolean(string="Is Main?", store=True)
    clan_id = fields.Many2one(comodel_name='ldk.clan', string='Clan', store=True)
        
    chest_ids = fields.One2many('ldk.chest', 'castle_id', string="Chests", store=True)
    
    partner_id = fields.Many2one('res.partner', string='Owner', store=True)

    chest_value_total = fields.Integer(string="Total value of chests", compute='_compute_chests')
    chest_value_week = fields.Integer(string="Chests Value 7 days", compute='_compute_week_chests')
    chest_value_week2 = fields.Integer(string="Chests Value 14 days", compute='_compute_week_chests')

    chest_count_ragnarok7 = fields.Integer(string="Ragnarok Chests last 7 days", compute='_compute_week_chests')
    chest_count_ragnarok14 = fields.Integer(string="Ragnarok Chests last 14 days", compute='_compute_week_chests')
    
    chest_count_ancient7 = fields.Integer(string="Ancients Chests last 7 days", compute='_compute_week_chests')
    chest_count_ancient14 = fields.Integer(string="Ancients Chests last 14 days", compute='_compute_week_chests')
    
    def _compute_week_chests(self):
        current_date = datetime.datetime.now()
        seven_days_ago = current_date - datetime.timedelta(days=7)
        fourteen_days_ago = current_date - datetime.timedelta(days=14)
        for castle in self:
            castle.chest_value_week = sum(chest.value for chest in castle.chest_ids if chest.recorded_date >= seven_days_ago)
            castle.chest_value_week2 = sum(chest.value for chest in castle.chest_ids if chest.recorded_date >= fourteen_days_ago)

            chest_count_ragnarok7 = [chest for chest in castle.chest_ids if chest.recorded_date >= seven_days_ago and chest.chest_type == "Jormungandr Shop"]
            chest_count_ragnarok14 = [chest for chest in castle.chest_ids if chest.recorded_date >= fourteen_days_ago and chest.chest_type == "Jormungandr Shop"]
            chest_count_ancient7 = [chest for chest in castle.chest_ids if chest.recorded_date >= seven_days_ago and chest.chest_type == "Rise of the Ancients event"]
            chest_count_ancient14 = [chest for chest in castle.chest_ids if chest.recorded_date >= fourteen_days_ago and chest.chest_type == "Rise of the Ancients event"]

            castle.chest_count_ragnarok7 = len(chest_count_ragnarok7)
            castle.chest_count_ragnarok14 = len(chest_count_ragnarok14)
            castle.chest_count_ancient7 = len(chest_count_ancient7)
            castle.chest_count_ancient14 = len(chest_count_ancieent14)

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
