from flask import Flask
from flask import render_template
from flask import request
import time
import os
import datetime

import sqlite3
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

def genera_codibarra(numero):
     EAN = barcode.get_barcode_class('code128')
     numero="00"+numero
     ean = EAN(numero,writer=ImageWriter())
     nomimg="static"+"/"+"images"+"/"+numero
     ean.save(nomimg)
     return nomimg

def genera_codibarraBobina(codigobobina):
     EAN = barcode.get_barcode_class('code128')
     codigobobina="00"+codigobobina
     ean = EAN(codigobobina,writer=ImageWriter())
     nomimg="static"+"/"+"imagesbobina"+"/"+codigobobina
     ean.save(nomimg)
     return nomimg

def inserir_pedido(npedido,fecha):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Pedido(Npedido,Fecha) VALUES (?,?)',(npedido,fecha))
  conn.commit()

def existe_pedido(npedido):
  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Pedido WHERE Npedido = (?)',(npedido,))
  for row in cursor.fetchall():
    if row:
      np=row[0]
      fe=row[1]
      return np,fe

def inserir_orden(npedido,norden):
   conn = sqlite3.connect('gestion.db')
   with conn:
      cursor = conn.cursor()
      cursor.execute('INSERT INTO Orden(Npedido,Norden) VALUES(?,?)',(npedido,norden))     

def existe_orden(npedido,norden):
   conn = sqlite3.connect('gestion.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM Orden WHERE (Npedido=(?) AND Norden=(?))',(npedido,norden))
   for row in cursor.fetchall():
      if row:
        np=row[0]
        no=row[1]
        return np,no

def inserir_sollado(npedido,norden,codlote,calidad):
   conn = sqlite3.connect('gestion.db')
   with conn:
      cursor = conn.cursor()
      cursor.execute('INSERT INTO Sollado(Npedido,Norden,Codlote,Calidad) VALUES(?,?,?,?)',(npedido,norden,codlote,calidad))

def existe_sollado(npedido,norden,codlote,calidad):
   conn = sqlite3.connect('gestion.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM Sollado WHERE (Npedido=(?) AND Norden=(?) AND Codlote=(?) AND Calidad=(?))',(npedido,norden,codlote,calidad))
   for row in cursor.fetchall():
      if row:
        print(row)
        np=row[0]
        no=row[1]
        cl=row[2]
        ca=row[3]
        return np,no,cl,ca

def existe_linea(npedido,norden,codlote,calidad,tipocodbarras,codbarras):
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM LineaPedido WHERE (Npedido=(?) AND Norden=(?) AND Codlote=(?) AND Calidad=(?) AND TipoCodBarras=(?) AND CodBarras=(?))',(npedido,norden,codlote,calidad,tipocodbarras,codbarras))
    for row in cursor.fetchall():
      if row:
        print(row)
        np=row[8]
        no=row[9]
        cl=row[10]
        ca=row[11]
        tp=row[7]
        cb=row[1]
        return np,no,cl,ca,tp,cb

def inserir_codigobarras(npedido,norden,codlote,calidad,tipocodbarras,codbarras):
   conn = sqlite3.connect('gestion.db')
   with conn:
      print (len(codbarras))
      if tipocodbarras=="Automatic":
        if len(codbarras)==30:
          with conn:
              Largo = int(codbarras[8:11])
              Ancho = int(codbarras[11:14])
              Hojas = int(codbarras[14:16])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/ (100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==20:
           with conn:
            Largo = int(codbarras[10:13])
            Ancho = int(codbarras[13:15])
            Hojas = int(codbarras[8:10])
            M2= Largo * Ancho * Hojas / (10000)
            Ml=Largo*Hojas/ (100)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==14:
           with conn:
              codbarras=codbarras.replace(",",".")
              Largo = float(codbarras[6:9])
              Ancho = float(codbarras[10:14])
              Hojas = float(codbarras[3:5])
              M2= (Largo*100) * Ancho * Hojas / (10000)
              Ml=Largo*Hojas
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==22:
           with conn:
              Largo = float(codbarras[11:14])
              Ancho = float(codbarras[14:16])
              Hojas= float(codbarras[9:11])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==13:
            with conn:
              Largo = float(codbarras[7:10])
              Ancho = float(codbarras[11:13])
              Hojas = float(codbarras[5:7])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))       
        elif len(codbarras)==16:
            with conn:
              Largo = float(codbarras[8:11])
              Ancho = float(codbarras[11:14])
              Hojas = float(codbarras[14:16])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==11:
           with conn:
              Largo = float(codbarras[2:5])
              Ancho = float(codbarras[6:8])
              Hojas = float(codbarras[9:11])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==31:
           with conn:
              Largo = float(codbarras[23:26])
              Ancho = float(codbarras[26:29])
              Hojas = float(codbarras[29:31])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        elif len(codbarras)==18:
           with conn:
              Largo = float(codbarras[11:14])
              Ancho = float(codbarras[14:17])
              Hojas = float(codbarras[9:11])
              M2= Largo * Ancho * Hojas / (10000)
              Ml=Largo*Hojas/(100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Codbarras,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,codbarras,tipocodbarras,Largo,Ancho,Hojas,M2,Ml))
        else:
            msg="Código de barras erróneo !!!"
            print ("Código de barras erróneo !!! ") 
            return msg 
   conn.commit()
   conn.close()   
   
def inserir_codigobarrasmanual(npedido,norden,codlote,calidad,tipocodbarras,largo,ancho,hojas):
   conn = sqlite3.connect('gestion.db')
   with conn:
          if tipocodbarras=="Manual":
            with conn:
              print("ESTIC DINS DEL METODO")
              largo = float(largo)
              ancho = float(ancho)
              hojas = float(hojas)
              M2= largo * ancho * hojas / (10000)
              Ml=largo*hojas/ (100)
              cursor = conn.cursor()
              cursor.execute('INSERT INTO LineaPedido(Npedido,Norden,Codlote,Calidad,Tipocodbarras,Largo,Ancho,Hojas,M2,Ml) VALUES(?,?,?,?,?,?,?,?,?,?)',(npedido,norden,codlote,calidad,tipocodbarras,largo,ancho,hojas,M2,Ml))

def suma_M2(npedido,norden,codlote,calidad):
    conn=sqlite3.connect('gestion.db')
    with conn:
      cursor = conn.cursor()
      cursor.execute('SELECT sum(M2) FROM LineaPedido WHERE (Npedido=(?) AND Norden=(?) AND CodLote=(?) AND Calidad=(?))',(npedido,norden,codlote,calidad))
      for row in cursor.fetchall():
        if row:
          suma=row[0]
          print(suma)
        return round(suma, 2)

def suma_Ml(npedido,norden,codlote,calidad):
    conn=sqlite3.connect('gestion.db')
    with conn:
      cursor = conn.cursor()
      cursor.execute('SELECT sum(Ml) FROM LineaPedido WHERE (Npedido=(?) AND Norden=(?) AND CodLote=(?) AND Calidad=(?))',(npedido,norden,codlote,calidad))
      for row in cursor.fetchall():
        if row:
          suma=row[0]
          print(suma)
        return round(suma, 2)

def numero_paquetes(npedido,norden,codlote,calidad):
    conn=sqlite3.connect('gestion.db')
    with conn:
      cursor = conn.cursor()
      cursor.execute('SELECT count(*) FROM LineaPedido WHERE (Npedido=(?) AND Norden=(?) AND CodLote=(?) AND Calidad=(?))',(npedido,norden,codlote,calidad))
      for row in cursor.fetchall():
        if row:
          numpaq=row[0]
          print(numpaq)
        return numpaq

def pinta_linea():
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('SELECT max(Numlin) from LineaPedido')
    for row in cursor.fetchall():
      if row:
        nl=row
        print("ESTIC ASI!!!!!!HOLA")
        print(nl)  
    cursor.execute('SELECT * FROM LineaPedido WHERE (Numlin=(?))',(nl))
    for row in cursor.fetchall():
      if row:
        print("Estic aci...9,5!!")
        print(row)
        print("Estic aci...9.6!!!")
        nl=row[0]
        cb1=row[1]
        la=row[2]
        an=row[3]
        ho=row[4]
        me=row[5]
        print(nl)
        print(cb1)
        print(la)
        print(an) 
        print(me)
        print("estic aci.. 9.7")
        return nl,cb1,la,an,ho,me

def pinta_linea_manual():
   conn = sqlite3.connect('gestion.db')
   with conn:
     cursor = conn.cursor()
     cursor.execute('SELECT max(Numlin) FROM LineaPedido')
     for row in cursor.fetchall():
      if row:
        nl=row
        print("ESTIC ASI!!!!!!HOLA")
        print(nl)
     cursor.execute('SELECT * FROM LineaPedido WHERE (Numlin=(?))',(nl))
     for row in cursor.fetchall():
      if row:
        print("Estic aci...9,5!!")
        print(row)
        print("Estic aci...9.6!!!")
        nl=row[0]
        la=row[2]
        an=row[3]
        ho=row[4]
        me=row[5]
        print(nl)
        print(la)
        print(an) 
        print(ho)
        print(me)
        print("estic aci.. 9.7")
        return nl,la,an,ho,me

def elimina_linea(numlinb):
    conn = sqlite3.connect('gestion.db')
    with conn:
      cursor = conn.cursor()
      cursor.execute('DELETE FROM LineaPedido WHERE (Numlin=(?))',(numlinb,))

def shutdown_server():
     func = request.environ.get('werkzeug.server.shutdown')
     if func is None:
         raise RuntimeError('Not running with the Werkzeug Server')
     func()

def inserir_stock(codlote,fecha,familia,nombrechapa,fsc,nombrebotanico,pais,m2entrada,proveedor,precio,anotaciones):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Stocks(Codlote,Fecha,Familia,Nombrechapa,Fsc,Nombrebotanico,Pais,M2entrada,Proveedor,Precio,Anotaciones) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(codlote,fecha,familia,nombrechapa,fsc,nombrebotanico,pais,m2entrada,proveedor,precio,anotaciones))
  conn.commit()

def existe_stock(codlote):
  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Stocks WHERE Codlote = (?)',(codlote,))
  for row in cursor.fetchall():
    if row:
      cl=row[0]
      fe=row[1]
      fa=row[2]
      nc=row[3]
      fsc=row[4]
      nb=row[5]
      pa=row[6]
      m2e=row[7]
      pro=row[8]
      pre=row[9]
      ano=row[10]
      return cl,fe,fa,nc,fsc,nb,pa,m2e,pro,pre,ano

def metodo_ultimo_stock():
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('SELECT max(Codlote) from Stocks')
    for row in cursor.fetchall():
      if row:
        ns=row[0]
        return ns+1

def insertar_bobinas(norden,codigobobina,fecha,noperario,largo,ancho,especie,calidad,zizu,ubicacion):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    Largo=int(largo)
    Ancho=int(ancho)
    M2=(Largo*Ancho)/1000
    cursor.execute('INSERT INTO Bobinas(Norden,Codigobobina,Fecha,Noperario,Largo,Ancho,M2,Especie,Calidad,Zizu,Ubicacion) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(norden,codigobobina,fecha,noperario,largo,ancho,M2,especie,calidad,zizu,ubicacion))

  conn.commit()

def insertar_acabados_bobinas(norden,codigobobina,soporte,cola,lijado,natural,calibrado,primer,barnizado,alistonado,atraves):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    if soporte:
      cursor.execute('UPDATE Bobinas SET Soporte=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(soporte,norden,codigobobina))
    if cola:
      cursor.execute('UPDATE Bobinas SET Cola=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(cola,norden,codigobobina))
    if lijado:
      cursor.execute('UPDATE Bobinas SET Lijado=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(lijado,norden,codigobobina))
    if natural:
      cursor.execute('UPDATE Bobinas SET Natural=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(natural,norden,codigobobina))
    if calibrado:
      cursor.execute('UPDATE Bobinas SET Calibrado=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(calibrado,norden,codigobobina))
    if primer:
      cursor.execute('UPDATE Bobinas SET Primer=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(primer,norden,codigobobina))
    if barnizado:
      cursor.execute('UPDATE Bobinas SET Barnizado=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(barnizado,norden,codigobobina))
    if alistonado:
      cursor.execute('UPDATE Bobinas SET Alistonado=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(alistonado,norden,codigobobina))
    if atraves:
      cursor.execute('UPDATE Bobinas SET Atraves=(?) WHERE (Norden=(?) AND Codigobobina=(?))',(atraves,norden,codigobobina))

  conn.commit()

def insertar_corte(codigobobina,norden,fecha,noperario,rollos,acabado,largo,ancho,especie,ubicacion):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    Rollos=int(rollos)
    Largo=int(largo)
    Ancho=int(ancho)
    M2=Rollos*((Largo*Ancho)/1000)
    cursor.execute('INSERT INTO Corte(Codigobobina,Norden,Fecha,Noperario,Rollos,Acabado,Largo,Ancho,M2,Especie,Ubicacion) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(codigobobina,norden,fecha,noperario,rollos,acabado,largo,ancho,M2,especie,ubicacion))
  conn.commit()

def genera_codi(norden,lineasbobina):
    if len(lineasbobina)==0:
        return norden+'B'+'1'
    else:
        num=[]
        for e in lineasbobina :
            _,b=e[0].split('B')
            num.append(int(b))
        nou_num=max(num)+1
        nou_num=str(nou_num)
        return norden+'B'+nou_num

def insertar_prensa(norden,fecha,noperario,codigobobina,codigoprensa):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Prensa(Norden,Fecha,Noperario,Codigobobina,Codigoprensa)  VALUES (?,?,?,?,?)',(norden,fecha,noperario,codigobobina,codigoprensa ))
  conn.commit()

def update_unodecorte(codigobobina):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('UPDATE Bobinas SET  Cortada=1  WHERE (Codigobobina=(?))',(codigobobina,))
  conn.commit()

def update_unodecorteprens(codigobobina):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('UPDATE Prensa SET  Cortada=1  WHERE (Codigoprensa=(?))',(codigobobina,))
  conn.commit()

def update_unodeprensa(codigobobina):
  conn = sqlite3.connect('gestion.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('UPDATE Bobinas SET  Prensada=1  WHERE (Codigobobina=(?))',(codigobobina,))
  conn.commit()


def insertar_ordenes(norden,fecha,espessor,ncliente,refclte,nrollos,mlrollo,mltotal,ancho,especie,acabado,comentario,totalordenes):
  conn = sqlite3.connect('ordenes.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Ordenes(Norden,Fecha,Espessor,Ncliente,Refclte,Nrollos,Mlrollos,Mltotal,Ancho,Especie,Acabado,Comentario,Totalordenes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(norden,fecha,espessor,ncliente,refclte,nrollos,mlrollo,mltotal,ancho,especie,acabado,comentario,totalordenes))
  conn.commit()


def saber_cliente(ncliente):
  conn = sqlite3.connect('ordenes.db')
  with conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Clientes WHERE (Ncliente=(?))',(ncliente,))
    for row in cursor.fetchall():
      if row:
        refcliente=row[1]
        comentario=row[2]
        return refcliente,comentario
  conn.commit()


@app.route('/',methods=['GET', 'POST'])
def indice():
  return render_template ("indice.html")

@app.route('/consulta_pedido',methods=['GET', 'POST'])
def consulta_pedido():
  np=""
  fecha=""
  ordenes=[]
  sollados=[]
  lineas=[]

  if len(request.form) == 1:
    np=request.form['Npedido']

  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Pedido WHERE Npedido = (?)',(np,))
  for row in cursor.fetchall():
    if row:
      fecha=row[1]
  
  cursor.execute('SELECT Norden FROM Orden WHERE Npedido=(?)', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      ordenes.append(row[0])
  print(ordenes)
 
  cursor.execute('SELECT Norden,Codlote,Calidad FROM Sollado WHERE Npedido=(?)', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      sollados.append(row)
  print(sollados)

  cursor.execute('SELECT Norden,CodLote,Calidad,Numlin,CodBarras,Largo,Ancho,Hojas,M2,Ml FROM LineaPedido WHERE Npedido=(?)', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      print(row[0:4])
      lineas.append(row)
  print(lineas)

  return render_template ("consulta_pedido.html",npedido=np,fecha=fecha,ordenes=ordenes,sollados=sollados,lineas=lineas)   

@app.route('/consulta_orden',methods=['GET', 'POST'])
def consulta_orden():
  np=request.form['Npedido']
  no=""
  fecha=""
  ordenes=[]
  sollados=[]
  lineas=[]
  lineasbobina=[]
  lineascorte=[]

  if len(request.form) == 3:
    no=request.form['Norden']

  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Pedido WHERE Npedido = (?)',(np,))
  for row in cursor.fetchall():
    if row:
      fecha=row[1] 
  
  cursor.execute('SELECT Norden FROM Orden WHERE Npedido=(?) ', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      ordenes.append(row[0])
  print(ordenes)

  cursor.execute('SELECT Norden,Codlote,Calidad FROM Sollado WHERE Npedido=(?)', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      sollados.append(row)
  print(sollados)

  cursor.execute('SELECT Norden,CodLote,Calidad,Numlin,CodBarras,Largo,Ancho,Hojas,M2,Ml FROM LineaPedido WHERE Norden=(?)', (no,))
  for row in cursor.fetchall():
    if row:
      print(row)
      print(row[0:4])
      lineas.append(row)
  print(lineas)

  cursor.execute('SELECT * From Bobinas Where Norden=(?)',(no,))
  for row in cursor.fetchall():
    if row:
      print(row)
      lineasbobina.append(row)
  print(lineasbobina)

  cursor.execute('SELECT * From Corte Where Norden=(?)',(no,))
  for row in cursor.fetchall():
    if row:
      print(row)
      lineascorte.append(row)
  print(lineascorte)

  return render_template ("consulta_orden.html",npedido=np,fecha=fecha,ordenes=ordenes,sollados=sollados,lineas=lineas,norden=no, lineasbobina=lineasbobina, lineascorte=lineascorte)  

@app.route('/pedido',methods=['GET', 'POST'])
def pedido():
  np=None
  fe=""
  msg=""
  print(request.form)
  if request.form:
    try:
      np=request.form['Npedido']
      fe=time.strftime("%d/%m/%y")
      inserir_pedido(np,fe)
      msg="Nuevo Pedido"
    except:
      np,fe=existe_pedido(request.form['Npedido'])
      msg="Pedido Existente"
  return render_template ("pedido.html",npedido=np,fecha=fe,msg=msg)

@app.route('/orden',methods=['GET', 'POST'])
def orden():
  np=request.form['Npedido']
  no=""
  msg=""
  fe=request.form['Fecha']
  if len(request.form)==4:
    print(request.form)
    try:
      print("Estic aci...2")
      no=request.form['Norden']
      inserir_orden(np,no)
      print(request.form)
      msg="Nueva Orden"
    except:
      print("Estic aci...3")
      np,no=existe_orden(np,request.form['Norden'])
      msg="Orden Existente"
  else:
    print("Form incomplet")
  return render_template ("orden.html",npedido=np,fecha=fe,norden=no,msg=msg)

@app.route('/sollado',methods=['GET', 'POST'])
def sollado():
  np=request.form['Npedido']
  no=request.form['Norden']
  cl=""
  ca=""
  msg=""
  fe=request.form['Fecha']
  if len(request.form)==6:
    print(request.form)
    try:
      print("Estic aci...2")
      cl=request.form['CodLote']
      ca=request.form['Calidad']
      print("estic en 2.1")
      print(cl)
      print(ca)
      inserir_sollado(np,no,cl,ca)
      print(request.form)
      msg="Nuevo Sollado"
    except:
      print("Estic aci...3")
      np,no,cl,ca=existe_sollado(np,no,request.form['CodLote'],request.form['Calidad'])
      msg="Sollado Existente"
  else:
    print("Form incomplet")
  return render_template ("sollado.html",npedido=np,norden=no,codlote=cl,calidad=ca,fecha=fe,msg=msg)

@app.route('/lineapedido',methods=['GET', 'POST'])
def lineapedido():
  msg=""
  np=request.form['Npedido']
  no=request.form['Norden']
  fe=request.form['Fecha']
  cl=request.form['CodLote']
  ca=request.form['Calidad']
  tp=""
  cb=""
  sumam=""
  sumal=""
  numpaq=""
  nl=""
  cb1=""
  la=""
  an=""
  ho=""
  me=""
  numb=""
  numlinb=""
  print("Estic aci...4")
  print(request.form)
  print(len(request.form))
  if len(request.form)==20:
    if request.form['TipoCodBarras']=="Manual":
      print("ESTIC EN EL 7")
      tp=request.form['TipoCodBarras']
      cb=request.form['CodBarras']
      la=request.form['Largo']
      an=request.form['Ancho']
      ho=request.form['Hojas']
      inserir_codigobarrasmanual(np,no,cl,ca,tp,la,an,ho)
      sumam=suma_M2(np,no,cl,ca)
      sumal=suma_Ml(np,no,cl,ca)
      numpaq=numero_paquetes(np,no,cl,ca)
      print(sumam)
      print("ESTIC EN EL 8")
      nl,la,an,ho,me=pinta_linea_manual()
    elif len(request.form['CodBarras'])>0:
      try:
        print("Estic aci...5")
        tp=request.form['TipoCodBarras']
        cb=request.form['CodBarras']
        msg=inserir_codigobarras(np,no,cl,ca,tp,cb)
        print("Estic aci...6")
        if(msg==None):
          sumam=suma_M2(np,no,cl,ca)
          sumal=suma_Ml(np,no,cl,ca)
          numpaq=numero_paquetes(np,no,cl,ca)
          print("Estic aci...9")
          nl,cb1,la,an,ho,me=pinta_linea()
          print("Estic aci...10")
          print(nl)
          print(cb1)
          print(la)
          print(an) 
          print(me)
          print("Estic asi...11")
      except:
          print("Estic aci ...33")
          np,no,cl,ca,tp,cb=existe_linea(np,no,cl,ca,request.form['TipoCodBarras'],request.form['CodBarras'].replace(",","."))
          msg="Paquete Repetido"
    elif len(request.form['NumLinB'])>0:
      numlinb=request.form['NumLinB']
      print("ESTIC DINS BORRANT")
      print('numlinb:',numlinb)
      elimina_linea(numlinb)
      print("JA HE BORRAT")
  return render_template ("lineapedido.html",msg=msg,npedido=np,norden=no,codlote=cl,calidad=ca,fecha=fe,resultado=sumam,resultado1=sumal,numpaq=numpaq,numlin1=nl,codbarras1=cb1,largo1=la,ancho1=an,hojas1=ho,m21=me)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    salida="Aplicación Finalizada."
    return salida

@app.route('/copia', methods=['POST'])
def copia():
  msg=""
  onestic=os.getcwd()
  print (onestic)
  kko=onestic+"\\"+"gestion.db"
  print (kko)
  if os.path.exists(kko):
    fitxer_actual,_="gestion.db".split(".")
    print(fitxer_actual)
    fecha=datetime.datetime.now().strftime("%d_%m_%y_%H_%M")
    fitxer_copia=fitxer_actual+fecha+".db"
    print (fitxer_copia)
    kkd=onestic+"\\"+"CPBDA"+"\\"+fitxer_copia
    print(kkd)
    os.system("COPY %s %s" % (kko,kkd))
    print("Copia de la base de datos realizada...")
    msg="Copia de la base de datos realizada..."
  return render_template ("copia.html", msg=msg)

@app.route('/stock',methods=['GET', 'POST'])
def stock():
  cl=None
  fe=""
  fa=""
  nc=""
  msg=""
  fsc=""
  nb=""
  pa=""
  m2e=""
  m2r=""
  pro=""
  pre=""
  ano=""
  ns=""
  print(request.form)
  if request.form:
    try:
      ns=metodo_ultimo_stock()
      cl=ns
      fe=time.strftime("%d/%m/%y")
      fa=request.form['Familia']
      nc=request.form['Nombrechapa']
      fsc=request.form['Fsc']
      nb=request.form['Nombrebotanico']
      pa=request.form['Pais']
      m2e=request.form['M2entrada']
      pro=request.form['Proveedor']
      pre=request.form['Precio']
      ano=request.form['Anotaciones']
      pre=pre.replace(",",".")
      m2e=m2e.replace(",",".")
      inserir_stock(cl,fe,fa,nc,fsc,nb,pa,m2e,pro,pre,ano)
      msg="NuevoSollado"
    except:
      cl,fe,fa,nc,fsc,nb,pa,m2e,pro,pre,ano=existe_stock(request.form['Codlote'])
      msg="SolladoExistente"
  return render_template ("stock.html",codlote=cl,fecha=fe,familia=fa,nombrechapa=nc,fsc=fsc,nombrebotanico=nb,pais=pa,m2entrada=m2e,proveedor=pro,precio=pre,anotaciones=ano,msg=msg)

@app.route('/consulta_stock',methods=['GET', 'POST'])
def consulta_stock():
  cl=""
  fe=""
  nc=""
  m2e=""
  pre=""
  arestar=""
  re=""
  cantidad=""
  fsc=""
  lineas=[]
  msg=""
  if len(request.form) == 1:
    cl=request.form['Codlote']
    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Stocks WHERE Codlote = (?)',(cl,))
      for row in cursor.fetchall():
        if row:
          fe=row[1]
          nc=row[3]
          m2e=row[7]
          pre=row[9]
          fsc=row[4]

      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT sum(M2) FROM LineaPedido WHERE CodLote= (?)',(cl,))
      for row in cursor.fetchall():
        if row:
          arestar=row[0]
          print("arestar: ",arestar)
          arestar=float(arestar)
          
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT M2entrada FROM Stocks WHERE CodLote= (?)',(cl,))
      for row in cursor.fetchall():
        if row:
          cantidad=row[0]
          print("cantidad:",cantidad)
          cantidad=cantidad.replace(",",".")
          cantidad=float(cantidad)
          
          re=cantidad-arestar

      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()  
      cursor.execute('SELECT Npedido,Norden,sum(M2) FROM LineaPedido WHERE Codlote=(?) GROUP BY Npedido,Norden',(cl,))
      for row in cursor.fetchall():
        if row:
          lineas.append(row)
    except:
      if arestar==None and len(fe)>0:
        msg="SolladoNoGastado"
      else:
        msg="SolladoNoExistente"
  return render_template ("consulta_stock.html", codlote=cl, fecha=fe,nombrechapa=nc,m2entrada=m2e,precio=pre,resto=re,lineas=lineas,fsc=fsc,msg=msg)

@app.route('/etiqueta_stock',methods=['GET', 'POST'])
def etiqueta_stock():
  cl=""
  fe=""
  nc=""
  m2e=""
  pre=""
  arestar=""
  re=""
  cantidad=""
  fsc=""
  lineas=[]
  eti1=[]
  nomimg=""
  if len(request.form) == 1:
    cl=request.form['Codlote']
    nomimg= genera_codibarra(cl)

    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Stocks WHERE Codlote = (?)',(cl,))
    for row in cursor.fetchall():
      if row:
        fe=row[1]
        nc=row[3]
        m2e=row[7]
        pre=row[9]
        fsc=row[4]
        pro=row[8]

  return render_template ("etiqueta_stock.html", codlote=cl, fecha=fe,nombrechapa=nc,m2entrada=m2e,precio=pre,resto=re,fsc=fsc,proveedor=pro,nomimg=nomimg)

@app.route('/consulta_stock_general',methods=['GET', 'POST'])
def consulta_stock_general():
  lineas=[]
  lineassol=[]
  lineasfsc=[]
  lineasfam=[]
  lineaspre=[]
  lineasfech=[]
  cl=None
  fam=None
  fsc=None
  pre=None
  fe=None
  fe1=None
  if len(request.form['Codlote'])>0:
    cl=request.form['Codlote']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * From Stocks Where Codlote >=(?)',(cl,))
    for row in cursor.fetchall():
      if row:
        lineassol.append(row)
  elif len(request.form['Fsc'])>0:
    fsc=request.form['Fsc']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Stocks where Fsc=(?)',(fsc,))
    for row in cursor.fetchall():
      if row:
        lineasfsc.append(row)
  elif len(request.form['Familia'])>0:
    fam=request.form['Familia']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Stocks where Familia=(?)',(fam,))
    for row in cursor.fetchall():
      if row:
        lineasfam.append(row)
  elif len(request.form['Precio'])>0:
    pre=request.form['Precio']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    if request.form['Signo']==">":
      cursor.execute('SELECT * FROM Stocks where Precio>=(?)',(pre,))
      for row in cursor.fetchall():
        if row:
          lineasfam.append(row)
    else:
      cursor.execute('SELECT * FROM Stocks where Precio<=(?)',(pre,))
      for row in cursor.fetchall():
        if row:
          lineasfam.append(row)
  elif len(request.form['Fecha'])>0:
    fe=request.form['Fecha']
    fe1=request.form['Fecha1']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Stocks where Fecha BETWEEN (?) AND (?)',(fe,fe1))
    for row in cursor.fetchall():
      if row:
        lineasfech.append(row)
  else:  
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM Stocks')
    for row in cursor.fetchall():
      if row:
        lineas.append(row)

  return render_template ("consulta_stock_general.html", lineas=lineas,lineassol=lineassol,lineasfsc=lineasfsc,lineasfam=lineasfam,lineaspre=lineaspre,lineasfech=lineasfech)

@app.route('/bobinas',methods=['GET', 'POST'])
def bobinas():
  no=None
  fe=""
  nop=""
  lar=""
  anch=""
  esp=""
  cal=""
  ubi=""
  zi=""
  codb=""
  numero=""
  lineasbobina=[]
  lineas=[]
  nor1=""
  codbobin1=""
  largo1=""
  ancho1=""
  m21=""
  especie1=""
  calidad1=""
  print(request.form)
  if request.form:
    no=request.form['Norden']

    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Codigobobina FROM Bobinas WHERE Norden = (?)',(no,))
    for row in cursor.fetchall():
      if row:
        lineasbobina.append(row)

    print("yee que vaig a pintar ATENTO:")
    print(lineasbobina)
    numero=genera_codi(no,lineasbobina)
    codb=numero
    fe=time.strftime("%d/%m/%y")
    nop=request.form['Noperario']
    lar=request.form['Largo']
    anch=request.form['Ancho']
    esp=request.form['Especie']
    cal=request.form['Calidad']
    zi=request.form['Zizu']
    ubi=request.form['Ubicacion']   
    insertar_bobinas(no,codb,fe,nop,lar,anch,esp,cal,zi,ubi)

    cursor.execute('SELECT * FROM Bobinas WHERE (Norden=(?))',(no,))
    for row in cursor.fetchall():
      if row:
        nor1=row[2]
        codbobin1=row[1]
        largo1=row[5]
        ancho1=row[6]
        m21=row[7]
        especie1=row[8]
        calidad1=row[9]
        lineas.append(row)

  return render_template ("bobinas.html", norden=no,fecha=fe,noperario=nop,largo=lar,ancho=anch,especie=esp,calidad=cal,zizu=zi,ubicacion=ubi,codigobobina=codb,lineas=lineas,nor1=nor1,codbobin1=codbobin1,largo1=largo1,m21=m21,especie1=especie1,calidad1=calidad1)

@app.route('/etiqueta_bobinas',methods=['GET', 'POST'])
def etiqueta_bobinas():

  no=None
  lineasbobina=[]
  codb=""
  nomimg=""
  no=request.form['Norden']

  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT Codigobobina FROM Bobinas WHERE Norden = (?)',(no,))
  for row in cursor.fetchall():
    if row:
      lineasbobina.append(row)

  numero=genera_codi(no,lineasbobina)
  codb=numero
  nomimg= genera_codibarraBobina(codb)
  fe=request.form['Fecha']
  nop=request.form['Noperario']
  lar=request.form['Largo']
  anch=request.form['Ancho']
  esp=request.form['Especie']
  cal=request.form['Calidad']
  ubi=request.form['Ubicacion']
  
  return render_template ("etiqueta_bobinas.html",norden=no,codigobobina=codb,fecha=fe,noperario=nop,largo=lar,ancho=anch,especie=esp,calidad=cal,ubicacion=ubi,nomimg=nomimg)

@app.route('/consulta_bobinas',methods=['GET', 'POST'])
def consulta_bobinas():
  no=""
  lineas=[]
  msg=""
  if len(request.form) == 1:
    no=request.form['Norden']
    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Bobinas WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineas.append(row)
    except:
      msg="OrdenNoExistente"

  return render_template ("consulta_bobinas.html",norden=no, msg=msg, lineas=lineas)

@app.route('/consulta_general_orden',methods=['GET', 'POST'])
def consulta_general_orden():
  no=""
  lineasorden=[]
  lineasbobina=[]
  lineascorte=[]
  lineasprensa=[]
  msg=""
  msg1=""
  msg3=""
  msg4=""
  if len(request.form) == 1:
    no=request.form['Norden']
    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM LineaPedido WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineasorden.append(row)
          msg="Orden en Guillotina"
    except:
      msg="Orden No Gastada en Guillotina"

    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Bobinas WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineasbobina.append(row)
          msg1="Orden en Bobinas"
    except:
      msg1="Orden No Gastada En Bobinas"

    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Corte WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineascorte.append(row)
          msg3="Orden en Cortes"
    except:
      msg3="Orden No Gastada En Cortes"

    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Prensa WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineasprensa.append(row)
          msg4="Orden en Prensa"
    except:
      msg3="Orden No Gastada En Prensa"

  return render_template ("consulta_general_orden.html",norden=no, msg=msg, msg1=msg1, msg3=msg3,msg4=msg4,lineasorden=lineasorden,lineasbobina=lineasbobina,lineascorte=lineascorte,lineasprensa=lineasprensa)

@app.route('/acabados_bobinas',methods=['GET', 'POST'])
def acabados_bobinas():
  no=""
  cdb=None
  sop=""
  col=""
  lij=""
  nat=""
  cal=""
  pri=""
  bar=""
  ali=""
  atra=""
  msg=""
  print(request.form)
  if request.form:
      cdb=request.form['Codigobobina']
      no=cdb[0:8]
      sop=request.form['Soporte']
      lij=request.form['Lijado']
      col=request.form['Cola']
      nat=request.form['Natural']
      cal=request.form['Calibrado']
      pri=request.form['Primer']
      bar=request.form['Barnizado']
      ali=request.form['Alistonado']
      atra=request.form['Atraves']
      insertar_acabados_bobinas(no,cdb,sop,col,lij,nat,cal,pri,bar,ali,atra)

  return render_template ("acabados_bobinas.html",norden=no,codigobobina=cdb,soporte=sop,lijado=lij,cola=col,natural=nat,calibrado=cal,primer=pri,barnizado=bar,alistonado=ali,atraves=atra,msg=msg)

@app.route('/corte',methods=['GET', 'POST'])
def corte():
  codb=None
  no=""
  fe=""
  nop=""
  ro=""
  aca=""
  lar=""
  anch=""
  esp=""
  cal=""
  ubi=""
  lineas=[]
  
  print(request.form)
  if request.form:
    codb=request.form['Codigobobina']
    no=codb[0:8]
    fe=time.strftime("%d/%m/%y")
    nop=request.form['Noperario']
    ro=request.form['Rollos']
    aca=request.form['Acabado']
    lar=request.form['Largo']
    anch=request.form['Ancho']
    esp=request.form['Especie']
    ro=request.form['Rollos']
    ubi=request.form['Ubicacion']
   
    insertar_corte(codb,no,fe,nop,ro,aca,lar,anch,esp,ubi)
    if len(codb) >10:
      update_unodecorteprens(codb)
    else:
      update_unodecorte(codb)

    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Corte WHERE Codigobobina = (?)',(codb,))
    for row in cursor.fetchall():
      if row:
        lineas.append(row)

  return render_template ("corte.html",norden=no,codigobobina=codb,fecha=fe,noperario=nop,rollos=ro,acabado=aca,largo=lar,ancho=anch,especie=esp,ubicacion=ubi,lineas=lineas)

@app.route('/consulta_corte',methods=['GET', 'POST'])
def consulta_corte():
  codb=None
  lineas=[]
  msg=""
  if len(request.form) == 1:
    codb=request.form['Codigobobina']
    try:
      conn = sqlite3.connect('gestion.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Corte WHERE Codigobobina = (?)',(codb,))
      for row in cursor.fetchall():
        if row:
          lineas.append(row)
    except:
      msg="Bobina No Existente"
  return render_template ("consulta_corte.html",codigobobina=codb, msg=msg, lineas=lineas)

@app.route('/prensa',methods=['GET', 'POST'])
def prensa():
  no=None
  fe=""
  nop=""
  codb=""
  codpren=""
  lineas=[]
  print(request.form)
  if request.form:
    no=request.form['Norden']
    fe=time.strftime("%d/%m/%y")
    nop=request.form['Noperario']
    codpren=request.form['Codigoprensa']
    codb=request.form['Codigobobina']
    insertar_prensa(no,fe,nop,codb,codpren) 
    update_unodeprensa(codb)
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Prensa WHERE codigoprensa = (?)',(codpren,))
    for row in cursor.fetchall():
      if row:
        lineas.append(row)
    
  return render_template ("prensa.html",norden=no,fecha=fe,noperario=nop,codigoprensa=codpren,lineas=lineas)

@app.route('/stockbobinas',methods=['GET', 'POST'])
def stockbobinas():
  cb=""
  lineas=[]
  lineasbob=[]
  if request.form:
    cb=request.form['Codigobobina']
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * From Bobinas Where Codigobobina =(?)',(cb,))
    for row in cursor.fetchall():
      if row:
        lineasbob.append(row)
  else:
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()  
    cursor.execute('SELECT * FROM BOBINAS WHERE CORTADA is null AND PRENSADA is null ')
    for row in cursor.fetchall():
      if row:
        lineas.append(row)
  
  return render_template ("stockbobinas.html",lineas=lineas,lineasbob=lineasbob)

@app.route('/imprimeorden',methods=['GET', 'POST'])
def imprimeorden():
  np=request.form['Npedido']
  no=request.form['Norden']
  fecha=""
  ordenes=[]
  sollados=[]
  lineas=[]

  if len(request.form) == 3:
    no=request.form['Norden']

  conn = sqlite3.connect('gestion.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Pedido WHERE Npedido = (?)',(np,))
  for row in cursor.fetchall():
    if row:
      fecha=row[1]
  
  cursor.execute('SELECT Norden FROM Orden WHERE Npedido=(?) ', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      ordenes.append(row[0])
  print(ordenes)

  cursor.execute('SELECT Norden,Codlote,Calidad FROM Sollado WHERE Npedido=(?)', (np,))
  for row in cursor.fetchall():
    if row:
      print(row)
      sollados.append(row)
  print(sollados)

  cursor.execute('SELECT Norden,CodLote,Calidad,Numlin,CodBarras,Largo,Ancho,Hojas,M2,Ml FROM LineaPedido WHERE Norden=(?)', (no,))
  for row in cursor.fetchall():
    if row:
      print(row)
      print(row[0:4])
      lineas.append(row)
  print(lineas)

  return render_template ("imprimeorden.html",npedido=np,fecha=fecha,ordenes=ordenes,sollados=sollados,lineas=lineas,norden=no)  


@app.route('/ordenes',methods=['GET', 'POST'])
def ordenes():
  no=None
  fe=""
  ncli=""
  refclte=""
  nr=""
  mlr=""
  mlt=""
  anc=""
  esp=""
  aca=""
  com=""
  nomimg=""
  espe=""
  totor=""
  refcliente=""
  comentario=""
  print(request.form)
  if request.form:
    no=request.form['Norden']
    fe=time.strftime("%d/%m/%y")
    espe=request.form['Espessor']
    ncli=request.form['Ncliente']
    refcliente,comentario=saber_cliente(ncli)
    refclte=refcliente
    nr=request.form['Nrollos']
    mlr=request.form['Mlrollo']
    mlt=int(nr)*int(mlr)
    anc=request.form['Ancho']
    esp=request.form['Especie']
    totor=request.form['Totalordenes']
    aca=request.form['Acabado']
    com=comentario
    nomimg= genera_codibarra(no)
    insertar_ordenes(no,fe,espe,ncli,refclte,nr,mlr,mlt,anc,esp,aca,com,totor) 
    
  return render_template ("ordenes.html",norden=no,fecha=fe,espessor=espe,refclte=refclte,ncliente=ncli,nrollos=nr,mlrollo=mlr,mltotal=mlt,ancho=anc,especie=esp,totalordenes=totor,acabado=aca,comentario=com,nomimg=nomimg)

@app.route('/consulta_ordenes',methods=['GET', 'POST'])
def consulta_ordenes():
  no=""
  lineas=[]
  msg=""
  if len(request.form) == 1:
    no=request.form['Norden']
    try:
      conn = sqlite3.connect('ordenes.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM Ordenes WHERE Norden = (?)',(no,))
      for row in cursor.fetchall():
        if row:
          lineas.append(row)
    except:
      msg="OrdenNoExistente"

  return render_template ("consulta_ordenes.html",norden=no, msg=msg, lineas=lineas)

@app.route('/imprime_ordenes',methods=['GET', 'POST'])
def imprime_ordenes():
  no=request.form['Norden']
  fe=""
  ncli=""
  refclte=""
  nr=""
  mlr=""
  mlt=""
  anc=""
  esp=""
  totor=""
  aca=""
  com=""
  nomimg=""
  espe=""
  refcliente=""
  comentario=""
  nomimg=""
  lineas=[]
  if len(request.form) >0:
    no=request.form['Norden']
    nomimg= genera_codibarra(no)

    conn = sqlite3.connect('ordenes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ordenes WHERE Norden = (?)',(no,))
    for row in cursor.fetchall():
      if row:
        ncli=row[0]
        no=row[1]
        refclte=row[2]
        fe=row[3]
        nr=row[5]
        mlr=row[6]
        mlt=row[7]
        anc=row[8]
        esp=row[9]
        aca=row[10]
        espe=row[4]
        com=row[11]
        lineas.append(row)
     

  return render_template ("imprime_ordenes.html", norden=no,fecha=fe,espessor=espe,refclte=refclte,ncliente=ncli,nrollos=nr,mlrollo=mlr,mltotal=mlt,ancho=anc,especie=esp,totalordenes=totor,acabado=aca,comentario=com,nomimg=nomimg,lineas=lineas)

if __name__ == "__main__":
   app.run(debug=False, host="0.0.0.0")
