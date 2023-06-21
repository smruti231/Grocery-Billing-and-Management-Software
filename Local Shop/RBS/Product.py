from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class PrdClass:
    def __init__(self,root,productFrame=None):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("--> Product Menu  ")
        self.root.config(bg="ivory3")
        self.icon_main=PhotoImage(file="images\product.png")
        self.root.iconphoto(False,self.icon_main)
        self.root.focus_force()
        #======================
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="ivory3")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #======title======
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="tan4",fg="white").pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="ivory3").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="ivory3").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="ProdName",font=("goudy old style",18),bg="ivory3").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="ivory3").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="ivory3").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="ivory3").place(x=30,y=310)


        #===column2====
        cmb_cat = ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style", 15))
        cmb_cat.place(x=150,y=65,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style", 15))
        cmb_sup.place(x=150,y=115,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg='seashell2').place(x=150,y=165,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg='seashell2').place(x=150,y=215,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg='seashell2').place(x=150,y=265,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style", 15))
        cmb_status.place(x=150,y=315,width=200)
        cmb_status.current(0)

        #============buttons=====================
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="chartreuse4",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="gold3",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete= Button(product_Frame,command=self.delete,text="Delete",font=("goudy old style", 15), bg="red3",fg="white",cursor="hand2").place (x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="blue",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)


        #=============search frame=======================
        searchFrame=LabelFrame(self.root,text="Search",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="ivory3")
        searchFrame.place(x=480,y=1,width=600,height=70)

#=================options================================
        cmb_Search=ttk.Combobox(searchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_Search.place(x=10,y=10,width=180)
        cmb_Search.current(0)

#for search we have 2 fields txt and entry entry for single data is used
        txt_search=Entry(searchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="seashell2").place(x=200,y=10)
        btn_search=Button(searchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="cornflower blue",fg="white",cursor="hand2").place(x=410,y=10,width=150,height=30)


        #===tree view====
#tree view it is a pre built class in python which helps us to show data in from database one type of list it is very effective as it
#displays all the information in tabular manner

#===Product details=====

        p_frame = Frame(self.root, bd=3,relief=RIDGE)   
        p_frame.place(x=480,y=80,width=600,height=410)
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.Product_Table=ttk.Treeview(p_frame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)  #tupple banaye hai
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)
        self.Product_Table.heading("pid",text="P ID")
        self.Product_Table.heading("Category",text="Category")
        self.Product_Table.heading("Supplier",text="Supplier")
        self.Product_Table.heading("name",text="Name")
        self.Product_Table.heading("price",text="Price")
        self.Product_Table.heading("qty",text="Qty")
        self.Product_Table.heading("status",text="Status")
        

        self.Product_Table["show"]="headings"

        self.Product_Table.column("pid",width=90)
        self.Product_Table.column("Category",width=100)
        self.Product_Table.column("Supplier",width=100)
        self.Product_Table.column("name",width=100)
        self.Product_Table.column("price",width=100)
        self.Product_Table.column("qty",width=100)
        self.Product_Table.column("status",width=100)
        

        self.Product_Table.pack(fill=BOTH,expand=1)
        self.Product_Table.bind("<ButtonRelease-1>",self.get_data)

        self.Product_Table.pack(fill=BOTH,expand=1)

        self.show()
        

     #=============================================================


    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
            for i in cat:
                self.cat_list.append(i[0])
            
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
            for i in sup:
                self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    

    def add(self):                                              
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select"  or self.var_name.get()=="":
                messagebox.showerror("Error","All Fields are required",parent=self.root)
            else:
                cur.execute("select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","product already present,try different",parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                                                self.var_cat.get(),
                                                self.var_sup.get(),
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                                                ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def get_data(self,ev):
        f=self.Product_Table.focus()
        content=self.Product_Table.item((f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])
       


    def update(self):                                               #self isliye kyuki sabse upar self use kiya ha widgets mai call kiya hai fun mai bhi use karna hai isliye
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(

                                                self.var_cat.get(),
                                                self.var_sup.get(),
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                                                self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def delete(self):
         con = sqlite3.connect(database=r'BSW.db')
         cur = con.cursor()
         try:
             if self.var_pid.get() == "":
                 messagebox.showerror("Error", "Select Product from the List", parent=self.root)
             else:
                 cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                 row = cur.fetchone()
                 if row == None:
                     messagebox.showerror("Invalid Product",parent=self.root)
                 else:
                     op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                     if op==True:
                         cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                         con.commit()
                         messagebox.showinfo("Delete", "Product Deleted  Successfully", parent=self.root)
                         self.clear()


         except Exception as ex:
             messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        
        self.var_searchtxt.set("")
        self.var_searchby.set("select")
        self.show()


    def search(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Search":
                messagebox.showerror("Error","Select search by options",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)

            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Product_Table.delete(*self.Product_Table.get_children())
                    for row in rows:
                        self.Product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=PrdClass(root)
    root.mainloop()
