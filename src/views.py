# Copyright 2020 `Kumar Nityan Suman` (https://github.com/nityansuman/). All Rights Reserved.
#
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
# ==============================================================================


# Import packages
from src import app
from flask import render_template, request
from src.utilities import MasterProphet
import yfinance as yf
import requests


@app.after_request
def add_header(response):
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

@app.route("/")
@app.route("/home")
def home():
	''' Renders the home page '''
	return render_template(
		"index.html"
	)

@app.route("/predict", methods=["POST", "GET"])
def predict():
	source_list = []
	url_list = []
	title_list = []

	ticker = request.form['ticker']
	#sending the ticker which is post from user front end
	make_uri_str = "https://newsapi.org/v2/everything?q={}&from=2021-03-23&sortBy=publishedAt&apiKey=545b62712cf14389b14d9a1af74d60cb".format(ticker)
	resp = requests.get(make_uri_str)
	print(resp.json())
	if resp.status_code != 200:
    # This means something went wrong.
		print("error")
    	# raise ApiError('GET /newapi/ {}'.format(resp.status_code))
	else:
		# print(resp.json())

		news_data = resp.json()
		article_data = news_data["articles"]
		for i in article_data[0:4]:
			print("SOURCE" , i["source"]["name"])
			print("TITLE" , i["title"])
			print("url" , i["url"])
			print("publishedAt" , i["publishedAt"])

			source = i["source"]["name"]
			title = i["title"]
			url = i["url"]
			publish = i["publishedAt"]
			source_list.append(source)
			url_list.append(url)
			title_list.append(title)

	yahoo_news_var = yf.Ticker(ticker)
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	# print(yahoo_news_var.info)
	master_prophet = MasterProphet(ticker)
	forecast = master_prophet.forecast()
	actual_forecast = round(forecast.yhat[0], 2)
	lower_bound = round(forecast.yhat_lower[0], 2)
	upper_bound = round(forecast.yhat_upper[0], 2)
	
	bound = round(((upper_bound - actual_forecast) + (actual_forecast - lower_bound) / 2), 2)
	# print(master_prophet.info)
		
	summary = master_prophet.info["summary"]
	country = master_prophet.info["country"]
	sector = master_prophet.info["sector"]
	website = master_prophet.info["website"]
	min_date = master_prophet.info["min_date"]
	max_date = master_prophet.info["max_date"]
	#new added today
	employees = master_prophet.info["employees"]


	forecast_date = master_prophet.forecast_date.date()
	
	return render_template(
		"output.html",
		ticker = ticker.upper(),
		sector = sector,
		country = country,
		website = website,
		summary = summary,
		min_date = min_date,
		max_date = max_date,
		forecast_date = forecast_date,
		forecast = actual_forecast,
		bound = bound,
		employees = employees,
		source_list = source_list,
		url = url_list,
		title = title_list
		
		)