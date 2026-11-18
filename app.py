import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='SupeRR Selector | Pressure Analytics', page_icon='🏏', layout='wide')
BASE = Path(__file__).parent

@st.cache_data
def load_data():
    bat = pd.read_csv(BASE / 'data' / 'batters_ranked.csv')
    bowl = pd.read_csv(BASE / 'data' / 'bowlers_ranked.csv')
    return bat, bowl

bat, bowl = load_data()

st.markdown('''<style>
.main {background:#0b1220;} .block-container{padding-top:1.5rem;max-width:1400px}
[data-testid="stMetric"]{background:#141f33;border:1px solid #263750;padding:16px;border-radius:12px}
[data-testid="stDataFrame"]{border:1px solid #263750;border-radius:10px}
</style>''', unsafe_allow_html=True)

st.title('🏏 SupeRR Selector')
st.subheader('Pressure Reliability Analytics Dashboard')
st.caption('Evidence-led player comparison | IPL & T20I dataset | High-pressure second-innings chase analysis')

with st.sidebar:
    st.header('Dashboard controls')
    view = st.radio('Player category', ['Batters', 'Bowlers'])
    n = st.slider('Show top N players', 5, 30, 10)
    st.divider()
    st.caption('Scores are model-based indicators, not guarantees of future performance. See methodology and limitations below.')

if view == 'Batters':
    df = bat.sort_values('score', ascending=False).reset_index(drop=True)
    name_col = 'striker_name'
    st.markdown('### Top pressure-reliable batters')
    a,b,c,d = st.columns(4)
    a.metric('Eligible batters', f'{len(df):,}')
    b.metric('Top score', f"{df.iloc[0]['score']:.2f}")
    c.metric('Top player', df.iloc[0][name_col])
    d.metric('Pressure balls (top player)', f"{int(df.iloc[0]['hp_balls']):,}")
    show = df.head(n).copy()
    show.insert(0, 'Rank', range(1, len(show)+1))
    cols = ['Rank',name_col,'score','hp_runs','hp_balls','hp_sr','sr_uplift','hp_dismissals','hp_matches','hp_average','consistency']
    st.dataframe(show[cols].rename(columns={name_col:'Player','score':'Reliability score','hp_runs':'Pressure runs','hp_balls':'Pressure balls','hp_sr':'Pressure SR','sr_uplift':'SR uplift','hp_dismissals':'Dismissals','hp_matches':'Matches','hp_average':'Pressure average','consistency':'Match consistency'}), use_container_width=True, hide_index=True)
    fig = px.bar(show.sort_values('score'), x='score', y=name_col, orientation='h', color='score', color_continuous_scale='Tealgrn', title=f'Top {n} batter reliability scores', labels={'score':'Score',name_col:'Player'})
    fig.update_layout(template='plotly_dark', height=480, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('### Batter profile explorer')
    chosen = st.selectbox('Choose a batter', df[name_col].tolist())
    r = df[df[name_col] == chosen].iloc[0]
    x1,x2,x3,x4,x5 = st.columns(5)
    x1.metric('Reliability score', f"{r.score:.2f}")
    x2.metric('Pressure strike rate', f"{r.hp_sr:.2f}")
    x3.metric('Pressure runs', int(r.hp_runs))
    x4.metric('Pressure dismissals', int(r.hp_dismissals))
    x5.metric('Matches', int(r.hp_matches))
    prof = pd.DataFrame({'Metric':['Pressure SR','Baseline SR','Pressure boundary rate','Baseline boundary rate','Pressure dot rate','Baseline dot rate'], 'Value':[r.hp_sr,r.base_sr,r.hp_boundary_rate,r.base_boundary_rate,r.hp_dot_rate,r.base_dot_rate]})
    fig2=px.bar(prof,x='Metric',y='Value',color='Metric',title=f'{chosen}: pressure vs baseline')
    fig2.update_layout(template='plotly_dark',showlegend=False)
    st.plotly_chart(fig2,use_container_width=True)
else:
    df = bowl.sort_values('score', ascending=False).reset_index(drop=True)
    name_col = 'bowler_name'
    st.markdown('### Top pressure-reliable bowlers')
    a,b,c,d = st.columns(4)
    a.metric('Eligible bowlers', f'{len(df):,}')
    b.metric('Top score', f"{df.iloc[0]['score']:.2f}")
    c.metric('Top player', df.iloc[0][name_col])
    d.metric('Pressure wickets (top player)', f"{int(df.iloc[0]['hp_wickets']):,}")
    show=df.head(n).copy(); show.insert(0,'Rank',range(1,len(show)+1))
    cols=['Rank',name_col,'score','hp_wickets','hp_balls','hp_econ','econ_improvement','hp_dot_rate','hp_matches','consistency']
    st.dataframe(show[cols].rename(columns={name_col:'Player','score':'Reliability score','hp_wickets':'Pressure wickets','hp_balls':'Pressure balls','hp_econ':'Pressure economy','econ_improvement':'Economy improvement','hp_dot_rate':'Dot-ball rate','hp_matches':'Matches','consistency':'Match consistency'}),use_container_width=True,hide_index=True)
    fig=px.bar(show.sort_values('score'),x='score',y=name_col,orientation='h',color='score',color_continuous_scale='Tealgrn',title=f'Top {n} bowler reliability scores',labels={'score':'Score',name_col:'Player'})
    fig.update_layout(template='plotly_dark',height=480,coloraxis_showscale=False)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('### Bowler profile explorer')
    chosen=st.selectbox('Choose a bowler',df[name_col].tolist())
    r=df[df[name_col]==chosen].iloc[0]
    x1,x2,x3,x4,x5=st.columns(5)
    x1.metric('Reliability score',f'{r.score:.2f}'); x2.metric('Pressure economy',f'{r.hp_econ:.2f}'); x3.metric('Pressure wickets',int(r.hp_wickets)); x4.metric('Pressure balls',int(r.hp_balls)); x5.metric('Matches',int(r.hp_matches))
    prof=pd.DataFrame({'Metric':['Pressure economy','Baseline economy','Pressure wickets/100 balls','Baseline wickets/100 balls','Pressure dot rate','Baseline dot rate'],'Value':[r.hp_econ,r.base_econ,r.hp_wickets100,r.base_wickets100,r.hp_dot_rate,r.base_dot_rate]})
    fig2=px.bar(prof,x='Metric',y='Value',color='Metric',title=f'{chosen}: pressure vs baseline')
    fig2.update_layout(template='plotly_dark',showlegend=False)
    st.plotly_chart(fig2,use_container_width=True)

with st.expander('Methodology and interpretation'):
    st.markdown('''
**Scope.** The supplied analysis classifies pressure deliveries in second-innings chases and compares player performance in those states with the same player's non-pressure baseline.

**Batter indicators.** Pressure strike rate, strike-rate uplift over baseline, boundary rate, dot-ball rate, dismissal rate, and match consistency contribute to the composite score. Lower dot-ball and dismissal rates are favourable; higher scoring and consistency indicators are favourable.

**Bowler indicators.** Pressure economy, improvement in economy versus baseline, wicket-taking rate, dot-ball rate, boundary prevention, and match consistency contribute to the composite score. Lower economy and boundary rates and higher wicket-taking/dot-ball rates are favourable.

**Important.** The displayed scores and ranks are those in the supplied analysis output CSVs. They are descriptive model outputs, not official player ratings. Rankings depend on the chosen pressure definition, weights, eligibility thresholds, competition mix, and available sample. They should not be interpreted as causal proof or a guarantee of future performance.
''')

with st.expander('Data dictionary'):
    st.write('**Batting:** pressure runs/balls, strike rate, boundary and dot-ball rates, dismissals, matches, batting average, baseline metrics, consistency, uplift, and composite score.')
    st.write('**Bowling:** pressure runs conceded, balls, wickets, economy, wickets per 100 balls, dot-ball and boundary rates, baseline metrics, consistency, improvements, and composite score.')

st.caption('SupeRR Selector | Prepared from the supplied data-pack analysis. Validate all definitions against the official challenge brief before final submission.')
