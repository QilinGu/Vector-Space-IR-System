import web
from web import form
from cosine_similarity_computing import search, get_similar_docs
import json

#open and read a json file into "data"
with open('2015_movies.json') as data_file:
    data = json.load(data_file)

render = web.template.render('templates/')

urls = ('/', 'index',
		'/results', 'results',
        '/similars','similars')
app = web.application(urls, globals())

myform = form.Form(form.Textbox("query:"))
next_button_myform = form.Form(form.Button("button", value="next", html="Next"),
                               form.Button("button", value="last", html="Last"))

class index:
    def GET(self):
        form = myform()
        return render.page_1(form)

class results:
    def GET(self):
        global hits, content_list, ignore_words, unknown_search_words, readUntilHere
        form = myform()
        if not form.validates():
            return render.page_1(form)
        #do search query
        readUntilHere = 10
        hits, content_list, ignore_words, unknown_search_words = search(form["query:"].value)
        return render.page_2(hits, content_list, readUntilHere, data, ignore_words, unknown_search_words, form(), next_button_myform())

    def POST(self):
        global hits, content_list, ignore_words, unknown_search_words, readUntilHere
        form = myform()
        if not form.validates():
            return render.page_1(form)
        web_data = web.input(doc_id = "")
        if web_data.button == 'next':
            if readUntilHere+10 <= len(content_list):
                readUntilHere = readUntilHere + 10
            else:
                readUntilHere = readUntilHere
        elif web_data.button == 'last':
            if readUntilHere-10 >= 10:
                readUntilHere = readUntilHere - 10
            else:
                readUntilHere = readUntilHere
        #do search query
        return render.page_2(hits, content_list, readUntilHere, data, ignore_words, unknown_search_words, form(), next_button_myform())

class similars:
    def GET(self):
        doc_id = str(web.input().doc_id)
        content_list = get_similar_docs(doc_id)
        return render.page_3(content_list, data)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
