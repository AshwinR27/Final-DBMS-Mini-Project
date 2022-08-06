
from flask import *
import sqlite3
import os
from forms import *
from flask import flash 



app = Flask(__name__) 
userid = 0
adminid = 0
source = ''
desti = ''
type = ''
driverData = []
bookingId = 0
statusOpt = ''
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
booked = False



@app.route('/index', methods=("GET","POST"))
def index():
    global booked
    print('index opened')
    conn = get_db_connection()
    book = conn.execute("select count(*) from booking where customer_id='"+str(userid)+"' and status='ACTIVE'")
    for i in book:
        if i[0] == 1:
            booked = True
        else:
            booked = False
    return render_template('index.html',userid=userid)

@app.route('/CreateAccount', methods=("GET","POST"))
def CreateAccount():
    global userid
    form = CreateCustomerForm()
    if form.validate_on_submit():
        f = request.form
        name = f['firstname']+' '+f['lastname']
        phone = f['phone']
        if phone == '':
            phone = 'NULL'
        email = f['email']
        if email == '':
            email = 'NULL'
        username = f['username']
        password = f['password']
        confirmpassword = f['confirmpassword']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "INSERT INTO CUSTOMER(USERNAME,PWD,NAME,PH_NO,EMAIL) VALUES('"+username+"','"+password+"','"+name+"','"+phone+"','"+email+"')"
        cur.execute(query)
        con.commit()
        con.close()
        flash("New Account has been successfully created ...")
        return redirect(url_for('login'))
    return render_template('AccountCreate.html',form=form)

@app.route('/')
@app.route('/login', methods=("GET","POST"))
def login():    
    global userid
    form = LoginForm()
    if form.validate_on_submit():
        userid = request.form
        userid = userid['username']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        for rowdata in rows: 
            if rowdata[1]==userid:
                userid=int(rowdata[0])        
        con.close() 
        flash("Successfully Logged In")
        return redirect(url_for('index'))        
    else:       
        return render_template('login.html',form=form)

@app.route('/EditProfile', methods=("GET","POST"))
def EditProfile():
    global userid
    userName = '';Name = ''; FName ='';LName ='' ;ph = 0;emailId = ''
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from customer where customer_id = "+str(userid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[1]
            Name = rowdata[3]
            NameData = Name.split(' ')
            max = len(NameData)
            FName = ' '.join(NameData[0:max-1])
            LName = NameData[max-1]
            ph = rowdata[4]
            emailId = rowdata[5]
            break
    con.close()
    form = EditCustomerForm(username = userName, firstname = FName, lastname = LName, phone = ph, email= emailId)
    if form.validate_on_submit():
        f = request.form
        name = f['firstname']+' '+f['lastname']
        phone = f['phone']
        if phone == '':
            phone = 'NULL'
        email = f['email']
        if email == '':
            email = 'NULL'
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE CUSTOMER SET NAME = '"+name+"', PH_NO = '"+phone+"', EMAIL = '"+emailId+"' WHERE CUSTOMER_ID = "+str(userid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Your profile has been successfully updated.... ")
        return redirect(url_for('index'))
    return render_template('EditProfile.html',form=form)

@app.route('/ChangePassword', methods=("GET","POST"))
def ChangePassword():
    global userid
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from customer where customer_id = "+str(userid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[1]
            break
    con.close()
    form = ChangePasswordForm(username = userName)
    if form.validate_on_submit():
        f = request.form
        pwd = f['newpassword']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE CUSTOMER SET PWD = '"+pwd+"' WHERE CUSTOMER_ID = "+str(userid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Password changed Successfully.... ")
        return redirect(url_for('index'))
    return render_template('ChangePassword.html',form=form)

@app.route('/Delete', methods=("GET","POST"))
def Delete():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "DELETE FROM CUSTOMER WHERE CUSTOMER_ID = "+str(userid)+";"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Account Deleted Successfully, You will be missed !!")
    form = LoginForm()
    return render_template('login.html',form=form)


@app.route('/mybookinghistory',methods=("GET","POST"))
def mybookinghistory():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING WHERE CUSTOMER_ID = '"+str(userid) +"' ORDER BY BOOKING_ID"
    cur.execute(query)
    rows = cur.fetchall()
    row2 = []
    for i in rows:
        row3 = []
        for j in range(len(i)):
            row3.append(i[j])
        row2.append(row3)
    if len(rows)==0:
        flash("No Bookings Founds !!!")
        return render_template('index.html',userid=userid)
    for i in row2:
        cur.execute("select source,destination from route where route_id="+str(i[2]))
        i[2]=cur.fetchone()
    con.close()
    return render_template('mybookinghistory.html',userid=userid,rows=row2)


@app.route('/DeleteAccount', methods=("GET","POST"))
def DeleteAccount():
    return render_template('DeleteAccount.html')




########################################################################################################################



@app.route('/AddAdmin', methods=("GET","POST"))
def AddAdmin():
    global userid
    form = AddAdminForm()
    if form.validate_on_submit():
        f = request.form
        name = f['name']
        username = f['username']
        password = f['password']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "INSERT INTO ADMIN(ANAME,AUSERNAME,APWD) VALUES('"+name+"','"+username+"','"+password+"')"
        cur.execute(query)
        con.commit()
        con.close()
        flash("New Admin added successfully....")
        return redirect(url_for('Adminindex'))
    return render_template('AddAdmin.html',form=form,adminid=adminid)

@app.route('/AdminLogin', methods=("GET","POST"))
def Adminlogin():
    global adminid;    
    form = AdminLoginForm()
    if form.validate_on_submit():
        adminid = request.form
        adminid = adminid['username']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        for rowdata in rows: 
            if rowdata[2]==adminid:
                adminid=int(rowdata[0])        
        con.close()
        flash("Successfully Logged In")
        return redirect(url_for('Adminindex')) 
    else:       
        return render_template('Adminlogin.html',form=form,adminid=adminid)
    
@app.route('/Adminindex', methods=("GET","POST"))
def Adminindex():
    return render_template('Adminindex.html',userid=userid,adminid=adminid)


@app.route('/ChangePasswordAdmin', methods=("GET","POST"))
def ChangePasswordAdmin():
    global adminid
    userName = '';Name = ''
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from admin where admin_id = "+str(adminid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[2]
            Name = rowdata[1]
            break
    con.close()
    form = ChangeAdminPasswordForm(username = userName,name = Name)
    if form.validate_on_submit():
        f = request.form
        pwd = f['newpassword']
        newName = f['name']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE ADMIN SET APWD = '"+pwd+"', ANAME ='"+newName+"' WHERE ADMIN_ID = "+str(adminid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Profile/Password Updated Successfully.... ")
        return redirect(url_for('Adminindex'))
    return render_template('ChangePasswordAdmin.html',form=form,adminid=adminid)

@app.route('/DeleteAdmin', methods=("GET","POST"))
def DeleteAdmin():
    global adminid
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "DELETE FROM ADMIN WHERE ADMIN_ID = "+str(adminid)+";"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Admin Account Deleted Successfully, You will be missed !!")
    form = LoginForm()
    return render_template('Adminlogin.html',form=form,adminid=adminid)

@app.route('/ViewDrivers',methods=("GET","POST"))
def ViewDrivers():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM DRIVER ORDER BY DRIVER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return render_template('ViewDrivers.html',adminid=adminid,rows=rows)

@app.route('/ReplaceDriver', methods=("GET","POST"))
def ReplaceDriver():
    global driverData
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM DRIVER ORDER BY DRIVER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    form = ReplaceDriverForm();
    if form.validate_on_submit():
        f = request.form
        driverData = []
        driverData.append(f['driverId'])
        driverData.append(f['name'])
        driverData.append(f['DL_no'])
        driverData.append(f['dph_no'])
        driverData.append(f['age'])
        return render_template('ReplaceConfirm.html',adminid=adminid,row=driverData)        
    return render_template('ReplaceDriver.html',adminid=adminid,rows=rows,form=form)

@app.route('/FinalReplace', methods=("GET","POST"))
def FinalReplace():
    global adminid
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "DELETE FROM DRIVER WHERE DRIVER_ID = "+str(driverData[0])+";"
    cur.execute(query)
    con.commit()
    query = "INSERT INTO DRIVER VALUES ("+driverData[0]+",'"+driverData[1]+"','"+driverData[2]+"',"+driverData[3]+","+driverData[4]+","+str(adminid)+");"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Driver successfully Replaced !!!")
    
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM DRIVER ORDER BY DRIVER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return redirect(url_for('ViewDrivers'))




@app.route('/ViewAll',methods=("GET","POST"))
def ViewAll():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING ORDER BY CUSTOMER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    row2 = []
    for i in rows:
        row3 = []
        for j in range(len(i)):
            row3.append(i[j])
        row2.append(row3)
    if len(rows)==0:
        flash("No Bookings Founds !!!")
        return render_template('Adminindex.html',userid=userid,adminid=adminid)
    for i in row2:
        cur.execute("select route_id,source,destination from route where route_id="+str(i[2]))
        i[2]=cur.fetchone()
    con.close()
    return render_template('ViewAll.html',adminid=adminid,rows=row2)



@app.route('/ViewActive',methods=("GET","POST"))
def ViewActive():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING WHERE STATUS='ACTIVE' ORDER BY CUSTOMER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    row2 = []
    for i in rows:
        row3 = []
        for j in range(len(i)):
            row3.append(i[j])
        row2.append(row3)
    if len(rows)==0:
        flash("No Bookings Founds !!!")
        return render_template('Adminindex.html',userid=userid,adminid=adminid)
    for i in row2:
        cur.execute("select route_id,source,destination from route where route_id="+str(i[2]))
        i[2]=cur.fetchone()
    con.close()
    return render_template('ViewActive.html',adminid=adminid,rows=row2)

@app.route('/ViewCancelled',methods=("GET","POST"))
def ViewCancelled():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING WHERE STATUS='CANCELLED' ORDER BY CUSTOMER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    row2 = []
    for i in rows:
        row3 = []
        for j in range(len(i)):
            row3.append(i[j])
        row2.append(row3)
    if len(rows)==0:
        flash("No Bookings Founds !!!")
        return render_template('Adminindex.html',userid=userid,adminid=adminid)
    for i in row2:
        cur.execute("select route_id,source,destination from route where route_id="+str(i[2]))
        i[2]=cur.fetchone()
    con.close()
    return render_template('ViewCancelled.html',adminid=adminid,rows=row2)

@app.route('/ViewCompleted',methods=("GET","POST"))
def ViewCompleted():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING WHERE STATUS='COMPLETED' ORDER BY CUSTOMER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    row2 = []
    for i in rows:
        row3 = []
        for j in range(len(i)):
            row3.append(i[j])
        row2.append(row3)
    if len(rows)==0:
        flash("No Bookings Founds !!!")
        return render_template('Adminindex.html',userid=userid,adminid=adminid)
    for i in row2:
        cur.execute("select route_id,source,destination from route where route_id="+str(i[2]))
        i[2]=cur.fetchone()
    con.close()
    return render_template('ViewCompleted.html',adminid=adminid,rows=row2)

@app.route('/ChangeStatus', methods=("GET","POST"))
def ChangeStatus():
    global bookingId, statusOpt
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "SELECT * FROM BOOKING ORDER BY CUSTOMER_ID"
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    form = ChangeStatusForm();
    if form.validate_on_submit():
        f = request.form
        bookingId = f['bookingId']
        statusOpt = f['statusOpt']
        return render_template('StatusConfirm.html',adminid=adminid,bookingId=bookingId,statusOpt=statusOpt)        
    return render_template('ChangeStatus.html',adminid=adminid,rows=rows,form=form)

@app.route('/FinalStatus', methods=("GET","POST"))
def FinalStatus():
    global bookingId, statusOpt
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "UPDATE BOOKING SET STATUS='"+statusOpt+"' WHERE BOOKING_ID="+str(bookingId)
    cur.execute(query)
    con.commit()
    con.close()
    return redirect(url_for('ChangeStatus'))


@app.route('/DeleteAccountAdmin', methods=("GET","POST"))
def DeleteAccountAdmin():
    return render_template('DeleteAccountAdmin.html')


#########################################################################################



def get_db_connection():
    conn = sqlite3.connect('DBMS.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/booking')
def booking():
    global booked
    if booked == True:
        flash("Cab already booked.")
        return render_template('index.html')
    else:
        conn = get_db_connection()
        data = conn.execute("select distinct source from route").fetchall()
        return render_template('booking.html',data=data)

@app.route("/dest" , methods=['GET', 'POST'])
def dest():
    conn1 = get_db_connection()
    select = request.form.get('comp_select')
    global source 
    source = select
    data1= conn1.execute("select destination from   route where source='"+str(select)+"'").fetchall()
    return render_template('dest.html',data1=data1,source=source)

def getdesti():
    if request.method=="POST":
        dselect = request.form.get('desti')
    global desti 
    desti = dselect

@app.route("/other" , methods=['GET', 'POST'])
def other():
    dselect = request.form.get('desti')
    global source,desti 
    desti = dselect
    return render_template('other.html',source=source,desti=desti) 

# @app.route("/test" , methods=['GET', 'POST'])
# def test():
#     global source,desti,type
#     return ' src= '+str(source) + 'dest= '+ str(desti)+' type= '+ str(type)

@app.route("/booked" , methods=['GET', 'POST'])
def sure():
    global source,desti,type,userid
    conn1 = get_db_connection()
    print(type)
    dat= conn1.execute("select fare,route_id,distance,time from route where source='"+str(source)+"' and destination='"+str(desti)+"'").fetchall()
    cad = conn1.execute("select driver_id,reg_no from cab where type='"+str(type)+"'").fetchall()
    if cad==None:
        return render_template('sure.html')
    else:
        for j in dat:
            fare = j[0]
            rid = j[1]
            d = j[2]
            t = j[3]
        for j in cad:
            did = j[0]
            reg = j[1]
        sql = """INSERT INTO Booking (route_id,customer_id,reg_no,driver_id,total_fare) VALUES('{}','{}','{}','{}','{}');""".format(int(rid),int(userid),str(reg),int(did),float(fare))
        print(rid,reg,did,fare)
        conn1.execute(sql)
        conn1.commit()
        return redirect(url_for('mybooking'))
 
@app.route("/mybooking" , methods=['GET', 'POST'])     
def mybooking():
    global source,desti,userid
    conn1 = get_db_connection()
    rcd = conn1.execute("select route_id,customer_id,driver_id from Booking where customer_id='"+str(userid)+"' and status='ACTIVE'").fetchall()
    print('assadasdasdasd',userid)
    cid = 0
    for i in rcd:
        ridd = int(i[0])
        cid = int(i[1])
        didd = int(i[2])
    if cid == 0:
        flash("No Booking Found.")
        return render_template('index.html')
    else:
        copydat= conn1.execute("select source,destination,fare,route_id,distance,time from route where route_id='"+str(ridd)+"'").fetchall()
        for cc in copydat:
            source = cc[0]
            desti = cc[1]
            d = cc[4]
            t = cc[5]
            
        dat= conn1.execute("select fare,route_id,distance,time from route where route_id='"+str(ridd)+"'").fetchall()
        typedat = conn1.execute("select type from cab where driver_id ="+str(didd)).fetchall()
        for i in typedat:
            type = i[0]
        udat = conn1.execute("select name,ph_no from customer where customer_id ="+str(userid))
        ddat = conn1.execute("select dname,dph_no from driver where driver_id ='"+str(didd)+"'")
        rdat = conn1.execute("select reg_no from cab where driver_id="+str(didd))
        
        return render_template('booked.html',source=source,desti=desti,type=type,dat=dat,cad=rdat,d=d,t=t,ddat=ddat,rdat=rdat,redat=dat,udat=udat)   

@app.route("/loading" , methods=['GET', 'POST'])
def loading():
    global booked 
    booked = True
    t = request.form.get("type")
    global source,desti,type
    type = t
    return render_template('loading.html',source=source,desti=desti), {"Refresh": "4; url=booked"}



@app.route("/deletebooking" , methods=['GET', 'POST'])
def deletebooking():
    return render_template('deletebooking.html')

@app.route("/deleteConfirm" , methods=['GET', 'POST'])
def deleteConfirm():
    global userid,booked
    conn1 = get_db_connection()
    bklist = conn1.execute("select booking_id from booking where customer_id='"+str(userid)+"' and status='ACTIVE'").fetchall()
    for i in bklist:
        conn1.execute("Update booking set status='CANCELLED' where booking_id="+str(i[0]))
        booked = False
        conn1.commit()
    flash("Booking Cancelled!")
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)