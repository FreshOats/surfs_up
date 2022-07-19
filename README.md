# Surf and Ice Cream Shop Business Sustainability:
## **Weather Trends in Oahu in June and December**
#### by Justin R. Papreck
---

## Overview

A client would like to open a Surf and Shake shop in Oahu and is seeking an investor to back this venture. The investor is on board with this venture so long as it can be shown that the climate will be sustainable throughout the year, as this investor had an experience backing a company that suffered losses during the off-season. A weather analysis of Oahu was used to show the temperatures in both the summer and winter, demonstrating the ideal climate that Oahu offers year round makes for an excellent area for a surf and shake shop. 

---
### Purpose

The purpose of this project is to use a local database of the weather conditions with SQLite and Pandas to get summary statistics for the temperature and precipitation. By looking at the average, median, and extrema temperatures in summer and winter should provide a good indicator as to whether the winter will be sustainable for a business that relies on warm temperatures for both of its products: surfing and ice cream. Additionally, it's important that during the colder parts of the year, it is not inundated with heavy rains and floods, as this would be very unattractive to potential customers. 

---
## Results and Analysis
### Temperatures in Oahu

The main times of year that could drammatically influence the success of this company are the summer and the winter. Temperatures were gathered from June and December and analyzed: 


![June_Temps](https://user-images.githubusercontent.com/33167541/179854409-3ba644d4-3464-46d7-8043-319619a35e8a.png)


![Dec_Temps](https://user-images.githubusercontent.com/33167541/179854423-b9868a25-5513-4007-aafe-5cafcf4ea762.png)


Due to Oahu's location, there is very little variance in the average and median temperatures in June and December.

- The average temperature in December is only 4 degrees cooler than the average June temperature
- The median temperature in December is also only 4 degrees cooler than the median June temperature
- The high temperature in December is only 2 degrees cooler than that in June
- The low temperaure in December is 8 degrees cooler than that in June
- There is a standard deviation of only 4 degrees

With these data, it looks like at heavy travel times, the temperatures are rather temperate, but warm enough to surf and enjoy ice cream outside.

---
### Futher Temperature Analysis

The data above only consider two months of the year, potential as these are when there is the highest influx of tourists, however it is critical to see what the rest of the year looks like, because there may be several months between that are unbearable. The above analysis did not determine whether June was the hottest month or December the coolest. Instead of just considering the last year, these data were queried over the past 2 years. 

The following query was made to acquire the data to show the Average Monthly Temperatures:

```
last_two_years = dt.date(2017,8,23) - dt.timedelta(days = 730)

year_temps = session.query(extract('month',Measurement.date), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= last_two_years)\
    .group_by(extract('month', Measurement.date)).all()
```

When plotted, the results showed that January was the coolest month of the year, and October was the warmest. 

![Avg_Monthly_Temp](https://user-images.githubusercontent.com/33167541/179856394-a03df6b3-3a58-4ddc-8647-d4b790622700.png)


Since the average high temperature in October is still around 80 degrees, which is not unbearably hot, the more important month to consider is January, the coldest month of year. While February and March are still lower than December, its critical to know if January is 'too cold'. Since December wasn't a problem and March has a similar average, it likely won't deviate far, but January and February can be 2 months of no sales.

Using the same code as was used the determine the June and December data, the January temperatures produced the following: 


![Jan_Temps](https://user-images.githubusercontent.com/33167541/179858824-7ecea6c5-8d23-43ec-9641-4ab32e60026f.png)


- The average January temperature is still only 6 degrees cooler than that in June 
- The median January temperature is similarly 6 degrees cooler than that in June
- The low temperature in January is 54 degrees, ten degrees cooler than the low in June, and two degrees cooler than December

---
### Analysis By Station 

Since there are 7 different stations making the temperature observations, the different stations were queried to find which has the highest average temperature in January, the most critical month for maintaining business which temperatures are at their lowest.

```
stations = session.query(Measurement.station, func.avg(Measurement.tobs))\
    .filter(Measurement.date >= last_two_years)\
    .filter(extract('month', Measurement.date) == 1)\
    .group_by(Measurement.station)\
    .order_by(func.avg(Measurement.tobs).desc()).all()

stations_df = pd.DataFrame(stations, columns=['Station', 'January Temperature'])
stations_df
```

![Station_Temps](https://user-images.githubusercontent.com/33167541/179858842-256434d6-264e-4181-9274-8af916bad00a.png)


Station USC00514830 (4830) had the highest average January temperature, at 74 degrees. Using this information, the other statistics were measured for this location: 


![Jan_at_4830](https://user-images.githubusercontent.com/33167541/179858781-b57682f1-267a-4f8b-bb96-a0bc2e95218b.png)


This station also had a minimum temperature of 66 degrees over the past two years, which is much more appealing than a location that drops to 54 degrees. 

---
### Precipitation in Oahu

Initially the preciptiation was considered for the past year, producing the following plot:


![Precipitation_by_date](https://user-images.githubusercontent.com/33167541/179860760-3880a747-7bb6-42fc-85c9-b5f5792d442c.png)


The highest dates accumulated nearly 7 cubic inches of rain, but there were only 4 days in the entire year that had over 4 inches of accumulation. While there aren't many days that had no rain at all, the accumulation was very low. There was not the presence of a 'rainy season', as the data did not have a chunk of time when there was elevated accumulation. 

In further considering the region near station 4830, the following shows the precipitation at this location: 


![Precipitation_by_4830](https://user-images.githubusercontent.com/33167541/179860842-10ff08b1-1fbb-4688-b178-2b2b9251b083.png)


Note, that the highest precipitation is lower than 2.5 cubic inches, and most of the year falls below a quarter of an inch. Finally, the last summary statistics show the preciptiation at this location in the three months of interest over the past two years: January, June, and December.


![Jan_Rain](https://user-images.githubusercontent.com/33167541/179861801-a309d888-f115-493c-844a-a64669da7049.png)


![June_Rain](https://user-images.githubusercontent.com/33167541/179861814-12a72515-72e8-419c-8831-6363e57555ae.png)


![December_Rain](https://user-images.githubusercontent.com/33167541/179861822-da92bf01-da40-46e5-9697-37b32c3e46fc.png)


- In January, the mean rainfall was less than 0.04 cubic inches
- In June and December, the mean rainfall was approximately 0.11 cubic inches
- The highest measured rainfall was in January, at 0.59 cubic inches, with December at 0.56 cu.in. and June at 0.53 cu.in.

The code used to acquire these data followed this query:

```
june_rain = session.query(Measurement.prcp)\
    .filter(Measurement.date >= last_two_years)\
    .filter(extract('month', Measurement.date) == 6)\
    .filter(Measurement.station == "USC00514830").all()

june_rain_df = pd.DataFrame(june_rain, columns=["June Rain at 4830"])
june_rain_df.describe()
```

---
## Summary

After evaluating the temperatures and precipitation throughout Oahu, the climate seems ideal for such a venture as a surf and shake type shop. There is a very small temperature variation throughout the year. Even in the winter months, the temperature still gets up to the high 70s, which is still great for surfing and ice cream. The precipitation in Oahu is seemingly low throughout the year, and there is not a rainy season. When evaluating which stations provided the highest temperatures, it was determined that locations near the station USC00514830 could be ideal to set up shop. The precipitation was further analyzes at this location, which was determined to be lower than the averages, so granted this location is near a beach, this could be an ideal location. 
