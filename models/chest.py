from odoo import models, fields, api
from odoo.exceptions import MissingError
from datetime import datetime, timedelta
import re

class Chest(models.Model):
    _name = 'ldk.chest'
    _description = 'Chest'
    _rec_name = 'chest_name'

    chest_name = fields.Char(string="Chest Name", store=True, required=True)
    chest_type = fields.Char(string="Chest Type", store=True, required=True)

    recorded = fields.Char(string='Recorded Timestamp', store=True)
    recorded_date = fields.Datetime(string="Recorded", compute='_compute_recorded', store=True)

    expiring_in = fields.Char(string='Expiring in', store=True)

    created = fields.Datetime(string='Created', compute='_compute_created', store=True)

    value = fields.Integer(string="Value", compute='_compute_value')
            
    castle_id = fields.Many2one('ldk.castle', string="Castle", store=True, required=True)

    @api.depends('recorded', 'recorded_date', 'expiring_in')
    def _compute_created(self):
        for rec in self:
            max_duration = timedelta(hours=20)
            expiring_in_timedelta = self.parse_expiring_in(expiring_in=rec.expiring_in)
            time_left = max_duration - expiring_in_timedelta
            if not rec.recorded_date:
                rec.recorded_date = datetime.now()
            rec.created = rec.recorded_date - time_left

    def parse_expiring_in(self, expiring_in):
        # Define regex patterns for hours, minutes, and seconds
        hours_pattern = re.compile(r'(\d+)h')
        minutes_pattern = re.compile(r'(\d+)m')
        seconds_pattern = re.compile(r'(\d+)s')

        clean_value = expiring_in.replace('[', '').replace(']', '').replace("'", "").replace(",", " ")

        hours = 0
        minutes = 0
        seconds = 0

        try:
            if hours_match := hours_pattern.search(clean_value):
                hours = int(hours_match.group(1))
            if minutes_match := minutes_pattern.search(clean_value):
                minutes = int(minutes_match.group(1))
            if seconds_match := seconds_pattern.search(clean_value):
                seconds = int(seconds_match.group(1))
        except Exception:
            # If there's an error in parsing, we use default 0 values
            pass

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

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
        for record in self:
            chest_value = self.env['ldk.chest.value'].search(domain=[('chest_name', '=', record.chest_name), ('chest_type', '=', record.chest_type)], limit=1)
            if not chest_value:
                chest_value = self.env['ldk.chest.value'].create({
                    'chest_name': record.chest_name,
                    'chest_type': record.chest_type,
                    'value': 0
                })
            record.value = chest_value.value

    def init(self):
        res = super().init()
        self._auto_init()
        return res
