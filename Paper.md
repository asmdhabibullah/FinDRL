### Project pipeline

#### My current work status is: 3

---

| Proposal Development (Month 1) |
| - Formulate research questions |
| - Develop research methodology |
| - Prepare and submit proposal |

---

---

| Literature Review (Months 2-3) |
| - Conduct literature review |
| - Identify key studies |
| - Highlight research gaps |

---

---

| Data Collection and Analysis (Months 3-4) |
| - Collect historical stock data |
| - Clean and preprocess data |
| - Perform exploratory data analysis |

---

---

| Model Development and Experimentation (Months 4-6) |
| - Design LSTM, GRU, Attention, Transformer models |
| - Perform hyperparameter tuning |
| - Train models with datasets |

---

---

| Results Analysis and Manuscript Composition (Months 6-8)|
| - Analyze results |
| - Document findings |
| - Draft dissertation manuscript |

---

---

| Peer Review and Final Manuscript Refinement (Months 8-10)|
| - Obtain peer feedback |
| - Refine manuscript |
| - Finalize dissertation |

---

Technologies and Tools:

- Python, NumPy, Pandas, Ta-Python, Click, Matplotlib
- MacBook Pro (M1, 16GB), Computer, Google Cloud (Google Colab)
- Custom Backtesting Platform: To backtest trading strategies

### Strategies & their Implementation

#### Explaination of the "Enhanced Flat Top Breakout Strategy" to your interviewer, covering its design, implementation, and functionality:

1. Introduction to the Strategy
   Name: Enhanced Flat Top Breakout Strategy
   Objective: To identify and capitalize on bullish breakout opportunities by combining price action with momentum indicators.
2. Key Components of the Strategy
   - Flat Top Breakout:
   1. Identification: The strategy identifies a flat top breakout pattern characterized by a horizontal resistance level and higher lows.
   2. Momentum Indicators:
   - RSI (Relative Strength Index): Used to confirm the trend is not overbought.
   - MACD (Moving Average Convergence Divergence): Used to confirm bullish momentum.
   - Stochastic Oscillator: Used to confirm the trend is not overbought.
   - Williams %R: Used to confirm the trend is not overbought.
3. Implementation Details
   Class Design:

   - MomentumIndicators: A class to calculate various momentum indicators.
   - EnhancedFlatTopBreakout: A strategy class that inherits from Strategy in Backtesting.py.

   Initialization:
   The strategy initializes with the necessary data and calculates the flat top breakout conditions and momentum indicators.

   - Buying Condition: A buy signal is triggered when the following conditions are met:

   1. Higher lows are detected.
   2. The price breaks above the flat top resistance level by a specified threshold (2%).
   3. RSI is below 70 (not overbought).
   4. MACD is above the signal line (bullish momentum).
   5. Stochastic Oscillator is below 80 (not overbought).
   6. Williams %R is above -20 (not overbought).

   - Exiting the Position:

   1. The position is closed if the stop loss or profit target is hit:
   2. Stop Loss: Set to 5% below the entry price.
   3. Profit Target: Set to 10% above the entry price.
   4. Additional exit condition based on the RSI indicator:
   5. Position is closed if RSI rises above 70 (indicating overbought conditions).

Next Work Plan (Months 1-4):

1.       Model Development and Experimentation :

§ Design Model Architectures : Finalize the architectures for LSTM, GRU, Attention, and Transformer models tailored for 1-minute, 30-minute and daily data for 1-day intervals.

§ Hyperparameter Tuning : Perform hyperparameter tuning to find the optimal configurations for each model.

§ Training : Train each model using the prepared datasets, ensuring to implement early stopping techniques to prevent overfitting.

2.       Key Technologies to be Solved :

§ Efficient Hyperparameter Tuning : Utilize techniques like grid search, random search, or Bayesian optimization for efficient hyperparameter tuning.

§ Real-time Data Handling : Develop mechanisms for real-time data ingestion and processing to ensure models can be applied in live trading environments.

§ Scalability : Ensure models are scalable and can handle large datasets effectively.

§ Interpretability : Create methods to interpret model predictions, focusing on feature importance and attention weights.

Subsequent Phases:

1.       Results Analysis and Manuscript Composition (Months 4-6) :

§ Analyze the results obtained from model training and evaluation.

§ Begin drafting the dissertation, documenting methodologies, results, and insights.

2.       Peer Review and Final Manuscript Refinement (Months 6-8) :

§ Share initial drafts with peers for feedback.

§ Refine the manuscript based on feedback and finalize the dissertation.
