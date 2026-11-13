"""Build the full styled Excel dataset with artifact_tool. CSV and JS remain canonical and in sync."""
from pathlib import Path
import csv,time,math,random
count_by_sheet={}
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'excel'/'FinSight_Synthetic_Dataset_FY2024_2027.xlsx'
source=ROOT/'data'/'csv'
wb=Workbook.create()
navy='#0C2033';mint='#1BC6A3';white='#F0F8FF';slate='#849CB1';tealFill='#DDF9F1';

intro=wb.worksheets.add('Read_Me')
intro.get_range('A1:H2').merge_cells if False else None
intro.merge_cells('A1:H2')
intro.get_range('A1').values=[['FINSIGHT  |  FINTECH PRODUCT INTELLIGENCE']]
intro.get_range('A1:H2').format={'fill':navy,'font':{'name':'Aptos Display','size':18,'bold':True,'color':white},'vertical_alignment':'center','row_height':25}
intro.merge_cells('A4:H4');intro.get_range('A4').values=[['SYNTHETIC DATA · NOT COINDCX OPERATIONAL DATA']]
intro.get_range('A4:H4').format={'fill':'#E9F9F4','font':{'bold':True,'color':'#087860'},'row_height':26}
info=[('Purpose','Portfolio demonstration of product growth, activation, retention, marketing, experimentation, and churn-risk analysis.'),
('Coverage','FY 2024–25, FY 2025–26, FY 2026–27 YTD (through 13 November 2026).'),
('Indian FY','1 April to 31 March. Example: FY2025-26 = 1 April 2025 through 31 March 2026.'),
('Currency','All spend, trading, fees, and deposit amounts are INR; visual dashboard uses ₹, Lakhs, Crores.'),
('Source','Generated using tools/generate_dataset.py with deterministic random seed 261113.'),
('Data integrity','Full records are supplied in CSV and dashboard-data.js. Excel includes full Users, Campaigns and SIP tabs plus curated event samples.'),
('Privacy','No real user names, emails, accounts, CoinDCX data, or sensitive personal data.'),
('Experiment','Control A vs Variant B onboarding simulation begins FY2026–27; variant assignment is synthetic.'),
('Model validation','Logistic regression; temporal holdout uses Sep 2026 features to predict Oct 2026 inactivity.'),
('License','MIT for the source code; dataset is simulated portfolio data.'),
('Tab Users','One row per registered synthetic user including milestone dates and demo churn score.'),
('Tab ActivityMonthly','Curated FY-stratified event sample. Use full data/csv/ActivityMonthly.csv for complete history.'),
('Tab Trades','Curated FY-stratified event sample. Full Trades.csv is included in the ZIP.'),
('Tab WalletTransactions','Curated FY-stratified wallet sample. Full WalletTransactions.csv is included in the ZIP.'),
('Tab SIPInstallments','Synthetic scheduled SIP installments and payment status.'),
('Tab Campaigns','Channel/month spend, clicks and impressions; organic spend treated as zero.'),
('Tab ModelValidation','A temporal validation summary; not a claim of deployment-ready ML accuracy.')]
intro.get_range('A6:B'+str(5+len(info))).values=[[a,b] for a,b in info]
intro.get_range('A6:A'+str(5+len(info))).format={'fill':'#EFF6FB','font':{'bold':True,'color':'#19344C'},'row_height':24}
intro.get_range('B6:B'+str(5+len(info))).format={'font':{'color':'#25445B'},'row_height':24}
intro.get_range('A:A').format.column_width=27;intro.get_range('B:B').format.column_width=110

names=['Users','ActivityMonthly','Trades','WalletTransactions','SIPInstallments','Campaigns','ModelValidation']
for name in names:
    t0=time.time();print('Building',name,flush=True)
    with (source/(name+'.csv')).open(encoding='utf-8',newline='') as fh:
        reader=csv.reader(fh);hdr=next(reader);rows=list(reader)
    sample_cap={'ActivityMonthly':3600,'Trades':3600,'WalletTransactions':2400}
    if name in sample_cap:
        fy_col=next((i for i,k in enumerate(hdr) if k in ('activity_fy','trade_fy','transaction_fy')),None)
        rng=random.Random(20261113)
        collected=[]
        for fyname in ('FY2024-25','FY2025-26','FY2026-27'):
            pool=[r for r in rows if r[fy_col]==fyname]
            collected += sorted(rng.sample(pool,min(len(pool),sample_cap[name]//3)),key=lambda r:r[0])
        rows=collected
    count_by_sheet[name]=len(rows)
    ws=wb.worksheets.add(name)
    ncols=len(hdr);nrows=len(rows)
    ws.get_range_by_indexes(0,0,1,ncols).values=[hdr]
    ws.get_range_by_indexes(0,0,1,ncols).format={'fill':navy,'font':{'bold':True,'color':white,'size':10},'row_height':30,'wrap_text':True,'vertical_alignment':'center'}
    for start in range(0,nrows,2500):
        chunk=rows[start:start+2500]
        numKeys=[i for i,k in enumerate(hdr) if k in ('notional_inr','fee_inr','amount_inr','spend_inr','planned_amount_inr','paid_amount_inr','churn_risk_score','sessions','active_days','support_tickets','impressions','clicks')]
        new=[]
        for r in chunk:
            line=[]
            for j,x in enumerate(r):
                if x=='' :line.append(None)
                elif j in numKeys:
                    try:line.append(float(x) if '.' in x else int(x))
                    except:line.append(x)
                else:line.append(x)
            new.append(line)
        ws.get_range_by_indexes(start+1,0,len(new),ncols).values=new
    ws.freeze_panes.freeze_rows(1)
    ws.get_range_by_indexes(0,0,nrows+1,ncols).format.column_width=19
    ws.get_range_by_indexes(0,0,nrows+1,1).format.column_width=19
    for k,col in enumerate(hdr):
        if col in ('acquisition_channel','most_used_feature','behavior_segment','payment_method','experiment_group','first_deposit_date','first_trade_date'):
            ws.get_range_by_indexes(0,k,nrows+1,1).format.column_width=22
        if col in ('notional_inr','fee_inr','amount_inr','spend_inr','planned_amount_inr','paid_amount_inr'):
            ws.get_range_by_indexes(1,k,nrows,1).set_number_format('"₹"#,##0.00;[Red]("₹"#,##0.00)')
        if col=='churn_risk_score': ws.get_range_by_indexes(1,k,nrows,1).set_number_format('0.0%')
    # AutoFilter will be available via the actual Excel table.
    if nrows:
        try: ws.tables.add(ws.get_range_by_indexes(0,0,nrows+1,ncols),True,'T_'+name[:16])
        except Exception as e:print('Table warning',name,str(e)[:150],flush=True)
    print('Finished',name,nrows,'rows',round(time.time()-t0,1),'seconds',flush=True)

# a compact, formula-driven consistency verification sheet
v=wb.worksheets.add('Data_Checks')
v.get_range('A1:D1').values=[['FINSIGHT · DATA QUALITY','CALCULATED','SOURCE / MEANING','STATUS']]
v.get_range('A1:D1').format={'fill':navy,'font':{'bold':True,'color':white},'row_height':30}
checks=[('Synthetic registered users',f'=COUNTA(Users!A2:A{count_by_sheet["Users"]+1})','All synthetic users'),
('Curated executed trade rows',f'=COUNTA(Trades!A2:A{count_by_sheet["Trades"]+1})','Full history available separately as CSV'),
('Marketing campaign rows',f'=COUNTA(Campaigns!A2:A{count_by_sheet["Campaigns"]+1})','Full spend by financial-year month')]
for idx,(label,formula,source_note) in enumerate(checks,2):
    v.get_range('A'+str(idx)).values=[[label]];v.get_range('B'+str(idx)).formulas=[[formula]];v.get_range('C'+str(idx)).values=[[source_note]];v.get_range('D'+str(idx)).values=[['Formula-driven']]
v.get_range('A:A').format.column_width=47;v.get_range('B:B').format.column_width=20;v.get_range('C:C').format.column_width=52;v.get_range('D:D').format.column_width=19
v.get_range('A2:D4').format.row_height=24
print('Exporting Excel...',flush=True)
SpreadsheetFile.export_xlsx(wb).save(str(OUT))
print('EXPORTED',OUT,OUT.stat().st_size,flush=True)
try:print('INSPECT',wb.inspect({'kind':'table','range':'Data_Checks!A1:D4','include':'values,formulas','table_max_rows':4,'table_max_cols':4}).ndjson[:1200],flush=True)
except Exception as e:print('INSPECT WARNING',e,flush=True)
