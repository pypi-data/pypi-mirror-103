#!/usr/bin/env python
""" Tests of Larch Scripts  """

from larch import Interpreter
import os

os.chdir('larch_scripts')

_larch = Interpreter()
_larch.run("run('read_ascii.lar')")
print("ERRORS ", _larch.error)

print("RESULTS ", _larch.symtable.get_symbol('results'))

# 
#         actual = self.session.get_symbol('results')
#         expected = self.session.get_symbol('expected')
#         print("actual ", actual)
#         print("expected ", expected)
#         
#         for fname, ncol, nrow, labels in expected:
#             acol, arow, alabs = actual[fname]
#             assert(acol == ncol)
#             assert(arow == nrow)
#             assert(alabs == labels)
# 
