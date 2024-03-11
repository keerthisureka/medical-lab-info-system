from tkinter import *
from tkinter import messagebox
from database import *

def fetch_data(details, details_table):
    if len(details) != 0:
        details_table.delete(*details_table.get_children())
        for i in details:
            details_table.insert("", END, values=i)

def labs(tab):
    def clear():
        txtLabName.delete(0, END)
        txtContactNo.delete(0, END)
        txtLocation.delete(0, END)
        txtOpenHrs.delete(0, END)
        txtYrsOfExp.delete(0, END)

    def on_lab_addclick():
        data = {"LabName": txtLabName.get(), "ContactNo": txtContactNo.get(), "Location": txtLocation.get(), "OpenHrs": txtOpenHrs.get(), "YrsOfExp": txtYrsOfExp.get()}
        if data["LabName"] == "" or data["ContactNo"] == "" or data["Location"] == "" or data["OpenHrs"] == "" or data["YrsOfExp"] == "":
            messagebox.showerror("Error", "Fields cannot be empty!")
        else:
            c = lab_add(data)
            if c == None:
                messagebox.showerror("Error", "Failed to add the details!")
            else:
                details = lab_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details added successfully!")
                clear()

    def on_lab_updateclick():
        data = {"LabName": txtLabName.get(), "ContactNo": txtContactNo.get(), "Location": txtLocation.get(), "OpenHrs": txtOpenHrs.get(), "YrsOfExp": txtYrsOfExp.get()}
        if data["LabName"] == "" or data["ContactNo"] == "" or data["Location"] == "" or data["OpenHrs"] == "" or data["YrsOfExp"] == "":
            details = lab_details()
            fetch_data(details, details_table)
        else:
            c = lab_update(data)
            if c == None:
                messagebox.showerror("Error", "Failed to update the details!")
            else:
                details = lab_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details updated successfully!")
                clear()


    def get_cursor(event=""):
        cursor_row=details_table.focus()
        content=details_table.item(cursor_row)
        row=content["values"]
        txtLabName.delete(0, tk.END)
        txtLabName.insert(0, row[0])
        txtContactNo.delete(0, tk.END)
        txtContactNo.insert(0, row[1])
        txtLocation.delete(0, tk.END)
        txtLocation.insert(0, row[2])
        txtOpenHrs.delete(0, tk.END)
        txtOpenHrs.insert(0, row[3])
        txtYrsOfExp.delete(0, tk.END)
        txtYrsOfExp.insert(0, row[4])
    
    def on_lab_deleteclick():
        data = {"LabName": txtLabName.get(), "ContactNo": txtContactNo.get(), "Location": txtLocation.get(), "OpenHrs": txtOpenHrs.get(), "YrsOfExp": txtYrsOfExp.get()}
        if data["LabName"] == "":
            messagebox.showerror("Error", "Lab Name cannot be empty!")
        else:
            c = lab_delete(data)
            if c == None:
                messagebox.showerror("Error", "No such entry exists!")
            else:
                details = lab_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Deleted successfully!")
                clear()

    lblLabName=Label(tab, font=("times new roman", 12, "bold"), text="Lab Name:", padx=3, pady=6)
    lblLabName.grid(row=0, column=0)
    txtLabName=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtLabName.grid(row=0, column=1)

    lblContactNo=Label(tab, font=("times new roman", 12, "bold"), text="Contact No:", padx=3, pady=6)
    lblContactNo.grid(row=1, column=0)
    txtContactNo=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtContactNo.grid(row=1, column=1)

    lblLocation=Label(tab, font=("times new roman", 12, "bold"), text="Location:", padx=3, pady=6)
    lblLocation.grid(row=2, column=0)
    txtLocation=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtLocation.grid(row=2, column=1)

    lblOpenHrs=Label(tab, font=("times new roman", 12, "bold"), text="Open Hrs:", padx=3, pady=6)
    lblOpenHrs.grid(row=3, column=0)
    txtOpenHrs=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtOpenHrs.grid(row=3, column=1)

    lblYrsOfExp=Label(tab, font=("times new roman", 12, "bold"), text="Experience (in yrs):", padx=3, pady=6)
    lblYrsOfExp.grid(row=4, column=0)
    txtYrsOfExp=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtYrsOfExp.grid(row=4, column=1)

    #================buttons==============
    btnadd=Button(tab, text="ADD", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_lab_addclick)
    btnadd.place(x=20, y=250)
    btnupdate=Button(tab,text="UPDATE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_lab_updateclick)
    btnupdate.place(x=185, y=250)
    btndelete=Button(tab,text="DELETE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_lab_deleteclick)
    btndelete.place(x=350, y=250)

    # ===============Lab Details================
    DataframeRight=LabelFrame(tab,bd=10,padx=10,relief=RIDGE,font=("times new roman", 12, "bold"),text="Labs Available")
    DataframeRight.place(x=530, y=10, width=970, height=600)
    scroll_x = ttk.Scrollbar(DataframeRight, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(DataframeRight, orient=VERTICAL)
    details_table = ttk.Treeview(DataframeRight, column=("id0", "id1", "id2", "id3", "id4"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)
    details_table.heading("id0", text="Lab Name")
    details_table.heading("id1", text="Contact No")
    details_table.heading("id2", text="Location")
    details_table.heading("id3", text="Open Hrs")
    details_table.heading("id4", text="Yrs Of Experience")
    details_table["show"] = "headings"
    details_table.pack(fill=BOTH, expand=1)
    details = lab_details()
    details_table.bind("<ButtonRelease-1>", get_cursor)
    fetch_data(details, details_table)


def tests(tab):
    def clear():
        txtTestName.delete(0, END)
        txtDescription.delete(0, END)
        txtSampleType.delete(0, END)
        txtTestDuration.delete(0, END)
        txtNormalRange.delete(0, END)

    def on_test_addclick():
        data = {"TestName": txtTestName.get(), "Description": txtDescription.get(), "SampleType": txtSampleType.get(), "TestDuration": txtTestDuration.get(), "NormalRange": txtNormalRange.get()}
        if data["TestName"] == "" or data["Description"] == "" or data["SampleType"] == "" or data["TestDuration"] == "" or data["NormalRange"] == "":
            messagebox.showerror("Error", "Fileds cannot be empty!")
        else:
            c = test_add(data)
            if c == None:
                messagebox.showerror("Error", "Failed to add the details!")
            else:
                details = test_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details added successfully!")
                clear()

    def on_test_updateclick():
        data = {"TestName": txtTestName.get(), "Description": txtDescription.get(), "SampleType": txtSampleType.get(), "TestDuration": txtTestDuration.get(), "NormalRange": txtNormalRange.get()}
        if data["TestName"] == "" or data["Description"] == "" or data["SampleType"] == "" or data["TestDuration"] == "" or data["NormalRange"] == "":
            details = test_details()
            fetch_data(details, details_table)
        else:
            c = test_update(data)
            if c == None:
                messagebox.showerror("Error", "Failed to update the details!")
            else:
                details = test_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details updated successfully!")
                clear()

    def get_cursor(event=""):
        cursor_row=details_table.focus()
        content=details_table.item(cursor_row)
        row=content["values"]
        txtTestName.delete(0, tk.END)
        txtTestName.insert(0, row[0])
        txtDescription.delete(0, tk.END)
        txtDescription.insert(0, row[1])
        txtSampleType.delete(0, tk.END)
        txtSampleType.insert(0, row[2])
        txtTestDuration.delete(0, tk.END)
        txtTestDuration.insert(0, row[3])
        txtNormalRange.delete(0, tk.END)
        txtNormalRange.insert(0, row[4])
    
    def on_test_deleteclick():
        data = {"TestName": txtTestName.get(), "Description": txtDescription.get(), "SampleType": txtSampleType.get(), "TestDuration": txtTestDuration.get(), "NormalRange": txtNormalRange.get()}
        if data["TestName"] == "":
            messagebox.showerror("Error", "Test Name cannot be empty!")
        else:
            c = test_delete(data)
            if c == None:
                messagebox.showerror("Error", "No such entry exists!")
            else:
                details = test_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Deleted successfully!")
                clear()

    lblTestName=Label(tab, font=("times new roman", 12, "bold"), text="Test Name:", padx=3, pady=6)
    lblTestName.grid(row=0, column=0)
    txtTestName=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtTestName.grid(row=0, column=1)

    lblDescription=Label(tab, font=("times new roman", 12, "bold"), text="Description:", padx=3, pady=6)
    lblDescription.grid(row=1, column=0)
    txtDescription=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtDescription.grid(row=1, column=1)

    lblSampleType=Label(tab, font=("times new roman", 12, "bold"), text="Sample Type:", padx=3, pady=6)
    lblSampleType.grid(row=2, column=0)
    txtSampleType=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtSampleType.grid(row=2, column=1)

    lblTestDuration=Label(tab, font=("times new roman", 12, "bold"), text="Test Duration:", padx=3, pady=6)
    lblTestDuration.grid(row=3, column=0)
    txtTestDuration=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtTestDuration.grid(row=3, column=1)

    lblNormalRange=Label(tab, font=("times new roman", 12, "bold"), text="Normal Range:", padx=3, pady=6)
    lblNormalRange.grid(row=4, column=0)
    txtNormalRange=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtNormalRange.grid(row=4, column=1)

    #================buttons==============
    btnadd=Button(tab, text="ADD", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_test_addclick)
    btnadd.place(x=20, y=250)
    btnupdate=Button(tab,text="UPDATE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_test_updateclick)
    btnupdate.place(x=185, y=250)
    btndelete=Button(tab,text="DELETE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_test_deleteclick)
    btndelete.place(x=350, y=250)

    # ===============Lab Details================
    DataframeRight=LabelFrame(tab,bd=10,padx=10,relief=RIDGE,font=("times new roman", 12, "bold"),text="Tests Available")
    DataframeRight.place(x=530, y=10, width=970, height=600)
    scroll_x = ttk.Scrollbar(DataframeRight, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(DataframeRight, orient=VERTICAL)
    details_table = ttk.Treeview(DataframeRight, column=("id0", "id1", "id2", "id3", "id4", "id5"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)
    details_table.heading("id0", text="Test Name")
    details_table.heading("id1", text="Description")
    details_table.heading("id2", text="sample Type")
    details_table.heading("id3", text="Test Duration")
    details_table.heading("id4", text="Normal Range")
    details_table["show"] = "headings"
    details_table.pack(fill=BOTH, expand=1)
    details = test_details()
    details_table.bind("<ButtonRelease-1>", get_cursor)
    fetch_data(details, details_table)

def efficiency(tab):
    def clear():
        sel1_option.set("")
        sel2_option.set("")
        txtPrice.delete(0, END)
        txtTestsPerDay.delete(0, END)
        txtSensitivity.delete(0, END)
        txtSpecificity.delete(0, END)

    def on_efficiency_addclick():
        data = {"Lab": sel1_option.get(), "Test": sel2_option.get(), "Price": txtPrice.get(), "TestsPerDay": txtTestsPerDay.get(), "Sensitivity": txtSensitivity.get(), "Specificity": txtSpecificity.get()}
        if data["Lab"] == "" or data["Test"] == "" or data["Price"] == "" or data["TestsPerDay"] == "" or data["Sensitivity"] == "" or data["Specificity"] == "":
            messagebox.showerror("Error", "Fields cannot be empty!")
        else:
            c = efficiency_add(data)
            if c == None:
                messagebox.showerror("Error", "Failed to add the details!")
            else:
                details = efficiency_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details added successfully!")
                clear()

    def on_efficiency_updateclick():
        data = {"Lab": sel1_option.get(), "Test": sel2_option.get(), "Price": txtPrice.get(), "TestsPerDay": txtTestsPerDay.get(), "Sensitivity": txtSensitivity.get(), "Specificity": txtSpecificity.get()}
        if data["Lab"] == "" or data["Test"] == "" or data["Price"] == "" or data["TestsPerDay"] == "" or data["Sensitivity"] == "" or data["Specificity"] == "":
            details = efficiency_details()
            fetch_data(details, details_table)
        else:
            c = efficiency_update(data)
            if c == None:
                messagebox.showerror("Error", "Failed to update the details!")
            else:
                details = efficiency_details()
                fetch_data(details, details_table)
                messagebox.showinfo("Success", "Details updated successfully!")
                clear()

    def get_cursor(event=""):
        cursor_row=details_table.focus()
        content=details_table.item(cursor_row)
        row=content["values"]
        sel1_option.set(row[0])
        sel2_option.set(row[1])
        txtPrice.delete(0, tk.END)
        txtPrice.insert(0, row[2])
        txtTestsPerDay.delete(0, tk.END)
        txtTestsPerDay.insert(0, row[3])
        txtSensitivity.delete(0, tk.END)
        txtSensitivity.insert(0, row[4])
        txtSpecificity.delete(0, tk.END)
        txtSpecificity.insert(0, row[5])
    
    def on_efficiency_deleteclick():
        data = {"Lab": sel1_option.get(), "Test": sel2_option.get(), "Price": txtPrice.get(), "TestsPerDay": txtTestsPerDay.get(), "Sensitivity": txtSensitivity.get(), "Specificity": txtSpecificity.get()}
        if data["Lab"] == "" or data["Test"] == "":
            messagebox.showerror("Error", "Lab Name and Test Name cannot be empty!")
        else:
            details = efficiency_details()
            fetch_data(details, details_table)
            efficiency_delete(data)
            messagebox.showinfo("Success", "Deleted successfully!")
            clear()

    lblLab=Label(tab, font=("times new roman", 12, "bold"), text="Lab:", padx=3, pady=6)
    lblLab.grid(row=0, column=0)
    options1 = labnames
    sel1_option=StringVar()
    lab = OptionMenu(tab, sel1_option, *options1)
    lab.grid(row=0, column=1, padx=0, pady=0, sticky="w")

    lblTest=Label(tab, font=("times new roman", 12, "bold"), text="Test:", padx=3, pady=6)
    lblTest.grid(row=1, column=0)
    options2 = testnames
    sel2_option=StringVar()
    test = OptionMenu(tab, sel2_option, *options2)
    test.grid(row=1, column=1, padx=0, pady=0, sticky="w")

    lblPrice=Label(tab, font=("times new roman", 12, "bold"), text="Price:", padx=3, pady=6)
    lblPrice.grid(row=2, column=0)
    txtPrice=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtPrice.grid(row=2, column=1)

    lblTestsPerDay=Label(tab, font=("times new roman", 12, "bold"), text="Tests per Day:", padx=3, pady=6)
    lblTestsPerDay.grid(row=3, column=0)
    txtTestsPerDay=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtTestsPerDay.grid(row=3, column=1)

    lblSensitivity=Label(tab, font=("times new roman", 12, "bold"), text="Sensitivity:", padx=3, pady=6)
    lblSensitivity.grid(row=4, column=0)
    txtSensitivity=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtSensitivity.grid(row=4, column=1)

    lblSpecificity=Label(tab, font=("times new roman", 12, "bold"), text="Specificity:", padx=3, pady=6)
    lblSpecificity.grid(row=5, column=0)
    txtSpecificity=Entry(tab, font=("times new roman", 12, "bold"), width=35)
    txtSpecificity.grid(row=5, column=1)

    #================buttons==============
    btnadd=Button(tab, text="ADD", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_efficiency_addclick)
    btnadd.place(x=20, y=250)
    btnupdate=Button(tab,text="UPDATE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_efficiency_updateclick)
    btnupdate.place(x=185, y=250)
    btndelete=Button(tab,text="DELETE", bg="green", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=6, command=on_efficiency_deleteclick)
    btndelete.place(x=350, y=250)

    # ===============Lab Details================
    DataframeRight=LabelFrame(tab,bd=10,padx=10,relief=RIDGE,font=("times new roman", 12, "bold"),text="Efficiencies")
    DataframeRight.place(x=530, y=10, width=970, height=600)
    scroll_x = ttk.Scrollbar(DataframeRight, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(DataframeRight, orient=VERTICAL)
    details_table = ttk.Treeview(DataframeRight, column=("id0", "id1", "id2", "id3", "id4", "id5"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=details_table.xview)
    scroll_y.config(command=details_table.yview)
    details_table.heading("id0", text="Test Name")
    details_table.heading("id1", text="Lab Name")
    details_table.heading("id2", text="Price")
    details_table.heading("id3", text="Tests Per Day")
    details_table.heading("id4", text="Sensitivity")
    details_table.heading("id5", text="Specificity")
    details_table["show"] = "headings"
    details_table.pack(fill=BOTH, expand=1)
    details = efficiency_details()
    details_table.bind("<ButtonRelease-1>", get_cursor)
    fetch_data(details, details_table)


import tkinter as tk
from tkinter import ttk

conn, cursor = initialize_connection()

class mlis_admin:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Laboratory Information System")
        self.root.geometry("1540x800+0+0")
        self.root.configure(background="dark blue")

        lbltitle=Label(self.root,bd=20,relief=RIDGE,text="Medical Laboratory Information System", fg="dark blue", bg="white", font=("times new roman", 50,"bold"))
        lbltitle.pack(side=TOP, fill=X)
        
        #======================DATAFRAMES======================
        Dataframe=Frame(self.root,bd=20,relief=RIDGE)
        Dataframe.place(x=0,y=120,width=1530,height=400)

        def logout(event=""):
            res = messagebox.askyesno("Medical Laboratory Information System", "Do you want to logout?")
            if res > 0:
                root.destroy()
            return

        def on_tab_change(event):
            current_tab = notebook.index(notebook.select())
            if current_tab == 0:
                labs(tab1)
            elif current_tab == 1:
                tests(tab2)
            else:
                efficiency(tab3)
        notebook=ttk.Notebook(self.root)
        tab1 = tk.Frame(notebook, bd=10, relief=RIDGE)
        tab2 = tk.Frame(notebook, bd=10, relief=RIDGE)
        tab3 = tk.Frame(notebook, bd=10, relief=RIDGE)
        notebook.add(tab1, text="Labs")
        notebook.add(tab2, text="Tests")
        notebook.add(tab3, text="Efficiency")
        ttk.Style().configure("TNotebook.Tab", font=("times new roman",12,"bold"), padding=(5, 5))
        btnlogout=Button(notebook,text="LOGOUT", bg="dark blue", fg="white", font=("times new roman", 12, "bold"), width=15, padx=2, pady=0, command=logout)
        btnlogout.place(x=1360, y=0)
        notebook.place(x=0, y=5, width=980, height=350)
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)
        notebook.pack(fill="both", expand=True, padx=0, pady=0)

def main_window_admin():
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    mlis_admin(root)
    root.mainloop()
main_window_admin()