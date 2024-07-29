from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1350x700+0+0")

        title = Label(self.root, text="Student Management System", bd=10, relief=GROOVE, font=("times new roman", 40, "bold"), fg='blue')
        title.pack(side=TOP, fill=X)

        self.name_var = StringVar()
        self.contact_var = StringVar()
        self.email_var = StringVar()
        self.branch_var = StringVar()
        self.year_var = StringVar()

        # Manage Left Frame
        self.Manage_frame_left = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.Manage_frame_left.place(x=15, y=100, width=450, height=560)

        DataLeftFrame = LabelFrame(self.Manage_frame_left, bd=4, relief=RIDGE, padx=2, text="Student Information", font=("times new roman", 15, "bold"), fg='blue', bg='white')
        DataLeftFrame.pack(side=LEFT, fill=BOTH, expand=1)

        lbl_name = Label(DataLeftFrame, text="Name:", font=("arial",12,"bold"), bg='white')
        lbl_name.grid(row=0, column=0, padx=25, pady=25, sticky=W)
        entry_name = Entry(DataLeftFrame, textvariable=self.name_var, font=("arial",12,"bold"), bg='white')
        entry_name.grid(row=0, column=1, padx=25, pady=25)

        lbl_contact = Label(DataLeftFrame, text="Contact:", font=("arial",12,"bold"), bg='white')
        lbl_contact.grid(row=1, column=0, padx=25, pady=25, sticky=W)
        entry_contact = Entry(DataLeftFrame, textvariable=self.contact_var, font=("arial",12,"bold"), bg='white')
        entry_contact.grid(row=1, column=1, padx=10, pady=10)

        lbl_email = Label(DataLeftFrame, text="Email:", font=("arial",12,"bold"), bg='white')
        lbl_email.grid(row=2, column=0, padx=25, pady=25, sticky=W)
        entry_email = Entry(DataLeftFrame, textvariable=self.email_var, font=("arial",12,"bold"), bg='white')
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        lbl_branch = Label(DataLeftFrame, text="Branch:", font=("arial",12,"bold"), bg='white')
        lbl_branch.grid(row=3, column=0, padx=25, pady=25, sticky=W)
        entry_branch = Entry(DataLeftFrame, textvariable=self.branch_var, font=("arial",12,"bold"), bg='white')
        entry_branch.grid(row=3, column=1, padx=10, pady=10)

        lbl_year = Label(DataLeftFrame, text="Year:", font=("arial",12,"bold"), bg='white')
        lbl_year.grid(row=4, column=0, padx=25, pady=25, sticky=W)
        entry_year = Entry(DataLeftFrame, textvariable=self.year_var, font=("arial",12,"bold"), bg='white')
        entry_year.grid(row=4, column=1, padx=10, pady=10)

        # Manage Right Frame
        self.Manage_frame_right = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.Manage_frame_right.place(x=470, y=100, width=860, height=560)

        DataRightFrame = LabelFrame(self.Manage_frame_right, bd=4, relief=RIDGE, padx=2, text="Detail Information", font=("times new roman", 15, "bold"), fg='blue', bg='white')
        DataRightFrame.pack(side=RIGHT, fill=BOTH, expand=1)

        tree_frame = Frame(DataRightFrame, bd=4, relief=RIDGE, padx=2, pady=2)
        tree_frame.place(x=10, y=5, width=830, height=450)

        scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        self.student_table = ttk.Treeview(tree_frame, columns=("Name", "Contact", "Email", "Branch", "Year"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Contact", text="Contact")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Branch", text="Branch")
        self.student_table.heading("Year", text="Year")

        self.student_table['show'] = 'headings'

        self.student_table.column("Name", width=150)
        self.student_table.column("Contact", width=150)
        self.student_table.column("Email", width=200)
        self.student_table.column("Branch", width=150)
        self.student_table.column("Year", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.viewstudent()

        btn_Add = Button(DataRightFrame, text="Add Student", command=self.add_data, font=("arial", 12, "bold"), bg='blue', width=15, fg='white', activebackground='green')
        btn_Add.place(x=10, y=460,width=120)

        btn_View = Button(DataRightFrame, text="View Student", font=("arial", 12, "bold"), bg='blue', width=15, fg='white', activebackground='green', command=self.viewstudent)
        btn_View.place(x=150, y=460,width=120)

        btn_Update = Button(DataRightFrame, text="Update Student", font=("arial", 12, "bold"), bg='blue', width=15, fg='white', activebackground='green', command=self.updatestudent)
        btn_Update.place(x=290, y=460,width=130)

        btn_Delete = Button(DataRightFrame, text="Delete Student", font=("arial", 12, "bold"), bg='blue', width=15, fg='white', activebackground='green', command=self.deletestudent)
        btn_Delete.place(x=430, y=460,width=130)

        btn_Exit = Button(DataRightFrame, text="Exit", font=("arial", 12, "bold"), bg='blue', width=15, fg='white', activebackground='green', command=self.exit)
        btn_Exit.place(x=570, y=460,width=130)

    def add_data(self):
        if self.name_var.get() == "" or self.email_var.get() == "" or self.branch_var.get() == "":
            messagebox.showerror("Error", "All Fields are Required")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="shrishti@m123", database="sys")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO student (name, contact, email, branch, year) VALUES (%s, %s, %s, %s, %s)", (
                    self.name_var.get(),
                    self.contact_var.get(),
                    self.email_var.get(),
                    self.branch_var.get(),
                    self.year_var.get()
                ))
                conn.commit()
                
                conn.close()
                messagebox.showinfo("Success", "Student has been added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Due To: {str(e)}")

    def viewstudent(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="shrishti@m123", database="sys")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()
        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #Get Cursor
    def get_cursor(self,event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data= content["values"]

        self.name_var.set(data[0])
        self.contact_var.set(data[1])
        self.email_var.set(data[2])
        self.branch_var.set(data[3])
        self.year_var.set(data[4])

        

    def updatestudent(self):
        if self.name_var.get() == "" or self.email_var.get() == "" or self.branch_var.get() == "":
            messagebox.showerror("Error", "All Fields are Required")
        else:
            try:
              update = messagebox.askyesno("Update", "Are You sure to Update this student data", parent=self.root)
              if update>0:
                  conn = mysql.connector.connect(host="localhost", username="root", password="shrishti@m123", database="sys")
                  my_cursor = conn.cursor()
                  my_cursor.execute("UPDATE student SET name=%s, contact=%s, email=%s, branch=%s, year=%s WHERE name=%s", (
                    self.name_var.get(),
                    self.contact_var.get(),
                    self.email_var.get(),
                    self.branch_var.get(),
                    self.year_var.get(),
                    self.name_var.get()
                ))
                  conn.commit()
                  self.viewstudent()
                  conn.close()
                  messagebox.showinfo("Success", "Successfully Updated Student Information", parent=self.root)
            except Exception as e:
               messagebox.showerror("Error", f"Due To: {str(e)}")
                

        

    def deletestudent(self):
        if (self.name_var.get() == "" or self.contact_var.get() == "" or
            self.email_var.get() == "" or self.branch_var.get() == "" or
            self.year_var.get() == ""):
            messagebox.showerror("Error", "All Fields are Required")
        else:
            try:
                delete = messagebox.askyesno("Delete", "Are You sure to Delete this student data", parent=self.root)
                if delete:
                    conn = mysql.connector.connect(host="localhost", username="root", password="shrishti@m123", database="sys")
                    my_cursor = conn.cursor()
                    my_cursor.execute("DELETE FROM student WHERE name=%s AND contact=%s AND email=%s AND branch=%s AND year=%s", (
                    self.name_var.get(),
                    self.contact_var.get(),
                    self.email_var.get(),
                    self.branch_var.get(),
                    self.year_var.get()
                ))
                    conn.commit()
                    
                    conn.close()
                    messagebox.showinfo("Success", "Successfully Deleted Student Information", parent=self.root)
            except Exception as e:
               messagebox.showerror("Error", f"Due To: {str(e)}")

                
    
            
        

    def exit(self):
        res = messagebox.askyesnocancel("Notification", "Do you want to exit?")
        if res:
            self.root.destroy()

if __name__ == '__main__':
    root = Tk()
    obj = Student(root)
    root.mainloop()
