# -*- coding: utf-8 -*-

import calendar
import logging
import base64


from datetime import date, datetime, timedelta
from odoo import api, fields, models, exceptions, _

_logger = logging.getLogger(__name__)


		
class DamancomPreta(models.Model):
    _name = 'hr.cnss'
    _description = 'CNSS'
    _order = "company_id "
	

    def _get_default_month(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%m')
		



    ebdsfile = fields.Binary('Fichier Préetabli Damancom')
    ebdsfile_name = fields.Char('Name')
	
    name = fields.Char(string='Déclaration N°',readonly=True, required=True, default=lambda *a: '...' )
    company_id = fields.Many2one('res.company', 'Société', required=True, default=lambda self: self.env.user.company_id)
    year = fields.Date('Année',)
    date_document = fields.Date('Date',readonly=True, default=lambda *a: date.today())
    month = fields.Char('Mois encours', required=True, default=_get_default_month)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'To Pay'),
        ('done', 'Payed'), ], 'État', index=True, default='draft', readonly=True, copy=False)
    cnss_lines = fields.One2many('hr.cnss.line', 'cnss_id',  'cnss')
    cnss_lines2 = fields.One2many('hr.cnss.line2', 'cnss_id2', 'cnss2')
    cnss_lines3 = fields.One2many('hr.cnss.line3', 'cnss_id3', 'cnss3')	
    cnss_lines4 = fields.One2many('hr.cnss.line4', 'cnss_id4', 'cnss4')		



    nemploye = fields.Integer("Nbre employee",compute='_compute_employee_count')	
    N_Num_AffilieA01 = fields.Char(string='Numéro affilié', compute='_get_numero_affilie')
    L_PeriodeA01 = fields.Char(string='Période',  compute='_get_periode')
    L_Raison_SocialeA01 = fields.Char(string='Raison sociale', compute='_get_raison_sociale')
    L_ActiviteA01 = fields.Char(string='Activité', compute='_get_activite')
    L_AdresseA01 = fields.Char(string='Adresse')
    L_VilleA01 = fields.Char(string='Ville',compute='_get_ville')
    C_Code_AgenceA01 = fields.Char(string='Code Agence',compute='_get_code_agence')
    D_Date_EmissionA01 = fields.Char(string='Date d\'émission',compute='_get_date_emission')
    D_Date_ExigA01 = fields.Char(string="Date d'exigence", compute='_get_date_exigence')
    N_Identif_Transfert00 = fields.Char(string="N_Identif_Transfert", compute='_get_N_Identif_Transfert')	

    N_Nbr_SalariesA03 = fields.Char('Nombre des salariés', compute='_get_nbr_salarie')	
    N_T_EnfantsA03 = fields.Char('Total des enfants', compute='_get_nbr_enfant')	
    N_T_AF_A_PayerA03 = fields.Char('Total des montants des allocations')	
    N_T_AF_A_DeduireA03 = fields.Char('T.allocations familiales à déduire ')	
    N_T_AF_Net_A_PayeA03 = fields.Char('T.allocations familiales  à payer', compute='_get_taf_apayer')	
    N_T_Num_ImmaA03 = fields.Char('Total des numéros d’immatriculations', compute='_get_t_num_imma')	
    total_numeros = fields.Char('Total des numéros Calculé',compute='_get_total_numeros')
    anneeperiode = fields.Char('annee')
    moisaperiode = fields.Char('Période à déclarer')	
    moisadec = fields.Char('Période à déclarer')	
    mois_Exig = fields.Char('mois exigence')
    jr_Exig = fields.Char("Date d'exigence")	
    warningval = fields.Char(default='Attention vous utilisez un ancien fichier préetabli  ou vous êtes en retard de déclaration !!!', readonly=True)
    warningval2 = fields.Char(default='La période à déclarer semble correcte', readonly=True)	
    warning = fields.Char(compute='_verify_periode')
	
    information = fields.Text(string = "Note")	
	
    _sql_constraints = [
        ('name_company_uniq', 'unique(month)', 'Cette déclaration existe déjà!'),]

    @api.onchange( 'month','mois_Exig')
    def _verify_periode(self):
        if int(self.month) <= int(self.mois_Exig):
           self.warning = self.warningval2
        else:
            self.warning = self.warningval			   
			   
	
	
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.cnss')
        daman= super(DamancomPreta, self).create(vals)
        return daman
		


    def _compute_employee_count(self):
        for p in self:
            p.nemploye = (len(p.cnss_lines))


    def _get_N_Identif_Transfert(self):       

        for p in self: 
            for line in p.cnss_lines4:			
                p.N_Identif_Transfert00= line.N_Identif_Transfert
   

    def _get_nbr_salarie(self):       

        for p in self: 
            nbrsalarie = 0
            for line in p.cnss_lines3:			
                nbrsalarie= line.N_Nbr_Salaries
        p.N_Nbr_SalariesA03 = nbrsalarie

    def _get_nbr_enfant(self):       

        for p in self: 
            nbrenfant = 0
            for line in p.cnss_lines3:			
                nbrenfant= line.N_T_Enfants
        p.N_T_EnfantsA03 = nbrenfant
			
    def _get_taf_apayer(self):       

        for p in self: 
            tafapayer = 0
            for line in p.cnss_lines3:			
                tafapayer= line.N_T_AF_Net_A_Paye
        p.N_T_AF_Net_A_PayeA03 = tafapayer


    def _get_raison_sociale(self):       

        for p in self: 
            rsociale = 0
            for line in p.cnss_lines2:			
                rsociale= line.L_Raison_Sociale
        p.L_Raison_SocialeA01 = rsociale 
 

    def _get_numero_affilie(self):  
        for p in self: 
            naffilie = 0
            for line in p.cnss_lines2:			
                naffilie= line.N_Num_AffilieA01 
        p.N_Num_AffilieA01 = naffilie 
	


    def _get_date_exigence(self):       
        for p in self: 
            exigence = 0
            for line in p.cnss_lines2:			
                exigence= line.D_Date_Exig
        p.D_Date_ExigA01 = exigence

    def _get_activite(self):       

        for p in self: 
            activite = 0
            for line in p.cnss_lines2:			
                activite= line.L_Activite
        p.L_ActiviteA01 = activite


    def _get_code_agence(self):       

        for p in self: 
            agence = 0
            for line in p.cnss_lines2:			
                agence= line.C_Code_Agence
        p.C_Code_AgenceA01 = agence


    def _get_date_emission(self):       

        for p in self: 
            emission = 0
            for line in p.cnss_lines2:			
                emission= line.D_Date_Emission
        p.D_Date_EmissionA01 = emission


    def _get_ville(self):       

        for p in self: 
            ville = 0
            for line in p.cnss_lines2:			
                ville= line.L_Ville
        p.L_VilleA01 = ville 
			
    def _get_periode(self):       

        for p in self: 
            periode = 0
            for line in p.cnss_lines2:			
                periode= line.L_PeriodeA01
        p.L_PeriodeA01 = periode 

  


    def _get_t_num_imma(self):       

        for p in self: 
            timma = 0
            for line in p.cnss_lines3:			
                timma= line.N_T_Num_Imma
        p.N_T_Num_ImmaA03 = timma 

		
    def _get_total_numeros(self):       
        for p in self: 
            total = 0
            for line in p.cnss_lines:			
                total += int(line.N_Num_Assure)
        p.total_numeros = total 	


    def cnss_confirm(self):
        return self.write({'state': 'waiting'})

    def cnss_payed(self):
        return self.write({'state': 'done'})
		
    # def print_report(self):
        # return self.env.ref('hr_payroll_ma_pro.action_report_etat_cnss').report_action(self)


    def parse_ebds(self):

        ebdslines = self.ebdsfile
        if not ebdslines:
            raise exceptions.UserError(_('Selectionnez un fichier preétabli !'))

        try:
            lines = str(base64.decodebytes(ebdslines), 'utf-8').split("\r\n")
        except ValueError as decode_err:
            raise exceptions.UserError(_(
                'Fichier non valide'
            ).format(
                repr(decode_err)
            ))
        # for line  in lines:
            # N_Num_AffilieA01 = line[7:10]
            # L_PeriodeA01 = line[10:17]
            # L_Type_EnregA01 = line[0:3]
        f_line_obj = self.env['hr.cnss.line']
        f_line_obj2 = self.env['hr.cnss.line2']
        f_line_obj3 = self.env['hr.cnss.line3']
		
        cnss_lines = []		
        cnss_lines2 = []	
        cnss_lines3 = []	
        cnss_lines4 = []			
        for o in self:
            old_f_lines = f_line_obj.search([('cnss_id', '=', o.id)])
            if old_f_lines:
                old_f_lines.unlink()
            for line  in lines:
                if line.startswith("A02"):			
                   cnss_lines.append((0, 0,{
		    'cnss_id': o.id,
            'L_Type_Enreg' : line[0:3],			
            'N_Num_Affilie' : line[3:10],
            'L_Periode' : line[10:16],
            'N_Num_Assure' : line[16:25],
            'L_Nom' : line[25:55],
            'L_Prenom' : line[55:85],			
            'N_Enfants' : line[85:87],
            'N_AF_A_Payer' : line[87:93],
            'N_AF_A_Deduire' : line[93:99],
            'N_AF_Net_A_Payer' : line[99:105],}))
            o.write({'cnss_lines': cnss_lines})
            
            old_f_lines2 = f_line_obj2.search([('cnss_id2', '=', o.id)])
            if old_f_lines2:
                old_f_lines2.unlink()	

			
            for line  in lines:           
                if line.startswith("A01"):			
                   cnss_lines2.append((0, 0,{
		    'cnss_id2': o.id,				   
            'L_Raison_Sociale' : line[16:56],
            'L_Activite' : line[56:96],
            'L_Adresse' : line[96:216],
            'L_Ville' : line[216:236],
            'C_Code_Agence' : line[236:244],
            'D_Date_Emission' : line[244:252],			
            'D_Date_Exig' : line[252:260],
            'D_mois_Exig' : line[256:258],
            'D_jr_Exig' : line[258:260],			
            'L_PeriodeA01' : line[10:16],
            'annee' : line[10:14],	
            'mois' : line[14:16],				
            'LigneA01' : line[3:260],			
            'N_Num_AffilieA01' : line[3:10],}))
            o.write({'cnss_lines2': cnss_lines2})

            old_f_lines3 = f_line_obj3.search([('cnss_id3', '=', o.id)])
            if old_f_lines3:
                old_f_lines3.unlink()


         
            for line  in lines:           
                if line.startswith("A03"):		
                   cnss_lines3.append((0, 0,{
		    'cnss_id3': o.id,				   
            'N_Nbr_Salaries'  : line[16:22],
            'N_T_Enfants' : line[22:28],
            'N_T_AF_A_Payer' : line[28:40],
            'N_T_AF_A_Deduire' : line[40:52],
            'N_T_AF_Net_A_Paye' : line[52:64],
            'N_T_Num_Imma' : line[64:80],}))
        
            o.write({'cnss_lines3': cnss_lines3})
			
            for line  in lines:           
                if line.startswith("A00"):		
                   cnss_lines4.append((0, 0,{
		    'cnss_id4': o.id,				   
            'N_Identif_Transfert' : line[3:17],}))
            o.write({'cnss_lines4': cnss_lines4})			
		
        return True


class CNSSLine(models.Model):
    _name = 'hr.cnss.line'
    _description = 'CNSS'

    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'CNSS' + str(record.cnss_id.id) + '-' +  '-' + str(record.id)
        return res

    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    cnss_id = fields.Many2one('hr.cnss', 'CNSS', required=True, ondelete='cascade', index=True)
    L_Type_Enreg = fields.Char('Type', size=3)
    N_Num_Affilie = fields.Char('Numéro Affilie', size=7)
    L_Periode = fields.Char('Période', size=6)
	
    N_Num_Assure = fields.Char('Numéro Assuré', size=9)
    L_Nom = fields.Char('Nom ', size=30)
    L_Prenom = fields.Char('Prénom', size=30)	
    N_Enfants = fields.Char('Nbre d\'enfants', size=2)
    N_AF_A_Payer = fields.Char('T.Alloc.Fam.', size=6)
    N_AF_A_Deduire = fields.Char('AF à déduire', size=6)
    N_AF_Net_A_Payer = fields.Char('AF net à payer', size=6)
    L_Raison_Sociale = fields.Char('Raison Sociale', size=40)	
    L_Activite = fields.Char('Activite', size=40)
    L_Adresse = fields.Char('Adresse', size=120)
    L_Ville = fields.Char('Ville', size=20)
    C_Code_Agence = fields.Char('Code agence', size=2)
    D_Date_Emission = fields.Char('Date emission', size=8)			
    D_Date_Exig = fields.Char('Date exigence', size=8)
	
    N_Num_AffilieA01 = fields.Char('Numéro Affilie', size=7)	
    L_PeriodeA01 = fields.Char('Période', size=6)	

    N_Nbr_Salaries = fields.Char('Nbre de salariés', size=6)	
    N_T_Enfants = fields.Char('Nbre enfants', size=6)	
    N_T_AF_A_Payer = fields.Char('T.Alloc Fam', size=12)	
    N_T_AF_A_Deduire = fields.Char('T.Alloc à Déduire', size=12)	
    N_T_AF_Net_A_Paye = fields.Char('T.Alloc à payer', size=12)	
    N_T_Num_Imma = fields.Char('Total des numéros immatriculation', size=15)








class CNSSLine2(models.Model):
    _name = 'hr.cnss.line2'
    _description = 'CNSS2'

    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'CNSS2' + str(record.cnss_id2.id) + '-' +  '-' + str(record.id)
        return res

    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    cnss_id2 = fields.Many2one('hr.cnss', 'CNSS2', required=True, ondelete='cascade', index=True)
    L_Raison_Sociale = fields.Char('Raison Sociale', size=40)	
    L_Activite = fields.Char('Activite', size=40)
    L_Adresse = fields.Char('Adresse', size=120)
    L_Ville = fields.Char('Ville', size=20)
    C_Code_Agence = fields.Char('Code agence', size=2)
    D_Date_Emission = fields.Char('Date emission', size=8)			
    D_Date_Exig = fields.Char('Date exigence', size=8)
    LigneA01 = fields.Char('ligne A01')
    N_Num_AffilieA01 = fields.Char('Numéro Affilie', size=7)	
    L_PeriodeA01 = fields.Char('Période', size=6)	
    N_Nbr_Salaries = fields.Char('Nbre de salariés', size=6)	
    N_T_Enfants = fields.Char('Nbre enfants', size=6)	
    N_T_AF_A_Payer = fields.Char('T.Alloc Fam', size=12)	
    N_T_AF_A_Deduire = fields.Char('T.Alloc à Déduire', size=12)	
    N_T_AF_Net_A_Paye = fields.Char('T.Alloc à payer', size=12)	
    N_T_Num_Imma = fields.Char('Total des numéros immatriculation', size=15)	
    annee = fields.Char('annee', size=4)
    mois = fields.Char('mois', size=2)	
    D_mois_Exig = fields.Char('mois exigence', size=4)
    D_jr_Exig = fields.Char('jour exigence', size=2)	
            

class CNSSLine3(models.Model):
    _name = 'hr.cnss.line3'
    _description = 'CNSS3'

    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'CNSS3' + str(record.cnss_id3.id) + '-' +  '-' + str(record.id)
        return res

    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    cnss_id3 = fields.Many2one('hr.cnss', 'CNSS3', required=True, ondelete='cascade', index=True)		
    N_Nbr_Salaries = fields.Char('Nbre de salariés', size=6)	
    N_T_Enfants = fields.Char('Nbre enfants', size=6)	
    N_T_AF_A_Payer = fields.Char('T.Alloc Fam', size=12)	
    N_T_AF_A_Deduire = fields.Char('T.Alloc à Déduire', size=12)	
    N_T_AF_Net_A_Paye = fields.Char('T.Alloc à payer', size=12)	
    N_T_Num_Imma = fields.Char('Total des numéros immatriculation', size=15)
	
class CNSSLine4(models.Model):
    _name = 'hr.cnss.line4'
    _description = 'CNSS4'

    def _name_get(self):
        res = {}
        for record in self:
            res[record.id] = 'CNSS4' + str(record.cnss_id4.id) + '-' +  '-' + str(record.id)
        return res

    name = fields.Char(compute='_name_get', type="char", string='Name', store=True)
    cnss_id4= fields.Many2one('hr.cnss', 'CNSS4', required=True, ondelete='cascade', index=True)		
    N_Identif_Transfert = fields.Char('identifiant', size=14)		
	
	


	