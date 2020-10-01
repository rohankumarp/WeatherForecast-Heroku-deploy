import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime,date
import pyowm
from pyowm import OWM
from matplotlib import rcParams
from pytz import timezone
from pyowm.utils import timestamps

weather_api='0833f103dc7c2924da06db624f74565c'
owm=OWM(weather_api)



def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()

html_temp = """
  <div style="background-color:black ;padding:10px">
  <h1 style="color:green;text-align:center;">Weather Forecaster ❄️🌧️🌦️⛅🌞🌕 </h1>
  </div>
  """
st.markdown(html_temp, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>Made by Rohan Kumar</h2>",
            unsafe_allow_html=True)
#html_temp = """
  #<div style="background-color:black ;padding:10px">
 # <h2 style="color:green;text-align:center;">MADE BY ROHAN KUMAR </h2>
  #</div>
  #"""
#st.markdown(html_temp, unsafe_allow_html=True)

st.write("### Follow the steps :")
place=st.text_input("ENTER NAME OF THE CITY :", "")
unit=st.selectbox("SELECT THE TEMPERATURE UNIT",("Celsius (°C)","Fahrenheit(°F)"))

g_type=st.selectbox("SELECT THE TYPE OF GRAPH",("Line Graph","Bar Graph"))
b=st.button("ENTER")


def plot_line(days, min_t, max_t):
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 7, 4
    plt.plot(days, max_t, color='green', linestyle='dashdot', linewidth=2, marker='o', markerfacecolor='red',
              markersize=6)
    plt.plot(days, min_t, color='red', linestyle='dashdot', linewidth=2, marker='o', markerfacecolor='green',
              markersize=6)
    plt.ylim(min(min_t) - 4, max(max_t) + 4)
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%d/%m')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.grid(True, color='white')
    plt.legend(["Maximum Temperaure", "Minimum Temperature"], loc=1)
    plt.xlabel('Dates(dd/mm)')
    plt.ylabel('Temperature')
    plt.title('5-Day Forecast')

    for i in range(5):
        plt.text(days[i], min_t[i] - 1.5, min_t[i],
                  horizontalalignment='center',
                  verticalalignment='bottom',
                  color='green')
    for i in range(5):
        plt.text(days[i], max_t[i] + 0.5, max_t[i],
                  horizontalalignment='center',
                  verticalalignment='bottom',
                  color='red')
    # plt.show()
    #plt.savefig('line.png')
    st.pyplot()
    plt.clf()


def plot_bars(days,min_t,max_t):  
        #print(days)      
        rcParams['figure.figsize']=6,4
        days=dates.date2num(days)
        #print(days) 
        min_temp_bar=plt.bar(days-0.2, min_t, width=0.3, color='yellow')
        max_temp_bar=plt.bar(days+0.2, max_t, width=0.3, color='green')
        plt.xticks(days)
        x_y_axis=plt.gca()
        xaxis_format=dates.DateFormatter('%d/%m')
        
        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.xlabel('Dates(dd/mm)')
        plt.ylabel('Temperature') 
        plt.title('5-Day Forecast')
        
        for bar_chart in [min_temp_bar,max_temp_bar]:
            for index,bar in enumerate(bar_chart):
                height=bar.get_height()
                xpos=bar.get_x()+bar.get_width()/2.0
                ypos=height 
                label_text=str(int(height))
                plt.text(xpos, ypos,label_text,
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='red')
        
        
        st.pyplot()
        plt.clf()
        
        

def find_min_max(place,unit,g_type):
    mgr=owm.weather_manager()
    days=[]
    dates_2=[]
    min_t=[]
    max_t=[]
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    if unit=='Celsius':
        unit_c='celsius'
    else:
        unit_c='fahrenheit'
    
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_2:
            dates_2.append(date)
            min_t.append(None)
            max_t.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1]=temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1]=temperature
    #days = dates.date2num(days)
    #plt.xticks(days)
    #return days,min_t,max_t
    #print(f"| Minimum Temperature in {unit_c} for {place} is |",min_t)
    #print(f"| Maximum Temperature in {unit_c} for {place} is |",max_t)
    if g_type=="Line Graph":
        plot_line(days,min_t,max_t)
    elif g_type=="Bar Graph":
        plot_bars(days,min_t,max_t)
    i=0
    st.write(f"#    Date :  Max - Min  ({unit})")
    for obj in days:
        d=(obj.strftime("%d/%m"))
        st.write(f"### \v {d} :\t  ({max_t[i]} - {min_t[i]})")
        i+=1
      
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title(f"Weather details in {place} currently:")
    st.write(f"### Sky 🌈 : {weather.detailed_status}")
    st.write(f"### Wind Speed 🌬️💨 : {weather.wind()['speed']} mph")
    st.write(f"### Sunrise Time ☀️ : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### Sunset Time ⛅🌥️ : {weather.sunset_time(timeformat='iso')} GMT")
    
    
    st.title("Expected Weather Changes:")
    if forecaster.will_have_fog():
        st.write("### FOG EXPECTED 🌫️")
    if forecaster.will_have_rain():
        st.write("### RAIN EXPECTED 🌦️")
    if forecaster.will_have_storm():
        st.write("### STORM MAYBE ⚡")
    if forecaster.will_have_snow():
        st.write("### SNOW EXPECTED ❄️☃️")
    if forecaster.will_have_tornado():
        st.write("### TORNADO ALERT 🌪️")
    if forecaster.will_have_hurricane():
        st.write("### HURRICANE ALERT ")
    if forecaster.will_have_clouds():
        st.write("### CLOUDY SKIES EXPECTED 🌤️⛅")
    if forecaster.will_have_clear():
        st.write("### YAY!! CLEAR WEATHER! 🌞")
        
if b:
    if not place=="":    
        find_min_max(place,unit,g_type)
    
    



