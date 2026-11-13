"""Reproducible synthetic FinTech product analytics demo. Not connected to CoinDCX or real customers."""
import csv, json, math, random
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'csv'; OUT.mkdir(parents=True,exist_ok=True)
RAND=random.Random(261113)
END=date(2026,11,13)
START=date(2024,4,1)
CHANNELS=['Organic','Paid Search','Social','Referral','Affiliate','Influencer']
REGIONS=['East','North','South','West']
DEVICES=['Android','iOS','Web']
SEGMENTS=['Explorer','Casual','Active','Power']
PRODUCTS=['Spot','Futures','Earn / SIP']
SCHEMES=['UPI','IMPS','NEFT','Card']
PROBS_SEG={'Explorer':.41,'Casual':.55,'Active':.72,'Power':.85}
rows={k:[] for k in ['Users','ActivityMonthly','Trades','WalletTransactions','SIPInstallments','Campaigns','ModelValidation']}

def dt(s): return date.fromisoformat(s) if isinstance(s,str) else s
def plus_month(d, n=1):
    y=d.year+(d.month-1+n)//12; m=(d.month-1+n)%12+1
    return date(y,m,1)
def mstr(d):return d.strftime('%Y-%m')
def fy(d):return f'FY{d.year if d.month>=4 else d.year-1}-{(d.year+1 if d.month>=4 else d.year)%100:02}'
def clamp(x,a,b):return max(a,min(b,x))
def rngfloat(a,b): return RAND.uniform(a,b)
def pick(w):return RAND.choices(list(w),weights=list(w.values()))[0]
def iso(d):return d.isoformat() if d else ''
def add_days(day,k):return (day+timedelta(days=k)) if day else None

def dump(name, items):
    if not items: return
    path=OUT/(name+'.csv')
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(items[0]))
        writer.writeheader(); writer.writerows(items)
    print(name,len(items),path.stat().st_size)

months=[]; cur=START
while cur<=END:
    months.append(cur)
    cur=plus_month(cur)
weights=[85+int(i*3.1)+15*math.sin(i/3)**2 for i in range(len(months))]
monthly_id_weights=[x/sum(weights) for x in weights]
users=[]
for i in range(4100):
    mon=RAND.choices(months,weights=monthly_id_weights,k=1)[0]
    day=mon+timedelta(days=RAND.randint(0,(min(plus_month(mon),END+timedelta(days=1))-mon).days-1))
    user_id=f'U{i+1:06}'
    channel=pick({'Organic':28,'Paid Search':22,'Social':17,'Referral':15,'Affiliate':11,'Influencer':7})
    region=pick({'East':24,'North':28,'South':27,'West':21})
    device=pick({'Android':64,'iOS':26,'Web':10})
    segment=pick({'Explorer':27,'Casual':38,'Active':26,'Power':9})
    experiment='Variant B' if day>=date(2026,4,1) and RAND.random()<.50 else ('Control A' if day>=date(2026,4,1) else 'Not exposed')
    ch_effect={'Organic':.07,'Paid Search':-.03,'Social':-.08,'Referral':.08,'Affiliate':-.06,'Influencer':-.04}[channel]
    segment_effect={'Explorer':-.09,'Casual':0,'Active':.11,'Power':.16}[segment]
    variant_effect=.09 if experiment=='Variant B' else 0
    kyc_p=clamp(.73+ch_effect+segment_effect+variant_effect*.50,.14,.95)
    kyc=add_days(day,RAND.randint(0,7)) if RAND.random()<kyc_p else None
    deposit=add_days(kyc,RAND.randint(0,13)) if kyc and RAND.random()<clamp(.69+ch_effect/2+segment_effect+variant_effect*.9,.12,.97) else None
    trade=add_days(deposit,RAND.randint(0,8)) if deposit and RAND.random()<clamp(.76+segment_effect/2+variant_effect*.7,.12,.98) else None
    if kyc and kyc>END: kyc=None;deposit=None;trade=None
    if deposit and deposit>END:deposit=None;trade=None
    if trade and trade>END:trade=None
    user={'user_id':user_id,'signup_date':iso(day),'signup_month':mstr(day),'signup_fy':fy(day),
          'acquisition_channel':channel,'region':region,'device':device,'behavior_segment':segment,
          'experiment_group':experiment,'kyc_date':iso(kyc),'first_deposit_date':iso(deposit),
          'first_trade_date':iso(trade),'churn_risk_score':None}
    rows['Users'].append(user);users.append(user)

activity_idx=defaultdict(dict)
trades_by_uid_month=defaultdict(list)
for user in users:
    uid=user['user_id']; sign=dt(user['signup_date']); seg=user['behavior_segment']; first_trade=dt(user['first_trade_date']) if user['first_trade_date'] else None
    price_mult={'Explorer':.48,'Casual':.9,'Active':1.65,'Power':3.45}[seg]
    month=date(sign.year,sign.month,1)
    prev_active=True
    while month<=END:
        age=(month.year-sign.year)*12+(month.month-sign.month)
        base=PROBS_SEG[seg]
        # activity persistence with realistic gradual cohort decay and occasional reactivation
        p=clamp(base-.02*min(age,12)+(.14 if prev_active else -.13)+(0.06 if month.month in (10,11,12) else 0),.09,.94)
        active= True if age==0 else RAND.random()<p
        if active:
            sessions=RAND.randint(2,9) if age==0 else RAND.randint(1,7+round(price_mult*2))
            active_days=min(RAND.randint(1,10+round(price_mult*3)),sessions+RAND.randint(0,3))
            feature=pick({'Market Watch':31,'Portfolio':22,'Order Book':28,'SIP Planner':11,'Rewards':8})
            support=1 if RAND.random()<.06 else 0
            ar={'user_id':uid,'activity_month':mstr(month),'activity_fy':fy(month),'sessions':sessions,'active_days':active_days,
                'most_used_feature':feature,'support_tickets':support}
            activity_idx[uid][mstr(month)]=ar
            rows['ActivityMonthly'].append(ar)
            if first_trade and (month.year,month.month)>=(first_trade.year,first_trade.month):
                n=RAND.randint(0,2)+int(RAND.random()<price_mult*.35)+(1 if mstr(month)==mstr(first_trade) else 0)
                for j in range(n):
                    if mstr(month)==mstr(first_trade) and j==0: tdate=first_trade
                    else:
                        last_day=min(plus_month(month)-timedelta(days=1),END)
                        first_day=max(month,first_trade)
                        if last_day<first_day:continue
                        tdate=first_day+timedelta(days=RAND.randint(0,(last_day-first_day).days))
                    prod=pick({'Spot':69,'Futures':21 if seg in ('Power','Active') else 8,'Earn / SIP':10})
                    amt=round(RAND.uniform(800,28000)*price_mult*(4.0 if prod=='Futures' else 1),2)
                    rate=.0010 if prod=='Spot' else (.00055 if prod=='Futures' else .0004)
                    fee=round(amt*rate,2)
                    trades_by_uid_month[(uid,mstr(month))].append({'trade_id':'','user_id':uid,'trade_date':iso(tdate),'trade_month':mstr(tdate),'trade_fy':fy(tdate),'product':prod,'asset':pick({'BTC':36,'ETH':25,'SOL':17,'Other':22}),'notional_inr':amt,'fee_inr':fee})
        prev_active=active
        month=plus_month(month)

# keep actual users with first-trade record; generate additional first-trade record if activity is anomalously missing
for u in users:
    ft=u['first_trade_date']
    if ft and not trades_by_uid_month[(u['user_id'],ft[:7])]:
        amt=round(RAND.uniform(900,22000),2)
        trades_by_uid_month[(u['user_id'],ft[:7])].append({'trade_id':'','user_id':u['user_id'],'trade_date':ft,'trade_month':ft[:7],'trade_fy':fy(dt(ft)),'product':'Spot','asset':'BTC','notional_inr':amt,'fee_inr':round(amt*.001,2)})
for group in trades_by_uid_month.values():
    for trade in group:
        trade['trade_id']=f'T{len(rows["Trades"])+1:07}'
        rows['Trades'].append(trade)
rows['Trades'].sort(key=lambda x:x['trade_date'])
# wallet tx
for u in users:
    uid=u['user_id']; first=u['first_deposit_date']; sign=dt(u['signup_date']); seg=u['behavior_segment']
    if first:
        amount=round(RAND.uniform(1000,45000)*({'Power':2.5,'Active':1.5}.get(seg,1)),2)
        rows['WalletTransactions'].append({'transaction_id':'','user_id':uid,'transaction_date':first,'transaction_month':first[:7],'transaction_fy':fy(dt(first)),
             'transaction_type':'Deposit','payment_method':pick({'UPI':64,'IMPS':20,'NEFT':12,'Card':4}),'amount_inr':amount,'status':'Success'})
    n=RAND.randint(0,3) if first else (1 if RAND.random()<.09 else 0)
    for _ in range(n):
        min_date=dt(first) if first else sign
        trans_date=min_date+timedelta(days=RAND.randint(0,max(0,(END-min_date).days)))
        typ=pick({'Deposit':72,'Withdrawal':28})
        status=pick({'Success':89,'Failed':7,'Pending':4})
        if not first and typ=='Withdrawal':typ='Deposit'
        rows['WalletTransactions'].append({'transaction_id':'','user_id':uid,'transaction_date':iso(trans_date),'transaction_month':mstr(trans_date),
         'transaction_fy':fy(trans_date),'transaction_type':typ,'payment_method':pick({'UPI':62,'IMPS':21,'NEFT':13,'Card':4}),
         'amount_inr':round(RAND.uniform(500,62000),2),'status':status})
rows['WalletTransactions'].sort(key=lambda x:x['transaction_date'])
for i,w in enumerate(rows['WalletTransactions']): w['transaction_id']=f'W{i+1:07}'

for u in users:
    if not u['first_trade_date'] or RAND.random()>.16:continue
    month=plus_month(dt(u['first_trade_date']))
    while month<=END:
        if RAND.random()<.65:
            planned=round(RAND.choice([500,1000,2000,5000,10000,15000]),2)
            paid=RAND.random()<.84
            rows['SIPInstallments'].append({'installment_id':f'S{len(rows["SIPInstallments"])+1:06}',
                'user_id':u['user_id'],'scheduled_month':mstr(month),'fy':fy(month),'planned_amount_inr':planned,
                'paid_amount_inr':planned if paid else 0,'status':'Paid' if paid else 'Missed'})
        if RAND.random()<.25:break
        month=plus_month(month)

for i,mon in enumerate(months):
    for ch in CHANNELS:
        n=sum(1 for u in users if u['signup_month']==mstr(mon) and u['acquisition_channel']==ch)
        if ch=='Organic':spend=0
        else:spend=round(n*{'Paid Search':1250,'Social':880,'Referral':475,'Affiliate':700,'Influencer':1050}[ch]*RAND.uniform(.87,1.12),2)
        rows['Campaigns'].append({'campaign_id':f'C{i*6+CHANNELS.index(ch)+1:04}', 'campaign_month':mstr(mon),
            'campaign_fy':fy(mon),'channel':ch,'spend_inr':spend,'impressions':int((n+15)*RAND.uniform(125,360)),
            'clicks':int((n+8)*RAND.uniform(5,14))})

# Predictive demo: supervised logistic regression, train on historical month-end snapshots and validate on Sep -> Oct 2026
activity=activity_idx
trades_index=defaultdict(list)
for t in rows['Trades']:trades_index[t['user_id']].append(t)

def features(u,month):
    midx=month.year*12+month.month
    start=dt(u['signup_date']); past=[plus_month(month,-k).strftime('%Y-%m') for k in (0,1,2)]
    acts=[activity.get(u['user_id'],{}).get(m) for m in past]
    recent=[t for t in trades_index[u['user_id']] if t['trade_month'] in past]
    days_since=0
    for k in range(12):
        mm=plus_month(month,-k).strftime('%Y-%m')
        if mm in activity.get(u['user_id'],{}):
            days_since=k*30;break
    else:days_since=360
    return {'sessions_latest':int(acts[0]['sessions']) if acts[0] else 0,'active_months_3m':sum(x is not None for x in acts),
        'sessions_3m':sum(int(x['sessions']) for x in acts if x),'trade_count_3m':len(recent),
        'trade_value_3m':round(sum(x['notional_inr'] for x in recent),2),
        'tenure_months':max(0,(month.year-start.year)*12+month.month-start.month),
        'months_since_active':days_since//30,'behavior_segment':u['behavior_segment'],'acquisition_channel':u['acquisition_channel'],'device':u['device']}
NUM=['sessions_latest','active_months_3m','sessions_3m','trade_count_3m','trade_value_3m','tenure_months','months_since_active']
CAT=['behavior_segment','acquisition_channel','device']
train=[]; test=[]
for u in users:
    signup=dt(u['signup_date'])
    for month in months:
        if month<date(2025,2,1) or month>date(2026,9,1) or signup>month:continue
        nxt=mstr(plus_month(month))
        feat=features(u,month)
        feat['target_inactive_next_month']=0 if nxt in activity.get(u['user_id'],{}) else 1
        (test if month==date(2026,9,1) else train).append(feat)

model=Pipeline([('prep',ColumnTransformer([
    ('num',StandardScaler(),NUM),('cat',OneHotEncoder(handle_unknown='ignore'),CAT)])),
    ('logreg',LogisticRegression(max_iter=700,C=0.45,random_state=261113))])
import pandas as pd
train_df=pd.DataFrame(train); test_df=pd.DataFrame(test)
model.fit(train_df[NUM+CAT],train_df['target_inactive_next_month'])
yp=model.predict_proba(test_df[NUM+CAT])[:,1]
auc=float(roc_auc_score(test_df['target_inactive_next_month'],yp)); ap=float(average_precision_score(test_df['target_inactive_next_month'],yp))
prev=float(test_df['target_inactive_next_month'].mean())
from sklearn.metrics import brier_score_loss
brier=float(brier_score_loss(test_df['target_inactive_next_month'],yp))
val={'metric':'Temporal holdout (Sep 2026 features → Oct 2026 inactivity)','sample_size':len(test),'positive_rate':round(prev,4),
     'roc_auc':round(auc,4),'pr_auc':round(ap,4),'brier_score':round(brier,4),'train_snapshots':len(train),
     'predictive_target':'No recorded app activity in subsequent calendar month',
     'scope':'Synthetic data only; not validated on real customers', 'model':'Logistic regression with standard scaling and one-hot encoding'}
rows['ModelValidation'].append(val)
for u in users:
    if dt(u['signup_date'])>date(2026,10,31):
        u['churn_risk_score']=''
    else:
        f=pd.DataFrame([features(u,date(2026,10,1))])
        u['churn_risk_score']=round(float(model.predict_proba(f[NUM+CAT])[:,1][0]),4)

# Sort and export; JSON is the same records as CSV and Excel (CSV uses readable headers).
for name, data in rows.items():dump(name,data)
# metadata - all monetary fields INR, dates ISO
meta={
  'as_of':END.isoformat(),'fy_begin_month':4,'simulated':True,'seed':261113,'period_start':START.isoformat(),
  'generation_note':'Entirely synthetic; generated independently for skills demonstration. Not actual CoinDCX metrics, customers, or operations.',
  'row_counts':{name:len(data) for name,data in rows.items()},'model_validation':val,
  'metric_definitions':{
    'activation':'Among users who signed up in the selected FY, percent with first trade on or before dataset end.',
    'M1_retention':'For signup cohorts with a fully observed subsequent calendar month, share with >=1 recorded app session in month M1.',
    'FY':'Indian financial year, 1 April through 31 March; FY2026-27 data only through 13 Nov 2026.',
    'trading_volume':'Sum of synthetic executed trade notional (INR) during report period.',
    'fee_revenue':'Sum of synthetic trading fees (INR), not profit.',
    'CAC':'Non-organic campaign spend divided by new users acquired in the same FY and channel. Simplified channel-attributed CAC.',
    'marketing_return_proxy':'(68% of attributed trading fee revenue minus marketing spend)/marketing spend, illustrative contribution ratio, not actual ROI.',
    'churn_model':'Logistic regression trained on prior monthly snapshots with following-month activity as outcome; scores anchored to Oct 2026 snapshot.'}}
(ROOT/'data'/'metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
with (ROOT/'data'/'dashboard-data.js').open('w',encoding='utf-8') as f:
    f.write('/* Synthetic demonstration data. Generated by tools/generate_dataset.py */\nwindow.FINTECH_DEMO_DATA=')
    json.dump({'metadata':meta,'users':rows['Users'],'activity':rows['ActivityMonthly'],'trades':rows['Trades'],
       'wallet':rows['WalletTransactions'],'sip':rows['SIPInstallments'],'campaigns':rows['Campaigns']},f,separators=(',',':'))
    f.write(';\n')

print('MODEL',val)
print('DATA JS MB',round((ROOT/'data'/'dashboard-data.js').stat().st_size/1048576,2))
