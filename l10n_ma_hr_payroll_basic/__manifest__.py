# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Morocco-payroll Basic',
    'category': 'Payroll',
    'author': 'paiesoft',
    'website': 'https://paieafricaine.online',

    'version': '1.15Basic',
    'depends': ['hr_payroll'],
    
	
    'description': """Paie Marocaine sous Odoo. Version Basique gratuite - Odoo entreprise sh
======================

    - Version gratuite de test
    - La version Pro est complète avec états CNSS,CIMR ,Etat 9421,et bulletin de paie bien élaboré.

    """,
    'data': [
        'data/l10n_ma_hr_payroll_data.xml',
        'data/l10n_ma_hr_payroll_data_employe.xml',
        'views/l10n_ma_hr_payroll_view.xml',
     
  
    ],
	
	'installable': True,	
     "images":['static/description/Banner.png'],	
}
