import requests
import flask
from flask import Flask, request,jsonify
import json
from newsapi.newsapi_client import NewsApiClient
from datetime import date
from dateutil.relativedelta import relativedelta


config = {}
config['session'] = True
config['api_key'] = 'ca808a32a3fd6079b50303c14d98a3b609b7029b'
newsapi = NewsApiClient(api_key='57dabe18bbe645a58f22308b04696501')
application = flask.Flask(__name__)

# def start_app():
#     # app = flask.Flask(__name__)
#     compress.init_app(app)
#     return app

@application.route('/')
def index_page():
    # return render_template('D:/Web/index.html')
    # return 'Hello world!'
    try:
        return application.send_static_file("index.html")
    except Exception as e:
        print(e)
    # return ""


@application.route('/company_outlook', methods=['GET'])
def get_ticker_from_source():
    headers = {
        'Content-Type': 'application/json'
    }
    # This was giving me a badKey errors
    #keyword= request.form['searchbox']
    keyword=request.args.get('keyword')
    # keyword=reques
    #keyword = request.args.get('keyword',None)
    # company_outlook = tiingoclient.get_ticker_metadata(keyword)
    # print(company_outlook)
    # return  company_outlook
    #print(keyword)
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/"+keyword+"?token=ca808a32a3fd6079b50303c14d98a3b609b7029b", headers=headers)
    #print(jsonify(requestResponse.json()))
    #print(jsonify(requestResponse))
    #return requestResponse.json()
    return jsonify(requestResponse.json())

@application.route('/stock_summary',methods=['GET'])
def get_stock_summary():
    headers = {
        'Content-Type': 'application/json'
    }
    keyword=request.args.get('keyword')
    # stock_summary = tiingoclient.get(keyword)
    # print(keyword)
    # requestResponse = requests.get("https://api.tiingo.com/iex/?tickers="+keyword+"&token=ca808a32a3fd6079b50303c14d98a3b609b7029b", headers=headers)
    requestResponse = requests.get("https://api.tiingo.com/iex/?tickers="+keyword+"&token=ca808a32a3fd6079b50303c14d98a3b609b7029b", headers=headers)
    # print("Response",requestResponse.json())
    if not requestResponse.json():
        return jsonify({})
    else:
        return jsonify(requestResponse.json()[0])
# requestResponses = requests.get("https://api.tiingo.com/iex/?tickers=aapl&token=ca808a32a3fd6079b50303c14d98a3b609b7029b", headers=headers)
# print(requestResponses.json())

# ticker_metadata = client.get_ticker_metadata("GOOGL")
# print(ticker_metadata)

#get_ticker_from_source()
# get_stock_summary()       
# get_ticker_from_source()

@application.route('/chart_summary',methods=['GET'])
def get_high_chart():
    headers = {
        'Content-Type': 'application/json'
    }
    keyword = request.args.get('keyword')
    start_date = date.today() + relativedelta(months=-6)
    #print(start_date)
    date_time = start_date.strftime("%Y-%m-%d")
    print(date_time)
    # This returns an array of json,so need to check how we can parse this?
    requestResponse = requests.get("https://api.tiingo.com/iex/"+keyword+"/prices?startDate="+date_time+"&resampleFreq=12hour&columns=open,high,low,close,volume&token=ca808a32a3fd6079b50303c14d98a3b609b7029b", headers=headers) 
    # print(requestResponse.json())
    data = requestResponse.json()
    high_charts ={}
    high_charts['chart_data'] = data
    return jsonify(high_charts)

# Articles is an array and we need to diaplay top-5 articles.
@application.route("/news",methods=['GET'])
def get_latest_news():

    keyword = request.args.get('keyword')
    news = newsapi.get_everything(q=keyword)
    
    # print(news)
    return json.dumps(news)

#get_high_chart()

#get_latest_news()

if __name__ == "__main__":
    # start_app()
	application.run(debug=True)
