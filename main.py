from flask import Flask, render_template, request

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1SWjNBVu3bDMev3NQe1Bef9VTx48WLP-SsoUADCLmDRE'

app = Flask(__name__)
        
def get_cell_value(sheet, cell_range):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=cell_range).execute()
    values = result.get("values", [])
    
    return values

@app.route('/', methods=['GET', 'POST'])
def display_cells():
    
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        #all input properties
        if request.method == 'POST':

            updates = []

            name = request.form.get('name')
            if name:
                updates.append(('DASHBOARD!C3', name))

            purchase_price = request.form.get('purchase_price')
            if purchase_price:
                updates.append(('DASHBOARD!C10', int(purchase_price)))

            unit_count = request.form.get('unit_count')
            if unit_count:
                updates.append(('DASHBOARD!C6', int(unit_count)))

            sample = request.form.get('sample')
            if sample:
                updates.append(('Investor Sample!E3', int(sample)))
            
            lp_split = request.form.get('lp_split')
            if lp_split:
                updates.append(('DASHBOARD!L4', float(lp_split)/100))

            asset_management_fee = request.form.get('asset_management_fee')
            if asset_management_fee:
               updates.append(('DASHBOARD!D36', float(asset_management_fee)/100))

            preferred_return = request.form.get('preferred_return')
            if preferred_return:
               updates.append(('DASHBOARD!L6', float(preferred_return)/100))

            hurdle = request.form.get('hurdle')
            if hurdle:
               updates.append(('DASHBOARD!L8', float(hurdle)/100))

            earnest_money = request.form.get('earnest_money')
            if earnest_money:
               updates.append(('DASHBOARD!C21', int(earnest_money)))

            acq_fee = request.form.get('acq_fee')
            if acq_fee:
               updates.append(('DASHBOARD!D35', float(acq_fee)/100))

            closing_cost = request.form.get('closing_cost')
            if closing_cost:
                updates.append(('ClosingCosts!D7', float(closing_cost)/100))

            capex = request.form.get('capex')
            if capex:
                updates.append(('CapEx&Reserves!D4', int(capex)))

            down_payment = request.form.get('down_payment')
            if down_payment:
                updates.append(('DASHBOARD!I5', float(down_payment)/100))

            rate = request.form.get('rate')
            if rate:
                updates.append(('DASHBOARD!I6', float(rate)/100))

            io_months = request.form.get('io_months')
            if io_months:
                updates.append(('DASHBOARD!I7', int(io_months)))

            amor_months = request.form.get('amor_months')
            if amor_months:
                updates.append(('DASHBOARD!I8', int(amor_months)))

            ltv_refi = request.form.get('ltv_refi')
            if ltv_refi:
                updates.append(('DASHBOARD!I30', float(ltv_refi)/100))

            rate_refi = request.form.get('rate_refi')
            if rate_refi:
                updates.append(('DASHBOARD!I23', float(rate_refi)/100))

            refi_year = int(request.form.get('refi_year'))
            if refi_year:
                updates.append(('DASHBOARD!I28', int(refi_year)))

            cap_rate_refi = request.form.get('cap_rate_refi')
            if cap_rate_refi:
                updates.append(('DASHBOARD!I29', float(cap_rate_refi)/100))

            sale_year = request.form.get('sale_year')
            if sale_year:
                updates.append(('DASHBOARD!I31', int(sale_year)))

            cap_rate_sale = request.form.get('cap_rate_sale')
            if cap_rate_sale:
                updates.append(('DASHBOARD!I32', float(cap_rate_sale)/100))

            rent = request.form.get('rent')
            if rent:
                updates.append(('Actuals&UnitMix!C6', int(rent)*12))

            vacancy = request.form.get('vacancy')
            if vacancy:
                updates.append(('Actuals&UnitMix!D7', float(vacancy)/100))

            other_income = request.form.get('other_income')
            if other_income:
                updates.append(('Actuals&UnitMix!C10', int(other_income)))

            annual_expenses = request.form.get('annual_expenses')
            if annual_expenses:
                updates.append(('Actuals&UnitMix!C30', int(annual_expenses)*12))

            rent_escalator_1 = request.form.get('rent_escalator_1')
            if rent_escalator_1:
                updates.append(('P&L!D3', float(rent_escalator_1)/100))

            rent_escalator_2 = request.form.get('rent_escalator_2')
            if rent_escalator_2:
                updates.append(('P&L!F3', float(rent_escalator_2)/100))

            rent_escalator_3 = request.form.get('rent_escalator_3')
            if rent_escalator_3:
                updates.append(('P&L!H3', float(rent_escalator_3)/100))

            expenses_escalator = request.form.get('expenses_escalator')
            if expenses_escalator:
                updates.append(('P&L!D4', float(expenses_escalator)/100))

            #batch update
            if updates:
                batch_update = {
                    'data': [],
                    'valueInputOption': 'RAW'
                }

                for update in updates:
                    cell_range = update[0]
                    value = update[1]
                    update_values = [[value]]
                    batch_update['data'].append({
                        'range': cell_range,
                        'values': update_values
                    })

                result = sheet.values().batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body=batch_update
                ).execute()
                
        #output
        equity_stack = get_cell_value(sheet, 'DASHBOARD!C27:C32')
        project_returns = get_cell_value(sheet, 'DASHBOARD!L35:L38')
        investor_returns = get_cell_value(sheet, 'Investor Sample!G12:G16')
        sample_returns = get_cell_value(sheet, 'Investor Sample!Q6:Q11')
        splits = get_cell_value(sheet, 'DASHBOARD!L4:L5')
        details = get_cell_value(sheet, 'P&L!D16:V78')

        return render_template('index.html', equity_stack=equity_stack, project_returns=project_returns, investor_returns=investor_returns, sample_returns=sample_returns, splits=splits, details=details)
    
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)