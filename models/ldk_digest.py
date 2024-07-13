from odoo import models, fields, api

class LdkDigest(models.Model):
    _inherit='digest.digest'

    # kpi_res_users_connected = fields.Boolean('Connected Users')
    # kpi_res_users_connected_value = fields.Integer(compute='_compute_kpi_res_users_connected_value')
    # kpi_mail_message_total = fields.Boolean('Messages')
    # kpi_mail_message_total_value = fields.Integer(compute='_compute_kpi_mail_message_total_value')
    
    kpi_ldk_total_chests = fields.Boolean(string='Total Chests')
    kpi_ldk_total_chests_value = fields.Integer(compute='_compute_kpi_ldk_total_chests_value')

    kpi_ldk_top_count = fields.Boolean(string='Top1 by Count')
    kpi_ldk_top_count_value = fields.Integer(compute='_compute_kpi_ldk_top1_value')

    kpi_ldk_top_value = fields.Boolean(string='Top1 by Value')
    kpi_ldk_top_value_value = fields.Integer(compute='_compute_kpi_ldk_top1_value')

    #def _compute_kpi_ldk_total_chests_value(self):
