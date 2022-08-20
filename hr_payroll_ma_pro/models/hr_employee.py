# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta


from odoo import fields, models,api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'




    def _get_default_month(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%m')


    birth = fields.Date(string="birthday", related='birthday',readonly=True)
    cin = fields.Char(string="Numéro CIN")
    numcee= fields.Char(string="Numéro CE")
    nation = fields.Char(string="Nationalité", default="Marocaine")	
    cpte_bank = fields.Char(string="Compte bancaire",default=0)
    sit_famille = fields.Selection([('C', 'C'), ('M', 'M'), ('D', 'D'), ('V', 'V')], 'Situation de Famille')
    diplome = fields.Selection([('Bac+2', 'Bac+2'), ('Bac+4', 'Bac+4'),('Master', 'Master'),('Doctorat', 'Doctorat'), ('Technicien OFPPT', 'Technicien OFPPT'),('BTS', 'BTS'), ('Ingénieur', 'Ingénieur'),('Autre', 'Autre') ,('Sans Diplôme', 'Sans Diplôme')], 'Diplôme')	
    titre = fields.Selection([('Monsieur', 'Monsieur'), ('Madame', 'Madame'), ('Mademoiselle', 'Mademoiselle')], 'Titre')	
    matricule_cnss = fields.Char(string="Numéro CNSS")
    adresse = fields.Char(string="Adresse personnelle")	
    id_fiscal = fields.Char(string="identifiant Fiscal")
    numppr = fields.Char(string="Numéro PPR")
    ifu = fields.Char(string="identifiant fiscal (ifu)")
    jours_t_an = fields.Integer(string="Nombre légal de jours de travail par an",default=312,readonly=True )
    heures_t = fields.Integer(string="Nombre légal d'heures de travail par mois",default=191, readonly=True)
    jours_t = fields.Integer(string="Nombre légal de jours de travail par mois",default=26,readonly=True )	

    heure_25 = fields.Integer(string="Heures supplémentaires +25%",default=0)	
    heure_50 = fields.Integer(string="Heures supplémentaires +50%",default=0)
    heure_100 = fields.Integer(string="Heures supplémentaires +100%",default=0)
    avance = fields.Integer(string="Avance sur salaire du mois",default=0)
    jrs_trav_cemois = fields.Integer(string="Jours travaillés ce mois",default=26)
    hrs_trav_cemois = fields.Integer(string="Heures travaillées ce mois",default=191)
    presence_impor = fields.Boolean(string="Cochez si la présence est gérée par le système", default=False)

    today = fields.Date(default=fields.Date.today)		
    age = fields.Integer(string="Age", compute='_age')	
    image_certificate = fields.Binary('Importer un diplôme')
    certificate_name = fields.Char('Nom du document')	

    first_name = fields.Char(string="Prénom", required=False)
    last_name = fields.Char(string="Nom", required=False)
    code2 = fields.Char('Code', default='Rempli automatiquement')
    imageemp = fields.Binary(string="Photo" ,related='image_1920')	
    contractn = fields.Binary(string="Photo" ,related='image_1920')	
    cname = fields.Char(string="Contract N°", related='contract_id.name')
    cstate = fields.Selection(string="Contract State", related='contract_id.state')
    start = fields.Date(string="Contract Start", related='contract_id.date_start')
    end = fields.Date(string="Contract end", related='contract_id.date_end')
    first_nameup = fields.Char(string="Prénom", compute='check_change' , store=True)
    last_nameup = fields.Char(string="Nom", compute='check_change', store=True)	







    @api.depends('first_name', 'last_name')
    def check_change(self): 
        for s in self:
            s.first_nameup = (str(s.first_name)).upper() 
            s.last_nameup = (str(s.last_name)).upper() 


    @api.onchange('first_name', 'last_name') 
    def name_change(self):     

        self.name = (self.first_nameup or '')+' '+(self.last_nameup or '')

		
    @api.model
    def create(self, vals):
        vals['code2'] = self.env['ir.sequence'].next_by_code('employee.code2') 
        code = super(HrEmployee, self).create(vals)
        return code		
		

				
    @api.depends('birth','today','birthday')
    def _age(self):
        for r in self:
            end = date.today()
            self.age = relativedelta(end,r.birthday).years



