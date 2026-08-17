import pandas as pd
import plotly.express as px
import streamlit as st 

df =pd.read_csv("M_PESA_statement.csv")
fuliza_trend = (
    df[df['received'] == 'Fuliza credit']
    .groupby('month')['Paid In']
    .sum()
    .reset_index()
)

print(fuliza_trend)
cash_flow = (
    df.groupby('month')
    [['Paid In', 'Withdrawn']]
    .sum()
    .reset_index()
)

print(cash_flow)
#creating the dashboard using plotly and streamlit 
# dashboard title 
st.title('M-PESA Financial Analytics Dashboard')
st.caption("Analyze spending, cash flow, Fuliza usage, and transaction trends.")
# adding the KPI metric 
col1 ,col2= st.columns(2)
col1.metric("Total Cash In","Ksh 69,565.84")
col2.metric('Total Cash out','Ksh 116,831.84')
col3,col4=st.columns(2)
col3.metric("Fuliza Credit","Ksh 21,375.84")
col4.metric("Fuliza Repaid",'Ksh 21,298.57')
col5,col6=st.columns(2)
col5.metric('Net Cash Flow','KSh -47,266')

col1 ,col2 =st.columns(2)
#left line graph Monthly Inflow Vs outflow
with col1:
    st.markdown("____________________________________________________________________________")
    fig1=px.line(
        cash_flow,
        x="month",
        y=['Paid In','Withdrawn'],
        title="Monthly Inflow vs Outflow",
        color_discrete_map={
            'Paid In': 'green',
            'Withdrawn': 'red'
        },
        markers=True 
        
    )
    fig1.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (KSH)",
        showlegend=True
    )
    
    st.plotly_chart(fig1, use_container_width=True)
#Incoming transaction by source
with col2:
    st.markdown('______________________________________________________________________________________________')
    fig2=px.pie(
        data_frame=df,
        values='Paid In',
        names='received',
        title='source of cash Inflow'
    )
    st.plotly_chart(fig2,use_container_width=True)
col1 ,col2=st.columns(2)
#top recepient 
with col1:
    st.markdown('__________________________________________________________________________________________________')
    bar_data = (
    df.groupby("Spending")["Withdrawn"]
      .sum()
      .abs()
      .sort_values(ascending=True)
      .reset_index()
)   
    fig1= px.bar(
    bar_data,
    x="Withdrawn",
    y="Spending",
    orientation="h",
    title="Spending by Category"
)

    fig1.update_xaxes(
    title="Amount (KSh)",
    tickprefix="KSh "
)

    st.plotly_chart(fig1, use_container_width=True)
#fuliza trend over time     
with col2:
    st.markdown('___________________________________________________________________________________________________')
    fig2=px.line(
        fuliza_trend,
        x='month',
        y='Paid In',
        title= "Fuliza Usage Trend"
    )
    st.plotly_chart(fig2,use_container_width=True)

