from flask import Flask, render_template, url_for, redirect, session, request

.....
#TABLE FOR WRITING POSTS
class PostForm(FlaskForm):
	title=StringField('Title*', validators=[DataRequired()])
	body=TextAreaField('Body*', validators=[DataRequired()])
	submit=SubmitField('Post')
  
  
#CREATING A PAGE WITH THE POST FORM THAT, ONCE SUBMITTED, INSERTS THE POSTS INTO A MYSQL TABLE NAMED `posts`
@app.route('/post/', methods=["GET", "POST"])
@login_required
def post():
	try:
	
		form=PostForm()
		c, conn = connection()
	
		if request.method == "POST" and form.validate():
			username=session['username']
			author=session['name']
			title=form.title.data
			body=form.body.data
		
			c.execute("INSERT INTO posts(username, author, title, body) VALUES(%s, %s, %s, %s)", (username, author, thwart(title), thwart(body)))
			conn.commit()
			c.close()
			conn.close()
			return redirect(url_for('dashboard'))
		return render_template('post.html', title="Post", form=form)
	except Exception as e:
		return(str(e))

#RENDERING THE POSTS INTO A TIMELINE FORMATS VIA DATABASE QUERY FROM `posts` TABLE
@app.route('/dashboard/')
@login_required
def dashboard():
	try:
		dash=[]
		c, conn = connection()
		x = int(c.execute("SELECT pid FROM posts ORDER BY pid DESC"))
		for num in range(1,x+1):
			posts=[]
			username = c.execute("SELECT username FROM posts WHERE pid = {}".format(num))
			username = str(c.fetchone()[0])
			posts.append(username)
			
			author = c.execute("SELECT author FROM posts WHERE pid = {}".format(num))
			author = str(c.fetchone()[0])
			posts.append(author)
			
			title = c.execute("SELECT title FROM posts WHERE pid = {}".format(num))
			title = (str(c.fetchone()[0]).decode("string_escape"))
			posts.append(title)
			
			body = c.execute("SELECT body FROM posts WHERE pid = {}".format(num))
			body = (str(c.fetchone()[0])).decode("string_escape")
			posts.append(body)
			
			dash.append(posts)
			#the list here allows the programs
			#to successfully query it backwards by post id 
			#thus displaying most recent to least recent
		return render_template("dashboard.html", title="Dashboard", postings=dash)
	except Exception as e:
		return(str(e))
    ...
