#imports
from matplotlib import pyplot
from openpyxl import load_workbook

#declaration
#Get value function
def getvalue(x):
    return x.value

#execution
wb = load_workbook('data_analysis_lab.xlsx')
sheet = wb['Data']

years = list(map(getvalue, sheet['A'][1:]))
temperature = list(map(getvalue, sheet['C'][1:]))
sunActivity = list(map(getvalue, sheet['D'][1:]))

pyplot.plot(years, temperature, label="Отн. температура")
pyplot.plot(years, sunActivity, label="Акт. Солнца")

pyplot.show()