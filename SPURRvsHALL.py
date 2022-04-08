import pandas as pd
import statistics
import math
import numpy as np
import statsmodels.api as sm
import requests
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import tkinter as tk
import matplotlib.image as mpimg
from statsmodels.formula.api import ols
from tkinter import *
from statsmodels.compat import lzip
from PIL import ImageTk,Image
from tkinter.messagebox import showinfo
from tkinter import ttk
from PIL import Image
from tkinter import messagebox
import os


def tudo():
  data2 = pd.read_csv("Cubagemvolume.csv")
  constante1=40000
  pi=3.14159265359
  data2 = data2.replace(',','.', regex=True)

  data2['hi'] = data2['hi'].astype(float)
  data2['di'] = data2['di'].astype(float)
  data2['DAP'] = data2['DAP'].astype(float)
  data2['HT'] = data2['HT'].astype(float)
  data2['area_sec'] = ((data2['di']**2)*pi/constante1)
  narv=0
  narv1=1
  narv2=-1

  nlinhas=len(data2)
  nlinhas=nlinhas-1

  while narv<nlinhas:
    teste1=data2.iloc[narv, 5]
    teste2=data2.iloc[narv1, 5]
    teste3=data2.iloc[narv1, 1]
    teste4=data2.iloc[narv, 1]
    narv=narv+1
    narv1=narv1+1
    narv2=narv2+1
    data2.at[narv, "vol_sec"] = ((teste1+teste2)/2)*(teste3-teste4)
    valip=data2.iloc[narv, 5]
    valip1=data2.iloc[narv, 1]
    if valip == 0:
      teste5=data2.iloc[narv2, 5]
      teste6=data2.iloc[narv2, 1]
      teste7=data2.iloc[narv, 1]
      data2.at[narv, "vol_sec"] = (((1/2)*teste5)*(teste7-teste6))
    if valip1 == 0.1:
      teste8=data2.iloc[narv, 5]
      teste9=data2.iloc[narv, 1]
      data2.at[narv, "vol_sec"] = teste8*teste9


  teste10=data2.iloc[0, 5]
  teste11=data2.iloc[0, 1]
  data2.at[0, "vol_sec"] = teste10*teste11


  freq=data2.groupby(["arv"]).count()

  b=data2.iloc[nlinhas, 0]
  b=b+1
  a=data2.iloc[0, 0]
  p=0
  k=-1
  cont1=0
  while b>a:
    m=freq.iloc[p, 0]
    p=p+1
    a=a+1
    k=k+1
    cont=0
    n=0
    while m>cont:
      o=data2.iloc[cont1, 6]
      n=n+o
      data2.at[k, "somarv"]=n
      cont=cont+1
      cont1=cont1+1


  datah=data2
  data3 = data2
  data3=data3[(data2[["hi"]] == 0.1).all(axis=1)]
  data3=data3.drop(["hi", "di", "area_sec", "vol_sec", "somarv"], axis=1)
  data3.reset_index(inplace=True)
  data3=data3.drop(["index"], axis=1)
  extrac = datah["somarv"]

  data3 = data3.join(extrac)


  data3['landap'] = np.log(data3['DAP'])
  data3['lanht'] = np.log(data3['HT'])
  data3['lanvol'] = np.log(data3['somarv'])

  #hall
  datah=data2
  data3 = data2
  data3=data3[(data2[["hi"]] == 0.1).all(axis=1)]
  data3=data3.drop(["hi", "di", "area_sec", "vol_sec", "somarv"], axis=1)
  data3.reset_index(inplace=True)
  data3=data3.drop(["index"], axis=1)
  extrac = datah["somarv"]

  data3 = data3.join(extrac)


  data3['landap'] = np.log(data3['DAP'])
  data3['lanht'] = np.log(data3['HT'])
  data3['lanvol'] = np.log(data3['somarv'])


  endog = data3['lanvol']
  exog = sm.add_constant(data3[['landap','lanht']])

  modelo = sm.OLS(endog, exog)
  resultado = modelo.fit()
  #print (resultado.summary())

  #spur


  datasp=data3.drop(["landap", "lanht", "lanvol"], axis=1)
  datasp["multi"] = ((datasp['DAP']**2)*datasp['HT'])

  endog = datasp['somarv']
  exog = sm.add_constant(datasp[['multi']])

  modelo = sm.OLS(endog, exog)
  resultado1 = modelo.fit()


  plt.rc('figure', figsize=(8,5.5))

  plt.text(0.01, 0.01, str(resultado.summary()), {'fontsize': 9.}, fontproperties='monospace')
  plt.axis('off')
  plt.tight_layout()
  plt.savefig('hall.png')
  plt.clf() #limpa o plot


  plt.text(0.01, 0.01, str(resultado1.summary()), {'fontsize': 9.}, fontproperties='monospace')
  plt.axis('off')
  plt.tight_layout()
  plt.savefig('spurr.png')
  plt.clf()


  plt.rc("figure", figsize=(8.5,5.9))
  plt.rc("font", size=6)

  fig_spurr = sm.graphics.plot_regress_exog(resultado1, "multi")
  fig_spurr.tight_layout(pad=1.0)
  plt.savefig("fig_spurr.png")
  plt.clf()

  fig_spurr = Image.open("fig_spurr.png")

  left = 0
  top = 0
  right = 900
  bottom = 300

  fig_spurr = fig_spurr.crop((left, top, right, bottom))

  fig_spurr = fig_spurr.save("fig_spurr.png")


  fig_hall = sm.graphics.plot_regress_exog(resultado, "landap")
  fig_hall.tight_layout(pad=1.0)
  plt.savefig("fig_hall.png")
  plt.clf()

  fig_hall = Image.open("fig_hall.png")

  left = 0
  top = 0
  right = 900
  bottom = 300

  fig_hall = fig_hall.crop((left, top, right, bottom))

  fig_hall = fig_hall.save("fig_hall.png")

  fig_hall1 = sm.graphics.plot_regress_exog(resultado, "lanht")
  fig_hall1.tight_layout(pad=1.0)
  plt.savefig("fig_hall1.png")
  plt.clf()

  fig_hall1 = Image.open("fig_hall1.png")

  left = 0
  top = 0
  right = 900
  bottom = 300

  fig_hall1 = fig_hall1.crop((left, top, right, bottom))

  fig_hall1 = fig_hall1.save("fig_hall1.png")

  photo = PhotoImage(file='hall.png')
  lbl = Label(root, image=photo, anchor=SE)
  lbl.image = photo
  lbl.grid(column=2, row=0)

  photo = PhotoImage(file='spurr.png')
  lbl = Label(root, image=photo, anchor=SE)
  lbl.image = photo
  lbl.grid(column=1, row=0)

  photo = PhotoImage(file="fig_spurr.png")
  lbl = Label(root, image=photo)
  lbl.image = photo
  lbl.grid(column=1, row=1)

  photo = PhotoImage(file="fig_hall.png")
  lbl = Label(root, image=photo)
  lbl.image = photo
  lbl.grid(column=2, row=1)

  photo = PhotoImage(file="fig_hall1.png")
  lbl = Label(root, image=photo)
  lbl.image = photo
  lbl.grid(column=2, row=2)

  y = data3["somarv"]
  y_hat = resultado1.predict()
  syx = y - y_hat
  syx = syx ** 2
  syx = syx.sum(axis=0)
  syx = syx / (k - 1)
  syx = math.sqrt(syx)
  syx = syx / statistics.mean(data3["somarv"])
  syx = syx * 100

  y1 = data3["somarv"]
  y_hat = resultado1.predict()
  syx1 = y1 - y_hat
  syx1 = syx1 ** 2
  syx1 = syx1.sum(axis=0)
  syx1 = syx1 / (k - 2)
  syx1 = math.sqrt(syx1)
  syx1 = syx1 / statistics.mean(data3["somarv"])
  syx1 = syx1 * 100

  if syx>syx1:
    modelo="spurr"
  else:
    modelo="hall"

  syx = str(syx)
  syx1 = str(syx1)
  printao= "syx% spurr: " + syx + "\n syx% hall:" +syx1 +"\n\n Levando em consideração apenas as estatísticas, escolhemos o modelo de "+ modelo

  info["text"]=printao


  
root = tk.Tk()
root.title('SPURRvsHALL')


root.columnconfigure(0, weight=0)
root.rowconfigure(0, weight=1)


botao= Button(root, text="IR", command= tudo)
botao.grid(column= 0, row=1)

info= Label(root, text="")
info.grid(column= 1, row=2)

xl = pd.ExcelFile("Cubagemvolume.xlsx")
xl1 = xl.sheet_names

langs = (xl1)

langs_var = tk.StringVar(value=langs)

listbox = tk.Listbox(
    root,
    listvariable=langs_var,
    height=6,
    selectmode='extended')

listbox.grid(
    column=0,
    row=0,
    sticky='nwes'
)


scrollbar = ttk.Scrollbar(
    root,
    orient='vertical',
    command=listbox.yview
)

listbox['yscrollcommand'] = scrollbar.set




def items_selected(event):
  
    selected_indices = listbox.curselection()
    
    selected_langs = ",".join([listbox.get(i) for i in selected_indices])
    read_file = pd.read_excel('Cubagemvolume.xlsx', sheet_name=selected_langs)
    read_file.to_csv('Cubagemvolume.csv', index=None, header=True)


def on_closing():
  if messagebox.askokcancel("Sair", "Já acabou?"):
    os.remove("Cubagemvolume.csv")
    os.remove("fig_hall1.png")
    os.remove("fig_spurr.png")
    os.remove("fig_hall.png")
    os.remove("hall.png")
    os.remove("spurr.png")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


listbox.bind('<<ListboxSelect>>', items_selected)

root.mainloop()

