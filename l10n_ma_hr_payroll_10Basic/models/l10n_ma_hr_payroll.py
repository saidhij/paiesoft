# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    plafond_secu = fields.Float(string="Plafond de la Sécurité Sociale", required=True, default=6000)
    nombre_employes = fields.Integer(string="Nombre d’employés")
    cotisation_prevoyance = fields.Float(string="Cotisation Patronale")
    org_ss = fields.Char(string="Organisme de sécurité sociale")
    conv_coll = fields.Char(string="Convention collective")


class HrContract(models.Model):
    _inherit = 'hr.contract'

    qualif = fields.Char(string='Qualification')
    niveau = fields.Char()
    coef = fields.Char(string='Coefficient')


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    payment_mode = fields.Char(string='Mode de paiement')


class hr_employee(models.Model):
    _inherit = 'hr.employee'

	
   
    cin = fields.Char(string="Numéro CIN", required=False)
    matricule_cnss = fields.Char(string="Numéro CNSS", required=False)
    matricule_cimr = fields.Char(string="Numéro CIMR", required=False)
    matricule_mut = fields.Char(string="Numéro MUTUELLE", required=False)
    num_chezemployeur = fields.Integer(string="Matricule")
    abs = fields.Integer(string="Absence en heures" ,default=0)
    hs25 = fields.Integer(string="Heures sup à 25" ,default=0)
    hs50 = fields.Integer(string="Heures sup à 50",default=0)
    hs100 = fields.Integer(string="Heures sup à 100",default=0)
    av_sal = fields.Integer(string="Avance sur Salaire",default=0)   
    rem_mut = fields.Integer(string="Remboursement Mutuelle",default=0)