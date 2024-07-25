from odoo import fields, models, api
from datetime import datetime
import pytz
from odoo.exceptions import UserError

class SummaryMovement(models.TransientModel):
    _name = 'wh.wizard'
    _description = "Account info wizard"

    # Fields for the wizard
    date_start = fields.Date('Date From')
    date_end = fields.Date('Date To', default=fields.Date.today)
    product_id = fields.Many2one('product.product')
    lot_id = fields.Many2one('stock.production.lot')
    partner_id = fields.Many2one('res.partner', string='Customer')

    # Method to generate Excel report
    def print_excel_report(self):
        domain = []
        product_id = self.product_id
        lot_id = self.lot_id
        date_start = self.date_start
        date_end = self.date_end

        if date_start:
            domain += [('date', '>=', date_start)]
        if date_end:
            domain += [('date', '<=', date_end)]
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        if lot_id:
            domain += [('lot_id', '=', lot_id.id)]

        # Search for stock move lines with serial numbers
        k_move_in = self.env['stock.move.line'].search(domain + [('location_dest_id.usage', '=', 'internal'), ('lot_id', '!=', False)])
        k_move_out = self.env['stock.move.line'].search(domain + [('location_id.usage', '=', 'internal'), ('lot_id', '!=', False)])

        product_moves = {}

        # Categorize moves by product and lot
        for move in k_move_in:
            key = (move.product_id.id, move.lot_id.id)
            if key not in product_moves:
                product_moves[key] = {'in': [], 'out': []}
            product_moves[key]['in'].append(move)

        for move in k_move_out:
            key = (move.product_id.id, move.lot_id.id)
            if key not in product_moves:
                product_moves[key] = {'in': [], 'out': []}
            product_moves[key]['out'].append(move)

        account_moves_data = []

        # Collect data for each move
        for key, moves in product_moves.items():
            if moves['in'] and moves['out']:
                for move in moves['in'] + moves['out']:
                    data = {
                        'date': move.date,
                        'serial_no': move.lot_id.name,
                        'lot_no': move.lot_id.name,
                        'partner': move.picking_id.partner_id.name if move.picking_id else move.pos_order_id.partner_id.name,
                        'partner_address': move.picking_id.partner_id.street if move.picking_id else move.pos_order_id.partner_id.street,
                        'partner_city': move.picking_id.partner_id.city if move.picking_id else move.pos_order_id.partner_id.city,
                        'partner_zip': move.picking_id.partner_id.zip if move.picking_id else move.pos_order_id.partner_id.zip,
                        'product': move.product_id.name,
                    }
                    account_moves_data.append(data)

        # Get the current date and time in the user's timezone
        user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
        current_datetime_user = datetime.now(pytz.timezone(user_tz))
        data = {
            'account_moves_data': account_moves_data,
            'form': self.read()[0],
            'current_date': current_datetime_user.strftime('%Y-%m-%d'),
            'current_time': current_datetime_user.strftime('%H:%M:%S'),
        }

        # Return the action for generating the Excel report
        return self.env.ref('wh_in_out_report_xlsx_pdf.wh_in_out_xlsx_action_report').report_action(self, data=data)

    # Method to generate PDF report
    def print_pdf_report(self):
        domain = []
        product_id = self.product_id
        lot_id = self.lot_id
        date_start = self.date_start
        date_end = self.date_end

        if date_start:
            domain += [('date', '>=', date_start)]
        if date_end:
            domain += [('date', '<=', date_end)]
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        if lot_id:
            domain += [('lot_id', '=', lot_id.id)]

        # Search for stock move lines with serial numbers
        k_move_in = self.env['stock.move.line'].search(domain + [('location_dest_id.usage', '=', 'internal'), ('lot_id', '!=', False)])
        k_move_out = self.env['stock.move.line'].search(domain + [('location_id.usage', '=', 'internal'), ('lot_id', '!=', False)])

        product_moves = {}

        # Categorize moves by product and lot
        for move in k_move_in:
            key = (move.product_id.id, move.lot_id.id)
            if key not in product_moves:
                product_moves[key] = {'in': [], 'out': []}
            product_moves[key]['in'].append(move)

        for move in k_move_out:
            key = (move.product_id.id, move.lot_id.id)
            if key not in product_moves:
                product_moves[key] = {'in': [], 'out': []}
            product_moves[key]['out'].append(move)

        account_moves_data = []

        # Collect data for each move
        for key, moves in product_moves.items():
            if moves['in'] and moves['out']:
                for move in moves['in'] + moves['out']:
                    data = {
                        'date': move.date,
                        'serial_no': move.lot_id.name,
                        'lot_no': move.lot_id.name,
                        'partner': move.picking_id.partner_id.name if move.picking_id else move.pos_order_id.partner_id.name,
                        'partner_address': move.picking_id.partner_id.street if move.picking_id else move.pos_order_id.partner_id.street,
                        'partner_city': move.picking_id.partner_id.city if move.picking_id else move.pos_order_id.partner_id.city,
                        'partner_zip': move.picking_id.partner_id.zip if move.picking_id else move.pos_order_id.partner_id.zip,
                        'product': move.product_id.name,
                    }
                    account_moves_data.append(data)

        # Get the current date and time in the user's timezone
        user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
        current_datetime_user = datetime.now(pytz.timezone(user_tz))
        data = {
            'account_moves_data': account_moves_data,
            'form': self.read()[0],
            'current_date': current_datetime_user.strftime('%Y-%m-%d'),
            'current_time': current_datetime_user.strftime('%H:%M:%S'),
        }

        # Return the action for generating the PDF report
        return self.env.ref('wh_in_out_report_xlsx_pdf.wh_in_out_pdf_report_action').report_action(self, data=data)

class StockMoveWizard(models.TransientModel):
    _name = 'stock.move.wizard'
    _description = 'Stock Move Wizard'

    # Fields for the wizard
    check = fields.Boolean(default=False)
    processed = fields.Boolean(default=False)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", default=fields.Date.today)

    # Method to process stock moves
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

        k_move_in = self.env['stock.move.line'].search(domain_in + [('lot_id', '!=', False)])
        k_move_out = self.env['stock.move.line'].search(domain_out + [('lot_id', '!=', False)])

        created_moves = set()

        # Categorize moves by product and lot
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

        # Return the action for displaying the stock detail records
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Detail',
            'view_mode': 'tree',
            'res_model': 'stock.detail',
            'domain': detail_domain,
            'target': 'current',
        }
