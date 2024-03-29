import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def init():
    gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    gcredentials = os.getenv('GOOGLE_SHEETS_KEY')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    return gspread.authorize(credentials)

def add_to_gsheet(users_personal_data):
    gdocument = 'foodPlan'
    gc = init()
    wks = gc.open(gdocument).sheet1
    wks.append_row([users_personal_data['first_name'], users_personal_data['last_name'],
                    users_personal_data['phone_number']])


def add_sub_to_gsheet(users_personal_data, sub_parameters):
    gdocument = 'foodPlan'
    gc = init()
    wks = gc.open(gdocument).worksheet('Лист2')

    users_allergies = ''
    for allergy in sub_parameters['allergies']:
        if users_allergies:
            users_allergies = users_allergies + ', ' + allergy
        else:
            users_allergies = allergy

    wks.append_row([users_personal_data['first_name'], users_personal_data['last_name'],
                    users_personal_data['phone_number'], sub_parameters['menu_type'], 
                    sub_parameters['number_of_meals'], sub_parameters['number_of_persons'], 
                    users_allergies, sub_parameters['type_of_subs'], 
                    sub_parameters['promo_code'], sub_parameters['price']])


def get_data_from_worksheet(title, phone):
    gdocument = 'foodPlan'
    gc = init()
    wks = gc.open(gdocument).worksheet(title)
    all_values = wks.get_all_values()

    returned_values = []

    for value in all_values:
        if phone == value[2]:
            returned_values.append(value)

    return returned_values
    