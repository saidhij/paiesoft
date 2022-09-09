# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
# from odoo.addons import decimal_precision as dp
from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    mois=fields.Integer(string="N° mois", compute = '_get_numero')	
    datepaiem=fields.Date(string="Date de paiement",compute = '_datepaiement')	
    gross_wage = fields.Monetary(compute='_compute_gross_net')	

    @api.model
    def _get_total_by_rule_category(self, obj, code):
        payslip_line = self.env['hr.payslip.line']
        rule_cate_obj = self.env['hr.salary.rule.category']

        cate_ids = rule_cate_obj.search([('code', '=', code)])

        category_total = 0
        if cate_ids:
            payslip_lines = payslip_line.search([('slip_id', '=', obj.id), ('category_id', '=', cate_ids[0].id)])
            for line in payslip_lines:
                category_total += line.total

        return category_total
	
	
    date_payment = fields.Date(default=fields.Date.today)	

    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        self.compute_total_ytds()
        return res


    def compute_total_ytds(self):
        if not self.line_ids:
            return

        query = (
            """SELECT pl_1.id, sum(
                case when p.credit_note then -pl_2.amount else pl_2.amount end)
            FROM hr_payslip_line pl_1, hr_payslip_line pl_2, hr_payslip p
            WHERE pl_1.id IN %(payslip_line_ids)s
            AND pl_1.salary_rule_id = pl_2.salary_rule_id
            AND pl_2.slip_id = p.id
            AND p.employee_id = %(employee_id)s
            AND p.company_id = %(company_id)s
            AND (p.state = 'draft' OR p.state = 'done' OR p.id = %(payslip_id)s)

            GROUP BY pl_1.id
            """)

        date_payment = fields.Date.from_string(self.date_payment)
        date_from = fields.Date.to_string(datetime(date_payment.year, 1, 1))

        cr = self.env.cr

        cr.execute(query, {
            'date_from': date_from,
            'date_to': self.date_payment,
            'payslip_line_ids': tuple(self.line_ids.ids),
            'employee_id': self.employee_id.id,
            'company_id': self.company_id.id,
            'payslip_id': self.id,
        })

        res = cr.fetchall()

        line_model = self.env['hr.payslip.line']

        for (line_id, total_ytd) in res:
            line = line_model.browse(line_id)
            line.total_ytd = total_ytd

    @api.model 
    def total_ytd(self, total):
        """
        Get the total amount since the beginning of the year
        of a given salary rule code.

        :param code: salary rule code
        :return: float
        """
        self.ensure_one()

        date_slip = fields.Date.from_string(self.date_to)
        date_from = to_string(datetime(date_slip.year, 1, 1))

        query = (
            """SELECT sum(
                case when p.credit_note then -pl.total else pl.total end)
            FROM hr_payslip_line as pl, hr_payslip as p
            WHERE pl.slip_id = p.id
            AND pl.total = %(total)s
            AND p.employee_id = %(employee_id)s
            AND p.company_id = %(company_id)s
      
            """
        )

        cr = self.env.cr

        cr.execute(query, {
            'date_from': date_from,
            'date_to': self.date_payment,
            'company_id': self.company_id.id,
            'employee_id': self.employee_id.id,
            'total': total,
        })

        return cr.fetchone()[0] or 0
		


    # def get_worked_day_lines(self, contract_id,date_from, date_to):
        # self.ensure_one()	
        # res = super(HrPayslip, self).get_worked_day_lines(contract_id, date_from, date_to)
        # number_of_days =  self.employee_id.jrs_trav_cemois
        # number_of_hours = self.employee_id.hrs_trav_cemois
        # amount_wage = self.contract_id.wageh*number_of_hours if mode_pay =='hourly' else contract_id.wage	
        # for line in res:
            # if 'number_of_days' in line:
                # line['number_of_days'] =number_of_days
                # line['number_of_hours']=number_of_hours
                # line['amount']= amount_wage				
        # return res

    def _compute_gross_net(self):
        for p in self:
            p.gross_wage = p._get_salary_line_total('BRUT')



class hr_payslip_line(models.Model):
    _inherit = 'hr.payslip.line'

    total_ytd = fields.Float('Cumul')
