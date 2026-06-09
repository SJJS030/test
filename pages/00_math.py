import datetime as dt
from typing import Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Global Top 10 Market Cap Stock Dashboard",
    page_icon="📈",
    layout="wide",
)

TOP10: Dict[str, str] = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Alphabet": "GOOG",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "TSMC": "TSM",
    "Broadcom": "AVGO",
    "Saudi Aramco": "2222.SR",
    "Tesla": "TSLA",
    "Meta Platforms": "META",
}

DEFAULT_TICKERS: List[str] = list(TOP10.values())
TICKER_TO_NAME = {ticker: name for name, ticker in TOP10.items()}

st.title("📈 글로벌 시가총액 TOP 10 최근 1년 주가 대시보드")
st.caption(
    "Yahoo Finance 데이터를 yfinance로 불러와 Plotly로 시각화합니다. "
    "시총 순위는 변동될 수 있으니 필요하면 TOP10 딕셔너리만 갱신하세요."
)

with st.sidebar:
    st.header("설정")
    selected_tickers = st.multiselect(
        "종목 선택",
        options=DEFAULT_TICKERS,
        default=DEFAULT_TICKERS,
        format_func=lambda x: f"{TICKER_TO_NAME.get(x, x)} ({x})",
    )
    period = st.selectbox("조회 기간", ["1y", "6mo", "3mo", "2y"], index=0)
    interval = st.selectbox("간격", ["1d", "1wk", "1mo"], index=0)
    normalize = st.checkbox("첫 거래일을 100으로 정규화", value=True)
    show_raw = st.checkbox("원본 데이터 보기", value=False)

@st.cache_data(ttl=60 * 30, show_spinner=False)
def load_prices(tickers: List[str], period: str, interval: str) -> pd.DataFrame:
    if not tickers:
        return pd.DataFrame()

    raw = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )

    if raw.empty:
        return pd.DataFrame()

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"].copy()
    else:
        prices = raw[["Close"]].copy()
        prices.columns = tickers

    prices = prices.dropna(how="all")
    prices.index = pd.to_datetime(prices.index)
    return prices

with st.spinner("야후 파이낸스에서 데이터를 가져오는 중입니다. 금융 데이터 API에게 예의를 갖춰 기다립시다..."):
    prices = load_prices(selected_tickers, period, interval)

if not selected_tickers:
    st.warning("사이드바에서 최소 1개 종목을 선택하세요.")
    st.stop()

if prices.empty:
    st.error("데이터를 불러오지 못했습니다. 티커 또는 Yahoo Finance 상태를 확인하세요.")
    st.stop()

if normalize:
    chart_df = prices / prices.ffill().bfill().iloc[0] * 100
    y_title = "정규화 주가 지수, 시작일 = 100"
    chart_title = "최근 기간 주가 변화, 시작일 100 기준"
else:
    chart_df = prices
    y_title = "조정 종가"
    chart_title = "최근 기간 조정 종가 변화"

long_df = (
    chart_df.reset_index()
    .melt(id_vars="Date", var_name="Ticker", value_name="Value")
    .dropna()
)
long_df["Company"] = long_df["Ticker"].map(TICKER_TO_NAME).fillna(long_df["Ticker"])
long_df["Label"] = long_df["Company"] + " (" + long_df["Ticker"] + ")"

latest = prices.ffill().iloc[-1]
first = prices.ffill().bfill().iloc[0]
returns = ((latest / first - 1) * 100).sort_values(ascending=False)

col1, col2, col3 = st.columns(3)
col1.metric("선택 종목 수", len(selected_tickers))
col2.metric("조회 시작일", prices.index.min().strftime("%Y-%m-%d"))
col3.metric("마지막 데이터", prices.index.max().strftime("%Y-%m-%d"))

fig = px.line(
    long_df,
    x="Date",
    y="Value",
    color="Label",
    title=chart_title,
    labels={"Date": "날짜", "Value": y_title, "Label": "기업"},
)
fig.update_layout(
    hovermode="x unified",
    legend_title_text="기업",
    margin=dict(l=20, r=20, t=70, b=20),
)
st.plotly_chart(fig, use_container_width=True)

returns_df = (
    returns.rename("Return")
    .reset_index()
    .rename(columns={"index": "Ticker"})
)
returns_df["Company"] = returns_df["Ticker"].map(TICKER_TO_NAME).fillna(returns_df["Ticker"])
returns_df["Label"] = returns_df["Company"] + " (" + returns_df["Ticker"] + ")"

bar = px.bar(
    returns_df,
    x="Return",
    y="Label",
    orientation="h",
    title="선택 기간 수익률",
    labels={"Return": "수익률 (%)", "Label": "기업"},
    text=returns_df["Return"].map(lambda x: f"{x:.1f}%"),
)
bar.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=20, r=20, t=70, b=20))
st.plotly_chart(bar, use_container_width=True)

st.subheader("현재 TOP10 티커")
st.dataframe(
    pd.DataFrame([{"Company": name, "Ticker": ticker} for name, ticker in TOP10.items()]),
    use_container_width=True,
    hide_index=True,
)

if show_raw:
    st.subheader("원본 조정 종가 데이터")
    st.dataframe(prices, use_container_width=True)

st.caption(
    "주의: 이 앱은 투자 조언이 아니라 데이터 시각화 예시입니다. "
    "Yahoo Finance 데이터는 지연되거나 누락될 수 있습니다. 네, 금융도 결국 사람이 만든 혼돈입니다."
)
