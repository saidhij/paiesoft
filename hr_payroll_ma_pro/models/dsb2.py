# -*- coding: utf-8 -*-

import calendar
import logging
import base64
# from . import get_date_interval, get_years_from
from odoo.modules.module import get_module_resource
from datetime import date, datetime, timedelta
from odoo import api, fields, models, exceptions

_logger = logging.getLogger(__name__)

		
		
class DsbTwo(models.Model):
    _name = 'damancom.dsbtwo'
    _description = 'Partie B2 du fichier DS'





    name = fields.Char(string='Déclaration N°', size=64, readonly=True, required=True, default=lambda *a: '...')
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.user.company_id)	
    date_document = fields.Date('Date du document', default=lambda *a: date.today())
    cnss_lines = fields.One2many('hr.cnss.line', 'cnss_id',  'cnss')
    cnss_lines2 = fields.One2many('hr.cnss.line2', 'cnss_id2', 'cnss2')
    cnss_lines3 = fields.One2many('hr.cnss.line3', 'cnss_id3', 'cnss3')	
    dsbtwo_lines = fields.One2many('damancom.dsbtwo.line', 'dsbtwo_id',  'dsbtwo')
    dsbtwo_lines2 = fields.One2many('damancom.dsbtwo.line2', 'dsbtwo2_id',  'dsbtwo2')
    dsbtwo_lines3 = fields.One2many('damancom.dsbtwo.line3', 'dsbtwo3_id',  'dsbtwo3')	
    dsbtwo_lines4 = fields.One2many('damancom.dsbtwo.line4', 'dsbtwo4_id',  'dsbtwo4')		
    S_Ctr = fields.Char('Somme horizontale',compute='_get_S_Ctr')	
    N_Nbr_Salaries = fields.Char('Nombre des salariés',compute='_get_N_Nbr_Salaries')
    N_T_Enfants = fields.Char('Nombre enfants.',compute='_get_N_T_Enfants')
    N_T_AF_A_Payer = fields.Char('Nombre des salariés.',compute='_get_N_T_AF_A_Payer')
    N_T_AF_A_Deduire = fields.Char('Nombre des salariés.',compute='_get_N_T_AF_A_Deduire')
    N_T_AF_Net_A_Payer = fields.Char('Nombre des salariés.',compute='_get_N_T_AF_Net_A_Payer')
    N_T_Num_Imma = fields.Char('Nombre des salariés.',compute='_get_N_T_Num_Imma')
    N_T_AF_A_Reverser = fields.Char('Nombre des salariés.',compute='_get_N_T_AF_A_Reverser')
    N_T_Jours_Declares = fields.Char('Nombre des salariés.',compute='_get_N_T_Jours_Declares') 
    N_T_Salaire_Reel = fields.Char('Nombre des salariés.',compute='_get_N_T_Salaire_Reel')
    N_T_Salaire_Plaf = fields.Char('Nombre des salariés.',compute='_get_N_T_Salaire_Plaf')  
    L_Type_Enreg = fields.Char(string='Type', default='B03')
    N_Num_Affilie = fields.Char(string='Numéro affilié',compute='_get_numero_affilie')
    L_Periode = fields.Char(string='Période',compute='_get_L_Periode')	
    N_T_Ctr = fields.Char(string='cumul',compute='_get_N_T_Ctr')		

    L_Type_Enreg_entrant = fields.Char(string='Type ', default='B05')  
    N_Num_Affilie_entrant = fields.Char(string='Numéro affilié', size=7)
    L_Periode_entrant = fields.Char(string='Période', size=6)	
    N_Nbr_Salaries_entrant = fields.Char(string='Nombre de Salariés_entrants',compute='_get_N_Nbr_Salaries_entrant')
    salaries_entrant = fields.Char(string='Nombre de Salariés entrants',compute='total_Salaries_entrant')	
    N_Num_Assure_entrant = fields.Char(string='N_Num_Assure_entrant',compute='_get_N_Num_Assure_entrant')		
    N_Jours_Declares_entrant = fields.Char(string="N_Jours_Declares_entrant",compute='_get_N_Jours_Declares_entrant')
    N_Salaire_Reel_entrant = fields.Char('N_Salaire_Reel_entrant', compute='_get_N_Salaire_Reel_entrant')
    N_Salaire_Plaf_entrant = fields.Char('N_Salaire_Plaf_entrant', compute='_get_N_T_Salaire_Plaf_entrant')
    S_ctr_entrant = fields.Char('S_ctr_entrant', compute='_get_S_Ctr_entrant')	
    N_T_Ctr_entrant = fields.Char(string='N_T_Ctr_entrant',compute='_get_N_T_Ctr_entrant')

    L_Type_Enreg_total = fields.Char(string='Type ', default='B06')  
    N_Num_Affilie_total = fields.Char(string='Numéro affilié', size=7)
    L_Periode_total = fields.Char(string='Période', size=6)	
    N_Nbr_Salaries_total = fields.Char(string='Total des salariés',compute='_get_N_Nbr_Salaries_total')
    total_des_salaries = fields.Char(string='Total des salariés ',compute='_get_Salaries_total')	
    N_Num_Assure_total = fields.Char(string='N_Num_Assure_total',compute='_get_N_Num_Assure_total')		
    N_Jours_Declares_total = fields.Char(string="Total des jours déclarés",compute='_get_N_Jours_Declares_total')
    N_Salaire_Reel_total = fields.Char('Montant Total salaire Brut', compute='_get_N_Salaire_Reel_total')
    N_Salaire_Plaf_total = fields.Char('Montant Total salaire plafonné', compute='_get_N_T_Salaire_Plaf_total')
    S_ctr_total = fields.Char('S_ctr_total', compute='_get_S_ctr_total')	
    N_T_Ctr_total = fields.Char(string='N_T_Ctr_total',compute='_get_N_T_Ctr_total')
    L_filler06 = fields.Char(string='Filler06',size=190)	

    L_Type_Enregb04 = fields.Char(string='Type' ,default='B04')  
    N_Num_Affilieb04 = fields.Char(string='Numéro affilié',compute='_get_N_Num_Affilie_b04')
    L_Periodeb04 = fields.Char(string='Période',compute='_get_L_Periode_b04')
    N_Num_Assureb04 = fields.Char(string='Numéro assuré',compute='_get_N_Num_Assure_b04')	
    L_Nomb04 = fields.Char(string='Nom',compute='_get_L_Nom_b04')
    L_Prenomb04 = fields.Char(string='Prénom',compute='_get_L_Prenom_b04')	
    Num_CINb04 = fields.Char(string='cin') 
    N_Jours_Declaresb04 = fields.Char(string="Jours déclarés",size=2)
    N_Salaire_Reelb04 = fields.Char('Salaire reel', size=13)
    N_Salaire_Plafb04 = fields.Char('Salaire plafonné', size=9)
    S_Ctr_b04 = fields.Char('S_Ctr_b04', size=13)
    L_filler_b04 = fields.Char('L_filler_b04', size=9)	
    N_Type_Contratb04 = fields.Char('Type de contrat')
    S_Ctr_entrantb04 = fields.Char('Somme horizontale', compute='_get_S_Ctr_entrant')	
    L_Type_Enreg00 = fields.Char(string='Type', default='B00')  
    N_Identif_Transfert00  = fields.Char(string='N_Identif_Transfert', compute='_get_N_Identif_Transfert')
    L_Cat00   = fields.Char(string='L_Cat', default='B0')	
    L_filler00  = fields.Char(string='L_filler' ,default="")
    L_filler000  = fields.Char(string='L_filler', compute='_get_L_filler00')
    L_Type_Enreg01 = fields.Char(string='Type', default='B01')
    ligneA01 = fields.Char(string='Type', compute='_get_ligneA01')
    L_fillerb03  = fields.Char(string='L_filler', compute='_get_L_fillerb03')
    L_filler05  = fields.Char(string='L_filler' , compute='_get_L_fillerb05')
    cnss_a_payer  = fields.Char(string='Montant Cotisations à payer en DH' , compute='_get_cnss_a_payer')
    paiedata = fields.Selection([('ODOO', 'Odoo'), ('EXL', 'Excel')], 'Choisir une source des données',dafault='Odoo')

	
    state = fields.Selection([
        ('draft', 'Ouvert'),
        ('done', 'Fermé'), ], 'État', index=True, default='draft', readonly=True, copy=False)




    def _get_cnss_a_payer(self):
        for p in self:
            plaf=(int(p.N_Salaire_Plaf_total))/100
            taux= p.company_id.t_pat			
             
            p.cnss_a_payer = int((plaf*taux)/100)





# ------------B00-------------

    def _get_N_Identif_Transfert(self):
        for p in self:	
            for line in p.dsbtwo_lines3:	
                p.N_Identif_Transfert00 = line.N_Identif_Transfert



    def _get_L_filler00(self):       
        for p in self: 
            for line in p.dsbtwo_lines3:	
                p.L_filler000 = line.L_filler00


# ------------END B00-------------


# ------------B01-------------

    def _get_ligneA01(self):
        for p in self:	
            for line in p.dsbtwo_lines4:	
                p.ligneA01 = line.LigneA01



# ------------END B01-------------


    def _get_S_Ctr(self):       
        for p in self: 
            for line in p.dsbtwo_lines:			
                p.S_Ctr = line.S_Ctr

# ------------ B03-------------


    def _get_N_T_Ctr(self):
        for p in self:
            total=0
            for line in p.dsbtwo_lines:			
                total += int(line.S_Ctr)
            p.N_T_Ctr = (str(total)).zfill(19)



    def _get_L_fillerb03(self):       
        for p in self: 
            k = str(p.L_filler00)		
            p.L_fillerb03 = k.rjust(116)





    def _get_numero_affilie(self):  
        for p in self: 		
            p.N_Num_Affilie= p.cnss_lines2.N_Num_AffilieA01 

		

    def _get_L_Periode(self):
        for p in self:
            p.L_Periode = p.cnss_lines2.L_PeriodeA01 


    def _get_N_Nbr_Salaries(self):
        for p in self:	
            p.N_Nbr_Salaries = p.cnss_lines3.N_Nbr_Salaries 


    def _get_N_T_Enfants(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_Enfants)
        p.N_T_Enfants = (str(total)).zfill(6) 



    def _get_N_T_AF_A_Deduire(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_AF_A_Deduire)
        p.N_T_AF_A_Deduire = (str(total)).zfill(12) 
				


    def _get_N_T_AF_A_Payer(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_AF_A_Payer)
        p.N_T_AF_A_Payer = (str(total)).zfill(12) 
		


    def _get_N_T_AF_Net_A_Payer(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_AF_Net_A_Payer)
        p.N_T_AF_Net_A_Payer = (str(total)).zfill(12) 


    def _get_N_T_Num_Imma(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_Num_Assure)
        p.N_T_Num_Imma = (str(total)).zfill(15) 


    def _get_N_T_AF_A_Reverser(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_AF_A_Reverser)
        p.N_T_AF_A_Reverser = (str(total)).zfill(12) 




    def _get_N_T_Jours_Declares(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_Jours_Declares)
        p.N_T_Jours_Declares = (str(total)).zfill(6) 


    def _get_N_T_Salaire_Reel(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_Salaire_Reel2)
        p.N_T_Salaire_Reel = (str(total)).zfill(15)


    def _get_N_T_Salaire_Plaf(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines:	
                total += int(line.N_Salaire_Plaf2)
        p.N_T_Salaire_Plaf = (str(total)).zfill(13)


# -------------salaries entrants 05--------------


    def _get_N_Nbr_Salaries_entrant(self):
        for p in self:
            total = (len(p.dsbtwo_lines2))	
        p.N_Nbr_Salaries_entrant = (str(total)).zfill(6) 

    def total_Salaries_entrant(self):
        for p in self:
            total = len(p.dsbtwo_lines2)	
        p.salaries_entrant = total

    def _get_N_Num_Assure_entrant(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:	
                total += int(line.N_Num_Assure)
        p.N_Num_Assure_entrant = (str(total)).zfill(15) 


    
    def _get_N_Jours_Declares_entrant(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:	
                total += int(line.N_Jours_Declares2)
        p.N_Jours_Declares_entrant = (str(total)).zfill(6) 

    
    def _get_N_Salaire_Reel_entrant(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:
                val = int(line.N_Salaire_Reel2)				
                total += val
        p.N_Salaire_Reel_entrant = (str(total)).zfill(15)

    
    def _get_N_T_Salaire_Plaf_entrant(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:
                val= int(line.N_Salaire_Plaf2)			
                total += val
        p.N_Salaire_Plaf_entrant = (str(total)).zfill(13)




    
    def _get_N_T_Ctr_entrant(self):
        for p in self:
            total = 0
            for line in p.dsbtwo_lines2:			
                total += int(line.S_Ctr_entrant)
        p.N_T_Ctr_entrant = (str(total)).zfill(19)

    
    def _get_L_fillerb05(self):       
        for p in self: 
              k = str(p.L_filler00)		
              p.L_filler05 = k.rjust(170)



# ------b04------------------




    
    def _get_N_Num_Affilie_b04(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:	
                total = int(line.N_Num_Affilie)
        p.N_Num_Affilieb04 = total

    
    def _get_L_Periode_b04(self):
        for p in self:
            total = 0		
            for line in p.dsbtwo_lines2:	
                total = int(line.L_Periode)
        p.L_Periodeb04 = total
		
		
    
    def _get_N_Num_Assure_b04(self):
        for p in self: 
              k = str(p.L_filler00)		
              p.N_Num_Assureb04 = k.rjust(9)		

    
    def _get_Num_CINb04(self):
        for p in self: 
              k = str(p.L_filler00)		
              p.Num_CINb04 = k.rjust(30)
            
		
    
    def _get_L_Prenom_b04(self):
        for p in self: 
              k = str(p.L_filler00)		
              p.L_Prenom_b04 = k.rjust(30)
            
            				
    
    def _get_L_Num_CIN_b04(self):
        for p in self: 
              k = str(p.L_filler00)		
              p.L_Num_CIN_b04 = k.rjust(8)                				
	
    
    def _get_N_Jours_Declaresb04(self):
        for p in self:
            k = 0
            p.N_Jours_Declaresb04 = (str(k)).zfill(2)  
       
    
    def _get_N_Salaire_Reelb04(self):
        for p in self:
            k = 0
            p.N_Salaire_Reelb04 = (str(k)).zfill(13)  
			
    
    def _get_N_Salaire_Plafb04(self):
        for p in self:
            k = 0
            p.N_Salaire_Plafb04 = (str(k)).zfill(9) 			
			
    
    def _get_S_Ctr_b04(self):
        for p in self:
            k = 0
            p.S_Ctr_b04 = (str(k)).zfill(19) 


    
    def _get_L_filler_b04(self):
        for p in self: 
              k = str(p.L_filler00)		
              p.L_filler_b04 = k.rjust(124)
			  
# -----------endb04--------------

# -----------b06--------------
    
    def _get_N_Nbr_Salaries_total(self):
        for p in self:
            k = int(p.N_Nbr_Salaries_entrant)+int(p.N_Nbr_Salaries)
            p.N_Nbr_Salaries_total = str(k).zfill(6) 

    def _get_Salaries_total(self):
        for p in self:
            k = int(p.N_Nbr_Salaries_entrant)+int(p.N_Nbr_Salaries)
            p.total_des_salaries = k 
    
    def _get_N_Num_Assure_total(self):
        for p in self:
            k = int(p.N_Num_Assure_entrant)+int(p.N_T_Num_Imma)		
            p.N_Num_Assure_total = str(k).zfill(15) 


    
    def _get_N_Jours_Declares_total(self):
        for p in self:
            k = int(p.N_Jours_Declares_entrant)+int(p.N_T_Jours_Declares)			
            p.N_Jours_Declares_total = str(k).zfill(6) 

    
    def _get_N_Salaire_Reel_total(self):
        for p in self:
            k = int(p.N_Salaire_Reel_entrant)+int(p.N_T_Salaire_Reel)			
            p.N_Salaire_Reel_total = str(k).zfill(15)

    
    def _get_N_T_Salaire_Plaf_total(self):
        for p in self:
            k = int(p.N_Salaire_Plaf_entrant)+int(p.N_T_Salaire_Plaf)			
            p.N_Salaire_Plaf_total = str(k).zfill(13)


    
    def _get_N_T_Ctr_total(self):
        for p in self:
            k = int(p.N_T_Ctr_entrant)+int(p.N_T_Ctr)		
            p.N_T_Ctr_total = str(k).zfill(19)
			
    
    def _get_S_ctr_total(self):
        for p in self:
            k = int(p.S_ctr_entrant)+int(p.S_Ctr)			
            p.S_ctr_total = str(k).zfill(19)			
			

# -----------endb06--------------
	
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('damancom.dsbtwo')or '/'
        dsbtwo = super(DsbTwo, self).create(vals)
        return dsbtwo

    def print_report(self):
        return self.env.ref('hr_payroll_ma_pro.action_report_etat_cnss_ds').report_action(self)
		
    def cnss_draft(self):
        return self.write({'state': 'draft'})

    def cnss_done(self):
        return self.write({'state': 'done'})

    def parse_ebds(self):

        dslines= self.env['hr.cnss.line']
        dslines3= self.env['hr.cnss.line4']	
        dslines4= self.env['hr.cnss.line2']			
        dslines2= self.env['hr.cnam.line']		
        lines= dslines.search([('L_Type_Enreg', '=', 'A02')])
		

				
        f_line_obj = self.env['damancom.dsbtwo.line']	
        f_line_obj2 = self.env['damancom.dsbtwo.line2']


		
        dsbtwo_lines = []
        dsbtwo_lines2 = []
        dsbtwo_lines3 = []  	
        dsbtwo_lines4 = []  

		
        for o in self:
            old_f_lines = f_line_obj.search([('dsbtwo_id', '=', o.id)])
            if old_f_lines:
                old_f_lines.unlink()		
            for line in lines:		
                lines2= dslines2.search([('N_Num_Assure', '=', line.N_Num_Assure)])				
                for line2 in lines2:
                    if line2.L_Situation != 'EN':				
                        dsbtwo_lines.append((0, 0,{
		    'dsbtwo_id': o.id,
            'L_Type_Enreg' : "B02",			
			'N_Num_Affilie' :line.N_Num_Affilie, 
			'L_Periode' :line.L_Periode,
			'L_Nom' :line.L_Nom,	
			'L_Prenom' :line.L_Prenom,				
			'N_Enfants' :line.N_Enfants,			
			'N_Num_Assure' :line.N_Num_Assure,
			'N_AF_A_Payer' :line.N_AF_A_Payer,
			'N_AF_A_Deduire' :line.N_AF_A_Deduire,
			'N_AF_A_Reverser' :0,		
			'N_AF_Net_A_Payer' :line.N_AF_Net_A_Payer,
			'N_Jours_Declares' :line2.N_Jours_Declares,
			'N_Salaire_Reel' :line2.N_Salaire_Reel,
			'L_Situation' :line2.L_Situation,}))	
            o.write({'dsbtwo_lines': dsbtwo_lines}) 
			
					
 
            old_f_lines2 = f_line_obj2.search([('dsbtwo2_id', '=', o.id)])
            if old_f_lines2:
                old_f_lines2.unlink()	
	
            linesb04= dslines2.search([('L_Situation', '=','EN')])				
            for lineb04 in linesb04 :						 		                			
                dsbtwo_lines2.append((0, 0,{
		    'dsbtwo2_id': o.id,
            'L_Type_Enreg' : "B04",			
			'N_Num_Affilie' :line.N_Num_Affilie, 
			'L_Periode' :line.L_Periode,
			'L_Nom' :lineb04.L_Nom,	
			'L_Prenom' :lineb04.L_Prenom,							
			'N_Num_Assure' :lineb04.N_Num_Assure,
			'Num_CIN' :lineb04.Num_CIN,
			'N_Jours_Declares' :lineb04.N_Jours_Declares,
			'N_Salaire_Reel' :lineb04.N_Salaire_Reel,}))
			
	
					

            o.write({'dsbtwo_lines2': dsbtwo_lines2}) 
			
            lines00= dslines3.search([])				
            for line00 in lines00 :						 		                			
                dsbtwo_lines3.append((0, 0,{
		    'dsbtwo3_id': o.id,
            'L_Type_Enreg' : "B00",			
			'N_Identif_Transfert' :line00.N_Identif_Transfert, 
			'L_Cat' :"B0",}))
					
            o.write({'dsbtwo_lines3': dsbtwo_lines3}) 


            lines01= dslines4.search([])				
            for line01 in lines01 :						 		                			
                dsbtwo_lines4.append((0, 0,{
		    'dsbtwo4_id': o.id,
            'L_Type_Enreg' : "B01",					
            'LigneA01' : line01.LigneA01,}))			
					
            o.write({'dsbtwo_lines4': dsbtwo_lines4}) 
			

		
        return True

 	

class CNSSLine(models.Model):
    _name = 'damancom.dsbtwo.line'
    _description = 'DSBTWO'
    _order = 'N_Num_Assure'



    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'DSBTWO' + str(record.dsbtwo_id.id) + '-' +  '-' + str(record.id)
        return res

    
		
  
    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    dsbtwo_id = fields.Many2one('damancom.dsbtwo', 'DSBTWO', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.user.company_id)	
    L_Type_Enreg = fields.Char(string='Type ', size=3)  
    N_Num_Affilie = fields.Char(string='Numéro affilié', size=7)
    L_Periode = fields.Char(string='Période', size=6)
    N_Num_Assure = fields.Char(string='Numéro assuré', size=9)	
    L_Nom = fields.Char(string='Nom 2', size=30)
    L_Prenom = fields.Char(string='2Prénom', size=30)	
    L_Nom2 = fields.Text(string='Nom',compute='_get_L_Nom')
    L_Prenom2 = fields.Text(string='Prénom',compute='_get_L_Prenom')	
    N_Enfants = fields.Char(string='Nbre enfants', size=2)
    N_Enfants2 = fields.Char(string='Nbre enfants',compute='_get_N_Enfants')	
    N_AF_A_Payer = fields.Char(string='Alloc.fam. à payer', size=6)
    N_AF_A_Payer2 = fields.Char(string='Alloc.fam. à payer',compute='_get_N_AF_A_Payer')	
    N_AF_A_Deduire = fields.Char(string='Alloc.fam. à déduire',size=6)
    N_AF_A_Deduire2 = fields.Char(string='Alloc.fam. à déduire',compute='_get_N_AF_A_Deduire')
    N_AF_Net_A_Payer = fields.Char(string='Alloc.fam.net. à payer',size=6)
    N_AF_Net_A_Payer2 = fields.Char(string='Alloc.fam.net. à payer',compute='_get_AF_Net_A_Payer')	
    N_AF_A_Reverser = fields.Char('Alloc.fam. à reverser', default=0)
    N_AF_A_Reverser2 = fields.Char('Alloc.fam. à reverser',compute='_get_N_AF_A_Reverser')	
    N_Jours_Declares = fields.Char(string="Jours déclarés",size=2)
    N_Jours_Declares2 = fields.Char(string="Jours déclarés",compute='_get_N_Jours_Declares')
    N_Salaire_Reel = fields.Char('Salaire reel', size=13)
    N_Salaire_Reel2 = fields.Char('Salaire reel',compute='_get_N_Salaire_Reel')	
    N_Salaire_Plaf = fields.Char('Salaire plafonné', size=9)
    N_Salaire_Plaf2 = fields.Char('Salaire plafonné',compute='_get_N_Salaire_Plaf')	
    L_Situation = fields.Char('Situation', size=2,default="00")
    L_Situation2 = fields.Char('Situation', compute='_get_situation_zfill')	
    S_Ctrsituation = fields.Char('Ctr_Situation', compute='get_situation')	
    S_Ctr = fields.Char('Somme horizontale', compute='_get_S_Ctr')	
    L_filler = fields.Char('Zone espaces vide', default="")
    L_filler2 = fields.Char('Zone espaces vide',compute='_get_L_filler')	
	
    def _get_situation_zfill(self):       
        for p in self:	
            k = p.L_Situation
            k2 = '  '             			  
            if not k :		
                p.L_Situation2 = k2  
            else:
                p.L_Situation2 = k			
			

    
    def _get_L_filler(self):       
        for p in self: 
              k = str(p.L_filler)		
              p.L_filler2 = k.rjust(104)
  
    
    def _get_N_Enfants(self):       
        for p in self: 	
              p.N_Enfants2 = p.N_Enfants.zfill(2)
			  
		  

    
    def _get_N_Salaire_Reel(self):       
        for p in self:
            val = 0
            val1 = int(p.N_Jours_Declares2)-1
            val0 = (self.company_id.smig)*100
            salreel = int(p.N_Salaire_Reel)			
            val2= round((salreel/26)* val1)			
            salreel = int(p.N_Salaire_Reel)
            if p.L_Situation == "CS" or p.L_Situation =="MS":
                p.N_Salaire_Reel2 = str(val).zfill(13)
            elif  salreel <= val0 and salreel > 0:								
                p.N_Salaire_Reel2 = str(val2).zfill(13)				
            else:				
                p.N_Salaire_Reel2 = str(salreel).zfill(13)


    
    def _get_N_Salaire_Plaf(self):       
        for p in self:
            val = 0	
            val1 = int((self.company_id.plafond_secu)*100)
            val2 = int(p.N_Salaire_Reel2)			
            if val2 >= val1 :
                p.N_Salaire_Plaf2 = str(val1).zfill(9)
            else:				
                p.N_Salaire_Plaf2 = str(val2).zfill(9)

  
    
    def _get_L_Nom(self):       
        for p in self: 
              k = p.L_Nom		
              p.L_Nom2 =  k.ljust(30)

    
    def _get_L_Prenom(self):       
        for p in self: 
              k = p.L_Prenom		
              p.L_Prenom2 =  k.ljust(30)

    
    def _get_N_AF_A_Reverser(self):       
        for p in self:
              k = str(p.N_AF_A_Reverser)		
              p.N_AF_A_Reverser2 = k.zfill(6)	
    
    def _get_N_AF_A_Payer(self):       
        for p in self:
              k = str(p.N_AF_A_Payer)		
              p.N_AF_A_Payer2 = k.zfill(6)
    			  
    def _get_N_AF_A_Deduire(self):       
        for p in self:
              k = str(p.N_AF_A_Deduire)		
              p.N_AF_A_Deduire2 = k.zfill(6)
    
    def _get_AF_Net_A_Payer(self):       
        for p in self:
              k = str(p.N_AF_Net_A_Payer)		
              p.N_AF_Net_A_Payer2 = k.zfill(6)
			  
    
    def _get_N_Jours_Declares(self):       
        for p in self:
            val = 0		
            njour = min(26,int(p.N_Jours_Declares))
            if p.L_Situation == "CS" or p.L_Situation =="MS":
                p.N_Jours_Declares2 = str(val).zfill(2)
            else:				
                p.N_Jours_Declares2 = str(njour).zfill(2)	

    def get_situation(self):
        self.S_Ctrsituation=0	
        for s in self:
            if(s.L_Situation == "SO"):
                s.S_Ctrsituation=1
            elif(s.L_Situation == "DE"):
                s.S_Ctrsituation=2
            elif(s.L_Situation == "IT"):
                s.S_Ctrsituation=3
            elif(s.L_Situation == "IL"):
                s.S_Ctrsituation=4
            elif(s.L_Situation == "AT"):
                s.S_Ctrsituation=5
            elif(s.L_Situation == "CS"):
                s.S_Ctrsituation=6 
            elif(s.L_Situation == "MS"):
                s.S_Ctrsituation=7
            elif(s.L_Situation == "MP"):
                s.S_Ctrsituation=8
							
    def _get_S_Ctr(self):
        for p in self: 
            val = 0
            k = 0		
            val1 = int(p.S_Ctrsituation)
            val2 = int(p.N_Num_Assure)
            val3 = int(p.N_AF_A_Reverser)
            val4 = int(p.N_Jours_Declares)
            val5 = int(p.N_AF_A_Reverser)
            val6 = int(p.N_Salaire_Plaf2)
            val = val1+val2+val3+val4+val5+val6
            k = str(val)
            p.S_Ctr = k.zfill(19) 

			

class CNSSLine2(models.Model):
    _name = 'damancom.dsbtwo.line2'
    _description = 'DSBTWOB02'
    _order = 'N_Num_Assure'


    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'DSBTWOB02' + str(record.dsbtwo2_id.id) + '-' +  '-' + str(record.id)
        return res

    
    def _get_S_Ctr_entrant(self):       
        for p in self: 	
            total = int(p.N_Num_Assure) + int(p.N_Jours_Declares) + int(p.N_Salaire_Reel)+ int(p.N_Salaire_Plaf)
        p.S_Ctr_entrant = (str(total)).zfill(19) 
		

    
    def _get_L_filler_entrant(self):       
        for p in self: 
              k = p.L_filler		
              p.L_filler_entrant = k.ljust(124)


    
    def _get_L_Nom_04(self):       
        for p in self: 
              k = p.L_Nom		
              p.L_Nom2 =  k.ljust(30)

    
    def _get_L_Prenom_04(self):       
        for p in self: 
              k = p.L_Prenom		
              p.L_Prenom2 =  k.ljust(30)
			  
    
    def _get_N_Jours_zfill(self):       
        for p in self:
            njour= min(26,int(p.N_Jours_Declares))		
            p.N_Jours_Declares2 = str(njour).zfill(2)			  
			  
    
    def _get_Num_CIN_zfill(self):       
        for p in self:	
            p.Num_CIN2 = str(p.Num_CIN).zfill(8)	

    def _get_N_Num_Affilie(self):
        for p in self:		
            p.N_Num_Affilie2 = str(p.N_Num_Affilie).zfill(7) 	

    
    def _get_N_Salaire_Reel(self):       
        for p in self:
            val = 0
            val1 = int(p.N_Jours_Declares2)-1
            val0 = int(self.company_id.smig*100)
            salreel = int(p.N_Salaire_Reel)			
            val2= round((salreel/26)* val1)			
            if salreel <= val0 and salreel > 0:								
                p.N_Salaire_Reel2 = str(val2).zfill(13)				
            else:				
                p.N_Salaire_Reel2 = str(salreel).zfill(13)


    
    def _get_N_Salaire_Plaf(self):       
        for p in self:
            val = 0	
            val1 = int((self.company_id.plafond_secu)*100)
            val2 = int(p.N_Salaire_Reel2)			
            if val2 >= val1 :
                p.N_Salaire_Plaf2 = str(val1).zfill(9)
            else:				
                p.N_Salaire_Plaf2 = str(val2).zfill(9)
			  
			  
			  
		
    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    dsbtwo2_id = fields.Many2one('damancom.dsbtwo', 'DSBTWOB02', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.user.company_id)	
    L_Type_Enreg = fields.Char(string='Type ', size=3)  
    N_Num_Affilie = fields.Char(string='Numéro affilié', size=7)
    N_Num_Affilie2 = fields.Char(string='Numéro affilié',  compute='_get_N_Num_Affilie')	
    L_Periode = fields.Char(string='Période', size=6)
    N_Num_Assure = fields.Char(string='Numéro assuré', size=9)	
    L_Nom = fields.Char(string='Nom', size=30)
    L_Prenom = fields.Char(string='Prénom', size=30)
    L_Nom2 = fields.Char(string='Nom', compute='_get_L_Nom_04')
    L_Prenom2 = fields.Char(string='Prénom', compute='_get_L_Prenom_04')	
    Num_CIN = fields.Char(string='cin') 
    Num_CIN2 = fields.Char(string='cin', compute='_get_Num_CIN_zfill') 	
    N_Jours_Declares = fields.Char(string="Jours déclarés",size=2)
    N_Jours_Declares2 = fields.Char(string="Jours déclarés", compute='_get_N_Jours_zfill')	
    N_Salaire_Reel = fields.Char('Salaire reel', size=13)
    N_Salaire_Reel2 = fields.Char('Salaire reel', compute='_get_N_Salaire_Reel')	
    N_Salaire_Plaf = fields.Char('Salaire plafonné', size=9)
    N_Salaire_Plaf2 = fields.Char('Salaire plafonné', compute='_get_N_Salaire_Plaf')	
    N_Type_Contrat = fields.Char('Type de contrat')
    S_Ctr_entrant = fields.Char('Somme horizontale', compute='_get_S_Ctr_entrant')
    L_filler = fields.Char('Zone espaces vide',default="")		
    L_filler_entrant = fields.Char('Zone espaces vide',compute='_get_L_filler_entrant')	
   
class CNSSLine00(models.Model):
    _name = 'damancom.dsbtwo.line3'
    _description = 'DSBTWOB00'



    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'DSBTWOB00' + str(record.dsbtwo3_id.id) + '-' +  '-' + str(record.id)
        return res



    
    def _get_L_filler00(self):       
        for p in self: 
              k = str(p.L_filler)		
              p.L_filler00 = k.rjust(241)

		
    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    dsbtwo3_id = fields.Many2one('damancom.dsbtwo', 'DSBTWO00', required=True, ondelete='cascade', index=True)
    L_Type_Enreg = fields.Char(string='Type', size=3)  
    N_Identif_Transfert  = fields.Char(string='N_Identif_Transfert', size=14)
    L_Cat   = fields.Char(string='L_Cat', size=2)
    L_filler = fields.Char('Zone espaces vide', default="")	
    L_filler00  = fields.Char(string='L_filler',compute='_get_L_filler00')

class CNSSLine01(models.Model):
    _name = 'damancom.dsbtwo.line4'
    _description = 'DSBTWOB01'



    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'DSBTWOB01' + str(record.dsbtwo4_id.id) + '-' +  '-' + str(record.id)
        return res



		
    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    dsbtwo4_id = fields.Many2one('damancom.dsbtwo', 'DSBTWO01', required=True, ondelete='cascade', index=True)
    L_Type_Enreg = fields.Char(string='Type', size=3)  
    LigneA01 = fields.Char(string='ligneA01')


    