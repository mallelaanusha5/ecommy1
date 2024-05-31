from flask import Flask,render_template,request,url_for,redirect,flash,session,Response
from flask_session import Session
import bcrypt
import mysql.connector
from otp import genotp
from cmail import cmail
from keys import secret_key,salt1,salt2
from tokens import token
from itsdangerous import URLSafeTimedSerializer
import os
import stripe
import pdfkit
stripe.api_key="sk_test_51MMsHhSGj898WTbYXSx509gD14lhhXs8Hx8ipwegdytPB1Bkw0lJykMB0yGpCux95bdw1Gk9Gb9nJIWzPEEDxSqf00GEtCqZ8Y"
app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
# Session(app)mydb=mysql.connector.connect(host='localhost',user='root',password='anusha153',db='ecommy')

app.secret_key=b'5\x07\xe8\xc5\x80\xceD\xb0G\xf0y\x8a'
#config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
user=os.environ.get('RDS_USERNAME')
db=os.environ.get('RDS_DB_NAME')
password=os.environ.get('RDS_PASSWORD')
host=os.environ.get('RDS_HOSTNAME')
port=os.environ.get('RDS_PORT')
with mysql.connector.connect(host=host,port=port,user=user,password=password,db=db) as conn:
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE if not exists vendor (email varchar(100) NOT NULL,name varchar(255) NOT NULL,mobile_no bigint NOT NULL,address text NOT NULL,password varbinary(255) DEFAULT NULL,PRIMARY KEY (email),UNIQUE KEY mobile_no (mobile_no))")
    cursor.execute("CREATE TABLE user (username varchar(255) NOT NULL,mobile_no bigint NOT NULL,email varchar(155) NOT NULL,address text NOT NULL,password varbinary(255) DEFAULT NULL,PRIMARY KEY (email),UNIQUE KEY mobile_no (mobile_no))")
    cursor.execute("CREATE TABLE additems (itemid binary(16) NOT NULL,item_name longtext NOT NULL,dis longtext NOT NULL,qyt int DEFAULT NULL,category enum(electronics,home,fashion,grocery) DEFAULT NULL,price int DEFAULT NULL,added_by varchar(255) DEFAULT NULL,img_id varchar(255) DEFAULT NULL,PRIMARY KEY (itemid),KEY added_by (added_by),CONSTRAINT additems_ibfk_1 FOREIGN KEY (added_by) REFERENCES vendor (email) ON DELETE CASCADE ON UPDATE CASCADE)")
    cursor.execute("CREATE TABLE orders (ordid binary(16) NOT NULL,itemid binary(16) NOT NULL,item_name varchar(255) DEFAULT NULL,qty int DEFAULT NULL,total_price decimal(20,4) DEFAULT NULL,user varchar(155) DEFAULT NULL,category varchar(255) DEFAULT NULL,imgid varchar(255) DEFAULT NULL,dis text,PRIMARY KEY (ordid),KEY itemid (itemid),KEY user (user),CONSTRAINT orders_ibfk_1 FOREIGN KEY (itemid) REFERENCES additems (itemid) ON DELETE CASCADE,CONSTRAINT orders_ibfk_2 FOREIGN KEY (user) REFERENCES user (email) ON DELETE SET NULL ON UPDATE CASCADE)")
mydb=mysql.connector.connect(host=host,user=user,port=port,password=password,db=db)
@app.route('/')
def home():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems')
    count=cursor.fetchall()

    if count:
        return render_template('home.html',count=count)
    else:
        return render_template('home.html')
    
@app.route('/vendorsignup',methods=['GET','POST'])
def vendorsignup():
    if request.method=='POST':
        email=request.form['email']
        name=request.form['name']
        mobile_no=request.form['mobile_no']
        address=request.form['address']
        password=request.form['password']
        
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from vendor where email=%s',[email])
            count=cursor.fetchone()[0]
            print(count)
            if count==1:
                raise Exception
        except Exception as e:
            flash('email already existed')
            return redirect(url_for('vlogin'))
        else:
            otp=genotp()
            data={'email':email,'name':name,'mobile_no':mobile_no,'address':address,'password':password,'otp':otp}
            subject='OTP for Ecom app'
            body=f'Verification otp for Ecom app {otp}'
            cmail(to=email,subject=subject,body=body)
            flash('OTP has sent to your Email.')
            return redirect(url_for('otp',data=token(data,salt=salt1)))
    return render_template('vendorsignup.html')
@app.route('/otp/<data>',methods=['GET','POST'])
def otp(data):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(data,salt=salt1,max_age=120)
    except Exception as e:
        print(e)
        flash('Link expired')
        return redirect(url_for('vendorsignup'))
    else:
        if request.method=='POST':
            uotp=request.form['otp']
            if uotp==data['otp']:
                bytes = data['password'].encode('utf-8')
                # generating the salt
                salt = bcrypt.gensalt()
                 # Hashing the password
                hash = bcrypt.hashpw(bytes,salt)
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into vendor(email,name,mobile_no,address,password) values(%s,%s,%s,%s,%s)',[data['email'],data['name'],data['mobile_no'],data['address'],hash])
                mydb.commit()
                cursor.close()
                flash('Registration successfully Done.')
                return redirect(url_for('vlogin'))
    return render_template('otp.html')    
@app.route('/vlogin',methods=['GET','POST'])
def vlogin():
    if session.get('vendor'):
        return redirect(url_for('vendor_dashboard'))
    if request.method=='POST':
        email=request.form['email']  
        password=request.form['password']    
        cursor=mydb.cursor(buffered=True)   
        cursor.execute('select password from vendor where email=%s',[email])
        hashed_password=cursor.fetchone()
       
        if hashed_password:
            hashed_password=hashed_password[0]
            if bcrypt.checkpw(password.encode('utf-8'), bytes(hashed_password)):
                session['vendor']=email
                if not session['vendor']:
                    session[email]={}
                return redirect(url_for('vendor_dashboard'))
            else:
                flash('Password incorrect')
                return redirect(url_for('vlogin'))
        else:
            flash('Email not registered.')
            return redirect(url_for('vendorsignup'))         
    return render_template('vlogin.html')
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        subject='Reset link for ecommerce Appliccation'
        body=f"Reset link for forgot password of ecommerce : {url_for('fconfirm',token=token(data=email,salt=salt2),_external=True)}"
        cmail(to=email,subject=subject,body=body)
       
        flash('Reset link has sent to given Email pls check')
        return redirect(url_for('forgot'))
    return render_template('forgot.html')
@app.route('/fconfirm/<token>',methods=['GET','POST'])
def fconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except Exception as e:
        return 'Link expired'
    else:
        if request.method=='POST':
            npassword=request.form['npassword']
            cnpassword=request.form['cnpassword']
            if npassword==cnpassword:
                bytes = npassword.encode('utf-8')
                # generating the salt
                salt = bcrypt.gensalt()
                # Hashing the password
                hash = bcrypt.hashpw(bytes,salt)
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update vendor set password=%s where email=%s',[hash,email])
                mydb.commit()
                cursor.close()
                return redirect(url_for('vlogin'))
            else:
                flash('password missmatch')
                return render_template('updatepassword.html')
    return render_template('updatepassword.html')
@app.route('/vendor_dashboard')
def vendor_dashboard():
    if session.get('vendor'):
        return render_template('vdashboard.html')
    else:
        return redirect(url_for('vlogin'))
@app.route('/vlogout')
def vlogout():
    if session.get('vendor'):
        session.pop('vendor')
        return redirect(url_for('vlogin'))
    else:
        return redirect(url_for('vlogin'))
@app.route('/additem',methods=['GET','POST'])
def additems():
    if session.get('vendor'):
        if request.method=='POST':
            name=request.form['name']
            dis=request.form['desc']
            qyt=request.form['qyt']
            category=request.form['category']
            price=request.form['price']
            img=request.files['image']
            imgextension=img.filename.split('.')[-1]
            imgname=genotp()
            filename=imgname+'.'+imgextension
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            img.save(os.path.join(static_path,filename))
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into additems(itemid,item_name,dis,qyt,category,price,added_by,img_id) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s,%s)',[name,dis,qyt,category,price,session.get('vendor'),filename])
            mydb.commit()
            cursor.close()
            flash(f'Item {name} Successfully added.')
            return redirect(url_for('vendor_dashboard'))
    return render_template('items.html')
@app.route('/viewitems')
def viewitems():
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('''select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems where added_by=%s''',[session.get('vendor')])
        count=cursor.fetchall()
        print(count)
        if count:
            return render_template('card.html',count=count)
        else:
            return render_template('card.html')
    else:
        return redirect(url_for('vlogin'))
@app.route('/deleteitem/<itemid>')
def deleteitem(itemid):
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select img_id from additems where itemid=uuid_to_bin(%s) and added_by=%s',[itemid,session.get('vendor')])
        count=cursor.fetchone()
        print(count)
        path=os.path.dirname(os.path.abspath(__file__))
        static_path=os.path.join(path,'static')
        file_path=os.path.join(static_path,count[0])
        os.remove(file_path)
        cursor.execute('delete from additems where itemid=uuid_to_bin(%s) and added_by=%s',[itemid,session.get('vendor')])
        mydb.commit()
        cursor.close()
        flash(f'item {itemid} deleted successfully')
        return redirect(url_for('viewitems'))
    return redirect(url_for('vlogin'))
@app.route('/updateitem/<itemid>',methods=['GET','POST'])
def updateitem(itemid):
    if session.get('vendor'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('''select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems where itemid=uuid_to_bin(%s) and added_by=%s''',[itemid,session.get('vendor')])
        count=cursor.fetchall()
        if request.method=='POST':
            name=request.form['name']
            dis=request.form['desc']
            qyt=request.form['qyt']
            category=request.form['category']
            price=request.form['price']
            if request.files['image'].filename=='':
                filename=count[0][7]
            else:
                img=request.files['image']
                imgextension=img.filename.split('.')[-1]
                imgname=genotp()
                filename=imgname+'.'+imgextension
                path=os.path.dirname(os.path.abspath(__file__))
                static_path=os.path.join(path,'static')
                file_path=os.path.join(static_path,count[0][7])
                os.remove(file_path)
                img.save(os.path.join(static_path,filename))
            cursor=mydb.cursor(buffered=True)
            cursor.execute('update additems set item_name=%s,dis=%s,qyt=%s,category=%s,price=%s,img_id=%s where itemid=uuid_to_bin(%s)',[name,dis,qyt,category,price,filename,itemid])
            mydb.commit()
            cursor.close()
            flash(f'item {name} updated successfully')
            return redirect(url_for('viewitems'))
        return render_template('updateitem.html',count=count)
    return redirect(url_for('vlogin'))
@app.route('/usersignup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        address = request.form['address']
        password = request.form['password']
        
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT COUNT(*) FROM user WHERE email=%s', [email])
            count = cursor.fetchone()[0]
            if count == 1:
                raise Exception
        except Exception as e:
            flash('Email already exists')
            return 'hi'
        else:
            # Generate OTP and send email
            otp = genotp()
            data = {'email': email, 'user_name': name, 'mobile_no': mobile_no, 'address': address, 'password': password, 'otp': otp}
            subject = 'OTP for Ecom app'
            body = f'Verification OTP for Ecom app: {otp}'
            # Assuming cmail() and token() functions are defined elsewhere
            cmail(to=email, subject=subject, body=body)
            flash('OTP has been sent to your email.')
            return redirect(url_for('otp_verification', data=token(data, salt=salt2)))
    return render_template('usersignup.html')
@app.route('/otp_verification/<data>', methods=['GET', 'POST'])
def otp_verification(data):
    try:
        serializer = URLSafeTimedSerializer(secret_key)
        data = serializer.loads(data, salt=salt2, max_age=120)
    except Exception as e:
        print(e)
        flash('Link expired')
        return redirect(url_for('usersignup'))
    else:
        if request.method == 'POST':
            uotp = request.form['otp']
            if uotp == data['otp']:
                try:
                    bytes = data['password'].encode('utf-8')
                # generating the salt
                    salt = bcrypt.gensalt()
                 # Hashing the password
                    hash = bcrypt.hashpw(bytes,salt)
                    # Hashing the password
                    cursor = mydb.cursor(buffered=True)
                    cursor.execute('INSERT INTO user (email, username, mobile_no, address, password) VALUES (%s, %s, %s, %s, %s)',(data['email'],data['user_name'], data['mobile_no'], data['address'], hash))
                    mydb.commit()
                    cursor.close()
                    flash('Registration successfully done.')
                    # Redirect to userlogin with token as parameter
                    return redirect(url_for('login'))
                except Exception as e:
                    print(e)
                    flash('Error occurred while registering user')
                    return redirect(url_for('usersignup'))
    return render_template('otp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('user_dashboard'))
    if request.method=='POST':
        email=request.form['email']  
        password=request.form['password']    
        cursor=mydb.cursor(buffered=True)   
        cursor.execute('select password from user where email=%s',[email])
        hashed_password=cursor.fetchone()
       
        if hashed_password:
            hashed_password=hashed_password[0]
            if bcrypt.checkpw(password.encode('utf-8'), bytes(hashed_password)):
                session['user']=email
                if not session.get(email):
                    session[email]={}
                return redirect(url_for('user_dashboard'))
            else:
                flash('Password incorrect')
                return redirect(url_for('login'))
        else:
            flash('Email not registered.')
            return redirect(url_for('usersignup'))         
    return render_template('userlogin.html')
@app.route('/user_dashboard')
def user_dashboard():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems')
    count=cursor.fetchall()

    if count:
        return render_template('home.html',count=count)
    else:
        return render_template('home.html')
@app.route('/userlogout')
def userlogout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))    
    return redirect(url_for('login'))    
@app.route('/category/<type>')
def category(type):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems where  category=%s',[type])
    count=cursor.fetchall()
    return render_template('udashboard.html',count=count)
@app.route('/dis/<itemid>')
def dis(itemid):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(itemid),item_name,dis,qyt,category,price,added_by,img_id from additems where  itemid=uuid_to_bin(%s)',[itemid])
    count=cursor.fetchone()
    print(count)

    return render_template('discription.html',count=count)
@app.route('/cart/<itemid>/<item_name>/<dis>/<category>/<price>/<img_id>/<qyt>')
def cart(itemid,item_name,dis,category,price,img_id,qyt):
    if not session.get('user'):
        return redirect(url_for('login'))
    print(session[session.get('user')])
    if itemid not in session[session.get('user')]:
        session[session.get('user')][itemid]=[item_name,dis,category,price,img_id,1]
        session.modified=True
        flash(f'{item_name} added to cart successfully ')
        return redirect(url_for('user_dashboard'))
    session[session.get('user')][itemid][5] += 1
    flash(f'{item_name} already added')
    return redirect(url_for('user_dashboard'))
@app.route('/viewcart')
def viewcart():
    if not session.get('user'):
        return redirect(url_for('login'))
    count=session.get(session.get('user')) if session.get(session.get('user')) else 'empty'
    if count=='empty':
        return 'No products added'
    print(count)
    return render_template('cart.html',count=count)
@app.route('/removecart/<itemid>')
def removecart(itemid):
    if session.get('user'):
        print(session[session.get('user')])
        data1=session[session.get('user')].pop(itemid)
        flash(f'{data1[0]} has been removed from cart')
        return redirect(url_for('viewcart'))
    return redirect(url_for('login'))
@app.route('/payment/<itemid>/<itemname>/<int:price>/<category>/<imgid>/<dis>',methods=['POST'])
def pay(itemid,itemname,price,category,imgid,dis):
    if session.get('user'):
        user=session.get('user')
        q=int(request.form['qyt']) if request.form['qyt'] else 1
        total=price*q
        checkout_session=stripe.checkout.Session.create(
            success_url=url_for('success',itemid=itemid,itemname=itemname,q=q,total=total,category=category,imgid=imgid,dis=dis,_external=True),
            line_items=[
                {
                    'price_data':{
                        'product_data':{
                            'name':itemname,
                        },
                        'unit_amount':price*100,
                        'currency':'inr',
                    },
                    'quantity':q,
                },
                ],
            mode="payment",)
        return redirect(checkout_session.url)
    else:
        return redirect(url_for('login'))
@app.route('/success/<itemid>/<itemname>/<q>/<total>/<category>/<imgid>/<dis>')
def success(itemid,itemname,q,total,category,imgid,dis):
    user=session.get('user')
    cursor=mydb.cursor(buffered=True)
    cursor.execute('insert into orders(ordid,itemid,item_name,qty,total_price,user,category,imgid,dis) values(uuid_to_bin(uuid()),uuid_to_bin(%s),%s,%s,%s,%s,%s,%s,%s)',[itemid,itemname,q,total,user,category,imgid,dis])
    mydb.commit()
    return redirect(url_for('orders'))
@app.route('/orders')
def orders():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(ordid),bin_to_uuid(itemid),item_name,qty,total_price,user,category,imgid,dis from orders where user=%s',[session.get('user')])
        count=cursor.fetchall()
        return render_template('orders.html',count=count)
    return redirect(url_for('login'))
'''@app.route('/getinvoice/<ordid>.pdf')
def invoice(ordid):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select username,mobile_no,address,u.email,bin_to_uuid(ordid),bin_to_uuid(itemid),item_name,qty,total_price,category,imgid,dis from user u join orders o on u.email=o.user where ordid=uuid_to_bin(%s)',[ordid])
    count=cursor.fetchone()
    if count:
        html=render_template('bill.html',count=count)
        pdf=pdfkit.from_string(html,False,configuration=config)
        response=Response(pdf,content_type='application/pdf')
        response.headers['Content-Disposition']='inline; filename=output.pdf'
        return response
    else:
        flash('something went wrong')
        return redirect(url_for('orders'))'''




app.run(debug=True,use_reloader=True)