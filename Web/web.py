from flask import Flask, render_template, request, redirect
from sqlite_ import insert
app = Flask(__name__)

@app.route('/')
def index():
	title = "Temperature Control"
	return render_template('index.html', title=title)

@app.route('/cats')
def cats():
	return render_template('cats.html')

@app.route('/send', methods = ['POST'])
def send():
	
        heat = False
        cool = False

        if 'Heat' in request.form:
                heat = True
	if 'Cool' in request.form:
                cool = True

        settings = (heat, cool)
        #print settings

        insert([settings])

	return redirect('/')
	
if __name__== '__main__':
	app.run('0.0.0.0', debug=True)
        
