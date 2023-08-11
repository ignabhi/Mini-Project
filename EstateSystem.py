from flask import *

from DBConnection import Db

app = Flask(__name__)

app.secret_key="sk"


staticpath = "C:\\Users\\HP\\PycharmProjects\\EstateSystem\\static\\"


@app.route('/')
def loginform():
    return render_template("loginindex.html")



# @app.route('/loginindex')
# def loginindex():
#     return render_template("loginindex.html")




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# @app.route('/listing')
# def listing():
#     return render_template("listing.html")


@app.route('/login_post', methods=['post'])
def login_post():
    username = request.form['textfield']
    password = request.form['textfield2']
    qry="SELECT * FROM `login` WHERE `username`='" + username + "' AND `password`='" + password + "'"
    db=Db()
    res = db.selectOne(qry)
    if res is None:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''
    else:
        session['lid']=res['lid']
        # print(session['lid'])
        if res['usertype'] == 'admin':
            return '''<script>alert("Admin Logged In Successfully");window.location="/admin_home"</script>'''
        else:
            if res['usertype'] == 'agent':
                qry2 = "SELECT * FROM `agent` WHERE `agentlid`=' "+ str(session['lid']) +" ' AND `status`='approved'"
                res2 = db.selectOne(qry2)
                if res2 is not None:
                    return '''<script>alert("Agent Logged In Successfully");window.location="/agent_home"</script>'''
                else:
                    return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''
            else:
                if res['usertype'] == 'user':
                    return '''<script>alert("User Logged In Successfully");window.location="/user_home"</script>'''
                else:
                    return '''<script> alert("Invalid Username or Password");window.location = "/" </script>'''


########################################################################################################################

#Admin_Start____________________________________________________________________________________________________________


@app.route('/admin_home')
def admin_home():
    return render_template('Admin/AdminHome.html')



@app.route('/admin_viewandapproveagents')
def admin_viewandapproveagent():
    qry="SELECT * FROM `agent` WHERE `status`='pending'"
    db=Db()
    res=db.select(qry)
    return render_template("Admin/ViewandApproveAgents.html",data=res)



@app.route('/admin_viewandapproveagents_searchagents', methods=['post'])
def admin_viewandapproveagents_searchagents():
    search = request.form['textfield']
    qry = "SELECT * FROM `agent` WHERE (`status`='pending') AND ((`agentname` LIKE '%"+search+"%') OR (`gender` LIKE '%"+search+"%'))"
    db = Db()
    res = db.select(qry)
    return render_template("Admin/ViewandApproveAgents.html", data=res)



@app.route('/approveagents/<id>')
def approveagents(id):
    qry="UPDATE `agent` SET `status`='approved' WHERE `agentid`='" + id + "'"
    db=Db()
    db.update(qry)
    return '''<script>alert("Approved Successfully");window.location="/admin_viewandapproveagents"</script>'''



@app.route('/rejectload/<aid>')
def rejectload(aid):
    return render_template("Admin/RejectReason.html", id=aid)



@app.route('/rejectagents', methods=['post'])
def rejectagents():
    id = request.form['aid']
    review = request.form['textarea']
    qry = "UPDATE `agent` SET `status`='rejected',`review`='" + review + "' WHERE `agentid`='" + id + "'"
    db = Db()
    db.update(qry)
    return '''<script>alert("Rejected Successfully");window.location="/admin_viewandapproveagents"</script>'''



@app.route('/rejectload2/<aid>')
def rejectload2(aid):
    return render_template("Admin/RejectReason2.html", id=aid)



@app.route('/rejectapprovedagents', methods=['post'])
def rejectapprovedagents():
    id = request.form['aid']
    review = request.form['textarea']
    qry = "UPDATE `agent` SET `status`='rejected',`review`='" + review + "' WHERE `agentid`='" + id + "'"
    db = Db()
    db.update(qry)
    return '''<script>alert("Rejected Successfully");window.location="/admin_viewapprovedagents"</script>'''



@app.route('/approverejectedagents<id>')
def approverejectedagents(id):
    qry = "UPDATE `agent` SET `status`='approved',`review`='NULL' WHERE `agentid`='" + id + "'"
    db = Db()
    db.update(qry)
    return '''<script>alert("Approve Successfully");window.location="/admin_viewrejectedagents"</script>'''



@app.route('/admin_viewapprovedagents')
def admin_viewapprovedagents():
    qry="SELECT * FROM `agent` WHERE `status`='approved'"
    db=Db()
    res = db.select(qry)
    return render_template("Admin/ViewApprovedAgents.html",data=res)



@app.route('/admin_viewapprovedagents_searchapprovedagents', methods=['post'])
def admin_viewapprovedagents_searchapprovedagents():
    search = request.form['textfield']
    qry = "SELECT * FROM `agent` WHERE (`status`='approved') AND ((`agentname` LIKE '%"+search+"%') OR (`gender` LIKE '"+search+"'))"
    db = Db()
    res = db.select(qry)
    return render_template("Admin/ViewApprovedAgents.html", data=res)



@app.route('/admin_viewrejectedagents')
def admin_viewrejectedagents():
    qry = "SELECT * FROM `agent` WHERE STATUS='rejected'"
    db = Db()
    res = db.select(qry)
    return render_template("Admin/ViewRejectedAgents.html", data=res)



@app.route('/admin_viewrejectedagents_searchrejectedagents', methods=['post'])
def admin_viewrejectedagents_searchrejectedagents():
    search = request.form['textfield']
    qry = "SELECT * FROM `agent` WHERE (`status`='rejected') AND ((`agentname` LIKE '%" + search + "%') OR (`gender` LIKE '" + search + "'))"
    db = Db()
    res = db.select(qry)
    return render_template("Admin/ViewRejectedAgents.html", data=res)


@app.route('/admin_viewpropertiesaddedbyagents')
def admin_viewpropertiesaddedbyagents():
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`email` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid`"
    res = db.select(qry)
    return render_template("Admin/ViewPropertiesAddedbyAgents.html",data=res)



@app.route('/admin_viewpropertiesaddedbyagentssearch', methods=['post'])
def admin_viewpropertiesaddedbyagentssearch():
    searchpd = request.form['textfield']
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`email` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid` WHERE (`agentname` LIKE '%"+searchpd+"%') OR (`propertytitle` LIKE '%"+searchpd+"%') OR (`propertytype` LIKE '%"+searchpd+"%') OR (`saletype` LIKE '%"+searchpd+"%') OR (`state` LIKE '%"+searchpd+"%')"
    res = db.select(qry)
    return render_template("Admin/ViewPropertiesAddedbyAgents.html",data=res)



@app.route('/viewpropertiesbyagentid<id>')
def viewpropertiesbyagentid(id):
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`email` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid` WHERE `agentid`='" + id + "'"
    res = db.select(qry)
    return render_template("Admin/ViewPropertiesAddedbyAgents.html",data=res)


@app.route('/admin_viewcomplaint')
def admin_viewcomplaint():
    db=Db()
    qry = "SELECT `complaint`.*,`user`.`username`, `user`.`email` FROM `user` INNER JOIN `complaint` ON `complaint`.`userlid`=`user`.`userlid`"
    res = db.select(qry)
    return render_template("Admin/ViewComplaintandSendReply.html",data=res)


@app.route('/admin_viewcomplaint_searchcomplaint', methods=['post'])
def admin_viewcomplaint_searchcomplaint():
    from_date = request.form['d1']
    to_date  = request.form['d2']
    db=Db()
    qry = "SELECT `complaint`.*,`user`.`username`, `user`.`email` FROM `user` INNER JOIN `complaint` ON `complaint`.`userlid`=`user`.`userlid` WHERE `date` BETWEEN '" + from_date + "' AND '" +to_date+ "'"
    res = db.select(qry)
    return render_template("Admin/ViewComplaintandSendReply.html", data=res)


@app.route('/admin_sendcomplaintreply/<cid>')
def admin_sendcomplaintreply(cid):
    return render_template("Admin/SendComplaintReply.html",id=cid)


@app.route('/getcomplaintreply', methods=['post'])
def getcomplaintreply():
    reply = request.form['textfield']
    cid = request.form['id']
    qry = "UPDATE `complaint` SET `reply`='" +reply+ "', status='replied' WHERE `complaintid`='" + cid + "'"
    db=Db()
    db.update(qry)
    return '''<script>alert('Reply Send');window.location="/admin_viewcomplaint#locations"</script>'''


@app.route('/admin_viewrating')
def admin_viewrating():
    db=Db()
    qry = "SELECT `rating`.*,`user`.`username`,`user`.`email` FROM `user` INNER JOIN `rating` ON `rating`.`userlid`=`user`.`userlid`"
    res = db.select(qry)

    return render_template("Admin/ViewRatingAdmin.html",data=res)


@app.route('/admin_viewrating_search', methods=['post'])
def admin_viewrating_search():
    from_date = request.form['d1']
    to_date = request.form['d2']
    db=Db()
    qry = "SELECT `rating`.*,`user`.`username`,`user`.`email` FROM `user` INNER JOIN `rating` ON `rating`.`userlid`=`user`.`userlid` WHERE `date` BETWEEN '" + from_date + "' AND '" + to_date+ "'"
    res = db.select(qry)
    return render_template("Admin/ViewRatingAdmin.html",data=res)

#Admin_End______________________________________________________________________________________________________________

########################################################################################################################

#Agent_Start____________________________________________________________________________________________________________

@app.route('/agent_home')
def agent_home():
    return render_template("Agent/AgentHome.html")


@app.route('/agent_signup')
def agent_signup():
    return render_template("Agent/AgentSignupForm.html")


@app.route('/signupvalues', methods=['post'])
def signupvalues():
    agentname = request.form['textfield']
    phone = request.form['textfield2']
    email = request.form['textfield3']

    file = request.files['file']
    file.save(staticpath+"Agent\\"+file.filename)
    path = "/static/Agent/"+file.filename

    gender = request.form['select']
    about = request.form['textarea']
    pword = request.form['textfield4']
    cpword = request.form['textfield5']
    db=Db()
    qry3 = "SELECT * FROM `login` WHERE `username`='"+email+"'"
    res3 = db.selectOne(qry3)
    if res3 is None:
        qry2 = "INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('" + email + "','" + pword + "','agent')"
        res2 = db.insert(qry2)
        qry1 = "INSERT INTO `agent`(`agentlid`,`agentname`,`phone`,`email`,`photo`,`gender`,`about`,`status`) VALUES('"+str(res2)+"','" + agentname + "','" + phone + "','" + email + "','" + str(path) + "','" + gender + "','" + about + "','pending')"
        res1 = db.insert(qry1)
        return '''<script>alert("Registered Successfully");window.location="/"</script>'''
    else:
        return '''<script>alert("Username Already Exists");window.location="/agent_signup#locations"</script>'''


@app.route('/agent_viewprofile')
def agent_viewprofile():
    db=Db()
    qry = "SELECT * FROM `agent` WHERE `agentlid`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template("Agent/ViewProfileAgent.html", data=res)


@app.route('/agent_editprofile')
def agent_editprofile():
    db = Db()
    qry = "SELECT * FROM `agent` WHERE `agentlid`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template("Agent/AgentProfileUpdate.html", data=res)


@app.route('/editagentprofilepost', methods=['post'])
def editagentprofilepost():
    agentname = request.form['textfield']
    phone = request.form['textfield2']
    email = request.form['textfield3']

    gender = request.form['select']
    about = request.form['textarea']
    db=Db()

    if 'file' in request.files:
        photo = request.files['file']
        if photo.filename!="":
            photo.save(staticpath+"Agent\\"+photo.filename)
            path = "/static/Agent/"+photo.filename
            qry = "UPDATE `agent` SET `agentname`='" + agentname + "',`phone`='" + phone + "',`email`='" + email + "',`photo`='" + str(path) + "',`gender`='" + gender + "',`about`='" + about + "' WHERE `agentlid`='" + str(session['lid']) + "'"
            res= db.update(qry)
            qry2 = "UPDATE `login` SET `username`='" + email + "' WHERE `lid`='" + str(session['lid']) + "'"
            db.update(qry2)
            return '''<script>alert("Updated");window.location="/agent_viewprofile"</script>'''
        else:
            qry = "UPDATE `agent` SET `agentname`='" + agentname + "',`phone`='" + phone + "',`email`='" + email + "',`gender`='" + gender + "',`about`='" + about + "' WHERE `agentlid`='" + str(session['lid']) + "'"
            res = db.update(qry)
            qry2 = "UPDATE `login` SET `username`='" + email + "' WHERE `lid`='" + str(session['lid']) + "'"
            db.update(qry2)
            return '''<script>alert("Updated");window.location="/agent_viewprofile"</script>'''
    else:
        qry = "UPDATE `agent` SET `agentname`='" + agentname + "',`phone`='" + phone + "',`email`='" + email + "',`gender`='" + gender + "',`about`='" + about + "' WHERE `agentlid`='" + str(session['lid']) + "'"
        res = db.update(qry)
        qry2 = "UPDATE `login` SET `username`='" + email + "' WHERE `lid`='" + str(session['lid']) + "'"
        db.update(qry2)
        return '''<script>alert("Updated");window.location="/agent_viewprofile"</script>'''


@app.route('/agent_addproperty')
def agent_addproperty():
    return render_template("Agent/AgentsAddProperty.html")


@app.route('/addpropertypost', methods=['post'])
def addpropertypost():
    propertytitle = request.form['textfield']
    propertytype = request.form['select']
    expectedprice = request.form['textfield2']
    totalarea = request.form['textfield3']
    housearea = request.form['textfield4']
    totalbeds = request.form['textfield5']
    totalbaths = request.form['textfield6']
    totalgarages = request.form['textfield7']
    address = request.form['textarea']
    city = request.form['textfield8']
    state = request.form['textfield9']
    pin = request.form['textfield10']
    country = request.form['textfield11']
    landmark = request.form['textarea2']


    pic1 = request.files['file']
    pic1.save(staticpath + "Property\\" + pic1.filename)
    path1 = "/static/Property/" + pic1.filename

    pic2 = request.files['file2']
    pic2.save(staticpath + "Property\\" + pic2.filename)
    path2 = "/static/Property/" + pic2.filename

    pic3 = request.files['file3']
    pic3.save(staticpath + "Property\\" + pic3.filename)
    path3 = "/static/Property/" + pic3.filename

    vid = request.files['file4']
    vid.save(staticpath + "Property\\" + vid.filename)
    path4 = "/static/Property/" + vid.filename


    description = request.form['textarea3']
    maplocation = request.form['textfield12']
    amentities = request.form['textarea5']
    propertystatus = request.form['select2']
    saletype = request.form['select3']
    availabledate = request.form['textfield14']
    yearbuilt = request.form['textfield13']
    nearestfacilities = request.form['textarea4']

    db=Db()
    # qry = "INSERT INTO `property`(`agentlid`,`propertytitle`,`propertytype`,`priceofproperty`,`totalarea`,`housesqft`,`totalbeds`,`totalbaths`,`totalgarages`,`propertylocation`,`city`,`state`,`pin`,`country`,`landmarks`,`pic1`,`pic2`,`pic3`,`video`,`propertydescription`,`gmaplocation`,`amentities`,`propertystatus`,`uploaddate`,`saletype`,`availabledate`,`nearestfacilities`,`yearbuilt`) VALUES('"+str(session['lid'])+"','"+propertytitle+"','"+propertytype+"','"+expectedprice+"','"+totalarea+"','"+housearea+"','"+totalbeds+"','"+totalbaths+"','"+totalgarages+"','"+address+"','"+city+"','"+state+"','"+pin+"','"+country+"','"+landmark+"','"+str(path1)+"','"+str(path2)+"','"+str(path3)+"','"+str(path4)+"','"+description+"','"+maplocation+"','"+amentities+"','"+propertystatus+"',curdate(),'"+saletype+"','"+availabledate+"','"+nearestfacilities+"','"+yearbuilt+"')"
    qry = "INSERT INTO `property`(`agentlid`,`propertytitle`,`propertytype`,`priceofproperty`,`totalarea`,`housesqft`,`totalbeds`,`totalbaths`,`totalgarages`,`propertylocation`,`city`,`state`,`pin`,`country`,`landmarks`,`pic1`,`pic2`,`pic3`,`video`,`propertydescription`,`gmaplocation`,`amentities`,`propertystatus`,`uploaddate`,`saletype`,`availabledate`,`nearestfacilities`,`yearbuilt`) VALUES('"+str(session['lid'])+"','"+propertytitle+"','"+propertytype+"','"+expectedprice+"','"+totalarea+"','"+housearea+"','"+totalbeds+"','"+totalbaths+"','"+totalgarages+"','"+address+"','"+city+"','"+state+"','"+pin+"','"+country+"','"+landmark+"','"+str(path1)+"','"+str(path2)+"','"+str(path3)+"','"+str(path4)+"','"+description+"','"+maplocation+"','"+amentities+"','"+propertystatus+"',curdate(),'"+saletype+"','"+availabledate+"','"+nearestfacilities+"','"+yearbuilt+"')"
    db.insert(qry)

    return '''<script>alert("Property Added");window.location="/agent_viewproperties#locations"</script>'''


@app.route('/agent_viewproperties')
def agent_viewproperties():
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname` FROM `property` INNER JOIN `agent` ON `property`.`agentlid`=`agent`.`agentlid` WHERE `agent`.`agentlid`='"+str(session['lid'])+"'"
    res = db.select(qry)
    return render_template("Agent/ViewEditDeletePropertyAgent.html", data=res)



@app.route('/agent_viewpropertiessearch', methods=['post'])
def agent_viewpropertiessearch():
    searchpr = request.form['textfield']
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname` FROM `property` INNER JOIN `agent` ON `property`.`agentlid`=`agent`.`agentlid` WHERE (`agentid`='"+str(session['lid'])+"') AND (`propertytitle` LIKE '%"+searchpr+"%') OR (`propertytype` LIKE '%"+searchpr+"%') OR (`saletype` LIKE '%"+searchpr+"%') OR (`priceofproperty` LIKE '%"+searchpr+"%')"
    res = db.select(qry)
    return render_template("Agent/ViewEditDeletePropertyAgent.html", data=res)




@app.route('/agent_editproperty<pid>')
def agent_editproperty(pid):
    db=Db()
    qry = "SELECT * FROM `property` WHERE `propertyid`='"+pid+"'"
    res = db.selectOne(qry)
    print(res)
    return render_template("Agent/EditPropertyAgent.html", id=pid, data=res)


@app.route('/editpropertypost', methods=['post'])
def editpropertypost():
    id = request.form['pid']
    propertytitle = request.form['textfield']
    propertytype = request.form['select']
    expectedprice = request.form['textfield2']
    totalarea = request.form['textfield3']
    housearea = request.form['textfield4']
    totalbeds = request.form['textfield5']
    totalbaths = request.form['textfield6']
    totalgarages = request.form['textfield7']
    address = request.form['textarea']
    city = request.form['textfield8']
    state = request.form['textfield9']
    pin = request.form['textfield10']
    country = request.form['textfield11']
    landmark = request.form['textarea2']
    description = request.form['textarea3']
    maplocation = request.form['textfield12']
    propertystatus = request.form['select2']
    saletype = request.form['select3']
    availabledate = request.form['textfield14']
    yearbuilt = request.form['textfield13']
    nearestfacilities = request.form['textarea4']

    amentities = request.form['textarea5']
    bought = request.form['textfield20']

    db = Db()

    if 'file1' in request.files:
        photo = request.files['file1']
        if photo.filename!="":
            photo.save(staticpath+"Property\\"+photo.filename)
            path = "/static/Property/"+photo.filename

            # qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`pic1`='"+str(path)+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+ id +"'"
            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`pic1`='"+str(path)+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("1")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''
        else:
            qry = "UPDATE `property` SET `propertytitle`='" + propertytitle + "',`bought`='"+bought+"',`propertytype`='" + propertytype + "',`priceofproperty`='" + expectedprice + "',`totalarea`='" + totalarea + "',`housesqft`='" + housearea + "',`totalbeds`='" + totalbeds + "',`totalbaths`='" + totalbaths + "',`totalgarages`='" + totalgarages + "',`propertylocation`='" + address + "',`city`='" + city + "',`state`='" + state + "',`pin`='" + pin + "',`country`='" + country + "',`landmarks`='" + landmark + "',`propertydescription`='" + description + "',`gmaplocation`='" + maplocation + "',`amentities`='" + amentities + "',`propertystatus`='" + propertystatus + "',`saletype`='" + saletype + "',`availabledate`='" + availabledate + "',`nearestfacilities`='" + nearestfacilities + "',`yearbuilt`='" + yearbuilt + "' WHERE `propertyid`='" + id + "'"
            # print(qry)
            # print("2")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''

    else:
        qry = "UPDATE `property` SET `propertytitle`='" + propertytitle + "',`bought`='"+bought+"',`propertytype`='" + propertytype + "',`priceofproperty`='" + expectedprice + "',`totalarea`='" + totalarea + "',`housesqft`='" + housearea + "',`totalbeds`='" + totalbeds + "',`totalbaths`='" + totalbaths + "',`totalgarages`='" + totalgarages + "',`propertylocation`='" + address + "',`city`='" + city + "',`state`='" + state + "',`pin`='" + pin + "',`country`='" + country + "',`landmarks`='" + landmark + "',`propertydescription`='" + description + "',`gmaplocation`='" + maplocation + "',`amentities`='" + amentities + "',`propertystatus`='" + propertystatus + "',`saletype`='" + saletype + "',`availabledate`='" + availabledate + "',`nearestfacilities`='" + nearestfacilities + "',`yearbuilt`='" + yearbuilt + "' WHERE `propertyid`='" + id + "'"
        # print(qry)
        # print("3")
        db.update(qry)
        # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''

    if 'file2' in request.files:
        photo = request.files['file2']
        if photo.filename != "":
            photo.save(staticpath + "Property\\" + photo.filename)
            path = "/static/Property/" + photo.filename

            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`pic2`='"+str(path)+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("4")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''
        else:
            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("5")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''

    else:
        qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
        # print(qry)
        # print("6")
        db.update(qry)
        # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''


    if 'file3' in request.files:
        photo = request.files['file3']
        if photo.filename != "":
            photo.save(staticpath + "Property\\" + photo.filename)
            path = "/static/Property/" + photo.filename

            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`pic3`='"+str(path)+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("7")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''
        else:
            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("8")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''


    else:
        qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
        # print(qry)
        # print("9")
        db.update(qry)
        # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''


    if 'file4' in request.files:
        photo = request.files['file4']
        if photo.filename != "":
            photo.save(staticpath + "Property\\" + photo.filename)
            path = "/static/Property/" + photo.filename

            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`video`='"+str(path)+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("7")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''
        else:
            qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
            # print(qry)
            # print("8")
            db.update(qry)
            # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''


    else:
        qry = "UPDATE `property` SET `propertytitle`='"+propertytitle+"',`bought`='"+bought+"',`propertytype`='"+propertytype+"',`priceofproperty`='"+expectedprice+"',`totalarea`='"+totalarea+"',`housesqft`='"+housearea+"',`totalbeds`='"+totalbeds+"',`totalbaths`='"+totalbaths+"',`totalgarages`='"+totalgarages+"',`propertylocation`='"+address+"',`city`='"+city+"',`state`='"+state+"',`pin`='"+pin+"',`country`='"+country+"',`landmarks`='"+landmark+"',`propertydescription`='"+description+"',`gmaplocation`='"+maplocation+"',`amentities`='"+amentities+"',`propertystatus`='"+propertystatus+"',`saletype`='"+saletype+"',`availabledate`='"+availabledate+"',`nearestfacilities`='"+nearestfacilities+"',`yearbuilt`='"+yearbuilt+"' WHERE `propertyid`='"+id+"'"
        # print(qry)
        # print("9")
        db.update(qry)
        # return '''<script>alert("Property Updated");window.location="/agent_viewproperties"</script>'''

    return '''<script>alert("Property Updated");window.location="/agent_viewproperties#locations"</script>'''


@app.route('/deleteproperty<pid>')
def deleteproperty(pid):
    db=Db()
    qry = "DELETE FROM `property` WHERE `propertyid`='" + pid + "'"
    db.delete(qry)
    return '''<script>alert("Property Deleted");window.location="/agent_viewproperties#locations"</script>'''


@app.route('/agent_viewuserinterest')
def agent_viewuserinterest():
    db=Db()
    qry = "SELECT `interest`.*,`user`.`username`,`property`.`propertytitle` FROM `interest` JOIN `user` ON `interest`.`userlid`=`user`.`userlid` JOIN `property` ON `property`.`propertyid`=`interest`.`propertyid` JOIN `agent` ON `agent`.`agentlid`=`property`.`agentlid` WHERE `agent`.`agentlid`='"+str(session['lid'])+"'"
    res = db.select(qry)
    return render_template("Agent/ViewInterestFromUser.html", data=res)


# @app.route('/agent_chatwithuser')
# def agent_chatwithuser():
#     return render_template("Agent/")


# @app.route('/agent_changepassword')
# def agent_changepassword():
#     return render_template("Agent/ChangePasswordAgent.html")


@app.route('/agent_viewrating')
def agent_viewrating():
    db=Db()
    qry = "SELECT `rating`.*,`user`.`username`,`user`.`email` FROM `user` INNER JOIN `rating` ON `rating`.`userlid`=`user`.`userlid`"
    res = db.select(qry)
    return render_template("Agent/ViewRatingAgent.html", data=res)


@app.route('/agent_viewrating_search', methods=['post'])
def agent_viewrating_search():
    from_date = request.form['d1']
    to_date = request.form['d2']
    db = Db()
    qry = "SELECT `interest`.*,`user`.`username`,`property`.`propertytitle` FROM `interest` JOIN `user` ON `interest`.`userlid`=`user`.`userlid` JOIN `property` ON `property`.`propertyid`=`interest`.`propertyid` JOIN `agent` ON `agent`.`agentlid`=`property`.`agentlid` WHERE (`agent`.`agentlid`='" + str(session['lid']) + "') AND (`date` BETWEEN '" + from_date + "' AND '" + to_date+ "')"
    res = db.select(qry)
    return render_template("Agent/ViewInterestFromUser.html", data=res)



#Agent_End______________________________________________________________________________________________________________

########################################################################################################################

#User_Start_____________________________________________________________________________________________________________

@app.route('/user_home')
def user_home():
    return render_template("User/UserHome.html")


@app.route('/user_signup')
def user_signup():
    return render_template("User/UserSignupForm.html")

@app.route('/usersignuppost', methods=['post'])
def usersignuppost():
    name = request.form['textfield']
    phone = request.form['textfield2']
    email = request.form['textfield3']
    gender= request.form['select']

    file = request.files['file']
    file.save(staticpath+"User\\"+file.filename)
    path = "/static/User/" + file.filename

    place = request.form['textfield4']
    city = request.form['textfield5']
    state = request.form['textfield6']
    pin = request.form['textfield7']
    pword = request.form['textfield8']
    cpword = request.form['textfield9']

    db = Db()
    qry3 = "SELECT * FROM `login` WHERE `username`='" + email + "'"
    res3 = db.selectOne(qry3)
    if res3 is None:
        qry2 = "INSERT INTO `login`(`username`,`password`,`usertype`) VALUES('" + email + "','" + pword + "','user')"
        res2 = db.insert(qry2)
        qry1 = "INSERT INTO `user` (`userlid`,`username`,`phone`,`email`,`photo`,`place`,`city`,`state`,`pincode`,`gender`) VALUES ('" +str(res2)+ "','" +name+ "','" +phone+ "','" +email+ "','" +str(path)+ "','" +place+ "','" +city+ "','" +state+ "','" +pin+ "','" +gender+ "')"
        res1 = db.insert(qry1)
        return '''<script>alert("Registered Successfully");window.location="/"</script>'''
    else:
        return '''<script>alert("Username Already Exists");window.location="/user_signup#locations"</script>'''



@app.route('/user_viewprofile')
def user_viewprofile():
    db=Db()
    qry = "SELECT * FROM `user` WHERE `userlid`='" +str(session['lid'])+ "'"
    res = db.selectOne(qry)
    return render_template("User/UserViewEditProfile.html", data=res)


@app.route('/user_editprofile')
def user_editprofile():
    db = Db()
    qry = "SELECT * FROM `user` WHERE `userlid`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template("User/UserProfileUpdate.html", data=res)


@app.route('/editprofilepost', methods=['post'])
def editprofilepost():
    name = request.form['textfield']
    phone = request.form['textfield2']
    email = request.form['textfield3']
    gender = request.form['select']
    place = request.form['textfield4']
    city = request.form['textfield5']
    state = request.form['textfield6']
    pin = request.form['textfield7']
    db=Db()

    if 'file' in request.files:
        photo = request.files['file']
        if photo.filename != "":
            photo.save(staticpath + "User\\" + photo.filename)
            path = "/static/User/" + photo.filename

            qry = "UPDATE `user` SET `username`='" +name+ "',`phone`='" +phone+ "',`email`='" +email+ "',`photo`='" +str(path)+ "',`place`='" +place+ "',`city`='" +city+ "',`state`='" +state+ "',`pincode`='" +pin+ "',`gender`='" +gender+ "' WHERE `userlid`='" +str(session['lid'])+ "'"
            db.update(qry)
            qry2 = "UPDATE `login` SET `username`='"+email+"' WHERE `lid`='"+str(session['lid'])+"'"
            db.update(qry2)
        else:
            qry = "UPDATE `user` SET `username`='" +name+ "',`phone`='" +phone+ "',`email`='" +email+ "',`place`='" +place+ "',`city`='" +city+ "',`state`='" +state+ "',`pincode`='" +pin+ "',`gender`='" +gender+ "' WHERE `userlid`='" +str(session['lid'])+ "'"
            db.update(qry)
            qry2 = "UPDATE `login` SET `username`='" + email + "' WHERE `lid`='" + str(session['lid']) + "'"
            db.update(qry2)
    else:
        qry = "UPDATE `user` SET `username`='" +name+ "',`phone`='" +phone+ "',`email`='" +email+ "',`place`='" +place+ "',`city`='" +city+ "',`state`='" +state+ "',`pincode`='" +pin+ "',`gender`='" +gender+ "' WHERE `userlid`='" +str(session['lid'])+ "'"
        db.update(qry)
        qry2 = "UPDATE `login` SET `username`='" + email + "' WHERE `lid`='" + str(session['lid']) + "'"
        db.update(qry2)

    return '''<script>alert("Updated");window.location="/user_viewprofile#locations"</script>'''


@app.route('/user_viewproperty')
def user_viewproperty():
    db=Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`phone`,`agent`.`email`,`agent`.`photo`,`agent`.`gender`,`agent`.`about` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid`"
    res = db.select(qry)
    return render_template("User/UserViewProperty.html", data=res)



@app.route('/propertysearch', methods=['post'])
def propertysearch():
    searchpd = request.form['search']
    db = Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`phone`,`agent`.`email`,`agent`.`photo`,`agent`.`gender`,`agent`.`about` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid`  WHERE (`state` LIKE '%"+searchpd+"%') OR (`country` LIKE '%"+searchpd+"%') OR (`saletype` LIKE '%"+searchpd+"%') OR (`saletype` LIKE '%"+searchpd+"%')"
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`phone`,`agent`.`email`,`agent`.`photo`,`agent`.`gender`,`agent`.`about` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid`  WHERE (`state` LIKE '%"+searchpd+"%') OR (`country` LIKE '%"+searchpd+"%') OR (`saletype` LIKE '%"+searchpd+"%') OR (`priceofproperty` LIKE '%"+searchpd+"%')"
    res = db.select(qry)
    return render_template("User/UserViewProperty.html", data=res)


@app.route('/user_propertysingle<pid>')
def user_propertysingle(pid):
    db = Db()
    qry = "SELECT `property`.*,`agent`.`agentname`,`agent`.`phone`,`agent`.`email`,`agent`.`photo`,`agent`.`gender`,`agent`.`about` FROM `agent` INNER JOIN `property` ON `agent`.`agentlid`=`property`.`agentlid` WHERE `propertyid`='"+pid+"'"
    res = db.selectOne(qry)
    ss=[]
    if res is not None:
        ff=res["amentities"]
        ss=ff.split(",")
    else:
        ss=[]
    # print(res)

    qq = []
    if res is not None:
        aa = res["nearestfacilities"]
        qq = aa.split(",")
    else:
        qq = []

    return render_template("User/user-property-single.html", data=res, ss=ss, qq=qq)


@app.route('/user_sentinterest<pid>')
def user_sentinterest(pid):
    db=Db()
    qry = "INSERT INTO `interest`(`userlid`,`propertyid`,`date`) VALUES('"+ str(session['lid']) +"','"+ pid +"',curdate())"
    db.insert(qry)
    return '''<script>alert("Interest Send");window.location="/user_viewproperty#locations"</script>'''


@app.route('/user_viewsentinterest')
def user_viewsentinterest():
    db=Db()
    qry = "SELECT `interest`.*,`property`.`propertytitle` FROM `interest` INNER JOIN `property` ON `interest`.`propertyid`=`property`.`propertyid` WHERE `userlid`='"+ str(session['lid']) +"'"
    res = db.select(qry)
    # print(qry)
    # print(session['lid'])
    return render_template("User/UserViewSentInterest.html", data=res)



@app.route('/interestsearch', methods=['post'])
def interestsearch():
    fdate = request.form['fdate']
    tdate = request.form['tdate']
    db = Db()
    qry = "SELECT `interest`.*,`property`.`propertytitle` FROM `interest` INNER JOIN `property` ON `interest`.`propertyid`=`property`.`propertyid` WHERE (`userlid`='" + str(session['lid']) + "') AND (`date` BETWEEN '"+fdate+"' AND '"+tdate+"')"
    res = db.select(qry)
    # print(qry)
    # print(session['lid'])
    return render_template("User/UserViewSentInterest.html", data=res)


# @app.route('/user_chantwithagent')
# def user_chantwithagent():
#     return render_template("User/")


# @app.route('/user_changepassword')
# def user_changepassword():
#     return render_template("User/UserChangePassword.html")


@app.route('/user_sendcomplaints')
def user_sendcomplaints():
    db=Db()
    qry = "SELECT * FROM `complaint` WHERE `userlid`='" +str(session['lid'])+ "'"
    res = db.select(qry)
    return render_template("User/UserViewComplaintsandReply.html" ,data=res)


@app.route('/sendpageload')
def sendpageload():
    return render_template("User/UserSentComplaints.html")


@app.route('/sendcomplaintpost', methods=['post'])
def sendcomplaintpost():
    complaint = request.form['textarea']
    db=Db()
    qry = "INSERT INTO `complaint` (`userlid`,`complaint`,`date`,`reply`,`status`) VALUES('" +str(session['lid'])+ "','" +complaint+ "',curdate(),'Not yet replyed','pending')"
    db.insert(qry)
    return '''<script>alert("Complaint Send");window.location="/user_sendcomplaints#locations"</script>'''



@app.route('/user_giverating')
def user_giverating():
    return render_template("User/UserGiveRating.html")



@app.route('/giverating', methods=['post'])
def giverating():
    rating = request.form['select']
    review = request.form['textfield2']
    db = Db()
    qry = "INSERT INTO `rating`(`userlid`,`rating`,`review`,`date`) VALUES('"+str(session['lid'])+"','"+rating+"','"+review+"',curdate())"
    db.insert(qry)
    return '''<script>alert("Rated");window.location="/user_home"</script>'''



#User_End_______________________________________________________________________________________________________________

########################################################################################################################


if __name__ == '__main__':
    app.run()
