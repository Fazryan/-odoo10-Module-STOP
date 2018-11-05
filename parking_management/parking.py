from odoo import api,models,fields
from datetime import date
from datetime import time
from datetime import datetime   




class ParkingLog(models.Model):
    _name='parking_management'
    _rec_name='vehicle_number'
    
      
    
    vehicle_number=fields.Many2one('vehicle_log',string='Nomor Kendaraan')
    vehicle_type=fields.Many2one('type_vehicle', string='Jenis Kendaraan', ondelete='cascade', related='vehicle_number.vehicle_tipe')
    parking_start=fields.Datetime(string='Masuk', default=fields.Datetime.now, required='True', readonly='True')
    parking_end=fields.Datetime(string='Keluar' ,states={'in' : [('readonly', 'False')], 'paid' : [('readonly', 'False')]})
    billing_id=fields.Integer('Tarif', related='vehicle_type.billing_ids',states={'in' : [('readonly', 'False')], 'paid' : [('readonly', 'False')]}, store='True', readonly='True', compute='action_close', track_visibility='onchange')
    staff_id=fields.Many2one('res.users',string='Petugas', default=lambda self: self.env.user, readonly='true')
 
    state = fields.Selection([
                                ('in', 'In'),
                                ('out', 'Out'),
                                ('paid', 'Paid'),
                                ], string='Status', readonly='True', copy='False',
                                default='in')
    
#     price_vehicle = fields.Selection ([
#                                         ('mtr','2000'),
#                                         ('mbl','3000'),
#                                         ('box','2000'),
#                                         ('bus/truk','5000'),], string='Tarif Kendaraan'
#                                         readonly='True', copy='False')
    
    vehicle_number_ids=fields.One2many('vehicle_log','vehicle_number') 

    
    @api.multi
    def action_confirm(self):
        self.write({'state': 'in'})
    @api.multi
    def action_cancel(self):
        self.write({'state': 'out'})
    @api.multi
    def action_close(self):
        first_billing = 2000
        parking_end_days = abs(fields.Datetime.from_string(fields.Datetime.now()) - fields.Datetime.from_string(self.parking_start)).days
        parking_end_seconds = abs(fields.Datetime.from_string(fields.Datetime.now()) - fields.Datetime.from_string(self.parking_start)).seconds
        parking_end_hours = parking_end_days * 24 + parking_end_seconds // 3600
        billing = first_billing + (parking_end_hours - 1) * 2000
        self.write({'billing_id' : billing}) 
        self.write({'parking_end':fields.Datetime.now(self)})
        self.write({'state':'paid'})
        
    
#     @api.multi('parking_end')
#     def tarif_parkir(self):
#         if self.parking_end:
#             tarif = datetime.strptime(self.tarif, '%m/%d/%Y')
#             self.parking_end = (parking_start.today() - tarif).hours + 2000

#     @api.depends('parking_end')
#     def compute_tarif_parking(self):
#         first_billing = 2000
#         for rec in self:
#             parking_end_days = abs(fields.Datetime.from_string(fields.Datetime.now()) - fields.Datetime.from_string(rec.parking_start)).days
#             parking_end_seconds = abs(fields.Datetime.from_string(fields.Datetime.now()) - fields.Datetime.from_string(rec.parking_start)).seconds
#             parking_end_hours = parking_end_days * 24 + parking_end_seconds // 3600
#             billing = first_billing + (parking_end_hours - 1) * 2000
#             rec.billing = billing

    
#     @api.depends('parkir.price_total')
#     def _amount_all(self):
#         for order in self:
#             amount_untaxed = amount_tax = 0.0
#             for line in order.parkir:
#                 amount_untaxed += line.price_subtotal
#                 amount_tax += line.price_tax
#             order.update({
#                 'amount_untaxed' : order.pricelist_id.currency_id.round(amount_untaxed)
#                 })
        
class TypeVehicle(models.Model):
    _name='type_vehicle'
    _rec_name='vehicle_id'
    
    vehicle_id=fields.Char('Jenis Kendaraan') 
    billing_ids=fields.Integer('Tarif')
    
    
class VehicleLog(models.Model):    
    _name='vehicle_log'
    _rec_name='vehicle_number'
 
    vehicle_tipe=fields.Many2one('type_vehicle',string='Tipe Kendaraan', ondelete='cascade')
    owner=fields.Many2one('res.partner',string='Pemilik', ondelete='cascade')
    vehicle_number=fields.Char('Nomor Kendaraan')

class Employee(models.Model):
    _inherit='hr.employee'
    _rec_name='name'
    
class Partner(models.Model):
    _inherit='res.partner'
    _rec_name='name'      
    
    vehicle_log_ids=fields.One2many('vehicle_log','owner',string='List Kendaraan')
    
class ParkingPoint(models.Model):
    _name='parking_point'
    
    
    parking_zone=fields.Selection([('a','Zona Pusat'),
                                   ('b','Zona Menengah'),
                                   ('c','Zona Pinggiran'),
                                   ],string='Zona parkir', copy='False' ,default='a')
    two_wheels = fields.Integer(string='Motor')
    four_wheels = fields.Integer(string='Mobil Umum')
    box_car = fields.Integer(string='Mobil Box')
    big_car = fields.Integer(string='Bus / Truk')
    
 
       

        