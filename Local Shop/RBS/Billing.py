import os
import time
import tempfile
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
from tkinter import messagebox

from User import UserClass
from Supplier import SupClass


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("RETAILER BILLING SOFTWARE BILLING SECTION")
        self.root.config(bg="ivory3")
        self.icon_main=PhotoImage(file="images\logo.png")
        self.root.iconphoto(False,self.icon_main)
        self.cart_list=[]
        self.chk_print=0


       # ===title=====

        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root, text="Retail Billing",image=self.icon_title,compound=LEFT,font=("times new roman", 40, "bold"),bg="light sea green",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        # ===btn_logout===
        btn_logout = Button(self.root, text="Logout",command=self.logout, font=("times new roman", 15, "bold"),bg="yellow",cursor="hand2").place(x=1150,
                                                                                                               y=10,height=50,width=150)
        #===clock===
        self.lbl_clock=Label(self.root, text="welcome to XYZ Store\t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS ",font=("times new roman", 15), bg="thistle4", fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        self.update_date_time()

        #========Product Frame========
       
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="ivory3")
        ProductFrame1.place(x=10,y=110,width=410,height=560)
        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="gold3",fg="white").pack(side=TOP,fill=X)

        # ========Product Search Frame========
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="ivory3")
        ProductFrame2.place(x=2,y=42,width=398,height=120)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="ivory3",fg="green").place(x=2,y=5)

        lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="ivory3",fg="green").place(x=5,y=45)

        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15,"bold"),bg="seashell2",fg="green").place(x=130,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        # ========Product Details Frame========

        ProductFrame3 = Frame(ProductFrame1, bd=3,relief=RIDGE, bg="ivory3")
        ProductFrame3.place(x=2, y=140, width=398, height=370)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.Product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty","status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)  
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)
        self.Product_Table.heading("pid", text="PID")
        self.Product_Table.heading("name", text="Name")
        self.Product_Table.heading("price", text="Price")
        self.Product_Table.heading("qty", text="QTY")
        self.Product_Table.heading("status", text="Status")

        self.Product_Table["show"] = "headings"

        self.Product_Table.column("pid", width=90)
        self.Product_Table.column("name", width=100)
        self.Product_Table.column("price", width=100)
        self.Product_Table.column("qty", width=100)
        self.Product_Table.column("status", width=100)
        self.Product_Table.pack(fill=BOTH, expand=1)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the Cart",font=("goudy old style",11),anchor='w',bg="ivory3",fg="red").pack(side=BOTTOM,fill=X)

        self.Product_Table.bind("<ButtonRelease-1>",self.get_data)


        #=============== Customer Frame=========
        self.var_cname=StringVar()
        self.var_contact_No=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="ivory3")
        CustomerFrame.place(x=425,y=110,width=530,height=400)
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",18,"bold"),bg="IndianRed2").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="ivory3",fg="blue").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="seashell2",fg="green").place(x=80,y=37,width=180)

        lbl_contac=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="ivory3",fg="blue").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact_No,font=("times new roman",13),bg="seashell2",fg="green").place(x=370,y=35,width=150)

        # ======= Cal Cart Frame=================

        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="ivory3")
        Cal_Cart_Frame.place(x=425,y=190,width=530,height=340)



        # =======Cart Frame=================

        Cart_Frame = Frame(Cal_Cart_Frame, bd=3,relief=RIDGE, bg = "ivory3")
        Cart_Frame.place(x=5, y=8, width=520, height=315)

        self.cartTitle=Label(Cart_Frame,text="Cart\tTotal Product: [0] ",font=("goudy old style",15,"bold"),bg="seashell2")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.cart_Table= ttk.Treeview(Cart_Frame,columns=("pid", "name", "price", "qty",),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)  # tupple banaye hai
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)
        self.cart_Table.heading("pid", text="PID")
        self.cart_Table.heading("name", text="Name")
        self.cart_Table.heading("price", text="Price")
        self.cart_Table.heading("qty", text="QTY")
       

        self.cart_Table["show"] = "headings"

        self.cart_Table.column("pid", width=30)
        self.cart_Table.column("name", width=95)
        self.cart_Table.column("price", width=85)
        self.cart_Table.column("qty", width=40)
        self.cart_Table.pack(fill=BOTH, expand=1)
        self.cart_Table.bind("<ButtonRelease-1>",self.get_data_cart)

        #=======Add cart Widgets Frame=================
        self.var_pid=StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()


        Add_cart_Widgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="ivory3")
        Add_cart_Widgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="ivory3")
        Add_cart_Widgets_Frame.place(x=425,y=510,width=530,height=110)

        lbl_p_name=Label(Add_cart_Widgets_Frame,text="Product name",font=("times new roman",15),bg="ivory3").place(x=5,y=5)
        txt_p_name = Entry(Add_cart_Widgets_Frame, textvariable=self.var_pname,font=("times new roman", 15), bg="seashell2",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_cart_Widgets_Frame,text="Price Per Qty",font=("times new roman",15),bg="ivory3").place(x=210,y=5)
        txt_p_price= Entry(Add_cart_Widgets_Frame, textvariable=self.var_price,font=("times new roman", 15), bg="seashell2",state='readonly').place(x=210,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_cart_Widgets_Frame,text="Quantity",font=("times new roman",15),bg="ivory3").place(x=380,y=5)
        txt_p_qty= Entry(Add_cart_Widgets_Frame, textvariable=self.var_qty,font=("times new roman", 15), bg="seashell2").place(x=380,y=35,width=120,height=22)

        self.lbl_inStock=Label(Add_cart_Widgets_Frame,text="In Stock",font=("times new roman",12),bg="ivory3")
        self.lbl_inStock.place(x=5,y=60)

        btn_clear_cart = Button(Add_cart_Widgets_Frame, text="Clear",command=self.clear_cart,font=("times new roman", 12), bg="tan2",cursor="hand2").place(x=180,y=60,width=150,height=25)
        btn_add_cart = Button(Add_cart_Widgets_Frame, text="Add | Update Cart",command=self.add_update_cart,font=("times new roman", 12), bg="tan2",cursor="hand2").place(x=340,y=60,width=180,height=25)


        #===============billing Area=========
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="ivory3")
        billFrame.place(x=953,y=110,width=410,height=509)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="red",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=============billing Buttons========
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=420,y=620,width=1111,height=80)
        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=('goudy old style',15,"bold"),bg="chartreuse4",fg="white")
        self.lbl_amnt.place(x=5,y=5,width=110,height=60)

        self.lbl_discount=Label(billMenuFrame,text="Discount \n[5%]",font=('goudy old style',15,"bold"),bg="blue",fg="white")
        self.lbl_discount.place(x=130,y=5,width=130,height=60)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=('goudy old style',15,"bold"),bg="red3",fg="white")
        self.lbl_net_pay.place(x=280,y=5,width=130,height=60)


        btn_print=Button(billMenuFrame,text="Print", command=self.print_bill, font=('goudy old style',15,"bold"),bg="gray",fg="white",cursor="hand2")
        btn_print.place(x=430,y=5,width=120,height=60)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=('goudy old style',15,"bold"),bg="gold3",fg="white",cursor="hand2")
        btn_clear_all.place(x=580,y=5,width=120,height=60)

        btn_generate=Button(billMenuFrame,text="Generate /Save Bill",command=self.generate_bill,font=('goudy old style',15,"bold"),bg="spring green",fg="white",cursor="hand2")
        btn_generate.place(x=730,y=5,width=190,height=60)

        #==footer===
        footer=Label(self.root,text="BILLING SOFTWARE | Devloped By Team SRP\nfor any Technical issue contact 986544xxyy")

        self.show()
        #self.bill_top()
        self.update_date_time()

        #===========All Functions=========

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
        self.chk_print = 0

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def logout(self):
        self.root.destroy()
        os.system("python Login.py")
    
    def show(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'" )
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Product_Table.delete(*self.Product_Table.get_children())
                    for row in rows:
                        self.Product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    
    def get_data(self,ev):
        f=self.Product_Table.focus()
        content=self.Product_Table.item((f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])   
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

     
    def get_data_cart(self,ev):
        f=self.cart_Table.focus()
        content=self.cart_Table.item((f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])   
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            
            #=====update_cart======
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update| Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #qty
            else:
            
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()


    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt.(Rs.)\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay(Rs.)\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Produt: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in self.cart_list:
                self.cart_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact_No.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to the Cart!!",parent=self.root)
        else:
            #===Bill top==
            self.bill_top()
            #===Bill middle==
            self.bill_middle()
            #===Bill bottom==
            self.bill_bottom()

            fp=open(f'Bill Reports/{str(self.billNo)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.billNo=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t       Retailer BILL-Management 
\t Phone No.7327852324,Mangalpur-752104
{str("="*47)}
 Customer Name: {self.var_cname.get()}\t\t\tTime: {str(time.strftime ("%H:%M:%S"))}
 Ph no. :{self.var_contact_No.get()}
 Bill No. {str(self.billNo)}\t\t\tDate: {str(time.strftime ("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice 
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        global status
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+(row[3])+"\tRs."+price)
                #===update qty in product table===
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid

                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')   
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
        

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact_No.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Produt: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Hii EMP! WELCOME TO BILLING SYSTEM\t\t Date: {str(date_)}\t\t Time: {str(time_)} ")
        self.lbl_clock.after(200,self.update_date_time)
        
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print', "Please generate bill, to print the receipt", parent=self.root)


if __name__=="__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
