#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import math
import re
integers_regex = re.compile(r'\b[\d\.]+\b')

def calc(expr, advanced=True):
   def safe_eval(expr, symbols={}):
       return eval(expr, dict(__builtins__=None), symbols)
   def whole_number_to_float(match):
       group = match.group()
       if group.find('.') == -1:
           return group + '.0'
       return group
   expr = expr.replace('^','**')
   expr = integers_regex.sub(whole_number_to_float, expr)
   if advanced:
       return safe_eval(expr, vars(math))
   else:
       return safe_eval(expr)

class CalcMixin(object):
    """Create a calculator command"""

    def cmd_calc(self, msg, args):
        """!calc <operation>   - calculate a math operation, i.e: 2+3, 2**3, pow(2,pi)..."""

        if len(args) == 0:
            return "I need some operation to calc."

        return str(calc(" ".join(args)))


