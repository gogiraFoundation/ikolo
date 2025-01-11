from portfolio_manager.technical_analysis import TechnicalAnalysis


class Advisor:
    """Class for providing stock advice."""
    
    @staticmethod
    def generate_advice(data, macd, signal, rsi):
        """
        Generate advice based on MACD and RSI.

        Args:
            data (pd.DataFrame): Stock data.
            macd (pd.Series): MACD line.
            signal (pd.Series): Signal line.
            rsi (pd.Series): RSI values.

        Returns:
            str: "Buy", "Sell", or "Hold".
        """
        latest_macd = macd.iloc[-1]
        latest_signal = signal.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        
        if latest_macd > latest_signal and latest_rsi < 30:
            return "Buy"
        elif latest_macd < latest_signal and latest_rsi > 70:
            return "Sell"
        else:
            return "Hold"
