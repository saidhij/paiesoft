# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta


from odoo import fields, models,api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'

    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired'),
        ('cancel', 'Cancelled')
    ], string='Status', group_expand='_expand_states', copy=False,
       tracking=True, help='Status of the contract', default='open')


    mode_pay = fields.Selection([
        ('monthly', 'Mensuel'),
	    ('hourly', 'Horaire'),	

    ], string='Période de Paie', index=True, default='monthly')
	

    start_date = fields.Date(string="Date d'embauche", related='date_start')
    contract_end = fields.Date(string="Date de Départ")	
    prime_saliss = fields.Integer(string="Prime Salissure",default=0,help="max 200dhs par mois")
    absence = fields.Integer(string="Absence en heures",default=0)	
    prime_bilan = fields.Integer(string="Prime du bilan",default=0,help="Prime annuelle taxable")	
    prime_ann = fields.Boolean(string="Prime 13 ième mois",help="Prime annuelle taxable")	
    wageh = fields.Monetary('Salaire horaire', required=True, tracking=True, help="Taux horaire",default=14.81)	    
    pay_period = fields.Selection([('monthly', 'Mensuel'),('hourly', 'Horaire')], string='Période de Paie', index=True, default='monthly')
    prime_vest = fields.Integer(string="Prime Vestimentaire",default=0,help="max 100dhs par mois")
    prime_rend = fields.Integer(string="Prime de rendement",default=0,help="Prime taxable")
    indem_licen = fields.Float(string="Indemnité de licenciement",default=0,help="Barème prévu par les dispositions de l article 53 du code du travail")	
    indem_voit = fields.Integer(string="Indemnité Utilisation de véhicule personnel",default=0,help="max 150dhs par mois")
    prime_repr = fields.Integer(string="Indemnité de représentation",default=0,help="Maximum 10% salaire de base Octroyée uniquement aux directeurs")
    indem_fj= fields.Integer(string="Indemnité pour frais justifiés",default=0,help="")
    prime_achoura = fields.Integer(string="Prime de jouets Achoura",default=0,help="max 150dhs par enfant. Max 750 dhs/employé")	
    alloc_scol = fields.Integer(string="Allocation de rentreee scolaire",default=0,help="400dhs par enfant.Max 1600 dhs/salarié")	

    prime_tax = fields.Integer(string="Autre prime taxable",default=0,help="Indemnité de transport du domicile vers le lieu de travail- périmètre urbain (500 dhs )")
    prime_ntax = fields.Integer(string="Autre prime non taxable",default=0,help="Utiliser pour des primes occasionnelles non taxables")	
    prime_annut = fields.Integer(string="Autre prime annuelle taxable",default=0,help="Utiliser pour autres primes annuelles taxables")	
    prime_panier = fields.Integer(string="Prime de panier",default=0,help="max 20dhs par jour")
    prime_tourn = fields.Integer(string="Prime de tournée",default=0,help="max 20dhs par jour")	
    prime_nuit = fields.Integer(string="Prime de nuit",default=0,help="Prime taxable pour le travail de nuit")	
    prime_outil = fields.Integer(string="Prime d’outillage",default=0,help="max 100dhs par mois")	
    indem_caisse = fields.Integer(string="Indemnité de caisse",default=0,help="max 190dhs par mois")	
    prime_adha = fields.Integer(string="Prime du mouton Aid El Adha",default=0,help="max 1500dhs par mois")
	
    aide_medicale = fields.Integer(string="Aide médicale",default=0,help="Frais médicaux doivent être dûment justifiés par des factures probante")	
    prime_haj = fields.Integer(string="Prime de voyage à la Mecque ",default=0,help="Prix d'avion et dotation de voyage")	    

    indem_depl = fields.Integer(string="Indemnité de déplacement(justificatifs)",default=0,help="sur présentation des justifs")
    indem_depl_note = fields.Text(default="Le montant total des frais est admis intégralement (billets de transport, notes de frais de restaurant et d'hôtels ...etc.).Le paiement desindemnités de mission et le remboursement des frais y afférents sont effectués au vu d'un état justificatif de frais accompagné des pièces justificatives nécessaires.")
    indem_depl_code = fields.Char(default='NAT_ELEM_EXO_1',readonly=True)    
	
    indem_depl2 = fields.Integer(string="Indemnité de déplacement (forfaitaire pontuels) ",default=0,help="Indemnité de déplacement et frais de déplacement accordée sur une base forfaitaire pour des déplacements ponctuels")
    indem_depl2_note = fields.Text(readonly=True,default="Le déplacement doit être justifié par l'ordre écrit délivré à l'intéressé ou tout document en tenant lieu mentionnant la nature de la mission et par l’objet du déplacementPour les frais du transport : ils sont calculés par référence à l'indemnité kilométrique. Nourriture :  évalués sur la base de dix (10) fois le salaire horaire minimum garanti par jour.Hébergement : calculés sur la base de trente (30) fois le salaire horaire minimum garanti par jour..")
    indem_depl2_code = fields.Char(default='NAT_ELEM_EXO_2',readonly=True)	

    indem_depl3 = fields.Integer(string="Indemnité de déplacement (forfaitaire réguliers) ",default=0,help="Indemnité de déplacement et frais de déplacement accordée sur une base forfaitaire pour des déplacements reguliers")
    indem_depl3_note = fields.Text(readonly=True,default="Régularité dans l'octroi de l'indemnité; - La profession exercé en nécessite des déplacements d'une manière continue et régulière (agent ou représentant commercial, VRP, agents itinérants,etc.).L'exonération est admise dans la limite de 100% du salaire de base avec un plafond de 5.000 dhs par mois.Le plafond visé ci-contre englobe aussi bien les frais d'hébergement, de nourriture, que de transport.")
    indem_depl3_code = fields.Char(default='NAT_ELEM_EXO_3',readonly=True)
   	
    indem_kilo = fields.Integer(string="Indemnité kilometrique",default=0,help="Salarié utilise son propre véhicule - Fixée à 3 dhs le km ")
    indem_kilo_note = fields.Text(readonly=True,default="Elle est accordée au salarié utilisant son propre véhicule pour l'exercice de ses fonctions professionnelles.Cette indemnité est fixée à 3 dhs par kilomètre et ce quelle que soit la puissance fiscale du véhicule.Le salarié utilise son propre véhicule ; - Les déplacements sont effectués dans le cadre professionnel et au départ de l'adresse de l'entreprise")
    indem_kilo_code = fields.Char(default='NAT_ELEM_EXO_4',readonly=True)

    indem_transp = fields.Integer(string="Indemnité de transport(p.urbain))",default=0,help="sur présentation des justifs")	
    indem_transp_note = fields.Text(readonly=True,default="Elle est accordée au salarié se rendant de son domicile au lieu habituel de son travail.500 Dhs par mois, dans le périmètre urbain des villes.Sont exclus du bénéfice del'exonération les indemnités accordées aux salariés : - dont les déplacements sont assurés par l'employeur ; - dont la résidence habituelle est située aumême endroit que le lieu de travail ; - qui disposent d'une voiture de fonction..")
    indem_transp_code = fields.Char(default='NAT_ELEM_EXO_5',readonly=True)	

    indem_transp2 = fields.Integer(string="Indemnité de transport(h.p.urbain))",default=0,help="Indemnité de transport du domicile vers le lieu de travail - en dehors du périmètre urbain (750dhs)")	
    indem_transp2_note = fields.Text(default="...")
    indem_transp2_code = fields.Char(default='NAT_ELEM_EXO_6',readonly=True)
	
    prime_tourn = fields.Integer(string="Prime de tournée",default=0,help="max 20dhs par jour")	
    prime_tourn_note = fields.Text(default="max 20dhs par jour")
    prime_tourn_code = fields.Char(default='NAT_ELEM_EXO_7',readonly=True)		
	
    indem_caisse = fields.Integer(string="Indemnité de caisse",default=0,help="max 190dhs par mois")	
    indem_caisse_note = fields.Text(default="max 190dhs par mois")
    indem_caisse_code = fields.Char(default='NAT_ELEM_EXO_8',readonly=True)

    prime_repr = fields.Integer(string="Indemnité de représentation",default=0,help="Maximum 10% salaire de base Octroyée uniquement aux directeurs")
    prime_repr_note = fields.Text(default="Maximum 10% salaire de base Octroyée uniquement aux directeurs")
    prime_repr_code = fields.Char(default='NAT_ELEM_EXO_9',readonly=True)	



    prime_outil = fields.Integer(string="Prime d'outilage",default=0,help="max 100dhs par mois")
    prime_outil_note = fields.Text(default="max 100dhs par mois")
    prime_outil_code = fields.Char(default='NAT_ELEM_EXO_11',readonly=True)	

    prime_saliss = fields.Integer(string="Prime Salissure",default=0,help="max 200dhs par mois")
    prime_saliss_note = fields.Text(readonly=True,default="Max. 200dhs par mois")
    prime_saliss_code = fields.Char(default='NAT_ELEM_EXO_12',readonly=True)


    indem_lait = fields.Integer(string="Indemnité de lait",default=0,help="max. 150dhs par mois.")
    indem_lait_note = fields.Text(default="max. 150dhs par mois.")
    indem_lait_code = fields.Char(default='NAT_ELEM_EXO_13',readonly=True)	
	
    prime_panier = fields.Integer(string="Prime de Panier ou de casse croute",default=0,help="max 20dhs par jour")
    prime_panier_note = fields.Text(default="...")
    prime_panier_code = fields.Char(default='NAT_ELEM_EXO_14',readonly=True)	


    reduc_interet = fields.Integer(string="Réduction d'intérêt",default=0)
    reduc_interet_note = fields.Text(default="Réduction d'intérêt de prêts consentis aux employés")
    reduc_interet_code = fields.Char(default='NAT_ELEM_EXO_16',readonly=True)

    gratif_sociale = fields.Integer(string="Gratifications sociales ",default=0,help=" prime naissance,mariage,circoncision,decès,allocation scolaires,jouets achoura,mouton Adha re,Max 2500dhs par an")	
    gratif_sociale_note = fields.Text(default="prime naissance,mariage,circoncision,decès,allocation scolaires,jouets achoura,mouton Adha re,Max 2500dhs par an")
    gratif_sociale_code = fields.Char(default='NAT_ELEM_EXO_17',readonly=True)

    prime_haj = fields.Integer(string="Prime de voyage à la Mecque ",default=0,help="Prime de voyage à la Mecque pour le pèlerinage Prix d'avion et dotation de voyage")	    
    prime_haj_note = fields.Text(default="Prix d'avion et dotation de voyage")
    prime_haj_code = fields.Char(default='NAT_ELEM_EXO_18',readonly=True)

    alloc_enfants = fields.Integer(string="Allocation versée à un enfant d'un travailleur de l'entreprise ",default=0,help="Allocation versée à un enfant d'un travailleur de l'entreprise")	    
    alloc_enfants_note = fields.Text(default="Allocation versée à un enfant d'un travailleur de l'entreprise")
    alloc_enfants_code = fields.Char(default='NAT_ELEM_EXO_19',readonly=True)	
	
    indem_demang = fields.Integer(string="Indemnité de déménagement",default=0,help="Indemnité de déménagement suite à mutation")	    
    indem_demang_note = fields.Text(default="Indemnité de déménagement suite à mutation")
    indem_demang_code = fields.Char(default='NAT_ELEM_EXO_20',readonly=True)


    deptelepho = fields.Float(string="Dépenses téléphone",default=0,help="Dépenses relatives aux postes de téléphone")
    deptelepho_note = fields.Text(readonly=True,default="Dépenses relatives aux postes de téléphone")
    deptelepho_code = fields.Char(default='NAT_ELEM_EXO21',readonly=True)

    bon_nour = fields.Float(string="Bons de Nourriture",default=0,help="Bons représentatifs des frais de nourriture ou d'alimentation délivrés aux salariés ")
    bon_nour_note = fields.Text(readonly=True,default="Bons représentatifs des frais de nourriture ou d'alimentation délivrés aux salariés ")
    bon_nour_code = fields.Char(default='NAT_ELEM_EXO22',readonly=True)	

    aide_medicale = fields.Integer(string="Aide médicale",default=0,help="Frais médicaux doivent être dûment justifiés par des factures probante")	
    aide_medicale_note = fields.Text(default="Frais médicaux doivent être dûment justifiés par des factures probante")
    aide_medicale_code = fields.Char(default='NAT_ELEM_EXO_23',readonly=True)

    indem_licen = fields.Float(string="Indemnité de licenciement",default=0,help="Barème prévu par les dispositions de l article 53 du code du travail")	
    indem_licen_note = fields.Text(default="Barème prévu par les dispositions de l article 53 du code du travail")
    indem_licen_code = fields.Char(default='NAT_ELEM_EXO_24',readonly=True)	 

    prime_ntax = fields.Integer(string="Autres éléments exonérés",default=0,help="Utiliser pour des primes occasionnelles non taxables")	
    prime_ntax_note = fields.Text(default="Utiliser pour des primes occasionnelles non taxables")
    prime_ntax_code = fields.Char(default='NAT_ELEM_EXO_25',readonly=True)	
	    
    taux_cimr = fields.Float(string="Taux de la CIMR  salariale",default=0)
    taux_cimr_p = fields.Float(string="Taux de la CIMR  patronale",default=0)	
    date_cimr = fields.Date(string="Date Affiliation CIMR", default=lambda *a: date.today())		
    categ_cimr = fields.Char(string="Numéro de catégorie CIMR",default='00')	
    cimr_bool = fields.Boolean(string="Cochez si cet employé bénéficie de la CIMR")
    taux_mut = fields.Float(string="Taux de la Mutuelle employé si existe",default=0)
    prime_encad = fields.Integer(string="Prime d'encadrement",default=0,help="Prime taxable")
    deptelepho = fields.Float(string="Dépenses téléphone",default=0,help="Prime exonérée")
    abondement = fields.Float(string="Abondement(PEE)",default=0,help="Exonérée a hauteur de 10% du salaire annuel")	
    anciennete = fields.Integer(string="Ancienneté", compute='_anciennete')	
    end_date = fields.Date(string="Date de Fin", related='date_end')	
    today = fields.Date(default=fields.Date.today)


    log = fields.Boolean(string="Cochez si cet employé bénéficie des déductions logement social")	
    type_ctr = fields.Selection([('CDI', 'CDI'), ('CDD', 'CDD'),('COC', 'Occasionnel'), ('STG', 'Stagiaire'), ('ANAPEC1', 'ANAPEC modèle I'), ('ANAPEC2', 'ANAPEC modèle II'), ('ANAPEC3', 'ANAPEC modèle III'), ('DOCT', 'DOCTORANTS'), ('AUTRE', 'AUTRE')], 'Type de contrat',required=True)
    situation = fields.Selection([('SO', 'SO'),('EN', 'EN'), ('DE', 'DE'), ('IT', 'IT'), ('IL', 'IL'), ('AT', 'AT'), ('CS', 'CS'), ('MS', 'MS'), ('MP', 'MP')], 'Situation CNSS')	
    anapec = fields.Boolean(string="Cochez si cet employé a un contrat Anapec",help="Exonération cnss-ir")
    quesmig = fields.Boolean(string="Cochez si cet employé aura que le SMIG")
    duration = fields.Float(digits=(6, 0), string="Durée du contrat en jours")	
    profession = fields.Char('Profession')
    expire = fields.Float(digits=(6, 0),string="Jours passés")	
    progress = fields.Float(string="Progrès du contrat")
    warning = fields.Char('warning')
    motif= fields.Selection([('Démission', 'Démission'), ('Licenciement', 'Licenciement'), ('Fin de contrat', 'Find de contrat'), ('Fermeture', 'Fermeture')], 'Motif de départ')
    warningval = fields.Char(default='Attention ce  contrat a expiré !')
    hours = fields.Integer(string='Nombre Heures de T',default=191,readonly=True)
    days = fields.Integer(string='Nombre Jours de T',default=26,readonly=True)
    jours_t = fields.Integer(string="Nombre de jours  par an",default=312,readonly=True)		
    leave = fields.Float(string='Cumul congé par Mois', compute='_get_leave')
    cpris = fields.Float(string="Congé pris en jours")
    crest = fields.Float(string="Congé restant en jours", compute='_get_crest' )
    com =fields.Integer(string="Commission sur ventes",default=0,help=" Taxable")


    frais_loge = fields.Float(string="Frais de logement",default=0,help="Logement y compris le matériel et le mobilier")
    frais_conso1= fields.Float(string="Frais eau et électricité",default=0,help="Factures eau et électricité:")
    frais_conso2= fields.Float(string="Frais Téléphone et Internet",default=0,help="Factures téléphone:")
    frais_conso3= fields.Float(string="Frais de domesticité",default=0,help="gardiens, jardiniers, cuisiniers, nourrices")
    frais_conso4= fields.Float(string="Impôts personnels",default=0,help="Paiement Impôts personnels:")
    frais_conso5= fields.Float(string="Transport et carburant",default=0,help="y compris les dotations en carburant, à l’exception des transports en commun")
    prime_nature= fields.Float(string="Autres primes en nature)",default=0)	
	

    assurvie =fields.Float(string="Montant Mensuel Assurance Vie ",default=0)
    assurvie_bol = fields.Boolean(string="Cochez si cet employé à une assurance vie")
    prime_bol = fields.Boolean(string="Cochez si cet employé a droit à des primes ou indemnités")	

    payment_mode = fields.Selection([('Virement', 'Virement'), ('Espece', 'Espèce'), ('Cheque', 'Chèque')], "Mode de paiement",default= 'Virement')	
	
    casSportif = fields.Selection([('True', 'True'), ('False', 'False')], 'Cas sportif ou nom',default='False')	
    code_formpro = fields.Selection([('code1', 'TPP.40.2009'), ('code2', 'TPP.45.2009'), ('code3', 'TPP.35.2009'), ('code4', 'TPP.25.2009'), ('code5', 'TPP.20.2009'), ('code6', 'TAS.40.2012')], "Code du taux des frais professionnels",default= 'code5')	
    t_ded_formpro = fields.Float(string="Taux des frais professionnels")		
    name = fields.Char('Référence contrat', required=False,readonly=True, copy=False, default='...')
    qualif = fields.Char(string='Qualification')
    niveau = fields.Char()
    coef = fields.Char(string='Coefficient')
	

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('contract.ref') 
        ref = super(HrContract, self).create(vals)
        return ref	

    @api.depends('today','date_start')
    def _anciennete(self):
        if self.date_start:
          
            end = date.today()
            self.anciennete = relativedelta(end,self.date_start).years

				
    @api.depends('today','date_start')
    def _get_leave(self):
        for r in self:
            if r.date_start:
                end = date.today()
                self.leave = relativedelta(end,self.date_start).months *1.5 
		

    # @api.depends('today')
    # def _get_leave(self):
        # for r in self:
            # if not r.leave:
                # r.leave=((fields.Datetime.from_string(self.today).month))*1.5 
				
    @api.depends('leave','cpris')
    def _get_crest(self):
        for d in self: 
            if not d.leave:
                d.crest = 0.0
            else:				
                d.crest=d.leave-d.cpris	


 


		


