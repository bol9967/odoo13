from odoo import models
from odoo.tools.misc import xlsxwriter
from datetime import datetime
from num2words import num2words


class CashBook(models.AbstractModel):
    _name = 'report.wh_in_out_report_xlsx_pdf.wh_in_out_report_xlsx_id'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('ST Register')
        cell_format = workbook.add_format({'font_size': 12, 'align': 'left', 'valign': 'top', 'bold': True})
        cell_format1 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True, 'color': 'green'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 20})
        format1 = workbook.add_format({'font_size': 10, 'align': 'center', 'bg_color': '#c5d3d4', 'border': 1})
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True, 'border': 1})
        format4 = workbook.add_format({'font_size': 10,
                                       'align': 'left',
                                       'valign': 'left',
                                       'bg_color': '#b7c3c7',
                                       'border': 1
                                       })
        format3 = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bg_color': '#b7c3c7',
            'border': 1
        })
        txt = workbook.add_format({'font_size': 10, 'align': 'center'})
        main_merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '13',
            "font_color": 'black',
            "bg_color": '#F7DC6F',
            'font_name': 'Metropolis',
        })

        sheet.write('B2 ', 'Print Date:', cell_format)
        sheet.set_column('B:C', 15)
        sheet.write('C2', data['current_date'], cell_format)
        sheet.write('B3', 'Print Time:', cell_format)
        sheet.set_column('B:C', 15)
        sheet.write('C3', data['current_time'], cell_format)

        if data['form']['date_start'] and data['form']['date_end']:
            sheet.write('F2', 'From:', cell_format)
            sheet.write('G2', data['form']['date_start'], cell_format)
            sheet.write('F3', 'To:', cell_format)
            sheet.write('G3', data['form']['date_end'], cell_format)

        t_row = 6
        col = 0

        sheet.merge_range('A6:A7', "Date In WH Location", format3)
        sheet.merge_range('B6:B7', "Date Out Going to Partner/Customer'", format3)
        sheet.merge_range('C6:C7', "Serial", format3)
        sheet.merge_range('D6:D7', "Inventory Variation Reference", format3)
        sheet.merge_range('E6:E7', "Inventory Variation Name", format3)
        sheet.merge_range('F6:F7', "Customer Name", format3)
        sheet.merge_range('G6:G7', "Customer Address St", format3)
        sheet.merge_range('H6:H7', "Address City", format3)
        sheet.merge_range('I6:I7', "Address Zip", format3)

        col += 1
        sheet.set_column('D:D', 25)
        sheet.set_column('C:C', 15)
        col += 1
        sheet.set_column('E:E', 25)
        col += 1
        sheet.set_column('B:B', 30)
        sheet.set_column('A:A', 30)
        col += 1
        sheet.set_column('F:F', 18)
        col += 1
        sheet.set_column('G:G', 25)
        col += 1
        sheet.set_column('H:H', 20)
        col += 1
        sheet.set_column('I:I', 15)
        col += 1
        sheet.set_column('J:J', 22)
        col += 1
        sheet.set_column('K:K', 20)
        col += 1
        sheet.set_column('L:L', 20)
        col += 1
        sheet.set_column('M:M', 15)
        sheet.set_column('N:N', 15)
        sheet.set_column('O:O', 15)

        row_number = t_row + 3

        for rec in data['account_moves_data']:
            t_row = t_row + 1
            row_number = t_row + 1
            if rec['serial_no'].startswith('WH/IN/'):
                sheet.write(row_number+1, col - 11, rec['date'], format1)  # Writing date for incoming records

            elif rec['serial_no'].startswith('WH/OUT/'):
                sheet.write(row_number, col - 10, rec['date'], format1)
                sheet.write(row_number, col - 9, rec['lot_no'], format1)
                sheet.write(row_number, col - 8, rec['serial_no'], format1)
                sheet.write(row_number, col - 7, rec['product'], format4)
                sheet.write(row_number, col - 6, rec['partner'], format4)
                sheet.write(row_number, col - 5, rec['partner_address'], format1)
                sheet.write(row_number, col - 4, rec['partner_city'], format1)
                sheet.write(row_number, col - 3, rec['partner_zip'], format1)
                # Writing date for outgoing records
