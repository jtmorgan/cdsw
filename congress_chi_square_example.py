#!/usr/bin/env python
# coding=utf-8

#from http://connor-johnson.com/2014/12/31/the-pearson-chi-squared-test-with-python-and-r/

#       Republican	Democrat	Totals
#Male	215	        143	        358
#Female	19	        64	        83
#Totals	234	        207	        441

import scipy.stats
 
house = [ [ 215, 143 ], [ 19, 64 ] ]
chi2, p, ddof, expected = scipy.stats.chi2_contingency( house )
msg = "Test Statistic: {}\np-value: {}\nDegrees of Freedom: {}\n"
print( msg.format( chi2, p, ddof ) )
print( expected )