from tkinter import*
import sqlite3

root=Tk()
root.title('MyCRUD Project')
root.geometry("500x500")

conn=sqlite3.connect('self_data.db')

f_name=Entry(root,width=30)

c=conn.cursor()
             
f_name=Entry(root,width=30)
f_name.grid(row=0,column=1,padx=20)
             
l_name=Entry(root,width=30)
l_name.grid(row=1,column=1,padx=20)
             
age=Entry(root,width=30)
age.grid(row=2,column=1,padx=20)
             
address=Entry(root,width=30)
address.grid(row=3,column=1,padx=20)
             
email=Entry(root,width=30)
email.grid(row=4,column=1,padx=20)
'''

c.execute("""CREATE TABLE"studentinfo"(CREATE TABLE "selfdata" (
	"f_name"	TEXT,
	"l_name"	TEXT,
	"age"	INTEGER,
	"address"	TEXT,
	"email"	TEXT 
))
'''

root.mainloop()
