import glob
import sys
from datetime import datetime
import json

import warnings
from io import BytesIO

from koala.xml.functions import fromstring, safe_iterator
from koala.ast.tokenizer import ExcelParser
from koala.ast.graph import ExcelCompiler, Spreadsheet
from koala.ast.excelutils import Cell
from koala.ast.astutils import *


if __name__ == '__main__':

    # files = glob.glob("./data/*.xlsx")
    # file = "./example/example.xlsx"
    file = "./data/100021224 - Far East - Indonesia - Abadi Gas (Phase 1) - Gas - New Project.xlsx"

    print file        
    startTime = datetime.now()

    # c = ExcelCompiler(file, ignore_sheets = ['IHS'])
    # c.clean_volatile()
    # print "___Timing___ %s cells and %s named_ranges parsed in %s" % (str(len(c.cells)-len(c.named_ranges)), str(len(c.named_ranges)), str(datetime.now() - startTime))
    # sp = c.gen_graph(outputs=["outNPV_Proj"])
    # print "___Timing___ Graph generated in %s" % (str(datetime.now() - startTime))
    
    # print "Serializing to disk...", file
    # sp.dump(file.replace("xlsx", "gzip"))


    startTime = datetime.now()
    print "Reading from disk...", file
    sp = Spreadsheet.load(file.replace("xlsx", "gzip"))
    print "___Timing___ Graph read in %s" % (str(datetime.now() - startTime))

    sys.setrecursionlimit(10000)

    
    print 'First evaluation', sp.evaluate('outNPV_Proj')

    tmp = sp.evaluate('IA_PriceExportGas')
    for addr, cell in sp.cellmap.items():
        sp.history[addr] = {'original': str(cell.value)}

    sp.set_value('IA_PriceExportGas', 0)
    sp.set_value('IA_PriceExportGas', tmp) # =InputData!$L$99:$DG$99

    startTime = datetime.now()
    print 'Second evaluation %s for %s' % (str(sp.evaluate('outNPV_Proj')),str(-1826))

    # startTime = datetime.now()
    # # # sp.set_value('InputData!G14', 0)
    # sp.set_value('InputData!G14', 2018)
    # print 'Second evaluation', sp.evaluate('Cashflow!G187')

    print "___Timing___  Evaluation done in %s" % (str(datetime.now() - startTime))

    print 'NB different', sp.count

    with open('history_dif.json', 'w') as outfile:
        json.dump(sp.history, outfile)

    
