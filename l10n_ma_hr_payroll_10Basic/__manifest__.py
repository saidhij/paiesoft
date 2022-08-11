# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022 paiesoft (<http://paieafricaine.online>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Morocco-payroll Basic',
    'category': 'Payroll',
    'author': 'paiesoft',
    'website': 'https://paieafricaine.online',

    'version': '1.14Basic',
    'depends': ['hr_payroll'],
    
	
    'description': """Paie Marocaine sous Odoo. Version Basique gratuite - Entreprise SH
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
