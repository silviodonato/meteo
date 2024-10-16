import csv
from datetime import datetime

xs = []
ys = []
import ROOT
graph = ROOT.TGraph()
graph_residual = ROOT.TGraph()


Jan1 = ROOT.TDatime(1995,1,1,0,0,0).Convert()
def transformDate(day):
    return Jan1 + 86400*day

c1 = ROOT.TCanvas("c1")

#fName = "MONTE_ROCCHETTA_TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C.csv"
fName = "LA_SPEZIA_TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C.csv"
#fName = "LA_SPEZIA_PRECIPITAZIONE__PRECIPITAZIONE_CUMULATA_mm.csv"
#fName = "SERO_DI_ZIGNAGO_TEMPERATURA__TEMPERATURA_MASSIMA_ASSOLUTA_DELLARIA___Gradi_C.csv"
#fName = "SERO_DI_ZIGNAGO_TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C.csv"

var = "__".join(fName.split("__")[1:]).split(".csv")[0]
var = var.split("_")[0]+"__"+var

# Open the CSV file
with open(fName, 'r') as f:
  # Create a DictReader object
  reader = csv.DictReader(f)

  # Iterate over the rows of the CSV file
  for row in reader:
    # Print the values of the row
#    print(row)
    
    date = datetime.strptime(row["Inizio rilevazione"], '%d/%m/%Y')
#    days = (int(date.timestamp()) - int(datetime(2010,1,1).timestamp()))/86400 #3.154e+7
    days = (date - datetime(2010,1,1)).days
    temp = float(row[var]) #"TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C"
    graph.AddPoint(days, temp)
    xs.append(days)
    ys.append(temp)


graph.Draw("APL")
#function = ROOT.TF1("function","[0] + [1]*sin([2]*x + [3]) + [4]*sin([5]*x + [6])",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())
function = ROOT.TF1("function","[0] + ([1]+[5]*x)*sin([2]*x + [3]) + [4]*x",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())
function.SetNpx(1000)
function.SetParameters(14,8,3.14*2./365,0,0,3.14*4./365,0)
function.FixParameter(4,0)
function.FixParameter(5,0)
function.FixParameter(6,0)
graph.Fit(function,"","",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())

function1 = function.Clone("function1")
function1.SetLineColor(ROOT.kBlue)

function.ReleaseParameter(4)
function.ReleaseParameter(5)
function.ReleaseParameter(6)

function.SetParameter(4, 0.1)
function.SetParameter(5, 4*3.14)
function.SetParameter(6, 0)


graph.Fit(function,"","",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())

function.Draw("same")
function1.Draw("same")


offset = 0
#offset = 100

average = {}
for i, x in enumerate(xs):
    x = x+offset
    x = x%365
    if not x in average: average[x] = []
    average[x].append(ys[i])

for x in sorted(average.keys()):
    print(x, len(average[x]), average[x])
    average[x] = sum(average[x])/len(average[x])


graph_average = ROOT.TGraph()
for x in sorted(average.keys()):
#    graph_residual.AddPoint(xs[i], ys[i] - function.Eval(xs[i]))
    graph_average.AddPoint(x, average[x])


function_average = ROOT.TF1("function","[0] + [1]*sin([2]*x + [3]) + [4]*sin([5]*x + [6]) + [7]*sin([8]*x + [9])",graph_average.GetXaxis().GetXmin(),graph_average.GetXaxis().GetXmax())
function_average.SetNpx(1000)
function_average.SetParameters(14,8,3.14*2./365,0,8,3.14*4./365,0,8,3.14*8./365,0)

c3 = ROOT.TCanvas("c3")

graph_average.Fit(function_average)
graph_average.SetMarkerStyle(21)
graph_average.Draw("AP")

c2 = ROOT.TCanvas("c2")
c2.SetGridx()
c2.SetGridy()

graph_residual = ROOT.TGraph()
for i, x in enumerate(xs):
    x = x+offset
    y = ys[i]
#    if i>10 and i<len(ys)-10:
#        y=sum(ys[i-10:i+10])/len(ys[i-10:i+10])
    graph_residual.AddPoint(xs[i], y - function_average.Eval(xs[i]%365))
#    graph_residual.AddPoint(xs[i], y - average[xs[i]%365])
    pass

function_residual = ROOT.TF1("function_residual","[0] + [1]*x",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())
function_residual.SetNpx(1000)
graph_residual.Fit(function_residual)
graph_residual.Draw("APL")

#1/0

from datetime import timedelta

graphs = {}
for i, x in enumerate(xs):
    x = x + offset
    year = round(x/365. + 0.5)+2009
    if not year in graphs:
        graphs[year] = ROOT.TGraph()
#        graphs[year] = ROOT.TGraph(str(year),str(year),366)
    days = x - int((datetime(year,1,1)-datetime(2010,1,1)).days)
    if days==217:
      print(year, days, ys[i])
#    dd = datetime(year,1,1)+timedelta(days=days)
    graphs[year].AddPoint(transformDate(days), ys[i])
#    graphs[year].Fill(days, ys[i])

colors = [ROOT.kRed +3,ROOT.kRed +1,ROOT.kRed -4,ROOT.kRed -7,ROOT.kRed -9,ROOT.kGreen +3,ROOT.kGreen +1,ROOT.kGreen -4,ROOT.kGreen -7,ROOT.kGreen -9,ROOT.kBlue +3,ROOT.kBlue +1,ROOT.kBlue -4,ROOT.kBlue -7,ROOT.kBlue -9,]


leg = ROOT.TLegend(0.1,0.5,0.15,0.9)
leg.SetHeader("")

graphs[2010].GetXaxis().SetTimeDisplay(1)
graphs[2010].GetXaxis().SetTimeFormat("%d/%m")
graphs[2010].Draw("APL")

graphs[2010].SetMaximum(40)
graphs[2010].Draw("AP")

for i, year in enumerate(graphs):
    graphs[year].SetLineColor(colors[i%len(colors)])
    if year == 2022: 
        graphs[year].SetLineWidth(3)
        graphs[year].SetLineColor(ROOT.kRed)
    if year == 2023: 
        graphs[year].SetLineWidth(3)
        graphs[year].SetLineColor(ROOT.kBlue)
    if year == 2024: 
        graphs[year].SetLineWidth(4)
        graphs[year].SetLineColor(ROOT.kBlack)
    graphs[year].Draw("PL")
    leg.AddEntry(graphs[year],str(year),"lep") # or lep or f</verbatim>
#    graphs[year].GetXaxis().SetRangeUser(-5,400)

graph_average2 = ROOT.TGraph()
for x,y in zip(graph_average.GetX(),graph_average.GetY()):
    graph_average2.AddPoint(transformDate(x), y)

graph_average2.SetLineWidth(5)
graph_average2.SetLineColor(ROOT.kGreen)
graph_average2.Draw("PL")
leg.AddEntry(graph_average2,"aver.","lep")

function_average.Draw("same")

leg.Draw("same")

#graphs.Draw("")





