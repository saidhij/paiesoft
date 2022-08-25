# -*- coding: utf-8 -*-

import calendar
import logging

from datetime import date, datetime, timedelta
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

def seq( start, stop, step = 1 ):
    """Return a list of float
    return eg : [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    with start=2 ; end=10; step =0.5
    """
    n = int( round( ( stop - start ) / float( step ) ) )
    if n > 1:
        return( [start + step * i for i in range( n + 1 )] ) 
    else:
        return( [] )
		
		
class Cnam(models.Model):
    _name = 'hr.cnam'
    _description = 'CNAM'
    _order = "company_id"
	
    def _get_year(self):
	
        START_YEAR = 2010
        STOP_YEAR = 2030
        STEP_YEAR = 1


        seq_year = seq(START_YEAR, STOP_YEAR, STEP_YEAR )
        seq_year = [str( i ) for i in seq_year]
        seq_year.reverse()
        year_selection = zip( seq_year, seq_year )
        return tuple( year_selection )




    _MONTH = [
        ('01', 'Janvier'),
        ('02', 'Février'),
        ('03', 'Mars'),
        ('04', 'Avril'),
        ('05', 'Mai'),
        ('06', 'Juin'),
        ('07', 'Juillet'),
        ('08', 'Août'),
        ('09', 'Septembre'),
        ('10', 'Octobre'),
        ('11', 'Novembre'),
        ('12', 'Décembre')]
		
		
    def _get_year(self):
	
        START_YEAR = 2010
        STOP_YEAR = 2030
        STEP_YEAR = 1


        seq_year = seq(START_YEAR, STOP_YEAR, STEP_YEAR )
        seq_year = [str( i ) for i in seq_year]
        seq_year.reverse()
        year_selection = zip( seq_year, seq_year )
        return tuple( year_selection )

    def _get_default_month(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%m')
		
    def _get_default_year(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%Y')
		
    @api.onchange('month','date_from','year')    
    def _get_default_start_date(self):	
        mois = int(self.month)
        year = int(self.year)		
        self.date_from= date(year, mois , 1)
 
    @api.onchange('month','date_to','year')		
    def _get_default_end_date(self):
        year = int(self.year)	
        mois = int(self.month)
        value =  mois + 1			
        self.date_to = date(year, value, 1)+ timedelta(days=-1)
		
		

    name = fields.Char(string='Déclaration N°', size=64, readonly=True, required=True, default=lambda *a: '...')
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.user.company_id)
    date_document = fields.Date('Date du document', default=lambda *a: date.today())
    year = fields.Selection(_get_year, 'Année', required=True, default=_get_default_year)
    month = fields.Selection(_MONTH, 'Mois', index=True, required=True, default=_get_default_month)	
    date_from = fields.Date("Date début",compute='_get_default_start_date')	
    date_to = fields.Date("Date de fin",compute='_get_default_end_date')		

    paie_date = fields.Char(string="Mois de la paie importée",compute='_get_paie_date')
    # periode = fields.Char('Période à déclarer',compute='_get_periode')	


    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'To Pay'),
        ('done', 'Payed'), ], 'État', index=True, default='draft', readonly=True, copy=False)
    cnam_lines = fields.One2many('hr.cnam.line', 'cnam_id', 'cnam')
	


    brut_total = fields.Float(compute='_get_total_brut', string="Masse salariale", digits=(8, 2))	
    cnam_total = fields.Float(compute='_get_total_cnam', string="TOTAL cnam", digits=(8, 2))


    net_total = fields.Float(compute='_get_total_net', string="NET A PAYER", digits=(8, 2))	
    nemploye = fields.Integer("Effectif traité",compute='_compute_employee_count')	
    cin = fields.Char(string="NNI")
    matricule_cnss = fields.Char(string="Numéro CNSS")

	
    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id)', 'Ce document existe déjà!'),]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.cnam')or '/'
        declaration = super(Cnam, self).create(vals)
        return declaration


		
   
    def _compute_employee_count(self):
        for p in self:
            p.nemploye = len(p.cnam_lines)

            
    def _get_total_brut(self):       
        for p in self: 
            total=0
            for line in p.cnam_lines:			
                total += int(line.N_Salaire_Brut)
            p.brut_total = total 
		
    def _get_paie_date(self):       
        for p in self: 
            val=0		
            for line in p.cnam_lines:
                val= line.slip_id.date_from.strftime('%B')			
            p.paie_date = val



    def cnam_confirm(self):
        return self.write({'state': 'waiting'})

    def cnam_payed(self):
        return self.write({'state': 'done'})


		
    def print_report(self):
        return self.env.ref('hr_payroll_ma_pro.action_report_etat_cnam').report_action(self)



    def cnam_generate(self):
        f_line_obj = self.env['hr.cnam.line']
        slip_obj = self.env['hr.payslip']
        slip_line_obj = self.env['hr.payslip.line']
        cnam_lines = []
        for o in self:
            old_f_lines = f_line_obj.search([('cnam_id', '=', o.id)])
            if old_f_lines:
                old_f_lines.unlink()
            date_from= o.date_from
            date_to= o.date_to	
            month = o.month if len(str(o.month)) == 1 else '0' + str(o.month)
			
            employee_ids = self.env['hr.employee'].search([('contract_id.state', '=', 'open')])
			
            slip_ids = slip_obj.search([
                ('date_from', '>=', date_from),
                ('date_to', '<=', date_to),
                ('employee_id', 'in', employee_ids.ids),
               ])
            for slip in slip_ids:
                # base = slip_line_obj.search([('slip_id', '=', slip.id), ('code', '=', 'BASIC')], limit=1)
                # base = base.total or 0.0

                brute = slip_line_obj.search([('slip_id', '=', slip.id), ('code', '=', 'BRUT')], limit=1)
                month_1 = brute.total or 0.0
				
                sal_plaf = slip_line_obj.search([('slip_id', '=', slip.id), ('code', '=', 'PLAFOND')], limit=1)
                sal_plaf = sal_plaf.total or 0.0

                tt = slip_line_obj.search([('slip_id', '=', slip.id), ('code', '=', 'WDAYS')], limit=1)
                tt1 = tt.total

                brute_total = month_1 
                cnam_lines.append((0, 0, {
                    'cnam_id': o.id,
					'Num_CIN':slip.employee_id.cin,
                    'slip_id': slip.id,
                    'L_Nom': slip.employee_id.last_nameup,
                    'L_Prenom': slip.employee_id.first_nameup,					
					'N_Num_Assure':slip.employee_id.matricule_cnss,
					'L_Situation':slip.employee_id.contract_id.situation,					
                    'N_Salaire_Brut': brute_total,					
                    'N_Jours_Declares': tt1,					
                   
        
                }))
            o.write({'cnam_lines': cnam_lines})
        return True
		


class CNAMLine(models.Model):
    _name = 'hr.cnam.line'
    _description = 'CNAM'

    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'CNAM' + str(record.cnam_id.id) + '-' + str(record.employee_id.id) + '-' + str(record.id)
        return res

    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    cnam_id = fields.Many2one('hr.cnam', 'CNAM', required=True, ondelete='cascade', index=True)
    observation = fields.Char('Observation', size=120)
    L_Nom = fields.Char( 'Nom')
    L_Prenom = fields.Char( 'Prénom')	
    slip_id = fields.Many2one('hr.payslip', 'Payslip', ondelete='cascade')	
    N_Salaire_Reel = fields.Char('Salaire Reel en centimes',compute='_get_Salaire_Reelcentimes')
    N_Salaire_Brut = fields.Float('Salaire Brut')	
    N_Jours_Declares = fields.Integer('Jours déclarés')
    Num_CIN = fields.Char(string="N° CIN")	
    L_Situation = fields.Char(string="Situation")		
    N_Num_Assure = fields.Char(string="Numéro CNSS")	



    def _get_Salaire_Reelcentimes(self):       
        for p in self: 	
            p.N_Salaire_Reel = int((p.N_Salaire_Brut)*100)
