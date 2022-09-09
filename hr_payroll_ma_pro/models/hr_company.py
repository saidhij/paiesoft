# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing det


from odoo import fields, models
from odoo.addons import decimal_precision as dp



	
class Res_company(models.Model):
    _inherit = 'res.company'

   
    plafond_secu = fields.Float(string="Plafond CNSS", required=True,default=6000,help="6000")
    policeat = fields.Char(string="Police AT")	
    nombre_employes = fields.Integer(string="Nombre d'employés")
    cotisation_prevoyance = fields.Float(string="Cotisation Patronale Prévoyance")
    org_ss = fields.Char(string="Numéro  CNSS")
    conv_coll = fields.Char(string='Convention collective')	
    patente = fields.Char(string="Numéro de la patente")
    idfiscal = fields.Char(string="Identifiant Fiscal")
    ice = fields.Char(string="Identifiant Commun (ICE)")
    n_af_cimr = fields.Char(string="Numéro  CIMR")
    t_pat = fields.Float(string="Taux CNSS Patronal",default=8.98,required=True,help="8.98")
    t_sal = fields.Float(string="Taux CNSS Salarial",default=4.48,required=True,help="4.48")
    t_alloc = fields.Float(string="Frais Allocations familiales",default=6.4,required=True,help="6.4")
    t_formpro = fields.Float(string="Frais Formation Professionnelle",default=1.6,required=True,help="1.6")
    t_ded_formpro = fields.Float(string="Taux déduction Formation Professionnelle",default=20,required=True,help="20")	
    code_formpro = fields.Selection([('code1', 'TPP.40.2009'), ('code2', 'TPP.45.2009'), ('code3', 'TPP.35.2009'), ('code4', 'TPP.25.2009'), ('code5', 'TPP.20.2009'), ('code6', 'TAS.40.2012')], "Code du taux des frais professionnels",default='code5',required=True)	
    tamo_pat = fields.Float(string="Taux AMO Patronal",default=2.26,help="2.26",required=True)
    tamo_sal = fields.Float(string="Taux AMO Salarial",default=2.26,help="2.26",required=True)
    tamopar_pat = fields.Float(string="Taux Particpation AMO",default=1.85,help="1.85",required=True)	
    t_cimr = fields.Float(string="Taux CIMR Patronal",default=0)
    t_mut = fields.Float(string="Taux Mutuelle Patronal",default=0)
    t_css = fields.Float(string="Taux Contribution de Solidarité Sociale",default=1.5)	
    mut_bool = fields.Boolean(string="Cochez si l'entreprise offrait autre assurance maladie privée avant application de l'AMO")
    af_mutu = fields.Char(string="Numéro  Mutuelle ")
    commune1 = fields.Many2one( comodel_name='hr.commune', string="Code Commune")
    commune = fields.Char(string="Code commune")		
    smig = fields.Float(string="Smig ",default=2829)
    hours = fields.Float(string="Heures par mois",default=191,readonly=True)
    days = fields.Integer(string="Jours par mois",default=26,readonly=True)
    nom = fields.Char(string="Nom (p.physique)")	
    prenom = fields.Char(string="Prénom (p.physique)")
    numeroCIN = fields.Char(string="Numéro CIN ", size=20)
    numeroCE = fields.Char(string="Numéro Carte étranger")
    numeroRC = fields.Char(string="Numéro RC")
    identifiantTP = fields.Char(string="Identifiant TP")
    nbrPersoPermanent = fields.Integer(string="Nombre des permanents ")
    nbrPersoOccasionnel = fields.Integer(string="Nombre des occasionnels ")
    nbrStagiaires = fields.Integer(string="Nombre de stagiaires ")
    formeJ = fields.Selection([('SARL', 'SARL'), ('SA', 'SA'), ('ENC', 'SNC'), ('PP', 'PP'), ('Autoentrepreneur', 'Autoentrepreneur')], "Forme juridique")
    capital = fields.Char(string="Capital Social")	
    signature = fields.Selection([('Directeur Général', 'Directeur Général'), ('Directeur des Ressources Humaines', 'Directeur Ressources Humaines')], "Signataire des documents")
    taux_bol = fields.Boolean(string="Cochez pour afficher le tableau des taux cnss,... (ATTENTION!!! Ne changer rien dans les taux cnss)")	
    cimr_bol = fields.Boolean(string="Cochez si l'entreprise offre la CIMR")	
    signataire = fields.Char(string="Nom du signataire")
    fonc_signat= fields.Char(string="Fonction du signataire")		

    


