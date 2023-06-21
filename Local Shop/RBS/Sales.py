from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class SalClass:
    def __init__(self,root,productFrame=None):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("--> Sales Menu  ")
        self.root.config(bg="ivory3")
        self.icon_main=PhotoImage(file="images\sales.png")
        self.root.iconphoto(False,self.icon_main)
        self.root.focus_force()

        self.bill_list=[]
        self.var_billNo=StringVar()

        #=====title=====
        lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",30),bg="tan4",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_bill=Label(self.root,text="Bill No.",font=("times new roman",15),bg="ivory3").place(x=50,y=100)

        txt_bill=Entry(self.root,textvariable=self.var_billNo,font=("times new roman",15),bg="seashell2").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="cornflower blue",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="gold",cursor="hand2").place(x=490,y=100,width=120,height=28)

        
        #===BILL LIST===
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="ivory2",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #===BILL AREA===
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)

        lbl_title2=Label(bill_Frame,text="Customer Bills Details",font=("goudy old style",20),bg="burlywood3").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="ivory2",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #====Image========
        self.bill_photo=Image.open("images\cat2.jpg")
        self.bill_photo=self.bill_photo.resize((430,360),Image.Resampling.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=110)

        self.show()

#===================================
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir('Bill Reports'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        #print(file_name)
        self.bill_area.delete('1.0',END)         #string indexing
        fp=open(f'Bill Reports/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_billNo.get()=="":
            messagebox.showerror("Error","Bill no. should be required",parent=self.root)
        else:
            if self.var_billNo.get() in self.bill_list:
                fp=open(f'bill/{self.var_billNo.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Bill No.",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)


if __name__=="__main__":
    root=Tk()
    obj=SalClass(root)
    root.mainloop()
