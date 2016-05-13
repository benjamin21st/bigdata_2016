NYC Taxi 2015
=============
This website is a visualization of NYC taxi data.
Based on repository [noisyNYC](https://github.com/zunayed/noisyNYC)

## Run
You will need flask > 0.10.1
```
python routes.py
```
Built using D3. Foundation CSS for styling

## Data
If you provide an object with values associated with zipcodes you can map you're own values. 

``` .js
var noiseData = {
  "0": 264,
  "1": 197,
  "2": 187,
  "3": 177,
  "4": 167,
  "5": 155,
  "6": 155,
...
}
```