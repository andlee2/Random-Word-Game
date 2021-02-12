from flask import Flask, request, session, redirect, render_template
import requests
import json
import random 

app = Flask(__name__)
app.secret_key='secret'

@app.route('/', methods = ['POST', 'GET'])
def home_page():
    #initiate session variables
    session['badGuess'] = -1
    session['hints'] = []
    session['letterHints'] = []
    session['gameStatus'] = ''
    session['images'] = [] #Image links
    return render_template('home_page.html')

@app.route('/image', methods = ['POST', 'GET'])
def image_page():
    isCorrect = '' #Remove
    
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

            #Generate underscores to indicate word length and generate letter hints
            for i in range(len(session.get('imageWord'))):
                session['hints'].append('_ ')
                session['letterHints'].append(i)

        #Compare guess word to real query    
        guess = request.form.get("guess")
        #Correct Guess
        if guess == session.get('imageWord'):
            isCorrect = 'Correct'
            session['hints'] = session.get('imageWord')
            session['gameStatus'] = 'You won with ' + str(session.get('badGuess')) + ' tries'
            return redirect('/gameover')
        #Incorrect Guess
        else:
            session['badGuess'] += 1
            isCorrect = str(session.get('badGuess')) + ' tries made'
            if session.get('badGuess') > 2 and session.get('badGuess') < (len(session.get('imageWord')) + 2): #Generate Random Letters
                random.seed()
                position = random.randrange(0, len(session.get('letterHints')))
                letterPositionNum = session['letterHints'][position]
                session['letterHints'].remove(letterPositionNum)
                session['hints'][letterPositionNum] = session['imageWord'][letterPositionNum]
            elif session.get('badGuess') >= (len(session.get('imageWord')) + 2):
                session['gameStatus'] = 'You are a failure, the correct word was ' + session.get('imageWord')
                return redirect('/gameover')

    return render_template('image.html', image=session.get('imageURL'), correct=isCorrect, hints="".join(session['hints']))

@app.route('/gameover')
def gameover_page():
    return render_template('gameover.html', status=session.get('gameStatus'))

if __name__=='__main__':
    app.run()