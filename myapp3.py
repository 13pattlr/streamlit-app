import streamlit as st
import requests
import pandas as pd
import datetime
import yfinance as yf
import streamlit_authenticator as stauth
import streamlit.components.v1 as stc 
import plotly.express as px 
import matplotlib.pyplot as plt 
import matplotlib
import seaborn as sns
import numpy as np
import altair as alt
import plotly.graph_objects as go
from pandas import read_html as rh
from bs4 import BeautifulSoup as bs
import tweepy
import config 
import psycopg2, psycopg2.extras



#Potential Next Projects
#scheduled tasks?
#open ended beautiful soup scaper
#craigslist scraper (real estate rentals)
#plotting craiglist real estate data
#geographical plotting, potentially around airbnb listings
#connect into social media api and surface keywords
#google trends?
#more complex forecasting
#machine learning






today = datetime.date.today()
default_start_date = today - datetime.timedelta(days=(365*5))


names = ['Patrick','Guest','pt']
usernames = ['patrick','guest','pt']
passwords = ['patrickpassword','guestpassword','pw']



hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,
'some_cookie_name','some_signature_key',cookie_expiry_days=0)

name, authentication_status = authenticator.login('Login','main')


HTML_BANNER = """
	    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
	    <h1 style="color:white;text-align:center;">PT's Viz App </h1>
	    <p style="color:white;text-align:center;">Built by Streamlit</p>
	    </div>
	    """

if authentication_status == True:
    st.write('Welcome *%s*' % (name))
    menu = ["Stock Prices","Option Prices","Probability","Twitter Mentions","About"]
    choice = st.sidebar.selectbox("Menu",menu)

if authentication_status == True:
	headers = {
		    'authority': 'api.nasdaq.com',
		    'accept': 'application/json, text/plain, */*',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
		    'origin': 'https://www.nasdaq.com',
		    'sec-fetch-site': 'same-site',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-dest': 'empty',
		    'referer': 'https://www.nasdaq.com/',
		    'accept-language': 'en-US,en;q=0.9',
	}

	params = (
		    ('tableonly', 'true'),
		    ('limit', '25'),
		    ('offset', '0'),
		    ('download', 'true'),
	)
	r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
	data = r.json()['data']
	df = pd.DataFrame(data['rows'], columns=data['headers'])

	ticker_list = df['symbol']
		 


if authentication_status == True:
	stc.html(HTML_BANNER)
	
	if choice == "Stock Prices":
		ticker = st.selectbox('Stock Ticker', ticker_list, index=19)

		start_date = st.date_input('Start Date', default_start_date)

		end_date = st.date_input('End Date', today)


		df_stockdata = yf.download(ticker, start=start_date, end = end_date,)
		df_stockdata2 = df_stockdata

		df_stockdata2["Share Price"] = df_stockdata2["Close"]
		df_stockdata_close = df_stockdata2['Share Price']
		st.subheader(ticker + " Stock Chart")
		st.line_chart(df_stockdata_close)



		df_stockdata.reset_index(inplace=True)
		# # df.reset_index(inplace=True)
		df = df_stockdata
		# # df.reset_index(inplace=True)
		st.dataframe(df.tail(10))

		df['20wma'] = df['Close'].rolling(window = 140).mean()

		fig = go.Figure(data=[go.Candlestick(x=df['Date'],
		                open=df['Open'],
		                high=df['High'],
		                low=df['Low'],
		                close=df['Close'],name = ticker + " Share Price",)])
		fig.add_trace(go.Scatter(x=df['Date'],y=df['20wma'], line = dict(color = '#e0e0e0'), name = "20 Week Moving Average", ))
		fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")
		fig.update_layout(plot_bgcolor='rgb(15,15,15)')
		fig.update_layout(title = "Candle Stick Chart", yaxis_title = "Share Price", xaxis_title = "Date")
		st.plotly_chart(fig, use_container_width=True)



	elif choice == "Option Prices":
		st.subheader("Option Prices")
		st.subheader("Pull Recent Option Prices from the Yahoo Finance Website")
		st.caption("Stocks without Options may cause errors")



		
		ticker = st.selectbox('Stock Ticker', ticker_list, index=19)

		url = "https://finance.yahoo.com/quote/" + ticker + "/options?p="+ticker

		r = requests.get(url, headers = {'User-Agent':'Mozilla/5.0'})
		soup = bs(r.content, 'lxml')

		calls_table = rh(str(soup.select_one('[class="calls W(100%) Pos(r) Bd(0) Pt(0) list-options"]')))[0]
		st.caption(ticker + " Calls")
		st.dataframe(calls_table)
		calls_table_csv = calls_table.to_csv()
		st.download_button(label="Download as CSV", data=calls_table_csv, file_name="calls_data.csv",mime='text/csv')


		puts_table = rh(str(soup.select_one('[class="puts W(100%) Pos(r) list-options"]')))[0]
		st.caption(ticker + " Puts")
		st.dataframe(puts_table)
		puts_table_csv = puts_table.to_csv()
		st.download_button(label="Download as CSV", data=puts_table_csv, file_name="put_data.csv",mime='text/csv')






	elif choice == "Probability":
		st.sidebar.selectbox("Project",("Loaded Dice",))

		st.subheader("Probability")
		st.subheader("Loaded Dice:")
		st.caption("We want to determine the outcome of rolling a dice with unfair probability")
		st.caption("Input the probability of each side of the dice. All inputs need to add up to 1.")
		prob_rolling_a_1 = st.slider('Probability of rolling a 1', min_value=0.0,max_value=1.0,value=.2,step=.01)
		prob_rolling_a_2 = st.slider('Probability of rolling a 2', min_value=0.0,max_value=1.0,value=.2,step=.01)
		prob_rolling_a_3 = st.slider('Probability of rolling a 3', min_value=0.0,max_value=1.0,value=.2,step=.01)
		prob_rolling_a_4 = st.slider('Probability of rolling a 4', min_value=0.0,max_value=1.0,value=0.0,step=.01)
		prob_rolling_a_5 = st.slider('Probability of rolling a 5', min_value=0.0,max_value=1.0,value=.2,step=.01)
		prob_rolling_a_6 = st.slider('Probability of rolling a 6', min_value=0.0,max_value=1.0,value=.2,step=.01)
		# def add_numbers(prob_rolling_a_1, prob_rolling_a_2, prob_rolling_a_3, prob_rolling_a_4, prob_rolling_a_5, prob_rolling_a_6):
		# 	total_value = prob_rolling_a_1+prob_rolling_a_2+prob_rolling_a_3+prob_rolling_a_4+prob_rolling_a_5+prob_rolling_a_6
		# 	print('total_value')
		# st.text(add_numbers(prob_rolling_a_1, prob_rolling_a_2, prob_rolling_a_3, prob_rolling_a_4, prob_rolling_a_5, prob_rolling_a_6))
		# if ((prob_rolling_a_1+prob_rolling_a_2+prob_rolling_a_3+prob_rolling_a_4+prob_rolling_a_5+prob_rolling_a_6)>1) == True
		# 	st.text("test 1")
		# elif
		# 	st.text("test 2")
		# st.text((123))
		total_value = prob_rolling_a_1+prob_rolling_a_2+prob_rolling_a_3+prob_rolling_a_4+prob_rolling_a_5+prob_rolling_a_6
		st.text("Total Value = %f" % (total_value))
		b = 1.00
		if total_value != b:
			st.text("Please Sum Up the Probabilities to 1")
		elif total_value == b:
			st.text("Clear to Proceed to Next Step")
		





		trial_count = st.number_input("Number of Trials", min_value=1, max_value=1000000,step=1,value=1000)



		dice_roll_1 = 0
		dice_roll_2 = 0
		dice_roll_3 = 0
		dice_roll_4 = 0
		dice_roll_5 = 0
		dice_roll_6 = 0
		total = 0


		def dice_rolls(trials):
		  global dice_roll_1
		  global dice_roll_2
		  global dice_roll_3
		  global dice_roll_4
		  global dice_roll_5
		  global dice_roll_6
		  global total
		  
		  for i in range(trials):
		    roll = np.random.choice(np.arange(1,7), p=[prob_rolling_a_1,prob_rolling_a_2,prob_rolling_a_3,prob_rolling_a_4,prob_rolling_a_5,prob_rolling_a_6]) 
		    if roll == 1:
		      dice_roll_1 += 1
		    elif roll == 2:
		      dice_roll_2 += 1
		    elif roll == 3:
		      dice_roll_3 += 1
		    elif roll == 4:
		      dice_roll_4 += 1
		    elif roll == 5:
		      dice_roll_5 += 1
		    elif roll == 6:
		      dice_roll_6 += 1
		    total += 1
		  

		st.button("Run Trials", on_click=dice_rolls(trial_count),)


		count_dice_1 = st.text('Count Where the Dice Rolled a 1: ' + str(dice_roll_1) + ' times')
		count_dice_2 = st.text('Count Where the Dice Rolled a 2: ' + str(dice_roll_2) + ' times')
		count_dice_3 = st.text('Count Where the Dice Rolled a 3: ' + str(dice_roll_3) + ' times')  
		count_dice_4 = st.text('Count Where the Dice Rolled a 4: ' + str(dice_roll_4) + ' times')
		count_dice_5 = st.text('Count Where the Dice Rolled a 5: ' + str(dice_roll_5) + ' times')
		count_dice_6 = st.text('Count Where the Dice Rolled a 6: ' + str(dice_roll_6) + ' times')




		probability_dice_roll_1 = "{:.0%}". format(dice_roll_1/total)
		probability_dice_roll_2 = "{:.0%}". format(dice_roll_2/total)
		probability_dice_roll_3 = "{:.0%}". format(dice_roll_3/total)
		probability_dice_roll_4 = "{:.0%}". format(dice_roll_4/total)
		probability_dice_roll_5 = "{:.0%}". format(dice_roll_5/total)
		probability_dice_roll_6 = "{:.0%}". format(dice_roll_6/total)




		pct_dice_1 = st.text('Percentage Time the Dice Rolled a 1: ' + str(probability_dice_roll_1) + ' of time')
		pct_dice_2 = st.text('Percentage Time the Dice Rolled a 2: ' + str(probability_dice_roll_2) + ' of time')
		pct_dice_3 = st.text('Percentage Time the Dice Rolled a 3: ' + str(probability_dice_roll_3) + ' of time')  
		pct_dice_4 = st.text('Percentage Time the Dice Rolled a 4: ' + str(probability_dice_roll_4) + ' of time')
		pct_dice_5 = st.text('Percentage Time the Dice Rolled a 5: ' + str(probability_dice_roll_5) + ' of time')
		pct_dice_6 = st.text('Percentage Time the Dice Rolled a 6: ' + str(probability_dice_roll_6) + ' of time')








		data1 = [dice_roll_1,dice_roll_2,dice_roll_3,dice_roll_4,dice_roll_5,dice_roll_6]
		data2 = ["Roll = 1","Roll = 2","Roll = 3","Roll = 4","Roll = 5","Roll = 6"]








	elif choice == "Twitter Mentions":
		st.subheader("Twitter Mentions")
		ticker = st.selectbox('Stock Ticker', ticker_list, index=19)

		r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json")
		data = r.json()
		#st.write(data)
		for message in data['messages']:

			st.image(message['user']['avatar_url'])
			st.write(message['user']['username'])
			st.write(message['created_at'])
			st.write(message['body'])



		# 
	elif choice == "About":
		st.subheader("About")
		st.text("PT is looking to improve his coding skills")

	else:
            st.subheader("About PT's Streamlit App")
            st.info("Built with Streamlit")
            st.info("PT")
            st.text("PT is looking to improve his data skills")



elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

