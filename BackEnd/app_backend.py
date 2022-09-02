from flask import Flask, request, jsonify
import schedule
import time
import pandas as pd
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import pickle

# initialize app
app = Flask(__name__)


# data is manually imported from (please check) notebook
token = ['ALI Token', 'AdShares', 'Age Of Knights', 'Atlantis Metaverse', 'CEEK VR', 'Decentraland', 'Drive 2', 'Enjin Coin', 'Fistiana', 'GameCredits', 'KingdomX', 'KlayCity', 'MStation', 'Magic Metaverse', 'MangaMon', 'Meta Dance Token', 'MetaCars', 'Metaverse Miner', 'Monavale', 'Moon Rabbit', 'PlayDapp', 'Sinverse', 'Star Atlas DAO', 'UFO Gaming', 'Verasity', 'X Protocol']
original_prices = [0.009009009525727724, 0.32861077253194404, 0.03320053149075533, 0.0029938289524685385, 0.279196300157807, 0.153997532226834, 0.0018040174615156427, 0.09526050235854708, 0.0011107735084844583, 0.019209789881132835, 0.6161988571754959, 0.06174926444372217, 0.003030115798964131, 0.16621370596038176, 0.011224015220876672, 0.07299748470105882, 0.04844021552926039, 0.016174810321490388, 0.010843669410543239, 0.017684890896706953, 0.015267177506943359, 0.0167087409858082, 0.0008265611199306522, 0.05804046686719992, 0.0036570863977862383, 0.005999331789919661]
future_prices = [1.3134313121554442e-05, 1.4056316614151, 9.59637836785987e-05, 0.020582780241966248, 0.2336307317018509, 0.6720395684242249, 0.012508251704275608, 0.4241279363632202, 0.2520744800567627, 0.016123205423355103, 0.09946747869253159, 0.07731432467699051, 0.006555549800395966, 0.001912317587994039, 0.007072742562741041, 0.025181720033288002, 0.0019404147751629353, 0.036209430545568466, 0.5105111002922058, 3.533509880071506e-05, 8.969238479039632e-06, 0.0007363884942606091, 0.038526568561792374, 0.0005155240651220083, 0.005114264320582151, 0.0032673049718141556]
growth = [-0.9985420913271269, 3.277497206146702, -0.9971095708601737, 5.875068872921038, -0.16320262277903252, 3.3639632317895174, 5.933553566475359, 3.452295818962434, 225.93598481718712, -0.16067767929149834, -0.8385789302686051, 0.25206875536880635, 1.163465106725305, -0.9884948261219213, -0.36985629264064623, -0.6550330448177382, -0.9599420697459361, 1.2386309221480896, 46.079183343217636, -0.998001961165206, -0.99941251495406, -0.9559279484381217, 45.61067116854556, -0.9911178511657813, 0.39845323962758816, -0.4553885188840491]
risk = ['low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'high', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'medium', 'low', 'low', 'low']
recommendation = ['sell', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'buy', 'buy', 'sell', 'sell', 'buy', 'buy', 'sell', 'sell', 'sell', 'sell', 'buy', 'buy', 'sell', 'sell', 'sell', 'buy', 'sell', 'buy', 'sell']
symbols = ['ALI', 'ADS', 'GEM', 'TAU', 'CEEK', 'MANA', 'DMT', 'ENJ', 'FCT', 'GAME', 'KT', 'ORB', 'MST', 'MAC', 'MAN', 'MDT', 'MTC', 'META', 'MONA', 'AAA', 'PLA', 'SIN', 'POLIS', 'UFO', 'VRA', 'POT']

result = pd.DataFrame()
result['token'] = token
result['original_prices'] = original_prices
result['future_prices'] = future_prices
result['growth'] = growth
result['risk'] = risk
result['recommendation'] = recommendation
result['symbols'] = symbols

# define function to open model
def open_model(model_path):
    with open(model_path, "rb") as modelfile:
        model = pickle.load(modelfile)
    return model

# regressor = open_model("regressor_model.pkl")

@app.route("/")  # Home
def home():
    return "Program is up and running"

# define function to get real time price
prices = {}
updates = []

def get_data():
    url = f'https://rest.coinapi.io/v1/quotes/current'
    headers={"X-CoinAPI-Key": "004D4DE3-D4F9-4C91-8535-BB9552467393"}
    response = requests.get(url, headers=headers)

    for i in result['symbols']:
        for j in range(len(response.json())):
            if i in response.json()[j]['symbol_id']:
                updates.append(i)
                prices[i] = response.json()[j]['ask_price']

    return updates, prices

sc = MinMaxScaler(feature_range=(0,1))
@app.route("/predict")  # Home
def predict_future():
    update_symbol, price_result = get_data()
    for i, value in enumerate(update_symbol):
        a0 = np.array(price_result[value])
        a0 = a0.reshape(a0.shape[0],1)
        transform_inf = sc.fit_transform(a0)
        scaler_inf = {}
        scaler_inf = sc

        time_step = 7
        X_test = []
        y_test = []
        testset_inf = {}

        for j in range(len(transform_inf) - time_step -  1):
            X_test.append(transform_inf[j:(j + time_step), 0])
            y_test.append(transform_inf[j + time_step, 0])
        
        X_test, y_test = np.array(X_test), np.array(y_test)
        testset_inf["X"] = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        testset_inf["y"] = y_test
        y_future = []

        x_pred = testset_inf['X'][-1:, :, :]
        y_pred = testset_inf["y"][-1]

        for j in range(10):
            x_pred = np.append(x_pred[:, 1:, :], y_pred.reshape(1, 1, 1), axis=1)
            # y_pred = regressor.predict(x_pred)
            y_future.append(y_pred.flatten()[0])

        y_future = np.array(y_future).reshape(-1, 1)
        y_future = scaler_inf.inverse_transform(y_future)
        return y_future[0][0]

price_container = {}
  
# define scheduler
def helper_predict():
    price_container = predict_future()
    return price_container
    
schedule.every(10).days.do(helper_predict)

while True:
    schedule.run_pending()
    time.sleep(1)

# app.run(debug=True)