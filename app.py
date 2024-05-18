import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Helper function to fetch and display market data


def get_market_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="2d")
    current_price = hist['Close'][-1]
    previous_price = hist['Close'][-2]
    change = ((current_price - previous_price) / previous_price) * 100
    return current_price, change

# to display cards by ticker


def display_market_data(ticker, name):
    price, change = get_market_data(ticker)
    st.metric(name, f"{price:.2f}", f"{change:.2f}%")


# stock info
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

# stock main info


def get_stock_card(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    st.metric(info['sector'],  info['shortName'])


# stock info show
def show_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # List of keys we want to extract
    list_keys = [
        'currentPrice', 'marketCap', 'trailingPE', 'forwardPE', 'revenueGrowth',
        'pegRatio', 'trailingPegRatio', 'priceToBook', 'debtToEquity', 'dividendRate',
        'trailingAnnualDividendRate', 'profitMargins', 'trailingEps', 'forwardEps',
        'shortRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', 'currentRatio',
        'freeCashflow', 'earningsGrowth', 'sector', 'website'
    ]

    list1_keys = ['previousClose', 'dayLow', 'dayHigh',
                  'averageVolume', 'averageVolume10days', 'targetMeanPrice', 'targetHighPrice', 'targetLowPrice', 'recommendationKey']

    # Build DataFrame with 'N/A' for missing keys
    df_info = pd.DataFrame({key: info.get(key, 'N/A')
                           for key in list_keys}, index=[0]).transpose()
    df_info.columns = ['Value']

    # Build DataFrame with 'N/A' for missing keys
    df_perf = pd.DataFrame({key: info.get(key, 'N/A')
                           for key in list1_keys}, index=[0]).transpose()
    df_perf.columns = ['Value']

    # Display table in Streamlit
    st.write('Stock Financial Data')
    st.table(df_info)
    st.write('Stock Performance Data')
    st.table(df_perf)


# news table


def get_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    df_news = pd.DataFrame(news)[['title', 'publisher', 'relatedTickers']]
    st.table(df_news)

#


def get_income_stat(ticker):
    stock = yf.Ticker(ticker)
    income_stat = stock.financials.transpose()
    return income_stat


def get_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    overview = stock.info
    income_statement = stock.financials.transpose()
    return overview, income_statement


def plot_margins_(income_statement):
    # Calculate margins
    income_statement['Gross Margin'] = income_statement['Gross Profit'] / \
        income_statement['Total Revenue']
    income_statement['Profit Margin'] = income_statement['Net Income'] / \
        income_statement['Total Revenue']

    # Prepare the DataFrame for Plotly
    df_plot = income_statement[['Gross Margin', 'Profit Margin']].reset_index()

    # Use Plotly Express to create the bar chart
    fig = px.bar(df_plot, x='index', y=['Gross Margin', 'Profit Margin'],
                 title="Gross Margin and Profit Margin",
                 labels={'index': 'Fiscal Year', 'value': 'Margin'},
                 )

    # Show the figure
    fig.show()
    return fig

# Example usage (assuming 'income_statement' is a DataFrame with the necessary columns)
# plot_margins(income_statement)


def plot_margins(income_statement):
    income_statement['Gross Margin'] = income_statement['Gross Profit'] / \
        income_statement['Total Revenue']
    income_statement['Profit Margin'] = income_statement['Net Income'] / \
        income_statement['Total Revenue']

    fig, ax = plt.subplots()
    income_statement[['Gross Margin', 'Profit Margin']].plot(kind='bar', ax=ax)
    plt.title("Gross Margin and Profit Margin")
    plt.ylabel("Margin")
    plt.xlabel("Fiscal Year")
    return fig


# Streamlit app
st.title("Financial Dashboard")

# Sidebar for API key input (no longer needed for yfinance)
st.sidebar.header("API Key Input")
st.sidebar.write(
    "Alpha Vantage API key is not required for this version using yfinance.")

# Tab navigation
tab1, tab2 = st.tabs(["Market Overview", "Company Analysis"])

# Tab 1: Market Overview
with tab1:
    st.header("Market Overview")

    try:
        nasdaq_price, nasdaq_change = get_market_data('^IXIC')
        sp500_price, sp500_change = get_market_data('^GSPC')
        treasury_10y_price, treasury_10y_change = get_market_data('^TNX')
        vix_price, vix_change = get_market_data('^VIX')
        # etf
        # Technology Select Sector SPDR Fund[^2^][7]
        XLK_price, XLK_change = get_market_data('XLK')
        # Vanguard Information Tech ETF[^2^][7]
        VGT_price, VGT_change = get_market_data('VGT')
        # First Trust Dow Jones Internet Index[^2^][7]
        FDN_price, FDN_change = get_market_data('FDN')

        # list indices
        mkt_list = [
            ('^IXIC', "NASDAQ"),
            ('^GSPC', "S&P 500"),
            ('^RUT', "RUSSEL 2000"),
            ('FDN', "DOW JONES"),
        ]
        # list indices 2
        us_list = [
            ('^VIX', "VIX"),
            ('^TNX', "10Y Treasury"),
            ('TLT', "TLT"),
            ('^GSPC', "S&P 500"),
        ]
        # list ETF
        etf_list = [
            ('ARKK', "ARKK"),
            ('SOXX', "SOXX"),
            ('HACK', "HACK"),
            ('ICLN', "ICLN"),
        ]

        # MKT
        st.subheader('US Market', divider='gray')

        x = st.columns(4)
        for i, (ticker, name) in enumerate(mkt_list):
            with x[i]:
                display_market_data(ticker, name)

        # US
        y = st.columns(4)
        for i, (ticker, name) in enumerate(us_list):
            with y[i]:
                display_market_data(ticker, name)

        # ETF
        st.subheader('ETF', divider='gray')

        z = st.columns(4)
        for i, (ticker, name) in enumerate(etf_list):
            with z[i]:
                display_market_data(ticker, name)

        ####

    except Exception as e:
        st.error(f"Error fetching market data: {e}")

# Tab 2: Company Analysis
with tab2:
    st.header("Company Analysis")
    ticker = st.text_input("Enter Ticker Symbol")

    if ticker:
        try:
            overview, income_statement = get_fundamental_data(ticker)

            if overview and not income_statement.empty:
                #
                col1, col2, col3 = st.columns(3)
                with col1:
                    get_stock_card(ticker)
                with col2:
                    st.write("")
                with col3:
                    display_market_data(ticker, ticker)

                #
                st.divider()
                st.subheader("Fundamental Data")
                show_stock_info(ticker)
                #
                st.subheader("Stock News")
                get_stock_news(ticker)
                st.divider()
                #
                st.subheader("Fundamental Data")
                st.write('Stock :')
                etf_list = ['dayHigh', 'payoutRatio',
                            'regularMarketPreviousClose']
                overview_df = pd.DataFrame({key: overview.get(key, 'N/A')
                                            for key in etf_list}, index=[0]).transpose()
                selected_data = overview_df.loc[etf_list]
                st.table(selected_data)
                #
                st.divider()
                st.write('Stock :')
                st.table(overview_df)
                #
                st.subheader("Financial Statement")
                st.table(income_statement)
                #
                st.subheader("Margins")
                fig_ = plot_margins_(income_statement)
                fig = plot_margins(income_statement)
                st.plotly_chart(fig_)
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error fetching financial data: {e}")
