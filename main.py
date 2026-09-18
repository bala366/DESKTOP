import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3,csv,os,sys
from pathlib import Path
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

APP="Movimentação de Clientes Sabor do Campo"
DATA=Path(os.environ.get("LOCALAPPDATA",Path.home()))/"CasaraoDoCampo"
DB=DATA/"carteira.db"
PDF=Path.home()/"Downloads"/APP
DATA.mkdir(parents=True,exist_ok=True); PDF.mkdir(parents=True,exist_ok=True)
def resource(p):
    return Path(getattr(sys,"_MEIPASS",Path(__file__).parent))/p

class Banco:
 def __init__(self):
  self.c=sqlite3.connect(DB); self.c.execute("create table if not exists clientes(id integer primary key autoincrement,nome text,doc text,tel text)")
  self.c.execute("create table if not exists mov(id integer primary key autoincrement,cid integer,data text,tipo text,valor real,obs text)"); self.c.commit()
  if self.c.execute("select count(*) from clientes").fetchone()[0]==0:
   with open(resource("assets/clientes_258.csv"),encoding="utf-8-sig") as f:
    r=csv.reader(f); next(r,None)
    for x in r:
     while len(x)<4:x.append("")
     self.c.execute("insert into clientes(nome,doc,tel) values(?,?,?)",(x[1],x[2],x[3]))
   self.c.commit()
 def clientes(self): return self.c.execute("select id,nome,doc,tel from clientes order by nome").fetchall()
 def addmov(self,cid,t,v,o):
  try:v=float(v.replace(".","").replace(",",".") or 0)
  except:v=0
  self.c.execute("insert into mov(cid,data,tipo,valor,obs) values(?,?,?,?,?)",(cid,datetime.now().strftime("%d/%m/%Y %H:%M"),t,v,o));self.c.commit()
 def movs(self):
  return self.c.execute("select m.id,m.data,c.nome,m.tipo,m.valor,m.obs from mov m join clientes c on c.id=m.cid order by m.id desc").fetchall()
 def update(self,i,t,v,o):
  try:v=float(v.replace(".","").replace(",",".") or 0)
  except:v=0
  self.c.execute("update mov set tipo=?,valor=?,obs=? where id=?",(t,v,o,i));self.c.commit()
 def delete(self,i): self.c.execute("delete from mov where id=?",(i,));self.c.commit()

b=Banco(); tipos=["VENDA","NÃO COMPROU","VISITA","TROCA","DEVOLUÇÃO","PEDIDO","PEDIDO ENTREGUE","PEDIDO CANCELADO"]
root=tk.Tk();root.title("Carteira de Clientes - Casarão do Campo");root.geometry("1100x720");root.minsize(900,600)
style=ttk.Style();style.configure("TButton",padding=9,font=("Segoe UI",10,"bold"));style.configure("Treeview",rowheight=28)
top=tk.Frame(root,bg="#203d31",height=80);top.pack(fill="x");tk.Label(top,text="CASARÃO DO CAMPO  |  CARTEIRA DE CLIENTES",bg="#203d31",fg="white",font=("Segoe UI",20,"bold")).pack(pady=22)
nav=tk.Frame(root);nav.pack(fill="x",padx=12,pady=8); body=tk.Frame(root);body.pack(fill="both",expand=True,padx=12,pady=5)
def clear():
 for w in body.winfo_children():w.destroy()
def pdf(title,rows):
 fn=PDF/(title.replace(" ","_")+"_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".pdf")
 c=canvas.Canvas(str(fn),pagesize=A4);w,h=A4;y=h-55;c.setFont("Helvetica-Bold",15);c.drawString(35,y,"CASARAO DO CAMPO - "+title);y-=28;c.setFont("Helvetica",9)
 for row in rows:
  line=" | ".join(map(str,row))
  for i in range(0,len(line),105):
   if y<45:c.showPage();c.setFont("Helvetica",9);y=h-45
   c.drawString(35,y,line[i:i+105]);y-=14
 c.save();messagebox.showinfo("PDF GERADO",str(fn))
def dashboard():
 clear(); cs=len(b.clientes()); ms=b.movs()
 tk.Label(body,text=f"CLIENTES: {cs}     LANÇAMENTOS: {len(ms)}",font=("Segoe UI",22,"bold")).pack(pady=30)
 ttk.Button(body,text="GERAR PDF DO DASHBOARD",command=lambda:pdf("DASHBOARD",[("Clientes",cs),("Lançamentos",len(ms))])).pack()
def clientes():
 clear();q=tk.StringVar(); ttk.Entry(body,textvariable=q).pack(fill="x",pady=5)
 tree=ttk.Treeview(body,columns=("nome","doc","tel"),show="headings");[tree.heading(x,text=x.upper()) for x in ("nome","doc","tel")];tree.pack(fill="both",expand=True)
 def load(*_):
  tree.delete(*tree.get_children())
  for i,n,d,t in b.clientes():
   if q.get().lower() in (n+" "+d+" "+t).lower():tree.insert("",'end',iid=str(i),values=(n,d,t))
 q.trace_add("write",load);load()
 ttk.Button(body,text="GERAR PDF DA CARTEIRA COMPLETA",command=lambda:pdf("CARTEIRA COMPLETA",[(n,d,t) for _,n,d,t in b.clientes()])).pack(pady=8)
def movimento():
 clear();cs=b.clientes(); names=[x[1] for x in cs]; combo=ttk.Combobox(body,values=names,state="readonly");combo.pack(fill="x",pady=5);combo.current(0)
 tp=ttk.Combobox(body,values=tipos,state="readonly");tp.pack(fill="x",pady=5);tp.current(0)
 val=ttk.Entry(body);val.insert(0,"0,00");val.pack(fill="x",pady=5);obs=ttk.Entry(body);obs.pack(fill="x",pady=5)
 def save():
  b.addmov(cs[combo.current()][0],tp.get(),val.get(),obs.get());pdf("MOVIMENTO",[(datetime.now().strftime("%d/%m/%Y %H:%M"),combo.get(),tp.get(),val.get(),obs.get())]);messagebox.showinfo("Salvo","Lançamento salvo.")
 ttk.Button(body,text="SALVAR E GERAR PDF",command=save).pack(pady=10)
def historico():
 clear();tree=ttk.Treeview(body,columns=("data","cliente","tipo","valor","obs"),show="headings")
 for x in ("data","cliente","tipo","valor","obs"):tree.heading(x,text=x.upper())
 tree.pack(fill="both",expand=True)
 def load():
  tree.delete(*tree.get_children())
  for i,d,n,t,v,o in b.movs():tree.insert("",'end',iid=str(i),values=(d,n,t,f"{v:.2f}",o))
 load()
 def edit():
  sel=tree.selection()
  if not sel:return
  i=int(sel[0]); vals=tree.item(sel[0],"values"); win=tk.Toplevel(root);win.title("Editar lançamento");win.geometry("430x300")
  tp=ttk.Combobox(win,values=tipos,state="readonly");tp.set(vals[2]);tp.pack(fill="x",padx=15,pady=8)
  va=ttk.Entry(win);va.insert(0,vals[3].replace(".",","));va.pack(fill="x",padx=15,pady=8)
  ob=ttk.Entry(win);ob.insert(0,vals[4]);ob.pack(fill="x",padx=15,pady=8)
  def sv():b.update(i,tp.get(),va.get(),ob.get());win.destroy();load()
  def dl():
   if messagebox.askyesno("Excluir","Apagar este lançamento?"):b.delete(i);win.destroy();load()
  ttk.Button(win,text="SALVAR ALTERAÇÕES",command=sv).pack(pady=5);ttk.Button(win,text="EXCLUIR LANÇAMENTO",command=dl).pack(pady=5)
 ttk.Button(body,text="EDITAR / EXCLUIR SELECIONADO",command=edit).pack(side="left",pady=8)
 ttk.Button(body,text="GERAR PDF DO HISTÓRICO",command=lambda:pdf("HISTORICO",b.movs())).pack(side="right",pady=8)
def relatorios():
 clear()
 mp={"QUEM COMPROU":"VENDA","QUEM NÃO COMPROU":"NÃO COMPROU","VISITADOS":"VISITA","TROCAS":"TROCA","DEVOLUÇÕES":"DEVOLUÇÃO","PEDIDOS":"PEDIDO","PEDIDOS ENTREGUES":"PEDIDO ENTREGUE","PEDIDOS CANCELADOS":"PEDIDO CANCELADO"}
 def gen(r):
  if r=="CARTEIRA COMPLETA": rows=[(n,d,t) for _,n,d,t in b.clientes()]
  else:
   rows=b.movs(); typ=mp.get(r); rows=[x for x in rows if typ is None or x[3]==typ]
  pdf(r,rows)
 for r in ["RELATÓRIO DA SEMANA","QUEM COMPROU","QUEM NÃO COMPROU","VISITADOS","TROCAS","DEVOLUÇÕES","PEDIDOS","PEDIDOS ENTREGUES","PEDIDOS CANCELADOS","CARTEIRA COMPLETA"]:
  ttk.Button(body,text=r+" - GERAR PDF",command=lambda x=r:gen(x)).pack(fill="x",pady=4)
for text,cmd in [("DASHBOARD",dashboard),("CLIENTES",clientes),("MOVIMENTO",movimento),("HISTÓRICO",historico),("RELATÓRIOS PDF",relatorios)]:
 ttk.Button(nav,text=text,command=cmd).pack(side="left",expand=True,fill="x",padx=3)
dashboard();root.mainloop()
