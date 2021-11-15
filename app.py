from flask import Flask, request, render_template

import json
import ast

f = open('./dinamin_1.json', encoding="utf8")
data = json.load(f)
f.close()


def get_sent(sent_num):
    sent = data[sent_num]['details']
    s = []
    for  i in sent:
        if(i[-1]=="."):
            x = i[:-1]
            s += x.split(" ")
            s.append(".")
        else:
            s += i.split(" ")
            s.append(".")
    return(s)

def write_to_file(words, tags, count):
    file = open('train.txt', 'a', encoding="utf8")
    for i in range(len(words)):
        file.write(words[i] + "\t" + tags[i])
        file.write("\n")
    file.close()
    f = open('count.txt', 'w')
    f.write(str(count))
    f.close()

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"] )
def home_form():
    if request.method == "GET":
        f = open('count.txt', 'r')
        c = int(f.read())
        f.close()
        return render_template('index.html', word_list=get_sent(c), count=c)

    if request.method == "POST":
        count = int(request.form['count']) + 1
        tags = request.form.getlist("ner_tags[]")
        words = ast.literal_eval(request.form['words'])

        write_to_file(words, tags, count)

        return render_template('index.html', word_list=get_sent(count), count=count)

@app.route('/next', methods = ["GET"] )
def home_form_next():
    f = open('count.txt', 'r')
    c = int(f.read()) + 1
    f.close()
    f = open('count.txt', 'w')
    f.write(str(c))
    f.close()
    
    return render_template('index.html', word_list=get_sent(c), count=c)

if __name__ == '__main__':
    app.run()