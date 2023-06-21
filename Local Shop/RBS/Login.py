from tkinter import *
from tkinter import messagebox
import sqlite3
import email_pass
import smtplib
import time
import os
from PIL import ImageTk 

class Login_System:
    def __init__(self,root):
        self.root=root                  
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.icon_main=PhotoImage(file="images\login_icon.png")
        self.root.iconphoto(False,self.icon_main)

        #====images===== 
        #self.phone_image=PhotoImage(file="images/phone.png")
        #self.lbl_phone_image = Label(self.root, image=self.phone_image,bd=0).place(x=200, y=90)    

        # ===loginframe======
        self.employee_id=StringVar()
        self.password=StringVar() 


        self.image=ImageTk.PhotoImage(file="images\login.png")
        self.lbl_inage=Label(self.root,image=self.image,bd=0).place(x=150,y=80)

        login_frame=Frame(self.root,bd=0,bg="#ffffff")
        login_frame.place(x=700,y=110,width=450,height=500)



        title=Label(login_frame,text="MANAGÉ",font=("Gloria Hallelujah",30,"bold"),bg="#ffffff").pack(side=TOP,fill=Y)
        title=Label(login_frame,text="RETAILER BILLING SOFTWARE",font=("Gloria Hallelujah",20,"bold"),bg="#ffffff").pack(side=TOP,fill=Y)

        lbl_user=Label(login_frame,text="Employee ID",font=("candara",20),bg="#ffffff").place(x=50,y=140)
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("candara",15),bg="#ececec").place(x=55,y=180,width=300,height=35)

        lbl_pass=Label(login_frame,text="Password",font=("candara",20),bg="#ffffff").place(x=50,y=260)
        txt_pass=Entry(login_frame,textvariable=self.password,show='*',font=("candara",15),bg="#ececec").place(x=55,y=300,width=300,height=35)

        self.icon_empid=PhotoImage(file="images\log.png")
        self.icon_pass=PhotoImage(file="images\passwordforgot.png")

        btn_login=Button(login_frame,text=" Login",command=self.login,image=self.icon_empid,compound=LEFT,padx=5,anchor="w",
                         font=("candara",20,"bold"),bg="#ffffff",bd=3,cursor="hand2").place(x=20,y=400,width=140)
        btn_forgot=Button(login_frame,text="Forgot Password",command=self.forget_window,image=self.icon_pass,compound=LEFT,padx=5,anchor="w",
                          font=("candara",20,"bold"),bg="#ffffff",bd=3,cursor="hand2").place(x=175,y=400)
        


        #login_frame=Frame(self.root, bd=2,relief=RIDGE,bg="white")
        #login_frame.place(x=750, y=90, width=350, height=460)

        #title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        #lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        #txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250,height=23)

        #lbl_pass=Label(login_frame,text="password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        #txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250,height=23)

        #btn_login= Button(login_frame,command=self.login, text="Log In", font=("Arial Rounded MT Bold",15),bg="#00B0F0",activeforeground="white",fg="white",cursor="hand2").place(x=50,y=300,height=30,width=250)
       

        #hr=Label(login_frame,bg="lightgrey").place(x=50,y=360,width=250,height=2)
        #or_= Label(login_frame,text="OR",bg="white",fg="lightgrey",font=("times new roman",15,"bold")).place(x=160, y=346)

        #btn_forgot=Button(login_frame,text="Forgot Password",command=self.forget_window, font=("times new roman",13),bg="white",fg="#00759E",bd=0,activeforeground="#00759E",activebackground="white").place(x=115,y=390)

        #======frame2=====
        #register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        #register_frame.place(x=750,y=570,width=350,height=60)

        #lbl_reg = Label(register_frame, text="STORE BILLING SYSTEM",font=("times new roman",13), bg="white").place(x=75, y=15)


    def login(self):
        con=sqlite3.connect(database=r'BSW.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All field are required",parent=self.root)
            else:
                cur.execute("select utype from user where uid=? AND password=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Employee":
                        self.root.destroy()
                        os.system("python Billing.py")
                    else:
                        self.root.destroy()
                        os.system("python Dashboard.py")


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'BSW.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("select email from user where uid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid Employee ID,try again", parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    chk = self.send_email(email[0])
                    
                    if chk != 's':
                        messagebox.showerror("Error", "Connection Error , try again", parent=self.root)
                    else:
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title = Label(self.forget_win, text="Reset Password", font=('goudy  old style', 15, 'bold'),
                                      bg="#3f51b5", fg="white").pack(side=TOP, fill=X)
                        lbl_reset = Label(self.forget_win, text="Enter OTP sent on Registered Email",
                                          font=("times new roman", 15)).place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15),
                                          bg='lightyellow').place(x=20, y=100, width=250, height=30)
                        self.btn_reset = Button(self.forget_win, text="Submit", command = self.validate_otp,
                                                font=("times new roman", 15), bg='lightblue')
                        self.btn_reset.place(x=280, y=100, width=100, height=30)

                        lbl_new_pass = Label(self.forget_win, text="New Password",
                                             font=('times new roman', 15)).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass,
                                             font=("times new roman", 15), bg='lightyellow').place(x=20, y=190,
                                                                                                   width=250,
                                                                                                   height=30)

                        lbl_c_pass = Label(self.forget_win, text="Confirm Password",
                                           font=("times new roman", 15)).place(x=20, y=225)
                        txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass,
                                           font=("times new roman", 15), bg='lightyellow').place(x=20, y=255,
                                                                                                 width=250,
                                                                                                 height=30)

                        self.btn_update = Button(self.forget_win, text="Update", command = self.update_password,
                                                 state=DISABLED, font=("times new roman", 15), bg='lightblue')
                        self.btn_update.place(x=150, y=300, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "Password is Required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password & confirm password should be same", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'BSW.db')
            cur = con.cursor()
            try:
                cur.execute("Update user SET password=? where uid=?",
                            (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Succes", "Password Updated Succesfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)




    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error", f"Invalid OTP , try again", parent=self.forget_win)


    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)
        self.otp = int(time.strftime("%H%M%S")) + int(time.strftime("%S"))

        subj = 'IMS-Reset Password OTP'
        msg = f'Dear Sir/Madam ,\n\n Your reset otp is {str(self.otp)}.\n\nWith Regards,\nBilling Software Team'
        msg = "Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'
                        


root = Tk()
obj = Login_System(root)
root.mainloop()
