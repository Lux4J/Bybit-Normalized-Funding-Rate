# Bybit BTC Normalized Funding Rate

This Python script fetches **Bitcoin price** and **funding rate data** from Bybit, applies **quantile normalization** to the funding rate, and plots it alongside the BTC price. The script highlights extreme values (overbought and oversold conditions) where the normalized funding rate exceeds ±2 standard deviations (Z > 1.96 or Z < -1.96).

# How does it work?

Binanace alongside Bybit are the two main exchanges for retail traders in the crypto market. Unlike tradional markets crypto has an instrument known as `perpetual futures`, which are futures contracts that don't expire. Futures in the stock market have the borrowing cost embedded within the price of the asset at expiry. Since there is no expiry funding represents the borrowing cost for traders to open a long or a short position. This borrowing cost is usually set to stablize the price difference between the perpetual market and the spot market.

Specifically, funding is calculated as:
Funding = Interest Rate + Premium Index

The Interest rate on Bybit is fixed at 0.09% a day. The Premium index represents the dislocation between the perpetual market and the spot market. If the perpetual markets are trading at a higher price than the spot market then the Premium index is positive and the funding rate increases(traders positioned long have to pay more in borrowing costs and traders positioned short recieve money instead of paying borrowing costs.) Conversely if the perpetual martket is at a discount, at a sufficient enough difference, traders positioned long recieve money in the form of interest and short traders must pay a borrowing cost.

Observing past behaviour traders typically take on more risk the more one directional the market gets. I.e. if BTC has been trending up with minimal pullbacks traders get positioned more aggressively long and vice-versa. 

The point of this script is to identify regions in which the funding rate is either too high or too low to be sustainable. If funding is too high and traders are positioned too aggressively long any pullback will cause a liquidation cascade to the downside and if funding is too low and traders are positioned too aggresively short any bounce will cause a 'short squeeze'.

Funding data is normalized so that the overbought and oversold zones can easily be marked at 2 standard deviations from the mean.

Below is the result as per the start of 2025: 

![image](https://github.com/user-attachments/assets/c73d7011-bab6-44c0-afd6-2f4230bb26a9)

---

## **Features**
1. Fetches **BTC price** and **funding rate data** from Bybit's public APIs.
2. Applies **quantile normalization** to the funding rate for better statistical analysis.
3. Highlights overbought (red) and oversold (green) areas based on a Z-score threshold of ±2.
4. Outputs a clear dual-axis plot of BTC price (orange) and normalized funding rate (blue).

---

## **Requirements**
- **Python Version**: Python 3.6 or higher.
- **Libraries**:
  - `requests`: For API calls to Bybit.
  - `pandas`: For data manipulation.
  - `matplotlib`: For plotting graphs.
  - `scikit-learn`: For quantile normalization.

---

## **Installation**

### **macOS and Windows**
1. **Install Python**:
   - **macOS**:
     ```bash
     brew install python
     ```
   - **Windows**:
     Download and install Python from the [official website](https://www.python.org/).

2. **Install the required Python libraries**:
   ```bash
   pip install requests pandas matplotlib scikit-learn
   ```

3. **Run the script**:
- Open command prompt or the terminal and enter the following commands:
```
git clone https://github.com/Lux4J/BTC-Bybit-Normalized-Funding-Rate.git

cd Bybit-Normalized-Funding-Rate

python Bybit_funding_rate.py.py
```
## **Output**

- **Graph**:
  - BTC price (orange line) plotted on the primary y-axis.
  - Normalized funding rate (blue line) plotted on the secondary y-axis.
  - Vertical red lines for overbought conditions (Z > 1.96).
  - Vertical green lines for oversold conditions (Z < -1.96).
