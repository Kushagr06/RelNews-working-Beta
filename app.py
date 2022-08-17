from flask import Flask, redirect,render_template,request, url_for
import urllib.request, urllib.parse, urllib.error
import ssl
import ast

from newsapi import NewsApiClient

#ignore ssl certifications
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Init
newsapi = NewsApiClient(api_key='8990db3b361549da90178fc962d263d7')

def headlines(ctry):
 top_headlines = newsapi.get_top_headlines(country=ctry,page_size=25)   
 return top_headlines


def general(topic,frod,tod):
    all_articles = newsapi.get_everything(q=topic,
                                      from_param=frod,
                                      to=tod,
                                      language='en',
                                      sort_by='relevancy',
                                      page_size=25)
    return all_articles



app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
  if request.method=='POST':

   topic=request.form['topic']
   
   fro=request.form['from']
   

   to=request.form['to']
   

   type=request.form['type']
   ctry=request.form['ctry']

#    print(topic)
#    print(type)
#    print(fro)
#    print(to)
#    print(ctry)

   if(type=='2'):
    info= general(topic,fro,to)
   if(type=='1'):
    info= headlines(ctry)

   
   
   return redirect(url_for('hello_results',info=info))



  return render_template('index.html')



@app.route("/results")
def hello_results():
    info=request.args.get("info",None)
    
    y=ast.literal_eval(info)
    articles=y["articles"]
   
    return render_template('results.html',articles=articles)
 
 

if __name__ == '__main__':
    app.run(debug=True)