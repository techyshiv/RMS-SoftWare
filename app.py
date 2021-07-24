from flask import Flask, render_template, url_for, jsonify, Response,redirect,request
import json
import datetime
import num2word
from datetime import date,datetime, timedelta
import smtplib as sm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
from itertools import groupby
from operator import itemgetter
import logging

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

# ui=FlaskUI(app)
# <---------------------Starter Route------------------------------->

# <-------------------- Checkfor exe ---------------------------->
def CheckExe():
    with open('details.json',"r+") as file:
        json_data = json.loads(file.read())
        admindetails = json_data["Admin_Details"]
        if (admindetails["hide"] == "False"):
            data = "Yes"
        else:
            data = "No"
    return data
# <---------------------- Ends ---------------------------------->

@app.route("/")
def start():
    return render_template("choose.html")

@app.route("/SignAsAdmin",methods=["GET","POST"])
def SignAsAdmin():
    try:
        if request.method == "POST":
            code = request.form.get("access")
            with open("details.json",'r+') as file:
                json_data = json.loads(file.read())
                admindetails = json_data["Admin_Details"]
                if int(code) == 3898:
                    admindetails.update({
                        "hide":"False"
                    })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return Response(
                            response=json.dumps({"Res":"Valid Code"}),
                            status=200,
                            mimetype="application/json"
                        )
                else:
                    return Response(
                            response=json.dumps({"Res":"Invalid Code"}),
                            status=422,
                            mimetype="application/json"
                        )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Res":"Internal Serer Error"}),
            status=200,
            mimetype="application/json"
        )
    finally:
        pass

@app.route("/SignAsExecutive",methods=["GET","POST"])
def SignAsExecutive():
    try:
        if request.method == "POST":
            email = request.form.get("email")
            passw = request.form.get("pass")
            with open("details.json",'r+') as file:
                json_data = json.loads(file.read())
                register = json_data["Register"]
                admindetails = json_data["Admin_Details"]
                for val in register:
                    if email == val["Email"] and passw == val["Password"]:
                        admindetails.update({
                            "hide":"True"
                        })
                        # print(admindetails)
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                        response=json.dumps({"Res":"Valid Code"}),
                        status=200,
                        mimetype="application/json"
                    )
                    else:
                        return Response(
                        response=json.dumps({"Res":"Invalid Code"}),
                        status=422,
                        mimetype="application/json"
                    )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Res":"Internal Serer Error"}),
            status=200,
            mimetype="application/json"
        )
    finally:
        file.close()

@app.route("/home")
def home():
    with open("details.json", "r+") as file:
        json_data = json.loads(file.read())
        admin = json_data["Admin_Details"]
        if admin["Rememberme"]:
            return render_template("login.html",email=admin["Email"],passw=admin["Password"])
        else:
            return render_template("login.html")
# <---------------------Starter Route Ends------------------------------->

# <---------------------Homepage Route------------------------------->
@app.route("/index")
def index():
    with open('details.json',"r+") as file:
        json_data = json.loads(file.read())
        admindetails = json_data["Admin_Details"]
        if (admindetails["hide"] == "False"):
            data = "Yes"
        else:
            data = "No"
    return render_template("index.html",checkexe=data)
# <---------------------Homepage Route Ends------------------------------->

# <---------------------------- Login Route ------------------------------>
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            useremail = request.form.get("email")
            userpass = request.form.get("pass")
            check = request.form.get("check")
            print("Checkin = ",check)
            with open("details.json", "r+") as file:
                json_data = json.loads(file.read())
                admin = json_data["Admin_Details"]
                if useremail == admin["Email"] or userpass == admin["Password"]:
                    print("User Login Successfully")
                    if(check == ""):
                        pass
                    else:
                        admin["Rememberme"] = check
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                            response=json.dumps(
                                {
                                    "Message": "valid"
                                }
                            ),
                            status=200,
                            mimetype="application/json"
                        )
                else:
                    print("Invalid Crediantials")
                    return Response(
                        response=json.dumps(
                            {
                                "Message": "Invalid"
                            }
                        ),
                        status=401,
                        mimetype="application/json"
                    )
        except Exception as e:
            print("Error =", e)
            return Response(
                response=json.dumps(
                    {
                        "Message": "Internal Server Error"
                    }
                ),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <---------------------------- Login Route Ends------------------------------>

# <---------------------------- Signup Route ------------------------------>
@app.route("/signup")
def signup():
    return render_template("signup.html")
# <---------------------------- Signup Route Ends------------------------------>

# <-----------------------------Add own-credientials route---------------------->
@app.route("/Adddata",methods=["GET","POST"])
def Adddata():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            passw = request.form.get("pass")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                admin = json_data["Admin_Details"]
                admin["Email"] = email
                admin["Password"] = passw
                admin["Rememberme"] = ""
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
                print("Admin Registered Successfully")
            return Response(
                response=json.dumps({"Message": "valid"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
        
# <----------------------------- Add own-credientials route Ends---------------------->

# <---------------------------- Forgot Password Route ------------------------------>
@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")
# <---------------------------- Forgot Password Route Ends ------------------------->

# <---------------------------- Check Email for forgot Password Route ------------------------------>
@app.route("/check_email",methods=["GET","POST"])
def check_email():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                admin = json_data["Admin_Details"]
                if email == admin["Email"]:
                    return Response(
                            response=json.dumps({"Message": "valid"}),
                            status=200,
                            mimetype="application/json"
                        )
                else:
                    return Response(
                response=json.dumps({"Message": "Not Found"}),
                status=401,
                mimetype="application/json"
            )   
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <---------------------------- Check Email for forgot Password Route Ends ------------------------->

# <--------------------------- Update Password Page Route ------------------------------>
@app.route("/recovery")
def recovery():
    return render_template("password_recovery.html")
# <---------------------------- Update Password Page Route Ends ------------------------->

# <---------------------------- Update Password Route Start --------------------------->
@app.route("/recovery_password",methods=["GET","POST"])
def recovery_password():
    if request.method == "POST":
        try:
            passw = request.form.get("pass")
            conpass = request.form.get("conpass")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                admin = json_data["Admin_Details"]
                admin["Password"] = passw
                admin["Rememberme"]=""
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                        response=json.dumps({"Message": "valid"}),
                        status=200,
                        mimetype="application/json"
                    )  
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <---------------------------- Update Password Route Ends --------------------------->

###################################### Customer Management Section Start #######################

# <------------------------- Area Page Route -------------------------------------------->
@app.route("/area")
def area():
    with open('details.json',"r+") as file:
        json_data = json.loads(file.read())
        admindetails = json_data["Admin_Details"]
        if (admindetails["hide"] == "False"):
            data = "Yes"
        else:
            data = "No"
    return render_template("area.html",checkexe=data)
# <------------------------- Area Page Route Ends---------------------------------------->

# <------------------------ Area Data add Route Start ------------------------------------>
@app.route("/Add_area_data",methods=["GET","POST"])
def Add_area_data():
    if request.method == "POST":
        try:
            area = request.form.get("area")
            areapin = request.form.get("pin")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                areadetails = json_data["Area_Details"]
                if(len(areadetails)>0):
                    for val in areadetails:
                        if val["AreaName"] == area or val["AreaPin"] == areapin:
                            return Response(
                                response=json.dumps({"Message": "Invalid"}),
                                status=422,
                                mimetype="application/json"
                            )
                            break
                    else:
                        areadetails.append({
                            "AreaName":area,
                            "AreaPin":areapin
                        })
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                else:
                    areadetails.append({
                        "AreaName":area,
                        "AreaPin":areapin
                    })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
            return Response(
                        response=json.dumps({"Message": "valid","Data":areadetails}),
                        status=200,
                        mimetype="application/json"
                    )

        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <------------------------ Area Data add Route Ends -------------------------------------->

# <------------------------- Executive Page Route -------------------------------------------->
@app.route("/executive")
def executive():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            areadetails = json_data["Area_Details"]
            admindetails = json_data["Admin_Details"]
            if (admindetails["hide"] == "False"):
                data = "Yes"
            else:
                data = "No"
        return render_template("executive.html",data1=areadetails,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return render_template("executive.html",checkexe=data)
    finally:
        file.close()
# <------------------------- Executive Page Route Ends---------------------------------------->

# <------------------------ Executive Data add Route Start ------------------------------------>
@app.route("/Add_Executive_data",methods=["GET","POST"])
def Add_Executive_data():
    if request.method == "POST":
        try:
            area = request.form.get("area")
            exename = request.form.get("exename")
            exeid = request.form.get("exeid")
            address = request.form.get("address")
            mobile = request.form.get("mobile")
            what = request.form.get("what")
            email = request.form.get("email")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                exedetails = json_data["Executive_Details"]
                if len(exedetails)>0:
                    for val in exedetails:
                        if val["ExecutiveId"] == exeid or val["Mobile"] == mobile:
                            return Response(
                            response=json.dumps({"Message": "Data is Invalid"}),
                            status=422,
                            mimetype="application/json"
                        )
                            break
                    else:
                        exedetails.append({
                            "AreaName":area,
                            "ExecutiveName":exename,
                            "ExecutiveId":exeid,
                            "Address":address,
                            "Mobile":mobile,
                            "WhatsApp":what,
                            "Email":email
                        })
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                else:
                    exedetails.append({
                    "AreaName":area,
                    "ExecutiveName":exename,
                    "ExecutiveId":exeid,
                    "Address":address,
                    "Mobile":mobile,
                    "WhatsApp":what,
                    "Email":email
                })
                file.seek(0)
                json.dump(json_data,file,indent=4)
            return Response(
                        response=json.dumps({"Message": "valid"}),
                        status=200,
                        mimetype="application/json"
                    )

        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <------------------------ Executive Data add Route Ends-------------------------------------->

# <----------------------- Executive Details Page Route ----------------------------------->
@app.route("/exedetails")
def exedetails():
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        exedata = json_data["Executive_Details"]
        data = CheckExe()
    return render_template("executive_details.html",org_data=exedata,checkexe=data)
# <----------------------- Executive Details Page Route Ends----------------------------------->

# <------------------------ View Executive Route Start -------------------------------------->

@app.route("/View/Executive/<id>")
def VieWExecutive(id):
    try:
        exe_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            exedetails=json_object["Executive_Details"]
            for val in range(len(exedetails)):
                if exe_id==exedetails[val]["ExecutiveId"]:
                    data1 = exedetails[val]
                    break
        data = CheckExe()
        return render_template("executive.html",data=data1,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
        f.close()
# <------------------------ View Executive Route Ends --------------------------------------->

# <------------------- Edit Executive route Start ------------------------------------->
@app.route("/Edit_Executive/<id>")
def Edit_Executive(id):
    try:
        exe_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            exedetails=json_object["Executive_Details"]
            for val in range(len(exedetails)):
                if exe_id==exedetails[val]["ExecutiveId"]:
                    data1 = exedetails[val]
                    break
        data = CheckExe()
        return render_template("executive.html",edit=data1,data=0,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
        f.close()
# <------------------ Edit Executive route Ends --------------------------------------->

# <------------------ Change Executive Data Route Start ------------------------------->
@app.route("/Edit_Add_Executive_data",methods=["GET","POST"])
def Edit_Add_Executive_data():
    if request.method == "POST":
        try:
            area = request.form.get("area")
            exename = request.form.get("exename")
            exeid = request.form.get("exeid")
            address = request.form.get("address")
            mobile = request.form.get("mobile")
            what = request.form.get("what")
            email = request.form.get("email")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                exedetails = json_data["Executive_Details"]
                for val in exedetails:
                    if val["ExecutiveId"] == exeid:
                        val["AreaName"] = area 
                        val["ExecutiveName"] = exename 
                        val["ExecutiveId"] = exeid
                        val["Address"] = address 
                        val["Mobile"] = mobile
                        val["WhatsApp"] = what
                        val["Email"] = email
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=201,
                        mimetype="application/json"
                    )
                    break                
        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <-----------------  Change Executive Data Route Ends -------------------------------->

# <----------------- Executive Data Deleted Route Start ------------------------------------->
@app.route("/delete/Executive/",methods=["GET","POST"])
def delete_executive():
    if request.method == "POST":
        try:
            id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                exedetails = json_data["Executive_Details"]
                for val in range(len(exedetails)):
                    if id == exedetails[val]["ExecutiveId"]:
                        del exedetails[val]
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
                return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()

# <---------------- Executive Data Deleted Route Ends --------------------------------->

# <---------------- Customer Page Route Start ----------------------------------------->
@app.route("/customer")
def customer():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            exedetails = json_data["Executive_Details"]
        data = CheckExe()
        return render_template("customer.html",data1=exedetails,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to the adminstrator"
        })
    finally:
        file.close()
# <---------------- Customer Page Route Start Ends----------------------------------------->


# <------------------------ Customer Data add Route Start ------------------------------------>
@app.route("/Add_Customer_data",methods=["GET","POST"])
def Add_Customer_data():
    if request.method == "POST":
        try:
            exename = request.form.get("executive")
            cname = request.form.get("cusname")
            fname = request.form.get("fname")
            cusid = request.form.get("cusid")
            address = request.form.get("address")
            mobile = request.form.get("mobile")
            what = request.form.get("what")
            email = request.form.get("email")
            start = request.form.get("start")
            dob = request.form.get("dob")
            gender = request.form.get("gender")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                cusdetails = json_data["Customer_Details"]
                if len(cusdetails)>0:
                    for val in exedetails:
                        if val["CustomerId"] == cusid or val["Mobile"] == mobile:
                            return Response(
                            response=json.dumps({"Message": "Data is Invalid"}),
                            status=422,
                            mimetype="application/json"
                        )
                            break
                    else:
                        cusdetails.append({
                            "ExecutiveName":exename,
                            "CustomerName":cname,
                            "CustomerId":int(cusid),
                            "FatherName":fname,
                            "Address":address,
                            "Mobile":mobile,
                            "WhatsApp":what,
                            "Email":email,
                            "StartDate":start,
                            "D.O.B":dob,
                            "Gender":gender
                        })
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                else:
                    cusdetails.append({
                            "ExecutiveName":exename,
                            "CustomerName":cname,
                            "CustomerId":int(cusid),
                            "FatherName":fname,
                            "Address":address,
                            "Mobile":mobile,
                            "WhatsApp":what,
                            "Email":email,
                            "StartDate":start,
                            "D.O.B":dob,
                            "Gender":gender
                        })
                file.seek(0)
                json.dump(json_data,file,indent=4)
            return Response(
                        response=json.dumps({"Message": "valid"}),
                        status=200,
                        mimetype="application/json"
                    )

        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <------------------------ Customer Data add Route Ends-------------------------------------->

# <----------------------- Customer Details Route Start -------------------------------------->
@app.route("/cusdetails")
def cusdetails():
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        cusdata = json_data["Customer_Details"]
    data = CheckExe()
    return render_template("customer_details.html",org_data=cusdata,checkexe=data)
# <----------------------- Customer Details Route Ends --------------------------------------->

# <---------------------- Customer View Route Start ----------------------------------------->
@app.route("/View/Customer/<id>")
def VieWCustomer(id):
    try:
        cus_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            cusdetails=json_object["Customer_Details"]
            for val in range(len(cusdetails)):
                if int(cus_id)==cusdetails[val]["CustomerId"]:
                    data1 = cusdetails[val]
                    break
        data = CheckExe()
        return render_template("customer.html",data=data1,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
            f.close()
# <---------------------- Customer View Route Ends ------------------------------------------>

# <------------------- Edit Customer route Start ------------------------------------->
@app.route("/Edit_Customer/<id>")
def Edit_Customer(id):
    try:
        cus_id=id
        with open("details.json","r+") as file:
            json_object=json.loads(file.read())
            cusdetails=json_object["Customer_Details"]
            exedetails=json_object["Executive_Details"]
            for val in range(len(cusdetails)):
                if int(cus_id)==cusdetails[val]["CustomerId"]:
                    data1 = cusdetails[val]
                    break
        data = CheckExe()
        return render_template("customer.html",edit=data1,data=0,exe=exedetails,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
        file.close()
# <------------------ Edit Customer route Ends --------------------------------------->

# <------------------ Change Customer Data Route Start ------------------------------->
@app.route("/Edit_Add_Customer_data",methods=["GET","POST"])
def Edit_Add_Customer_data():
    if request.method == "POST":
        try:
            exename = request.form.get("executive")
            cname = request.form.get("cusname")
            fname = request.form.get("fname")
            cusid = request.form.get("cusid")
            address = request.form.get("address")
            mobile = request.form.get("mobile")
            what = request.form.get("what")
            email = request.form.get("email")
            start = request.form.get("start")
            dob = request.form.get("dob")
            gender = request.form.get("gender")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                cusdetails = json_data["Customer_Details"]
                for val in cusdetails:
                    if  val["CustomerId"] == int(cusid):
                        val["ExecutiveName"] = exename 
                        val["CustomerId"] = int(cusid)
                        val["CustomerName"] = cname
                        val["FatherName"] = fname
                        val["Address"] = address 
                        val["Mobile"] = mobile
                        val["WhatsApp"] = what
                        val["Email"] = email
                        val["StartDate"] = start
                        val["D.O.B"] = dob
                        val["Gender"] = gender
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=201,
                        mimetype="application/json"
                    )
                    break                
        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <-----------------  Change Customer Data Route Ends -------------------------------->

# <----------------- Customer Data Delete Route Start ------------------------------->
@app.route("/delete/Customer/",methods=["GET","POST"])
def delete_customer():
    if request.method == "POST":
        try:
            id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                cusdetails = json_data["Customer_Details"]
                for val in range(len(cusdetails)):
                    if int(id) == cusdetails[val]["CustomerId"]:
                        print("ID Match")
                        del cusdetails[val]
                        break
                print("Cus Details = ",cusdetails)
                json_data["Customer_Details"] = cusdetails
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
                return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <----------------- Customer Data Delete Route Ends -------------------------------->
###################################### Customer Management Section Ends #######################

###################################### Product Management Section Start #######################
# <------------------------------------ Product Page Route ------------------------------------>
@app.route("/product")
def product():
    data = CheckExe()
    return render_template("product.html",checkexe=data)
# <------------------------------------ Product Page Route Ends ------------------------------->

# <----------------------------------- Addproduct Route Start --------------------------->
@app.route("/AddProduct",methods=["GET","POST"])
def AddProduct():
    if request.method == "POST":
        try:
            proname = request.form.get("proname")
            procode = request.form.get("procode")
            proprice = request.form.get("proprice")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                prodetails = json_data["Product_Details"]
                if len(prodetails)>0:
                    for val in prodetails:
                        if val["ProductCode"] == procode or ":" not in procode or proname == val["ProductName"]:
                            return Response(
                            response=json.dumps({"Message": "Data is Invalid"}),
                            status=422,
                            mimetype="application/json"
                        )
                            break
                    else:
                        prodetails.append({
                            "ProductId":len(prodetails)+1,
                            "ProductName":proname,
                            "ProductCode":procode,
                            "ProductPrice":proprice,
                        })
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                else:
                    prodetails.append({
                            "ProductId":len(prodetails)+1,
                            "ProductName":proname,
                            "ProductCode":procode,
                            "ProductPrice":proprice,
                        })
                file.seek(0)
                json.dump(json_data,file,indent=4)
            return Response(
                        response=json.dumps({"Message": "valid"}),
                        status=200,
                        mimetype="application/json"
                    )

        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <----------------------------------- Addproduct Route Start Ends ---------------------->

# <---------------------------------- Product Details Page Route ------------------------->
@app.route("/product_details")
def product_details():
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        prodata = json_data["Product_Details"]
        data = CheckExe()
    return render_template("product_details.html",org_data=prodata,checkexe=data)
# <---------------------------------- ends ---------------------------------------------->

# <---------------------- Product View Route Start ----------------------------------------->
@app.route("/View/Product/<id>")
def VieWProduct(id):
    try:
        pro_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            prodetails=json_object["Product_Details"]
            for val in range(len(prodetails)):
                if int(pro_id) == prodetails[val]["ProductId"]:
                    data = prodetails[val]
                    break
        newdata = CheckExe()
        return render_template("product.html",data=data,checkexe=newdata)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
            f.close()
# <---------------------- Product View Route Ends ------------------------------------------>

# <------------------- Edit Product route Start ------------------------------------->
@app.route("/Edit_Product/<id>")
def Edit_Product(id):
    try:
        pro_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            prodetails=json_object["Product_Details"]
            for val in range(len(prodetails)):
                if int(pro_id) == prodetails[val]["ProductId"]:
                    data = prodetails[val]
                    break
        newdata = CheckExe()
        return render_template("product.html",edit=data,data=0,checkexe=newdata)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
        f.close()
# <------------------ Edit Product route Ends --------------------------------------->

# <------------------ Change Product Data Route Start ------------------------------->
@app.route("/Edit_Add_Product_data",methods=["GET","POST"])
def Edit_Add_Product_data():
    if request.method == "POST":
        try:
            proid = request.form.get("id")
            proname = request.form.get("proname")
            procode = request.form.get("procode")
            proprice = request.form.get("proprice")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                prodetails = json_data["Product_Details"]
                for val in prodetails:
                    if  val["ProductId"] == int(proid):
                        val["ProductName"] = proname 
                        val["ProductCode"] = procode
                        val["ProductPrice"] = proprice 
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=201,
                        mimetype="application/json"
                    )
                    break                
        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <-----------------  Change Product Data Route Ends -------------------------------->

# <----------------- Product Data Delete Route Start ------------------------------->
@app.route("/delete/Product/",methods=["GET","POST"])
def delete_product():
    if request.method == "POST":
        try:
            id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                prodetails=json_data["Product_Details"]
                for val in range(len(prodetails)):
                    if int(id) == prodetails[val]["ProductId"]:
                        del prodetails[val]
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
                return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <----------------- Product Data Delete Route Ends -------------------------------->

###################################### Product Management Section Ends ########################

##################################### Stock Management Section Start ##########################
# <--------------------------------- Stock Party Data Page ----------------------------------->
@app.route("/StockParty")
def StockParty():
    try:
        with open("details.json","r+") as f:
            json_data = json.loads(f.read())
            party_details = json_data["Party_Details"]
            data = CheckExe()
            if len(party_details)>0:
                return render_template("stock_party.html",details = party_details,checkexe=data)
            else:
                return render_template("stock_party.html",checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Conatact Your Administrator"
        })
    finally:
        f.close()
# <--------------------------------- Stock Party Data Page Ends----------------------------------->

# <-------------------------------- Add Stock Party Data ------------------------------------->
@app.route("/PartyDetailsAdd",methods=["GET","POST"])
def PartyDetailsAdd():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            party_date = request.form.get("date")
            email = request.form.get("email")
            address = request.form.get("address")
            number = request.form.get("number")
            gstin = request.form.get("gstin")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                party_details = json_data["Party_Details"]
                if len(party_details)>0:
                    Party_Emails = [emails["Party_Email"] for emails in json_data["Party_Details"]]
                    Party_Numbers = [number["Party_Number"] for number in json_data["Party_Details"]]
                    Party_GSTIN = [gstin["Party_GSTIN"] for gstin in json_data["Party_Details"]]
                    if email not in Party_Emails:
                        if number not in Party_Numbers:
                            if gstin not in Party_GSTIN:
                                party_details.append({
                                    "Id":len(party_details)+1,
                                    "Party_Name":name,
                                    "Party_Deliver_Date":party_date,
                                    "Party_Email":email,
                                    "Party_Address":address,
                                    "Party_Number":number,
                                    "Party_GSTIN":gstin
                                })
                                file.seek(0)
                                json.dump(json_data,file,indent=4)
                                file.truncate()
                                return jsonify({"details":"Success"})
                            else:
                                return jsonify({"details":"GSTIN Exist"})
                        else:
                            return jsonify({"details":"Mobile Exist"})
                    else:
                        return jsonify({"details":"Email Exist"})
                else:
                    party_details.append({
                    "Id":1,
                    "Party_Name":name,
                    "Party_Deliver_Date":party_date,
                    "Party_Email":email,
                    "Party_Address":address,
                    "Party_Number":number,
                    "Party_GSTIN":gstin
                    })
                    file.seek(0)
                    file.truncate()
                    json.dump(json_data,file,indent=4)
                    return jsonify({"details":"Success"}) 
    except Exception as e:
        print("Error = ",e)
        return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
        )
    finally:
        file.close()
# <-------------------------------- Add Stock Party Data Ends------------------------------------->

# <------------------------------- Party Details Page ----------------------------------------->
@app.route("/Party_Details")
def Party_Details():
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        party_data = json_data["Party_Details"]
        data = CheckExe()
    return render_template("party_details.html",org_data=party_data,checkexe=data)
# <------------------------------- Party Details Page Ends ------------------------------------>

# <---------------------- Party View Route Start ----------------------------------------->
@app.route("/View/Party/<id>")
def VieWParty(id):
    try:
        pro_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            party_data=json_object["Party_Details"]
            for val in range(len(party_data)):
                if int(pro_id) == party_data[val]["Id"]:
                    data = party_data[val]
                    break
        newdata = CheckExe()
        return render_template("stock_party.html",data=data,checkexe=newdata)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
            f.close()
# <---------------------- Party View Route Ends ------------------------------------------>

# <------------------- Edit Party route Start ------------------------------------->
@app.route("/Edit_Party/<id>")
def Edit_Party(id):
    try:
        pro_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            party_data=json_object["Party_Details"]
            for val in range(len(party_data)):
                if int(pro_id) == party_data[val]["Id"]:
                    data = party_data[val]
                    break
        newdata = CheckExe()
        return render_template("stock_party.html",edit=data,data=0,checkexe=newdata)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to Adminstrator"
        })
    finally:
        f.close()
# <------------------ Edit Party route Ends --------------------------------------->

# <------------------ Change Party Data Route Start ------------------------------->
@app.route("/Edit_Add_Party_data",methods=["GET","POST"])
def Edit_Add_Party_data():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            party_date = request.form.get("date")
            email = request.form.get("email")
            address = request.form.get("address")
            number = request.form.get("number")
            gstin = request.form.get("gstin")
            proid = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                party_details = json_data["Party_Details"]
                for val in party_details:
                    if  val["Id"] == int(proid):
                        val["Party_Name"] = name 
                        val["Party_Deliver_Date"] = party_date
                        val["Party_Email"] = email 
                        val["Party_Address"] = address 
                        val["Party_Number"] = number 
                        val["Party_GSTIN"] = gstin
                        file.seek(0)
                        json.dump(json_data,file,indent=4)
                        file.truncate()
                        return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=201,
                        mimetype="application/json"
                    )
                    break                
        except Exception as e:
            print("Error = ",e)
            return Response(
                        response=json.dumps({"Message": "Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
        finally:
            file.close()
# <-----------------  Change Party Data Route Ends -------------------------------->

# <----------------- Party Data Delete Route Start ------------------------------->
@app.route("/delete/Party/",methods=["GET","POST"])
def delete_party():
    if request.method == "POST":
        try:
            id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                party_details = json_data["Party_Details"]
                for val in range(len(party_details)):
                    if int(id) == party_details[val]["Id"]:
                        del party_details[val]
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
                return Response(
                        response=json.dumps({"Message": "Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
        except Exception as e:
            print("Error = ",e)
            return Response(
                response=json.dumps({"Message": "Internal Server Error"}),
                status=500,
                mimetype="application/json"
            )
        finally:
            file.close()
# <----------------- Party Data Delete Route Ends -------------------------------->

# <--------------------------------- Add Stock Route Page ----------------------------------->
@app.route("/AddStock")
def AddStock():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            Party_Details = json_data["Party_Details"]
            data = CheckExe()
        return render_template("add_stock.html",data=Party_Details,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact your administrator"
        })
    finally:
        file.close()
# <---------------------------------- Add Stock Route Ends --------------------------------------------------> 

# <---------------------------------- Stock Data Add Route ----------------------------->
@app.route("/Stockdata",methods=["GET","POST"])
def Stockdata():
    if request.method == "POST":
        party_name = request.form.get("party_name")
        products = request.form.getlist("data1[]")
        quantity = request.form.getlist("data2[]")
        price = request.form.getlist("data3[]")
        ammount = request.form.getlist("data4[]")
        pack_type = request.form.get("pack_type")
        amm_paid = request.form.get("amm_paid")
        amm_due = request.form.get("amm_due")
        mode = request.form.get("mode")
        unit = request.form.get("unit")
        discount = request.form.get("discount")
        tax = request.form.get("tax")
        taxamm = request.form.get("tax_amm")
        grandtotal = request.form.get("total")
        now = datetime.now()
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            sales = json_data["Add_Stock_Data"]
            if len(sales)>0:
                for val in range(len(sales)):
                    if party_name == sales[val]["Party_Name"]:
                        rem_pay = round(float(sales[val]["Ammount_Due"]) + float(sales[val]["Previous_Ammount"]),2)
                        for val1 in range(len(sales[val]["AddData"])):
                            if sales[val]["AddData"][val1]["ProductName"].split(":")[0] in products:
                                ind = products.index(sales[val]["AddData"][val1]["ProductName"].split(":")[0])
                                sales[val]["AddData"][val1]["Quantity"] = quantity[ind]
                                sales[val]["AddData"][val1]["Price"] = price[ind]
                                sales[val]["AddData"][val1]["Ammount"] = ammount[ind]
                                products.pop(ind)
                                quantity.pop(ind)
                                price.pop(ind)
                                ammount.pop(ind)
                        if len(products)>0:
                            for new in range(len(products)):
                                sales[val]["AddData"].append({
                                    "ProductName":products[new] + ":" + str(val),
                                    "Quantity":quantity[new],
                                    "Price":price[new],
                                    "Ammount":ammount[new]
                                })
                        sales[val].update({
                            "Package_Type":pack_type,
                            "Unit":unit,
                            "Discount":discount,
                            "GrandTotal":grandtotal,
                            "Ammount_Paid":amm_paid,
                            "Ammount_Due":amm_due,
                            "Mode":mode,
                            "Tax":tax,
                            "TaxAmmount":taxamm,
                            "Party_Deliver_Date":now.strftime("%Y-%m-%d"),
                            "Previous_Ammount":rem_pay
                        })
                if party_name not in [sales[val]["Party_Name"] for val in range(len(sales))]:
                    sales.append({
                    "Party_Name":party_name,
                    "AddData":[],
                    "Package_Type":pack_type,
                    "Unit":unit,
                    "Discount":discount,
                    "GrandTotal":grandtotal,
                    "Ammount_Paid":amm_paid,
                    "Ammount_Due":amm_due,
                    "Mode":mode,
                    "Tax":tax,
                    "TaxAmmount":taxamm,
                    "Party_Deliver_Date":now.strftime("%Y-%m-%d"),
                    "Previous_Ammount":"0"
                })
                    for val in range(len(products)):
                        sales[-1]["AddData"].append({
                            "ProductName":products[val] +":" +str(len(sales)-1),
                            "Quantity":quantity[val],
                            "Price":price[val],
                            "Ammount":ammount[val]
                        })             
                file.seek(0)
                file.truncate()
                json.dump(json_data,file,indent=4)
            else:
                sales.append({
                    "Party_Name":party_name,
                    "AddData":[],
                    "Package_Type":pack_type,
                    "Unit":unit,
                    "Discount":discount,
                    "GrandTotal":grandtotal,
                    "Ammount_Paid":amm_paid,
                    "Ammount_Due":amm_due,
                    "Mode":mode,
                    "Tax":tax,
                    "TaxAmmount":taxamm,
                    "Party_Deliver_Date":now.strftime("%Y-%m-%d"),
                    "Previous_Ammount":"0"
                })
                for val in range(len(products)):
                    print("Enter in Loop")
                    sales[0]["AddData"].append({
                        "ProductName":products[val] +":" +"0",
                        "Quantity":quantity[val],
                        "Price":price[val],
                        "Ammount":ammount[val]
                    })
                print("Final Sales = ",sales)
                file.seek(0)
                file.truncate()
                json.dump(json_data,file,indent=4)
        return jsonify({"Message":"Success"})
# <---------------------------------- Stock Data Add Route Ends----------------------------->

# <-----------------------------------Add ingredients Page Route---------------------------->
@app.route("/AddIngredients")
def AddIngredients():
    try:
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            new_data1 = json_object["Product_Details"]
            data = CheckExe()
        return render_template("add_ingredients.html",values=new_data1,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact your administrator"
        })
# <-----------------------------------Add ingredients Page Route Ends ---------------------->

@app.route("/StockMaster",methods=["GET","POST"])
def StockMaster():
    try:
        if request.method=="POST":
            final=request.form.get('name')
            data1=request.form.getlist('data[]')
            data2=request.form.getlist('data1[]')
            data3=request.form.getlist('data3[]')
            now = datetime.now()
            curr_date = now.strftime("%Y-%m-%d")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                stock_data = json_data["Stock_Details"]
                if len(stock_data) == 0:
                    print("First Condition Match")
                    stock_data.append({
                        "Product_Name":final,
                        "Ingredients":data1,
                        "Quantity":data2,
                        "Unit":data3
                    })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return jsonify({
                        "Result":"Yes"
                    })
                else:
                    print("Second Condition Match")
                    left = []
                    for val in range(len(stock_data)):
                        if final == stock_data[val]["Product_Name"]:
                            if len(data1) > 1:
                                res = list(map(lambda x: x.lower(),stock_data[val]["Ingredients"]))
                                for new in range(len(data1)):

                                    if data1[new].lower() in res:
                                        left.append(data1[new])
                                    else:
                                        stock_data[val]["Ingredients"].append(data1[new])
                                        stock_data[val]["Quantity"].append(data2[new])
                                        stock_data[val]["Unit"].append(data3[new])
                                file.seek(0)
                                json.dump(json_data,file,indent=4)
                                file.truncate()
                                return jsonify({
                                    "Result":left,
                                })
                            else:
                                res = list(map(lambda x: x.lower(),stock_data[val]["Ingredients"]))
                                if data1[0] in res:
                                    left.append(data1[0])
                                    return jsonify({
                                        "Result":left
                                    })
                                else:
                                    stock_data[val]["Ingredients"].append(data1[0])
                                    stock_data[val]["Quantity"].append(data2[0])
                                    stock_data[val]["Unit"].append(data3[0])
                                    file.seek(0)
                                    json.dump(json_data,file,indent=4)
                                    file.truncate()
                                    return jsonify({
                                        "Result":left
                                    })  
    except Exception as e:
        print("Error = ",e)
    finally:
        file.close()
        
# <----------------------------------- Ends Ingredients Route ---------------------------->

# <---------------------------------- Show Ingredients ---------------------------------->
@app.route("/ShowIngredients")
def ShowIngredients():
    with open("details.json","r+") as f:
        json_object=json.loads(f.read())
        new_data1 = json_object["Product_Details"]
        new_data=json_object["Stock_Details"]
        data = CheckExe()
        return render_template("add_ingredients.html",org_data=new_data,values=new_data1,checkexe=data)

# <---------------------------------- Ends Ingredients ----------------------------------->

# <-------------------------------- Expense Data Page Route ------------------------------->
@app.route("/Expense")
def Expense():
    data = CheckExe()
    return render_template("expense.html",checkexe=data)
# <-------------------------------- Ends --------------------------------------------------->

# <------------------------------- Add Expense Data Route -------------------------------->
@app.route("/AddExpense",methods=["GET","POST"])
def AddExpense():
    try:
        if request.method == "POST":
            exp_name = request.form.get("expname")
            exp_price = request.form.get("expprice")
            exp_desc = request.form.get("description")
            now = datetime.now()
            curr_date = now.strftime("%Y-%m-%d")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                json_data["Expense_Details"].append({
                    "Expense_Name":exp_name,
                    "Expense_Price":exp_price,
                    "Expense_Description":exp_desc,
                    "Date":curr_date
                })
                file.seek(0)
                file.truncate()
                json.dump(json_data,file,indent=4)
                return jsonify({"Message":"Success"})
    except Exception as e:
        print("Error = ",e)
    finally:
        file.close()
# <------------------------------- Ends --------------------------------------------------->

# <------------------------------- Stock Report Show Page Route -------------------------->
@app.route("/StockReport")
def StockReport():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            party_name = [party["Party_Name"] for party in json_data["Party_Details"]]
            data = CheckExe()
            return render_template("stock_report.html",data=party_name,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to administrator"
        })
    finally:
        file.close()
# <------------------------------- Ends -------------------------------------------------->

def change_stock_data(arr):
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            stock = json_data["Add_Stock_Data"]
            for val in stock:
                for new in range(len(arr)):
                    for val1 in range(len(val["AddData"])):
                        if arr[new]["ProductName"] == val["AddData"][val1]["ProductName"].split(":")[0]:
                            val["AddData"][val1]["Quantity"] = arr[new]["Quantity"]
                        else:
                            print("No")


            file.seek(0)
            json.dump(json_data,file,indent=4)
            file.truncate()

            
        # print("Data = ",stock)
    except Exception as e:
        print("Error = ",e)

# <------------------------------- Show stock route ------------------------------------>
@app.route("/StockDataReport",methods=["GET","POST"])
def StockDataReport():
    if request.method == "POST":
        from_date = request.form.get("From").split("-")
        to_date = request.form.get("To").split("-")
        duration = request.form.get("Duration")
        sheet_type = request.form.get("Type")
        party_name = request.form.get("Party")
        now = datetime.now()
        curr_date = now.strftime("%Y-%m-%d")
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            sales = json_data["Add_Stock_Data"]
            expense = json_data["Expense_Details"]
            consumption = json_data["Payment_Details"]
            stock = json_data["Add_Stock_Data"]
            data = []
            other = []
            result = []
            result1 = []
            final = []
        if duration == "Today":
            if sheet_type == "SalesSheet":
                for val in range(len(sales)):
                    if party_name == sales[val]["Party_Name"] and curr_date == sales[val]["Party_Deliver_Date"]:
                        data = sales[val]["AddData"]
                        other.append({
                            "Tax":sales[val]["Tax"],
                            "Taxamm":sales[val]["TaxAmmount"],
                            "GrandTotal":sales[val]["GrandTotal"],
                            "Rem":sales[val]["Previous_Ammount"],
                            "Discount":sales[val]["Discount"],
                            "AmmPaid":sales[val]["Ammount_Paid"],
                            "AmmDue":sales[val]["Ammount_Due"],
                            "Pay":float(sales[val]["Ammount_Due"]) + float(sales[val]["Previous_Ammount"])
                        })
                        break
            elif sheet_type == "Expense":
                for val in range(len(expense)):
                    if curr_date == expense[val]["Date"]:
                        data.append(expense[val])
            else:
                for val in consumption:
                    for val1 in range(len(val["Product"])):
                        result.append({
                            "ProductName":val["Product"][val1],
                            "Quantity":val["Quantity"][val1]
                        })
                for val in stock:
                    for val1 in range(len(val["AddData"])):
                        result1.append({
                            "ProductName":val["AddData"][val1]["ProductName"].split(":")[0],
                            "Quantity":val["AddData"][val1]["Quantity"]
                        })
                for val in range(len(result1)):
                    for val1 in result:
                        if result1[val]["ProductName"] == val1["ProductName"]:
                            final.append({
                                "ProductName":val1["ProductName"],
                                "UseQuantity":val1["Quantity"],
                                "Remaining":int(result1[val]["Quantity"]) - int(val1["Quantity"])
                            })
                            result1[val]["Quantity"] = str(int(result1[val]["Quantity"]) - int(val1["Quantity"]))
            # print("Result = ",result)
            # print("Result1 = ",result1)

            change_stock_data(result1)

        else:
            if sheet_type == "SalesSheet":
                y1,m1,d1 = from_date[0],from_date[1],from_date[2]
                y2,m2,d2 = to_date[0],to_date[1],to_date[2]
                sdate = date(int(y1),int(m1),int(d1))
                edate = date(int(y2),int(m2),int(d2))   
                delta = edate - sdate    
                day = []   
                for i in range(delta.days + 1):
                    day.append(str(sdate + timedelta(days=i)))
                for val in range(len(sales)):
                    if party_name == sales[val]["Party_Name"] and sales[val]["Party_Deliver_Date"] in day:
                        data = sales[val]["AddData"]
                        other.append({
                            "Tax":sales[val]["Tax"],
                            "Taxamm":sales[val]["TaxAmmount"],
                            "GrandTotal":sales[val]["GrandTotal"],
                            "Rem":sales[val]["Previous_Ammount"],
                            "Discount":sales[val]["Discount"],
                            "AmmPaid":sales[val]["Ammount_Paid"],
                            "AmmDue":sales[val]["Ammount_Due"],
                            "Pay":float(sales[val]["Ammount_Due"]) + float(sales[val]["Previous_Ammount"])
                        })
                        break
            elif sheet_type == "Expense":
                y1,m1,d1 = from_date[0],from_date[1],from_date[2]
                y2,m2,d2 = to_date[0],to_date[1],to_date[2]
                sdate = date(int(y1),int(m1),int(d1))
                edate = date(int(y2),int(m2),int(d2))   
                delta = edate - sdate    
                day = []   
                for i in range(delta.days + 1):
                    day.append(str(sdate + timedelta(days=i)))
                for val in range(len(expense)):
                    if expense[val]["Date"] in day:
                        data.append(expense[val])
            else:
                for val in consumption:
                    for val1 in range(len(val["Product"])):
                        result.append({
                            "ProductName":val["Product"][val1],
                            "Quantity":val["Quantity"][val1]
                        })
                for val in stock:
                    for val1 in range(len(val["AddData"])):
                        result1.append({
                            "ProductName":val["AddData"][val1]["ProductName"].split(":")[0],
                            "Quantity":val["AddData"][val1]["Quantity"]
                        })
                for val in range(len(result1)):
                    for val1 in result:
                        if result1[val]["ProductName"] == val1["ProductName"]:
                            final.append({
                                "ProductName":val1["ProductName"],
                                "UseQuantity":val1["Quantity"],
                                "Remaining":int(result1[val]["Quantity"]) - int(val1["Quantity"])
                            })
        return jsonify({"Mess":data,"Type":sheet_type,"Other":other,"con":final})
# <-------------------------------- Ends ---------------------------------------------->

# <------------------------------- Clear Due Route ------------------------------------>
@app.route("/ClearDue",methods=["GET","POST"])
def ClearDue():
    try:
        if request.method == "POST":
            party_name = request.form.get("party")
            due_amm = request.form.get("amm")
            due_amm = float(due_amm)
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                stock = json_data["Add_Stock_Data"]
                for val in range(len(stock)):
                    if party_name == stock[val]["Party_Name"]:
                        due = float(stock[val]["Ammount_Due"])
                        if int(due_amm) == int(due):
                            stock[val]["Ammount_Due"] = "0"
                            stock[val]["Ammount_Paid"] = stock[val]["GrandTotal"]
                            due_amm = "0"
                            break
                        else:
                            stock[val]["Ammount_Due"] = float(stock[val]["Ammount_Due"]) - due_amm
                            stock[val]["Ammount_Paid"] = int(stock[val]["Ammount_Paid"]) + int(due_amm)
                            break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                response=json.dumps({"Message": due_amm}),
                status=200,
                mimetype="application/json"
            )            
    except Exception as e:
        print("Error = ",e)
    finally:
        file.close()
# <------------------------------- Ends ------------------------------------------------>
##################################### Stock Management Section Ends ##########################

#################################### Invoice Section Start ##################################

# <-------------------------------- Create Invoice Page Route ------------------------------>
@app.route("/Invoice")
def Invoice():
    try:
        with open("details.json","r+") as file:
            json_object=json.loads(file.read())
            product_data = json_object["Product_Details"]
            data = CheckExe()
        return render_template("invoice.html",org_data=product_data,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()
# <-------------------------------- Ends ---------------------------------------------------->

# <------------------------------- Autocomplete Name ---------------------------------------->
@app.route("/invoice/invoice_autocomplete",methods=["POST"])
def Autocomplete():
    try:
        data=request.get_json(force=True)
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            cus_detail=json_object["Customer_Details"]
            result=[]
            for val in range(len(cus_detail)):
                if data['words'] in cus_detail[val]["CustomerName"] or data['words'] in cus_detail[val]["WhatsApp"]:
                    result.append(cus_detail[val])
        return jsonify({"Result":result})
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Mesage":"Contact your administrator"
        })
    finally:
        f.close()
# <------------------------------- Ends ----------------------------------------------------->

# <------------------------------- Product Add in Invoice ---------------------------------->
@app.route("/Invoice/Product")
def productdata():
    try:
        pro=request.args.get("pro")
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            new_data=json_object["Product_Details"]
            pro_list=[]
            for val in range(len(new_data)):
                if pro == new_data[val]["ProductName"]:
                    pro_list.append(new_data[val])
            return jsonify({"Result":pro_list})
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Mesage":"Contact your administrator"
        })
    finally:
        f.close()
# <------------------------------- Ends ---------------------------------------------------->

# <------------------------------- Payment Data Route --------------------------------------->
@app.route("/Payment",methods=["GET","POST"])
def Payment():
    try:
        if request.method=="POST":
            name=request.form.get("name")
            address=request.form.get("address")
            mobile=request.form.get("mobile")
            email=request.form.get("email")
            date=request.form.get("date")
            month=request.form.get("month")
            year=request.form.get("year")
            charge=request.form.get("charge")
            payment_mode=request.form.get("mode")
            data1=request.form.getlist('data1[]')
            data2=request.form.getlist('data2[]')
            data3=request.form.getlist('data3[]')
            data4=request.form.getlist('data4[]')
            subtotal=request.form.get("subtotal")
            tax=request.form.get("tax")
            taxammount=request.form.get("taxammount")
            grandtotal=request.form.get("GrandTotal")
            gst=request.form.get("GST")
            m,d,y=request.form.get("fulldate").split("/")
            fulldate=y + "-" + m + "-" + d
            if charge:
                pass
            else:
                charge = 0

            with open("details.json","r+") as f:
                json_object=json.loads(f.read())
                new_data=None
                exename=None
                cusid=None
                count=0
                cus_detail=json_object["Customer_Details"]
                names=[cus_detail[i]["CustomerName"] for i in range(len(cus_detail))]
                if len(cus_detail)>0:
                    if name not in names:
                        cus_detail.append({  
                            "ExecutiveName":"Self",
                            "CustomerName":name,
                            "CustomerId":len(cus_detail)+1,
                            "FatherName":"",
                            "Address":address,
                            "Mobile":mobile,
                            "WhatsApp":mobile,
                            "Email":email,
                            "Gender":"Person"
                        })
                        f.seek(0)
                        f.truncate()
                        json.dump(json_object,f,indent=4)
                else:
                    cus_detail.append({  
                        "ExecutiveName":"Self",
                        "CustomerName":name,
                        "CustomerId":len(cus_detail)+1,
                        "FatherName":"",
                        "Address":address,
                        "Mobile":mobile,
                        "WhatsApp":mobile,
                        "Email":email,
                        "Gender":"Person"
                    })
                    f.seek(0)
                    f.truncate()
                    json.dump(json_object,f,indent=4)

                for val in range(len(cus_detail)):
                    if cus_detail[val]["CustomerName"] in name:
                        exename =cus_detail[val]["ExecutiveName"]
                        cusid=cus_detail[val]["CustomerId"]
                new_data=json_object["Payment_Details"]
                if(len(new_data)>0):
                    count+=len(new_data)
                    new_data.append({
                            "Id":str(len(new_data)+1),
                            "Name":name,
                            "Executive":exename,
                            "CustomerId":cusid,
                            "Address":address,
                            "Mobile":mobile,
                            "Email":email,
                            "Date":date,
                            "Month":month,
                            "Year":year,
                            "FullDate":fulldate,
                            "PaymentMode":payment_mode,
                            "PaymentStatus":"pending",
                            "Product":data1,
                            "Quantity":data2,
                            "Price":data3,
                            "Ammount":data4,
                            "DeliveryCharge":charge,
                            "GST":gst,
                            "Tax":tax,
                            "TaxAmmount":str(round(float(taxammount),3)),
                            "SubTotal":str(round(float(subtotal),3)),
                            "GrandTotal":str(round(float(grandtotal),3))
                        })
                    f.seek(0)
                    f.truncate()
                    json.dump(json_object,f,indent=4)
                else:
                    count=0
                    new_data=[
                        {
                        "Id":"1",
                        "Name":name,
                        "Executive":exename,
                        "CustomerId":cusid,
                        "Address":address,
                        "Mobile":mobile,
                        "Email":email,
                        "Date":date,
                        "Month":month,
                        "Year":year,
                        "FullDate":fulldate,
                        "PaymentMode":payment_mode,
                        "PaymentStatus":"pending",
                        "Product":data1,
                        "Quantity":data2,
                        "Price":data3,
                        "Ammount":data4,
                        "DeliveryCharge":charge,
                        "GST":gst,
                        "Tax":tax,
                        "TaxAmmount":str(round(float(taxammount),3)),
                        "SubTotal":str(round(float(subtotal),3)),
                        "GrandTotal":str(round(float(grandtotal),3))
                    }
                    ]
                    f.seek(0)
                    f.truncate()
                    json_object["Payment_Details"]=new_data
                    json.dump(json_object,f,indent=4)
                    print("Payment = ",new_data)
                
            return jsonify({"Result":new_data[count]["Id"]})
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()
# <------------------------------- Ends ---------------------------------------------------->

# <---------------------------------- Show Invoice Route ---------------------------------->
@app.route("/invoice/showInvoice/")
def make_payment():
    try:
        user=request.args.get("id")
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            new_data=json_object["Payment_Details"]
            inv_id=None
            cusname=None
            address=None
            mobile=None
            date=None
            month=None
            year=None
            product=None
            quantity=None
            price=None
            amm=None
            tax=None
            subtotal=None
            grand=None
            taxammount=None
            full=None
            email=None
            length=None
            charge=None
            for val in range(len(new_data)):
                if user==new_data[val]["Id"]:
                    inv_id=new_data[val]["Id"]
                    cusname=new_data[val]["Name"]
                    address=new_data[val]["Address"]
                    email=new_data[val]["Email"]
                    mobile=new_data[val]["Mobile"]
                    date=new_data[val]["Date"]
                    month=new_data[val]["Month"]
                    year=new_data[val]["Year"]
                    product=new_data[val]["Product"]
                    quantity=new_data[val]["Quantity"]
                    price=new_data[val]["Price"]
                    amm=new_data[val]["Ammount"]
                    tax=new_data[val]["Tax"]
                    taxammount=new_data[val]["TaxAmmount"]
                    subtotal=new_data[val]["SubTotal"]
                    grand=new_data[val]["GrandTotal"]
                    charge=new_data[val]["DeliveryCharge"]
                    length=[i+1 for i in range(len(product))]
                    print("Id = ",inv_id)
        newdata = CheckExe()
        return render_template("invoice_print.html",inv_id=inv_id,name=cusname,add=address,mob=mobile,date=date,month=month,year=year,product=product,tax=tax,taxam=taxammount,sub=subtotal,total=grand,emails=email,quan=quantity,price=price,amm=amm,length=length,charge=charge,checkexe=newdata)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()
# <------------------------------------ Ends ---------------------------------------------->

# <------------------------------- Payment Success Route ----------------------------------->

@app.route("/Invoice/Payment/Success")
def Success():
    try:
        id=request.args.get("pro")
        print("ID = ",id)
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            new_data=json_object["Payment_Details"]
            for val in range(len(new_data)):
                if id == new_data[val]["Id"]:
                    new_data[val]["PaymentStatus"] = "Success"
                    f.seek(0)
                    f.truncate()
                    json_object["Payment_Details"] = new_data
                    json.dump(json_object,f,indent=4)
        data = CheckExe()
        return render_template("invoice_print.html",checkexe=data)
    except Exception as e:
        print("Error in Id = ",e)
    finally:
        f.close()
# <-------------------------------- Ends --------------------------------------------------->

# <----------------------------------- Bill Print Route ----------------------------------->
@app.route("/print_bill/<int:id>")
def print_bill(id):
    try:
        cus_id=id
        customer_ids=[]
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            details=[]
            tax=0
            total=0
            sgst=0
            quan_sum=[]
            name=None
            mobile=None
            msg=""
            prev_amm=0
            payment=json_object["Payment_Details"]
            for val in range(len(payment)):
                if payment[val]["PaymentStatus"] == "pending" and payment[val]["Id"]!=str(cus_id):
                    customer_ids.append({
                        "cus_id":payment[val]["CustomerId"],
                        "total":payment[val]["GrandTotal"]
                    })
            for val in range(len(payment)):
                if cus_id==int(payment[val]["Id"]):
                    cus_ids=payment[val]["CustomerId"]
                    name=payment[val]["Name"]
                    mobile=payment[val]["Mobile"]
                    charge=payment[val]["DeliveryCharge"]
                    for val1 in range(len(payment[val]["Product"])):
                        quan_sum.append(int(payment[val]["Quantity"][val1]))
                        details.append({
                            "Id":val1+1,
                            "Product":payment[val]["Product"][val1].split(":")[0],
                            "Quantity":payment[val]["Quantity"][val1],
                            "Price":payment[val]["Price"][val1],
                            "Ammount":payment[val]["Ammount"][val1]
                        })
                    if payment[val]["PaymentStatus"] == "Success":
                        msg="Success"
                    else:
                        msg="Pending"  
                    sub=payment[val]["SubTotal"]
                    tax=payment[val]["Tax"]
                    taxammount = payment[val]["TaxAmmount"]
                    sgst=int(payment[val]["Tax"])/2
                    total=payment[val]["GrandTotal"]
                    for val in range(len(customer_ids)):
                        if customer_ids[val]["cus_id"] == cus_ids:
                            prev_amm+=float(customer_ids[val]["total"])

                    subtotal=float(total)+prev_amm
                    print("Prev = ",prev_amm)
                    print("Message = ",msg)
        if charge:
            newtotal = float(total) + float(charge)
        else:
            newtotal = subtotal   
        data = CheckExe()         
        return render_template("bill_payment.html",org_data=details,tax=tax,sgst=sgst,total=total,sub=sub,quan=sum(quan_sum),item=len(details),name=name,taxm=taxammount,mobile=mobile,cus=cus_id,msg=num2word.word(int(newtotal)),msgs=msg,prev=round(prev_amm,3),charge=charge,newtotal=newtotal,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Adminitrator"
        })
    finally:
        f.close()
# <----------------------------------- Ends ----------------------------------------------->

# <---------------------------------- View Invoice Route Start ---------------------------->
@app.route("/ViewInvoice")
def ViewInvoice():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            cus_data = json_data["Customer_Details"]
            data = CheckExe()
        return render_template("view_invoice.html",data=cus_data,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Conatact Your Administrator"
        })
    finally:
        file.close()
# <---------------------------------- Ends ------------------------------------------------>

# <------------------------------------- Show Invoice Data ------------------------------->
@app.route("/Invoice/getdata/")
def view_invoice():
    try:
        date1=request.args.get("pro")
        out=list(date1.split(","))
        strat=out[0]
        end=out[1]
        name=out[2]
        duration=out[3]
        exename=out[4]
        m,d,y=out[5].split("/")
        full=y + "-" + m + "-" + d
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            data=None
            new_data=[]
            invoice_details=None
            payment=json_object["Payment_Details"]
            if duration=="Today":
                if payment:
                    for val in range(len(payment)):
                        if full==payment[val]["FullDate"] and name=="All":
                            print("Customers All Condition Match")
                            new_data.append(payment[val])
                        elif full==payment[val]["FullDate"] and name == payment[val]["Name"]:
                            print("Customers With Specific Name Condition Match")
                            new_data.append(payment[val])
            else:
                if payment!=None:
                    for val in range(len(payment)):
                        if name == "All":
                            getdate=payment[val]["FullDate"]
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2-d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            # print(d3)
                            if d3 in all_dates:
                                new_data.append(payment[val])
                            else:
                                pass
                        
                        elif name == payment[val]["Name"]:
                            getdate=payment[val]["FullDate"]
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2 - d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            if d3 in all_dates:
                                new_data.append(payment[val])
                            else:
                                pass
            # print("New Data = ",new_data)
            copy_invoice = []
            for val in range(len(new_data)):
                if new_data[val]["PaymentStatus"] == "Success":
                    copy_invoice.append(new_data[val])
        return jsonify({"Result":copy_invoice})
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()
# <------------------------------------- Ends -------------------------------------------->

#################################### Invoice section Ends ###################################  

################################### Payment Report Section Start ############################
# <---------------------------------- Daybook Section Start ---------------------------->
@app.route("/Daybook")
def Daybook():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            cus_data = json_data["Customer_Details"]
            data = CheckExe()
        return render_template("daybook.html",data=cus_data,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Conatact Your Administrator"
        })
    finally:
        file.close()
# <---------------------------------- Ends --------------------------------------------->

# <------------------------------------ Daybook Data Route -------------------------->
@app.route("/Payment/Daybook/")
def show_payment_report():
    try:
        data1=request.args.get("pro")
        out=list(data1.split(","))
        # print(f"Out is:{out}")
        cus_name=out[2]
        duration=out[3]
        strat=out[0]
        end=out[1]
        y,d,m=out[4].split("-")
        full=y + "-" + d + "-" + m
        # print(f"Full is:{full}")
        exename=out[5]
        invoice_type=out[6]
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            data=None
            new_data=json_object["Payment_Details"]
            new_data1=json_object["Customer_Details"]
            invoice_details=[]
            cus_details=[]   
            if duration=="Today":
                # print("Today")
                if(new_data):
                    for val in range(len(new_data)):
                        if full==new_data[val]["FullDate"] and cus_name=="All" and invoice_type=="All":
                            # print("First Condition")
                            invoice_details.append(new_data[val])
                        elif full==new_data[val]["FullDate"] and cus_name =="All" and invoice_type==new_data[val]["GST"]:
                            # print("Second Condition")
                            invoice_details.append(new_data[val])
                        elif full==new_data[val]["FullDate"] and cus_name in new_data[val]["Name"] and invoice_type=="All":
                            # print("First Condition")
                            invoice_details.append(new_data[val])
                        elif full==new_data[val]["FullDate"] and cus_name in new_data[val]["Name"] and invoice_type==new_data[val]["GST"]:
                            # print("Second Condition")
                            invoice_details.append(new_data[val])
            else:
                if(new_data!=None):
                    for val in range(len(new_data)):
                        if cus_name =="All" and invoice_type=="All":
                            getdate=new_data[val]["FullDate"]
                            # print(getdate)
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2 - d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            if d3 in all_dates:
                                invoice_details.append(new_data[val])
                            else:
                                pass
                        elif cus_name =="All" and invoice_type==new_data[val]["GST"]:
                            getdate=new_data[val]["FullDate"]
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2 - d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            if d3 in all_dates:
                                invoice_details.append(new_data[val])
                            else:
                                pass

                        elif cus_name in new_data[val]["Name"] and invoice_type=="All":
                            getdate=new_data[val]["FullDate"]
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2 - d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            if d3 in all_dates:
                                invoice_details.append(new_data[val])
                            else:
                                pass
                        elif cus_name in new_data[val]["Name"] and invoice_type==new_data[val]["GST"]:
                            getdate=new_data[val]["FullDate"]
                            y2,m2,d2=getdate.split("-")
                            y2,m2,d2=int(y2),int(m2),int(d2)
                            y,m,d=strat.split("-")
                            y1,m1,d1=end.split("-")
                            m,d,y=int(m),int(d),int(y)
                            m1,d1,y1=int(m1),int(d1),int(y1)
                            if len(str(m2))<2:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + "0" + str(m2) + "-" + str(d2)
                            else:
                                if len(str(d2))<2:
                                    d3=str(y2) + "-" + str(m2) + "-" + "0" + str(d2)
                                else:
                                    d3=str(y2) + "-" + str(m2) + "-" + str(d2)
                            d2=date(y1,m1,d1)
                            d1=date(y,m,d)
                            delta = d2 - d1
                            all_dates = []
                            for i in range(delta.days + 1):
                                day = d1 + timedelta(days=i)
                                all_dates.append(str(day))
                            if d3 in all_dates:
                                new_data.append(new_data[val])
                            else:
                                pass
            copy_invoice = []
            for val in range(len(invoice_details)):
                if invoice_details[val]["PaymentStatus"] == "Success":
                    copy_invoice.append(invoice_details[val])
                    
        return jsonify({"Invoice":invoice_details})
    except Exception as e:
        print("Error = ",e)
    finally:
        f.close()
# <------------------------------------ Daybook Data Route Ends ------------------------>

# <---------------------------------- Payment Update Page Route ---------------------->
@app.route("/payment_update")
def payment_update():
    data = CheckExe()
    return render_template("payment_update.html",checkexe=data)
# <---------------------------------- Ends ------------------------------------------>

# <------------------------------------ Update Payment Status------------------------->
@app.route("/update_payment",methods=["GET","POST"])
def update_payment():
    try:
        if request.method=="POST":
            invoice_id=request.form.get("invoicelabel")
            with open("details.json","r+") as f:
                json_object=json.loads(f.read())
                data1=None
                prop = "alert alert-info"
                data2="Payment Status already Success"
                payment=json_object["Payment_Details"]
                for val in range(len(payment)):
                    if invoice_id==payment[val]["Id"]:
                        # print("Yes")
                        if payment[val]["PaymentStatus"]=="Success":
                            # print("yes")
                            data2="Payment Status already Success"
                            data1=2
                            # print(data2)
                            break
                        else:
                            data1=1
                            f.seek(0)
                            f.truncate()
                            json_object["Payment_Details"][val]["PaymentStatus"]="Success"
                            json.dump(json_object,f,indent=4)
                    else:
                        data2="Invoice Id is Not Present."
            data = CheckExe()
            return render_template("payment_update.html",data1=data1,prop=prop,data2=data2,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()
# <------------------------------------Ends ------------------------------------------>

######################## Payment Section Ends ####################################################  

###################################### Email Management Start #############################

# <---------------------------------- Notice Page Start ----------------------------------->
@app.route("/Notice")
def Notice():
    data = CheckExe()
    return render_template("notice.html",checkexe=data)
# <---------------------------------- Notice Page Ends ------------------------------------->

# <------------------------------- Add Notice Route Start ---------------------------------->
@app.route("/AddNotice",methods=['GET','POST'])
def AddNotice():
    try:
        if request.method == "POST":
            notice_name = request.form.get("notice")
            sub = request.form.get("sub")
            mess = request.form.get("mess")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                notice_details = json_data["Notice_Details"]
                if(len(notice_details)>0):
                    all_notice_name = [name["Notice_Name"] for name in notice_details]
                    if notice_name in all_notice_name:
                        return Response(
                            response=json.dumps({"Message":"Data is Invalid"}),
                            status=422,
                            mimetype="application/json"
                        )
                    else:
                        notice_details.append({
                            "Id":len(notice_details)+1,
                            "Notice_Name":notice_name,
                            "Subject":sub,
                            "Body":mess
                        })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return Response(
                            response=json.dumps({"Message": "Data is Valid"}),
                            status=201,
                            mimetype="application/json"
                        )
                else:
                    notice_details.append({
                            "Id":len(notice_details)+1,
                            "Notice_Name":notice_name,
                            "Subject":sub,
                            "Body":mess
                        })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return Response(
                            response=json.dumps({"Message": "Data is valid"}),
                            status=201,
                            mimetype="application/json"
                        )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Message": "InterNal Server Error"}),
            status=500,
            mimetype="application/json"
        )
    finally:
        file.close()
# <------------------------------ Ends ----------------------------------------------------->

# <------------------------------------ View All Notice ---------------------------------------->
@app.route("/NoticeDetails")
def NoticeDetails():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            notice_details = json_data["Notice_Details"]
            data = CheckExe()
        return render_template("notice_details.html",org_data=notice_details,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()
# <------------------------------------ Ends ----------------------------------------------->

# <----------------------------------- View Individual Notice ----------------------------->
@app.route('/ViewNotice/<id>')
def ViewNotice(id):
    try:
        notice_id = id
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            notice_details = json_data["Notice_Details"]
            data = CheckExe()
            for val in notice_details:
                if int(notice_id) == val["Id"]:
                    name = val["Notice_Name"]
                    sub = val["Subject"]
                    mess = val["Body"]
                    break
        return render_template("notice.html",name=name,sub=sub,mess=mess,data="True",checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close() 
# <----------------------------------- Ends ----------------------------------------------->

# <------------------------------------ Edit Notice Page Route -------------------------->
@app.route('/EditNotice/<id>')
def EditNotice(id):
    try:
        notice_id = id
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            notice_details = json_data["Notice_Details"]
            data = CheckExe()
            for val in notice_details:
                if int(notice_id) == val["Id"]:
                    name = val["Notice_Name"]
                    sub = val["Subject"]
                    mess = val["Body"]
                    notice_id = val["Id"]
                    break
        return render_template("notice.html",id=notice_id,name=name,sub=sub,mess=mess,edit="True",checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close() 
# <------------------------------------- Ends ------------------------------------------>

# <------------------------------------ Add Edit Notice Data ------------------------------>
@app.route("/Edit_Add_data_Notice",methods=["GET","POST"])
def Edit_Add_data_Notice():
    try:
        if request.method == "POST":
            notice_name = request.form.get("notice")
            sub = request.form.get("sub")
            mess = request.form.get("mess")
            notice_id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                notice_details = json_data["Notice_Details"]
                for val in notice_details:
                    if int(notice_id) == val["Id"]:
                        val["Notice_Name"] = notice_name
                        val["Subject"] = sub
                        val["Body"] = mess
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                response=json.dumps({"Message":"Data is valid"}),
                status=201,
                mimetype="application/json"
            )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Message":"Internal Server Error"}),
            status=500,
            mimetype="application/json"
        )
    finally:
        file.close()
# <------------------------------------ Ends ---------------------------------------------->

# <--------------------------------- Delete Notice Route ------------------------------->
@app.route("/DeleteNotice",methods=["GET","POST"])
def DeleteNotice():
    try:
        if request.method == "POST":
            notice_id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                notice_details = json_data["Notice_Details"]
                for val in range(len(notice_details)):
                    if int(notice_id) == notice_details[val]["Id"]:
                        del notice_details[val]
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                response=json.dumps({"Message":"Data is valid"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Message":"Internal Server Error"}),
            status=500,
            mimetype="application/json"
        )
    finally:
        file.close()

# <--------------------------------- Ends ---------------------------------------------->

# <------------------------------------ Compose Page Route ----------------------------->
@app.route("/Compose")
def Compose():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            notice_details = json_data["Notice_Details"]
            customer = json_data["Customer_Details"]
            data = CheckExe()
        return render_template("compose.html",notice=notice_details,cus=customer,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()
# <------------------------------------ Ends ------------------------------------------> 

# <------------------------------- Fetch Template Data --------------------------------->
@app.route("/fetch/notice",methods=["GET","POST"])
def fetchnotice():
    try:
        if request.method == "POST":
            template = request.form.get("Id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                notice_details = json_data["Notice_Details"]
                sub = ""
                body = ""
                for val in notice_details:
                    if val["Notice_Name"] == template:
                        sub = val["Subject"]
                        body = val["Body"]
                        break
            return jsonify({
                "Result":{"Subject":sub,"Body":body}
            })
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()

# <------------------------------- Ends ------------------------------------------------>

# <----------------------------------- Send Email --------------------------------------->
@app.route("/notice/composenotice",methods=["GET","POST"])
def compose_notice():
    if request.method=="POST":
        cus_name=request.form.get("cus")
        mail_subject=request.form.get("sub")
        mail_body=request.form.get("body")
        name=request.form.get("temp")
        email=request.form.get("email")
        password=request.form.get("pass")
        
        with open('details.json',"r+") as file:
            json_data = json.loads(file.read())
            cus_details = json_data["Customer_Details"]
            notice_details = json_data["Notice_Details"]
            compose_details = json_data["Compose_Details"]
            if cus_name == "All":
                emails = [val["Email"] for val in cus_details if val["Email"] !=""]
                print("Send Emails = ",emails)
                today = date.today()
                try:
                    server=sm.SMTP("smtp.gmail.com",587)
                    server.starttls()
                    server.login(email,password)
                    for i in emails:
                        print("Email = ",i)
                        message=MIMEMultipart()
                        message["From"] = email
                        message["To"]= i
                        message['Subject']= mail_subject
                        message["body"]= mail_body
                        html=f'''
                        <html>
                        <head>
                        </head>
                        <body>
                        <h3>{mail_body}</h3>
                        </body>
                        </html>

                        '''
                        try:
                            part2=MIMEText(html,"html")
                            message.attach(part2)
                            server.sendmail(email,i,message.as_string())
                        except Exception as e:
                            print("Error = ",e)
                        compose_details.append({
                            "Id":len(compose_details) + 1,
                            "Template":name,
                            "Customer":cus_name,
                            "Subject":mail_subject,
                            "Body":mail_body,
                            "Time":datetime.today().strftime("%H:%M:%S %p"),
                            "FullDate":today.strftime("%b-%d-%Y")
                        })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return Response(
                        response=json.dumps({"Message":"Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
                except Exception as e:
                    print("Error = ",e)
                    return Response(
                        response=json.dumps({"Message":"Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
            else:
                emails = [val["Email"] for val in cus_details if val["CustomerName"] == cus_name]
                print("Send Emails = ",emails)
                today = date.today()
                try:
                    server=sm.SMTP("smtp.gmail.com",587)
                    server.starttls()
                    server.login(email,password)
                    for i in emails:
                        print("Email = ",i)
                        message=MIMEMultipart()
                        message["From"] = email
                        message["To"]= i
                        message['Subject']= mail_subject
                        message["body"]= mail_body
                        html=f'''
                        <html>
                        <head>
                        </head>
                        <body>
                        <h3>{mail_body}</h3>
                        </body>
                        </html>

                        '''
                        try:
                            part2=MIMEText(html,"html")
                            message.attach(part2)
                            server.sendmail(email,i,message.as_string())
                        except Exception as e:
                            print("Error = ",e)
                        compose_details.append({
                            "Id":len(compose_details) + 1,
                            "Template":name,
                            "Customer":cus_name,
                            "Subject":mail_subject,
                            "Body":mail_body,
                            "Time":datetime.today().strftime("%H:%M:%S %p"),
                            "FullDate":today.strftime("%b-%d-%Y")
                        })
                    file.seek(0)
                    json.dump(json_data,file,indent=4)
                    file.truncate()
                    return Response(
                        response=json.dumps({"Message":"Data is valid"}),
                        status=200,
                        mimetype="application/json"
                    )
                except Exception as e:
                    print("Error = ",e)
                    return Response(
                        response=json.dumps({"Message":"Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
# <---------------------------------- Ends --------------------------------------------->

# <------------------------------------ View Compose Route --------------------------->
@app.route("/ViewCompose")
def ViewCompose():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            compose_details = json_data["Compose_Details"]
            data = CheckExe()
            return render_template("view_compose.html",compose=compose_details,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()
# <------------------------------------ Ends ----------------------------------------->

# <------------------------------------ See Compose Route ------------------------------>
@app.route("/ViewSendCompose/<id>")
def ViewSendCompose(id):
    try:
        compose_id = id
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            compose_details = json_data["Compose_Details"]
            data = CheckExe()
            for val in compose_details:
                if int(compose_id) == val["Id"]:
                    compose = val
                    break
            return render_template("compose.html",compose=compose,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        file.close()
# <------------------------------------ Ends ------------------------------------------->

# <---------------------------------- Delete Compose Route ------------------------------>
@app.route("/DeleteCompose",methods=["GET","POST"])
def DeleteCompose():
    try:
        if request.method == "POST":
            compose_id = request.form.get("id")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                compose_details = json_data["Compose_Details"]
                for val in range(len(compose_details)):
                    if int(compose_id) == compose_details[val]["Id"]:
                        del compose_details[val]
                        break
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                response=json.dumps({"Message":"Data is valid"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Message":"Internal Server Error"}),
            status=500,
            mimetype="application/json"
        )
    finally:
        file.close()
# <---------------------------------- Ends ---------------------------------------------->
###################################### Email Management Ends ############################## 

###################################### Most Frequent Section Start #########################
# <-------------------------------------- Frequent Customer Route ------------------------>
@app.route("/frequent_customer")
def frequent_customer():
    data = CheckExe()
    return render_template("frequent_customer.html",checkexe=data)
# <-------------------------------------- Ends ------------------------------------------->

# <------------------------------------- Show frequent Csutomer ------------------------>
@app.route("/frequent_customer_data",methods=["GET","POST"])
def frequent_customer_data():
    try:
        if request.method == "POST":
            month = request.form.get("month")
            year = request.form.get("year")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                payment_details = json_data["Payment_Details"]
                frequent_cus = []
                total = 0
                cus_id = ""
                name = ""
                exe = ""
                names = [val['Name'] for val in payment_details]
                unique_names = list(set(names))
                if month == "All" and year == "All":
                    for name in unique_names:
                        for val in payment_details:
                            if name == val['Name']:
                                name = val['Name']
                                cus_id = val['CustomerId']
                                exe = val["Executive"]
                                total += float(val["GrandTotal"])
                        if total:
                            frequent_cus.append({
                                    "Cus_Id":cus_id,
                                    "Cus_Name":name,
                                    "Exe_Name":exe,
                                    "Total":total,
                                    "Visit":names.count(name)
                                })
                        total = 0
                else:
                    new_payment_details = [val for val in payment_details if val['Month'] == month and val['Year'] == 'Year']
                    if len(new_payment_details)>0:
                        for name in unique_names:
                            for val in new_payment_details:
                                if name == val['Name']:
                                    name = val['Name']
                                    cus_id = val['CustomerId']
                                    exe = val["Executive"]
                                    total += float(val["GrandTotal"])
                            if total:
                                frequent_cus.append({
                                        "Cus_Id":cus_id,
                                        "Cus_Name":name,
                                        "Exe_Name":exe,
                                        "Total":total,
                                        "Visit":names.count(name)
                                    })
                            total = 0
                    else:
                        pass
                return Response(
                        response=json.dumps({"Res":frequent_cus}),
                        status=200,
                        mimetype="application/json"
                    )
    except Exception as e:
        print("Error = ",e)
        return Response(
                        response=json.dumps({"Message":"Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
    finally:
        file.close()
# <------------------------------------- Ends ------------------------------------------>

# <-------------------------------------- Frequent Product Route ------------------------>
@app.route("/frequent_product")
def frequent_product():
    data = CheckExe()
    return render_template("frequent_product.html",checkexe=data)
# <-------------------------------------- Ends -------------------------------------------

# <------------------------------------- Show frequent Product ------------------------>
def find_optimize_result(arr):
    result = []
    temp = ""
    for val in range(len(arr)):
        if len(result) == 0:
            result.append(arr[val])
        else:
            for pro in range(len(result)):
                if arr[val]['Name'] == result[pro]['Name']:
                    result[pro]['quantity'] = str(int(result[pro]['quantity']) + int(arr[val]['quantity']))
                    result[pro]['price'] = str(float(result[pro]['price']) + float(arr[val]['price']))
                else:
                    result.append(arr[val])
    return result

@app.route("/frequent_product_data",methods=["GET","POST"])
def frequent_product_data():
    try:
        if request.method == "POST":
            month = request.form.get("month")
            year = request.form.get("year")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                payment_details = json_data["Payment_Details"]
                product = []
                names = []
                result = []
                if month == "All" and year == "All":
                    try:
                        for val in range(len(payment_details)):
                            for pro in range(len(payment_details[val]["Product"])):
                                names.append(payment_details[val]["Product"][pro])
                                product.append({
                                    "Name":payment_details[val]["Product"][pro],
                                    "quantity":payment_details[val]["Quantity"][pro],
                                    "price":payment_details[val]["Price"][pro]
                                })
                    except Exception as e:
                        print("Error = ",e)
                    
                    result = find_optimize_result(product)
                
                    for val in range(len(result)):
                        result[val]["Sold"] = names.count(result[val]['Name'])
                        result[val]["Amm"] = float(result[val]["quantity"]) * float(result[val]["price"])
                else:
                    new_payment_details = [val for val in payment_details if val['Month'] == month and val['Year'] == year]
                    new_payment_details = [new_payment_details[val] for val in range(5)]
                    # print(new_payment_details)
                    if len(new_payment_details)>0:
                        try:
                            for val in new_payment_details:
                                for pro in range(len(val["Product"])):
                                    names.append(val["Product"][pro])
                                    product.append({
                                        "Name":val["Product"][pro],
                                        "quantity":val["Quantity"][pro],
                                        "price":val["Price"][pro]
                                    })
                        except Exception as e:
                            print("Error = ",e)
                        result = find_optimize_result(product)                       
                        # print("Data = ",result)
                        for val in range(len(result)):
                            result[val]["Sold"] = names.count(result[val]['Name'])
                            result[val]["Amm"] = float(result[val]["quantity"]) * float(result[val]["price"])
                    else:
                        return Response(
                            response=json.dumps({"Res":"Too Large"}),
                            status=200,
                            mimetype="application/json"
                    )
                return Response(
                        response=json.dumps({"Res":result}),
                        status=200,
                        mimetype="application/json"
                    )
    except Exception as e:
        print("Error = ",e)
        return Response(
                        response=json.dumps({"Message":"Internal Server Error"}),
                        status=500,
                        mimetype="application/json"
                    )
    finally:
        file.close()
# <------------------------------------- Ends ------------------------------------------
###################################### Ends ################################################  

###################################### Assign Credientials Start ##########################
# <------------------------------- assign credientials page route ---------------------->
@app.route("/crediential")
def crediential():
    try:
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            product_details=json_object["Executive_Details"]
            reg=json_object["Register"]
            data1=0
            full=[]
            name=[]

            if reg!=None:
                for val in range(len(reg)):
                    name.append(reg[val]["Name"])
            if product_details!=None:
                for val in range(len(product_details)):
                    if product_details[val]['ExecutiveName'] not in name:
                        full.append({
                            "Id":product_details[val]["ExecutiveId"],
                            "Name":product_details[val]["ExecutiveName"],
                            "Area":product_details[val]["AreaName"],
                            "What":product_details[val]["WhatsApp"],
                            "data2":0
                        })
                    else:
                        full.append({
                            "Id":product_details[val]["ExecutiveId"],
                            "Name":product_details[val]["ExecutiveName"],
                            "Area":product_details[val]["AreaName"],
                            "What":product_details[val]["WhatsApp"],
                            "data2":1
                        })
                    print("Full = ",full)
        data = CheckExe()
        return render_template("credientials.html",data1=data1,org_data=full,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()

@app.route('/assign/<int:id>')
def assign(id): 
    try:
        exe_id=id
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            execetails=json_object["Executive_Details"]
            Name=None
            emails=None
            for val in range(len(execetails)):
                if exe_id==int(execetails[val]["ExecutiveId"]):
                    Name=execetails[val]["ExecutiveName"]
                    emails=execetails[val]["Email"]
        return render_template("assign.html",emails=emails,name=Name)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact Your Administrator"
        })
    finally:
        f.close()

@app.route("/credentials/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            reg=json_object["Register"]
            if len(reg)>0:
                reg.append({
                    "Id":len(reg)+1,
                    "Name":name,
                    "Email":email,
                    "Password":password
                })
                json_object['Register']=reg
                f.seek(0)
                json.dump(json_object,f,indent=4)
                f.truncate()
            else:
                reg.append({
                    "Id":1,
                    "Name":name
                })
                json_object['Register']=reg
                f.seek(0)
                json.dump(json_object,f,indent=4)
                f.truncate()
        return redirect(url_for('crediential'))

# <------------------------------- ends ------------------------------------------------>

###################################### Ends ###############################################  

##################################### Profile Section #####################################
@app.route("/Profile")
def Profile():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            profile_details = json_data["Profile_Details"]
            data = CheckExe()
        if len(profile_details) == 0:
            return render_template("profile.html",data={},checkexe=data)
        else:
            return render_template("profile.html",data=profile_details[0],checkexe=data)
    except Exception as e:
        print("Error = ",e)
    finally:
        file.close()

@app.route("/Update_Profile",methods=["GET","POST"])
def Update_Profile():
    try:
        if request.method == "POST":
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            passw = request.form.get('passw')
            cpass = request.form.get('cpass')
            mobile = request.form.get('mobile')
            oname = request.form.get('oname')
            gstin = request.form.get('gstin')
            state = request.form.get('state')
            address = request.form.get('address')
            pan = request.form.get('pan')
            district = request.form.get('district')
            gender = request.form.get("gender")
            imgsrc = request.form.get("imgsrc")
            print("SRC = ",imgsrc)
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                profile_details = json_data["Profile_Details"]
                profile_details[0]["FirstName"] = fname
                profile_details[0]["LastName"]=lname
                profile_details[0]["EmailId"]=email
                profile_details[0]["Gender"]=gender
                profile_details[0]["Password"]=passw
                profile_details[0]["ConfirmPassword"]=cpass
                profile_details[0]["OrganizationName"]=oname
                profile_details[0]["GSTIN"]=gstin
                profile_details[0]["PANNumber"]=pan
                profile_details[0]["Registered_Address"]=address
                profile_details[0]["Mobile"]=mobile
                profile_details[0]["State"]=state
                profile_details[0]["District"]=district  
                json_data["Profile_Details"] = profile_details 
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
        return Response(
            response=json.dumps({"Res":"Valid Data"}),
            status=200,
            mimetype="application/json"
        )  
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Res":"Valid Data"}),
            status=200,
            mimetype="application/json"
        )
    finally:
        file.close()

##################################### Ends ################################################ 

###################################### Contact Us Section Start ########################### 

# <------------------------------------- contact Pagr Route ------------------------->
@app.route("/Contact")
def Contact():
    data = CheckExe()
    return render_template("contact_us.html",checkexe=data)
# <--------------------------------------- Ends ---------------------------------------->

# <-------------------------------------- Contact Data Add ------------------------------>
@app.route("/AddContact",methods=["GET","POST"])
def AddContact():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            sub = request.form.get("sub")
            msg = request.form.get("mes")
            with open("details.json","r+") as file:
                json_data = json.loads(file.read())
                contact_details = json_data["Contact_Details"]
                contact_details[0]["Name"] = name
                contact_details[0]["Email"] = email
                contact_details[0]["Subject"] = sub
                contact_details[0]["Message"] = msg
                json_data["Contact_Details"] = contact_details
                file.seek(0)
                json.dump(json_data,file,indent=4)
                file.truncate()
            return Response(
                response=json.dumps({"Res":"Valid Data"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print("Error = ",e)
        return Response(
            response=json.dumps({"Res":"InValid Data"}),
            status=500,
            mimetype="application/json"
        )
    finally:
        file.close()

# <-------------------------------------- Ends ------------------------------------------>

############################################ Ends ##########################################

############################################ StartMap Section ##############################
def find_optimize_chart(arr,Key=None):
    result = []
    temp = ""
    for val in range(len(arr)):
        if len(result) == 0:
            result.append(arr[val])
        else:
            for pro in range(len(result)):
                if arr[val][Key] == result[pro][Key]:
                    result[pro]['Total'] = str(float(result[pro]['Total']) + float(arr[val]['Total']))
                else:
                    result.append(arr[val])
    return result

@app.route("/ShowChart_MonthWise")
def ShowChart_MonthWise():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            payment_details = json_data["Payment_Details"]
            details = []
            for val in payment_details:
                details.append({
                    "Month":val["Month"],
                    "Total":val["GrandTotal"]
                })
        get_name = itemgetter('Month')
        result = [{'label': name, 'y': sum(float(d['Total']) for d in dicts)} for name, dicts in groupby(sorted(details, key=get_name), key=get_name)]
        # result = find_optimize_chart(details,"Month")
        # print("Result = ",result)
        return jsonify({
            "Data":result
        })
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to administrator"
        })
    finally:
        file.close()

@app.route("/ShowChart_YearWise")
def ShowChart_YearWise():
    try:
        
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            payment_details = json_data["Payment_Details"]
            details=[]
            details1 = []
            for val in payment_details:
                details.append({
                    "Year":val["Year"],
                    "Total":val["GrandTotal"]
                })
            for val in payment_details:
                details1.append({
                    "Month":val["Month"],
                    "Total":val["GrandTotal"]
                })
        # print("DETAILS = ",details1)
        result = find_optimize_chart(details,"Year")
        # result1 = find_optimize_chart(details1,"Month")
        # print(result)
        # print(result1)
        return jsonify({
            "Data":result
            # "Data1":result1
        })
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact to administrator"
        })
    finally:
        file.close()
########################################### Ends ########################################### 

########################################## Logout Route #################################
@app.route("/logout")
def logout():    
    try:
        src_file_name="details.json"
        username = getpass.getuser()
        bkp_file_loc=r"C:/Users/{}/Desktop/Backup/".format(username)
        import backup
        backup.take_bkp(src_file_name,"","",bkp_file_loc)
        return render_template("choose.html")
    except Exception as e:
        print("The file you serach is not found in the current directory")
        return jsonify({
            "Status":"Backup File Not Found In your system",
            "Message":"Contact Your Administrator"
        })
######################################### Ends ##########################################  

# <--------------------------------- Record Page Route --------------------------------->
@app.route("/record")
def record():
    data = CheckExe()
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        cus_details = json_data["Customer_Details"]
    return render_template("record.html",checkexe=data,cus=cus_details)

@app.route("/RecordView",methods=["GET","POST"])
def RecordView():
    if request.method=="POST":
        month=request.form.get("month")
        print("Month = ",month)
        cus_id=request.form.get("cusname")
        # print(cus_id)
        new_data=[]
        with open("details.json","r+") as f:
            json_object=json.loads(f.read())
            payment_details=json_object["Payment_Details"]
            for val in range(len(payment_details)):
                if month == payment_details[val]["Month"] and int(cus_id) == int(payment_details[val]["CustomerId"]):
                    new_data.append(payment_details[val])
            else:
                new_data.append("No data found")
        return jsonify({"Result":new_data})

# <--------------------------------- Ends ---------------------------------------------->

# <--------------------------------------- Check Email Status ---------------------->
@app.route("/check_status")
def check_status():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            mail_details = json_data["Compose_Details"]
            notify = json_data["Payment_Details"]
            notify = [val["DeliveryCharge"] for val in notify if val["DeliveryCharge"]]
            executive = json_data["Register"]
            return jsonify({
                "Status":"Success",
                "Total":len(mail_details),
                "Total1":len(notify),
                "Total2":len(executive)
            })
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact To Administrator"
        })
    finally:
        file.close()

# <--------------------------------------------- Ends ---------------------------------->

# <----------------------------------- See home Delivery Payment ------------------------->
@app.route("/ViewDelivery")
def ViewDelivery():
    data = CheckExe()
    with open("details.json","r+") as file:
        json_data = json.loads(file.read())
        payment = json_data["Payment_Details"]
        details = []
        for val in payment:
            if val["DeliveryCharge"]:
                details.append(val)
    return render_template("view_home_delivery.html",checkexe=data,data=details)
# <----------------------------------- Ends ---------------------------------------------->

# <---------------------------------- Fetch Old Payment Data --------------------------->
@app.route("/old_details")
def old_details():
    try:
        with open("old.json","r+") as file:
            json_data = json.loads(file.read())
            old_payment_data = json_data["Payment_Details"]
            data = CheckExe()
            return render_template("old_payment_details.html",data = old_payment_data,checkexe=data)
    except Exception as e:
        print("Error = ",e)
        return jsonify({
            "Status":"Error",
            "Message":"Contact To Your Administrator"
        })
    finally:
        file.close()
# <---------------------------------- Ends --------------------------------------------->

# <---------------------------------- Check for new orders ----------------------------->
@app.route("/new_order")
def new_order():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            payment = json_data["Payment_Details"]
            if len(payment) > 0:
                payment = payment[-1]
            else:
                pass
            return jsonify({
                "Res":payment
            })
    except Exception as e:
        print(e)
    finally:
        file.close()
# <------------------------------------ Ends ------------------------------------------->

# <------------------------------- Check for total Customers ------------------------->
@app.route("/total_customer")
def total_customer():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            customer = json_data["Customer_Details"]
            return jsonify({
                "Res":customer
            })
    except Exception as e:
        print(e)
    finally:
        file.close()
# <------------------------------- Ends ------------------------------------------------->

# <---------------------------------- Check for new customers per day ----------------->
@app.route("/unique_customer")
def unique_customer():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            customer = json_data["Payment_Details"]
            return jsonify({
                "Res":customer
            })
    except Exception as e:
        print(e)
    finally:
        file.close()
# <--------------------------------------- Ends ------------------------------------->

# <----------------------------------------- Show Backup File ---------------------->
@app.route("/ShowJson")
def ShowJson():
    try:
        with open("details.json","r+") as file:
            json_data = json.loads(file.read())
            return jsonify({
                "Backup":"Successfull",
                "Data":json_data
            })
    except Exception as e:
        print("Error = ",e)
    finally:
        file.close()
# <--------------------------------------- Ends --------------------------------->

# ui.run()

if __name__ == "__main__":
    app.run(debug=True)