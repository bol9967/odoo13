from odoo import models, fields, api
from odoo.exceptions import UserError
import pytz

class StockDetail(models.Model):
    _name = 'stock.detail'
    _description = 'Stock Detail'

    date_in_wh_location = fields.Datetime(string="Date In WH Location")
    date_out_going_to_partner_customer = fields.Datetime(string="Date Out Going To Partner/Customer")
    serial = fields.Char(string="Serial")  # Ensure this is recorded only if present
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

class StockMoveWizard(models.TransientModel):
    _name = 'stock.move.wizard'
    _description = 'Stock Move Wizard'

    check = fields.Boolean(default=False)
    processed = fields.Boolean(default=False)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", default=fields.Date.today)

    def process_stock_moves(self):
        if self.processed:
            raise UserError('The stock moves have already been processed.')

        self.check = True

        domain = []
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))

        domain_in = domain + [('location_dest_id.usage', '=', 'internal')]
        domain_out = domain + [('location_id.usage', '=', 'internal')]

        k_move_in = self.env['stock.move.line'].search(domain_in)
        k_move_out = self.env['stock.move.line'].search(domain_out)

        created_moves = set()

        for move in k_move_in:
            if not move.lot_id:
                continue  # Skip if the product doesn't have a serial number

            key = move.lot_id.name
            if key not in created_moves:
                created_moves.add(key)

                product_moves = {
                    'in': [move],
                    'out': [],
                }

                for out_move in k_move_out.filtered(lambda m: m.lot_id.name == move.lot_id.name):
                    product_moves['out'].append(out_move)

                if product_moves['in'] and product_moves['out']:
                    date_in = product_moves['in'][0].date.date() if product_moves['in'] else False

                    for move_out in product_moves['out']:
                        existing_record = self.env['stock.detail'].search([
                            ('serial', '=', move_out.lot_id.name)
                        ], limit=1)

                        vals = {
                            'date_in_wh_location': date_in,
                            'date_out_going_to_partner_customer': move_out.date,
                            'serial': move_out.lot_id.name,
                            'inventory_variation_reference': move_out.picking_id.name if move_out.picking_id else move_out.pos_order_id.name,
                            'inventory_variation_name': move_out.product_id.name,
                            'customer_name': move_out.picking_id.partner_id.name if move_out.picking_id else move_out.pos_order_id.partner_id.name,
                            'customer_address_st': move_out.picking_id.partner_id.street if move_out.picking_id else move_out.pos_order_id.partner_id.street,
                            'address_city': move_out.picking_id.partner_id.city if move_out.picking_id else move_out.pos_order_id.partner_id.city,
                            'address_zip': move_out.picking_id.partner_id.zip if move_out.picking_id else move_out.pos_order_id.partner_id.zip,
                            'check': self.check,
                        }

                        if existing_record:
                            existing_record.write(vals)
                        else:
                            self.env['stock.detail'].create(vals)

        self.processed = True

        detail_domain = []
        if self.start_date:
            detail_domain.append(('date_in_wh_location', '>=', self.start_date))
        if self.end_date:
            detail_domain.append(('date_out_going_to_partner_customer', '<=', self.end_date))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Detail',
            'view_mode': 'tree',
            'res_model': 'stock.detail',
            'domain': detail_domain,
            'target': 'current',
        }
