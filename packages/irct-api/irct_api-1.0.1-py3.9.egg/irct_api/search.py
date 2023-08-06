from bs4 import BeautifulSoup
from requests import get

_dictionary = {'Assignment': 'assignment', 'IRCT Id': 'irct_id', 'Recruitment status': 'recruitment_status', "Blinding (investigator's opinion)": 'blinding', 'Blinding description': 'blinding_description', 'Contact': 'contact', 'Ethics committee': 'ethic_committee', 'Gender': 'gender', 'Health conditions studied': 'health_condition_description', 'Health conditions studied - ICD10 code': 'health_condition_icd10_code', 'Inclusion/Exclusion criteria': 'inc_exc_criteria', 'Interventions': 'intervention_description', 'Intervention categories': 'intervention_category', 'Maximum age': 'maximum_age', 'Minimum age': 'minimum_age', 'Other design features': 'other_design_features', 'Placebo': 'placebo', 'Primary outcome': 'primary_outcome_description', 'Outcome': 'outcome_description', 'Public title': 'public_title', 'Purpose': 'purpose', "Randomization (investigator's opinion)": 'randomization', 'Randomization description': 'randomization_description', 'Expected recruitment start date': 'recruitment_expected_start_date', 'Expected recruitment end date': 'recruitment_expected_end_date', 'Actual recruitment start date': 'recruitment_actual_start_date', 'Actual recruitment end date': 'recruitment_actual_end_date', 'Trial completion date': 'completion_date', 'Registration date': 'registration_date', 'Target sample size': 'target_sample_size', 'Scientific title': 'scientific_title', 'Sponsor': 'sponsor', 'Sponsor: public or private sector': 'sponsor_sector', 'Sponsor: domestic or foreign origin': 'sponsor_origin', 'Sponsor: origin is international organization': 'sponsor_origin_international', 'Sponsor: country of origin': 'sponsor_origin_country', 'Sponsor: type of organization providing the funding': 'sponsor_type', 'Summary': 'summary', 'Acronym': 'acronym', 'Phase': 'phase', 'Recruitment centers': 'recruitment_center'}
names = [i for i in list(_dictionary.keys())]
_special = {'Assignment':'[@property]', 'Recruitment status':'[@property]',"Blinding (investigator's opinion)":'[@property]','Gender':'[@property]',"Intervention categories":'[@property]','Maximum age':'[@property TO @prop]','Minimum age':'[@property TO @prop]','Placebo':'[@property]','Purpose':'[@property]',"Randomization (investigator's opinion)":'[@property]','Maximum age':'[@property TO @prop]','Expected recruitment start date':'[@property TO @prop]','Expected recruitment end date':'[@property TO @prop]','Actual recruitment start date':'[@property TO @prop]','Actual recruitment end date':'[@property TO @prop]','Registration date':'[@property TO @prop]','Target sample size':'[@property TO @prop]','Sponsor: public or private sector':'[@property]','Sponsor: domestic or foreign origin':'[@property]','Sponsor: origin is international organization':'[@property]','Sponsor: type of organization providing the funding':'[@property]','Phase':'[@property]'}
_url = "https://irct.ir/"
_search = "search/result"
_query = "?query="

class IRCTApiException(Exception):
    pass

def basic_search(q:str) -> list:
    '''
    q is search query string which used to search in all fileds. (take a look at advance_search function if you want search in a specify field.)
    you can use basic_search for your own command searches too just give advance_query string as q.
    '''
    resp = get(_url+_search+query+'+'.join(i for i in q.split(' ')))
    soup = BeautifulSoup(resp.text, 'html.parser')
    resl = soup.find_all('div',class_='col-md-11 texts')[1:]
    result = list()
    for i in resl:
        try:
            result.append({'title':i.find('div',class_='result-title').find('a').text,
                           'summary':i.find('div',class_='result-summary').text.replace('<span class="highlighted">','').replace('</span>','').replace('<span class="ellipsis">',''),
                           'irct-id':i.find('div',class_='result-irct-id').text[8:],
                           'similar':[(j.text, j.attrs['href']) for j in i.find('similar-trials', class_="ng-cloak").find_all('a')]})
        except Exception as e:
            pass
    return result


def advance_search(q:str="", advance_options:dict=dict()) -> list:
    '''
    q is search query string which is for all fields search.
    advance_options is a dictionary which contain the name of the field (which you can see in `names` list (`irct.names`)) in the key and the input(s) in the value section, for multi values you gotta use list in value section.
    advance_options example : {'IRCT Id':['ID'],'Actual recruitment end date':['1990-01-01','1990-01-02']}
    '''
    if len(list(advance_options.keys())) < 1:
        raise IRCTApiException("Requested to advance search with no argument for advance search.")
    if len(list(advance_options.keys())) != len(list(advance_options.values())):
        raise IRCTApiException("One of options is without value")

    squery = ""
    count = 1

    while True:
        key = list(advance_options.keys())[count-1]
        if squery == "":
            if key in _special:
                num = _special[key].count('@')
                if num > 2:
                    raise IRCTApiException("Special option get more than two input.")
                elif num < 1:
                    raise IRCTApiException("Special option get less than one input.")
                if advance_options[key].__class__ == list:
                    if len(advance_options[key]) != num:
                        raise IRCTApiException("Inputs are not equal to advance option.")
                    if num == 1:
                        squery = f"@{_dictionary[key]}:[{advance_options[key][0]}]"
                    else:
                        squery = f"@{_dictionary[key]}:[{advance_options[key][0]} TO {advance_options[key][1]}]"
                else:
                    if num != 1:
                        raise IRCTApiException("Inputs are not equal to advance option.")
                    squery = f"@{_dictionary[key]}:[{advance_options[key]}]"
            else:
                if advance_options[key].__class__ == list:
                    squery = f"@{_dictionary[key]}:{advance_options[key][0]}"
                else:
                    squery = f"@{_dictionary[key]}:{advance_options[key]}"
        else:
            squery = "(" + squery + ") AND "
            if key in _special:
                num = _special[key].count('@')
                if num > 2:
                    raise IRCTApiException("Special option get more than two input.")
                elif num < 1:
                    raise IRCTApiException("Special option get less than one input.")
                if advance_options[key].__class__ == list:
                    if len(advance_options[key]) != num:
                        raise IRCTApiException("Inputs are not equal to advance option.")
                    if num == 1:
                        squery += f"@{_dictionary[key]}:{_special[key].replace('@property',advance_options[key][0])}"
                    else:
                        squery += f"@{_dictionary[key]}:{_special[key].replace('@property',advance_options[key][0]).replace('@prop',advance_options[key][1])}"
                else:
                    if num != 1:
                        raise IRCTApiException("Inputs are not equal to advance option.")
                    squery += f"@{_dictionary[key]}:{_special[key].replace('@property',advance_options[key])}"
            else:
                if advance_options[key].__class__ == list:
                    squery += f"@{_dictionary[key]}:{advance_options[key][0]}"
                else:
                    squery += f"@{_dictionary[key]}:{advance_options[key]}"
        if count == len(list(advance_options.keys())):
            break
        else:
            count += 1

    if q != "":
        squery = "(" + squery + ")" + " AND " + q

    return basic_search(squery)
