# Bybit BTC Normalized Funding Rate

This Python script fetches **Bitcoin price** and **funding rate data** from Bybit, applies **quantile normalization** to the funding rate, and plots it alongside the BTC price. The script highlights extreme values (overbought and oversold conditions) where the normalized funding rate exceeds ±2 standard deviations (Z > 1.96 or Z < -1.96).

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
