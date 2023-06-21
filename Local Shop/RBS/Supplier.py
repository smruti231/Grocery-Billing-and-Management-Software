from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import random

class SupClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("--> Supplier Menu  ")
        self.root.config(bg="ivory3")
        self.icon_main=PhotoImage(file="images\supplier.png")
        self.root.iconphoto(False,self.icon_main)
        self.root.focus_force() 

        #all variables==============
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_id=StringVar()
        x = random.randint(100000, 999999)
        self.var_sup_id.set(str(x))

        
        self.var_name = StringVar()
        self.var_contact=StringVar()




        SearchFrame=LabelFrame(self.root,text="Search Supplier",font=("gordy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=545,y=65,width=500,height=70)

        #===option====
        cmd_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Name", "Supplier ID","Description"),state='readonly',justify=CENTER,font=("arial",12))
        cmd_search.place(x=10,y=7,width=140,height=28)
        cmd_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("groudy old style",15),bg="lightyellow").place(x=160,y=8,width=180)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("groudy old style",15),bg="lightgreen",cursor="hand2").place(x=350,y=9,width=120,height=28)
    

        

#=================options================================
        #lbl_Search=Label(self.root, text="Supplier ID", font=("goudy old style", 15), bg="ivory3")
        #lbl_Search.place(x=700,y=80)

        #txt_search=Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="seashell2").place(x=800, y=80,width=160)
        #btn_search=Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="cornflower blue", fg="white", cursor="hand2").place(x=980, y=79, width=100, height=28)
        
#======title======
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="tan4",fg="white").place(x=50,y=10,width=1000,height=40)

#====content============

       #===row1=======
        lbl_supplier_id=Label(self.root,text="Supplier ID",font=("goudy old style",15),bg="ivory3").place(x=50,y=80)
        txt_supplier_id = Entry(self.root, textvariable=self.var_sup_id, font=("goudy old style", 15),bg="seashell2").place(x=180, y=80, width=180)


        # ===row2=======
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="ivory3").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="seashell2").place(x=180, y=120, width=180)

        # ===row3=======
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="ivory3").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="seashell2").place(x=180, y=160, width=180)

        # ===row4=======
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="ivory3").place(x=50,y=200)
        self.txt_desc=Text(self.root, font=("goudy old style", 15), bg="seashell2")
        self.txt_desc.place(x=180, y=200, width=310, height=95)


#============buttons=====================
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="chartreuse4",fg="white",cursor="hand2").place(x=55,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="gold3",fg="white",cursor="hand2").place(x=175,y=370,width=110,height=35)
        btn_delete= Button(self.root,text="Delete",command=self.delete,font=("goudy old style", 15), bg="red3",fg="white",cursor="hand2").place (x=295,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="blue",fg="white",cursor="hand2").place(x=415,y=370,width=110,height=35)

#===tree view====
        
#===Supplier details=====

        emp_frame = Frame(self.root, bd=3,relief=RIDGE)  
        emp_frame.place(x=545, y=120, width=500, height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame, columns=("SupplierID", "name", "contact", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("SupplierID", text="Supplier ID")
        self.supplierTable.heading("name", text="NAME")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("description", text="Description")

        self.supplierTable["show"]= "headings"

        self.supplierTable.column("SupplierID", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("description", width=100)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.show()

        #===================================================================================================================================

    def add(self):                                              
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_sup_id.get()== "":
                messagebox.showerror("Error","Supplier ID is required",parent=self.root)
            else:
                cur.execute("select * from supplier where SupplierID=?", (self.var_sup_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Supplier ID already assigned,try diffrent",parent=self.root)
                else:
                    cur.execute("Insert into supplier(SupplierID,name,contact,desc) values(?,?,?,?)",(
                                                self.var_sup_id.get(),
                                                self.var_name.get(),
                                                self.var_contact.get(),
                                                self.txt_desc.get('1.0', END),

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            cur.execute("select * from Supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=self.supplierTable.item((f))
        row=content['values']
        #print(row)
        self.var_sup_id.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])


    def update(self):                                              
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_sup_id.get()== "":
                messagebox.showerror("Error","Supplier ID is required",parent=self.root)
            else:
                cur.execute("select * from supplier where SupplierID=?", (self.var_sup_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Invalid Supplier ID ",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where SupplierID=? ",(
                                                self.var_name.get(),
                                                self.var_contact.get(),
                                                self.txt_desc.get('1.0', END),
                                                self.var_sup_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def delete(self):
         con = sqlite3.connect(database=r'BSW.db')
         cur = con.cursor()
         try:
             if self.var_sup_id.get() == "":
                 messagebox.showerror("Error", "Supplier ID is required", parent=self.root)
             else:
                 cur.execute("select * from supplier where SupplierID=?", (self.var_sup_id.get(),))
                 row = cur.fetchone()
                 if row == None:
                     messagebox.showerror("Invalid Supplier ID",parent=self.root)
                 else:
                     op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                     if op==True:
                         cur.execute("delete from supplier where Supplier ID=?", (self.var_sup_id.get(),))
                         con.commit()
                         messagebox.showinfo("Delete", "Supplier Deleted  Successfully", parent=self.root)
                         self.clear()


         except Exception as ex:
             messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_id.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END,""),
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()


    def search(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by Option",parent=self.root) 
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Select input is required",parent=self.root)
            elif self.var_searchby.get()=="Supplier ID":
                cur.execute("select * from supplier where SupplierID LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
            elif self.var_searchby.get()=="Description":
                cur.execute("select * from supplier where desc LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
            else:
                cur.execute("select * from supplier where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



if __name__=="__main__":
    root = Tk()
    obj = SupClass(root)
    root.mainloop()
