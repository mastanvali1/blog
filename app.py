from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
mydb=mysql.connector.connect(host='localhost',user='root',password='MASTAN',db='mastan')
with mysql.connector.connect(host='localhost',password='MASTAN',user='root',db='mastan'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(Username varchar(30) primary key,Mobile varchar(30) unique,Address varchar(30),Email varchar(50) unique,Password varchar(50))")
@app.route("/home")
def home():
    return render_template("homepage.html")
@app.route("/reg",methods=['GET','POST'])
def register():
    if request.method=="POST":
        Username=request.form['Username']
        Mobile=request.form['Mobile']
        Address=request.form['Address']
        Email=request.form['Email']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[Username,Mobile,Email,Address,Password])
        cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INT NOT NULL AUTO_INCREMENT,title VARCHAR(255) DEFAULT NULL,content TEXT,date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,slug VARCHAR(255) DEFAULT NULL,poster_id VARCHAR(50) DEFAULT NULL,PRIMARY KEY (id),KEY poster_id (poster_id),CONSTRAINT fk_poster_id FOREIGN KEY (poster_id) REFERENCES registration (username))")
        mydb.commit()
        cursor.close()
        # return redirect('/login')
        return redirect(url_for('login'))
        print(Username)
    return render_template('register.html')
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        Username=request.form['Username']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where Username=%s && Password=%s',[Username,Password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['Username']=Username
            if not session.get(session['Username']):
                session[session['Username']]={}
            # return redirect('/')
            return redirect(url_for('home'))
        else:
            return"Invalid Username and Password"
    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('Username'):
        session.pop('Username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/addpost',methods=['GET','POST'])
def addpost():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts (title,content,slug) values (%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('addpost.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('delete from posts where id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost'))
@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    if request.method == 'POST':
        title=request.form['title']
        content = request.form['content']
        slug=request.form['slug']
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("UPDATE posts SET title = %s, content = %s, slug = %s where id = %s", (title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
       cursor=mydb.cursor(buffered=True)
       cursor.execute('select * from posts where id = %s',(id,))
       post=cursor.fetchone()
       cursor.close()
       return render_template('update.html',post=post)
app.run()