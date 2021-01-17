from flask import Flask, request, session
from flask import render_template
import requests
import json

app = Flask(__name__)
app.secret_key='secret'


@app.route('/')
def home_page():
    #initiate session variables
    session['badGuess'] = -1
    session['hints'] = []
    return render_template('home_page.html')

@app.route('/image', methods = ['POST', 'GET'])
def image_page():
    isCorrect = ''
    
    if request.method == 'POST':
        if request.form['randomWord'] == 'Random Word':
            responseWord = requests.get('https://random-word-api.herokuapp.com/word?number=1')
            session['imageWord'] = responseWord.json()[0]
            API_KEY = 'AIzaSyDuAf7WIjldlxW2NvgXzZ9qZPLkukQmEsQ'
            response = requests.get('https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=006191701364648993407:mcl3f-voruw&searchType=image&q='+ session['imageWord'])
            image_dict = response.json()
            session['imageURL'] = image_dict['items'][0]['link']
            print(session.get('imageURL'))
            print(session.get('imageWord'))

            #Generate underscores to indicate word length
            for i in range(len(session.get('imageWord'))):
                session['hints'].append('_ ')

        #Compare guess word to real query    
        guess = request.form.get("guess")
        if guess == session.get('imageWord'):
            isCorrect = 'Correct'
            session['hints'] = session.get('imageWord')
        else:
            session['badGuess'] += 1
            isCorrect = str(session.get('badGuess')) + ' tries made'
            if session.get('badGuess') > 2:
                #TODO: generate random letters
                session['hints'][session.get('badGuess')-3] = session['imageWord'][session.get('badGuess')-3]


        


        
        
    return render_template('image.html', image=session.get('imageURL'), correct=isCorrect, hints="".join(session['hints']))

if __name__=='__main__':
    app.run()