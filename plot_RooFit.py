import csv
from datetime import datetime

xs = []
ys = []
import ROOT
graph = ROOT.TGraph()

fName = "MONTE_ROCCHETTA_TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C.csv"
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
    temp = float(row["TEMPERATURA__TEMPERATURA_MEDIA_DELLARIA_Gradi_C"])
    graph.AddPoint(days, temp)
    xs.append(days)
    ys.append(temp)


graph.Draw("APL")
#function = ROOT.TF1("function","[0] + [1]*sin([2]*x + [3]) + [4]*sin([5]*x + [6])",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())
function = ROOT.TF1("function","[0] + ([1]+[5]*x)*sin([2]*x + [3]) + [4]*x",graph.GetXaxis().GetXmin(),graph.GetXaxis().GetXmax())
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

#1/0


from ROOT import RooRealVar, RooPolynomial, RooDataSet, RooFitResult, RooArgList, RooFit, RooGenericPdf, RooBinning, RooDataHist, RooAddPdf

# Crea i parametri di adattamento
x = RooRealVar("x", "x", min(xs), max(xs))
y = RooRealVar("y", "y", min(ys), max(ys))

x.setBinning(RooBinning(int((max(xs) - min(xs)))+1, float(min(xs)), float(max(xs))))


# Crea la lista di RooArgList
variables = RooArgList(x, y)
#variables = RooArgList(x)

# Crea il RooDataSet
data = RooDataHist("data", "data", variables)

# Aggiunge i punti di dati al RooDataSet
for i in range(len(xs)):
    x.setVal(xs[i])
#    y.setVal(ys[i])
#    data.add(variables, 1, 1)
    data.add(variables, ys[i]+20, 1)
    if xs[i]>-3120 and xs[i]<-3100:
        print(xs[i], ys[i])
#    print(variables.get()[0].getVal(), variables.get()[1].getVal())

# Crea il modello di adattamento

# Crea i parametri di adattamento
A = RooRealVar("A", "A", 14, 10, 20)
B = RooRealVar("B", "B", 8, 4, 15)
C = RooRealVar("C", "C", 3.14*2./365 , 3.14*1./365, 3.14*4./365)
D = RooRealVar("D", "D", 0, -3.15, +3.15)

# Crea la lista di RooArgList
parameters = RooArgList(A, B, C, D, x)

# Definisci la stringa di formula per la funzione A + B*sin(C*x+D)
formula = "A + B*sin(C*x+D)"

# Crea l'istanza di RooGenericPdf
model = RooGenericPdf("model", formula, parameters)

# Esegue il fit
result = model.fitTo(data, RooFit.Save())

# Stampa il resoconto del fit
result.Print()

plot = x.frame(RooFit.Title("Fit result"))



B2 = RooRealVar("B2", "B2", 8, 0, 15)
C2 = RooRealVar("C2", "C2", 3.14*4./365 , 0 , 3.14*8./365)
D2 = RooRealVar("D2", "D2", 0, -3.15, +3.15)

parameters2 = RooArgList(B2, C2, D2, x)
model2 = RooGenericPdf("model2", "B2*sin(C2*x+D2)", parameters2)

tot = RooAddPdf("sum","g+a",RooArgList(model,model2),RooArgList(B,B2))

# Esegue il fit
result2 = tot.fitTo(data, RooFit.Save())

# Stampa il resoconto del fit
result2.Print()

data.plotOn(plot)

model.plotOn(plot)

tot.plotOn(plot)


#c2 = ROOT.TCanvas("c2")
#plot.Draw()

    
