from odoo import models, fields,api

import pytz



class StockDetail(models.Model):
    _name = 'stock.detail'
    _description = 'Stock Detail'

    date_in_wh_location = fields.Datetime(string="Date In WH Location")
    date_out_going_to_partner_customer = fields.Datetime(string="Date Out Going To Partner/Customer")
    serial = fields.Char(string="Serial")  # Change to Char field
    inventory_variation_reference = fields.Char(string="Inventory Variation Reference")
    inventory_variation_name = fields.Char(string="Inventory Variation Name")
    customer_name = fields.Char(string="Customer Name")
    customer_address_st = fields.Char(string="Customer Address St")
    address_city = fields.Char(string="Address City")
    address_zip = fields.Char(string="Address Zip")
    check = fields.Boolean()

    def filter_stock_record(self):
        action = self.env.ref('wh_in_out_report_xlsx_pdf.action_report_wizard')
        return action.read()[0]


