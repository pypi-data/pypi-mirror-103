import json

from requests_html import HTMLSession
from polypuppet.server.person import Person, PersonType
from polypuppet.messages import error

_payload = {
    "username": "",
    "password": "",
    "execution": "3ed9e215-050f-4cc8-97e6-332c9cb56b90_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuMXB3czNaVk1xbTlITS80QUd6Y2phUyt2R3M0aVNXU1Z5KzdjcHI2bzkyL1BzV1dXRHV2WXNKc3hjd2gyVGIyMGw1TVN3bEd3dHFyeEljZi9EWENiUE82c3lSdnlBWGlYQmV6UFRjaWhLbWUrM01Xazd3SWVGL3pWNkhIOFRQZ2N2YzdlTUJMKzBTN1FldVgxMURwelIxMXZPek9vdEt0WkhsWWQxSUpoNzlRYjQydUs5TGprMi9zY1Z0d083WTV1dkI2OFM5TENsMURxSWVWdGp5cUhyZW9LbDlBbm5sNkU0VnR4L3RTMEpxZTB5VnJvQnIvSG4rd3JQUWx0NXNwRXI0SFdDNUhaRkhIVkNLM3RwdDM3b042UWZzRTFWVDJtdWtXK3NNL0NoTnR0WDFRZE9lQ2E3R3BiYXcwT2Jjb3VFK1k0dS9NTUhKaVd0bVFIazNia2V5N1JCSXhrajhsbjY4YzRxbGVMWTd5eEJLVlE2dHA1U1RLYXpJRkhscnkwNlgvS1lyOGJTUHpoUWIwOEFJZlBBdDdHcjNVUHk4NkQ0TjFSclF6Tm1EV3d4SDZtV3FBTWM4TFRYaldwbi91V2NESU81d0czVlZoY2xJSnFwMm9RWGE0Ly9OUGlYMGh0cjZ5S1lPLzN3M01Qa0IrdUViR1lmUGFEdlJmNjdMcFpMZHhNckoxOUFjOVhMMnQvbXBGeGl2eFZyZDVqTU1tY0liZllkb0NJWFJXci9acDZmL2pMTDNpcVRRb2txdmE0YjAwb25HakxIc1RoRGRsc1lEeHBJdEZVZ2U4WDFNVlRxMUpyQnM0NkdoTnE1bk9oY3dhTVFuY3Y0WDY5dGlKdlRPMENyMTlMUFdXUUp2bkpOc2xMSDdkT3R5cWt1alBMTmZROGR4SHF0dGRCNEFIRnc4aTNCMVZlVnVXOUZDaEVVSUJjMitzOE1tN2V1eVBLOHBMOFFiNjZBMkpEODBrU3ZRYXVEanVHaFJzZEZnRnZNMnE1cmhRcHRNaHpSMFdnTWdzMlV5SmFQYWsrdFRQZlBjWHk4UnlSbGJWdm16MHA5SUlkaWNsRE5UQmxMQW1TSU1Lb1gxQWpsLzB3dlNCVDVGSkpIdmo1ZzFGRVdwemRoWW55RTNuYkhOMnhLZGlyTk9keTAwWmk4SWpJdlV5cVhyTCtWalI1azRYcjkrb2hPR0h4QlhCTHJMSTBrSjYyblBIUjNBb1VIc2ZERk9MUTV0alpXb3dNdWVldVlOdVBBRDFRdG10VnlZcVZsQlRBN0lucGpGMm5qWU8xdzJPMGN1S0FGTHRudit3Nmd5aU1uaTdCUlVOZUE0WHB1Q1VaYjBzUVpNaXRjVVNSN0FIRS5uSGVTeGpFVC04SDRvcFdmS0JPLXJXX1NZYmlOd015NmRxdWVoY1Fsb0FLOS1QUlhBcFllZXFuM3ZtQ09mdGhqY1E3MEVJYlFWN2JJbENZaVN6SC1pQQ==",
    "_eventId": "submit",
    "geolocation": ""
}


def authenticate(username, password):
    _payload['username'] = username
    _payload['password'] = password

    session = HTMLSession()
    try:
        r = session.post('https://cas.spbstu.ru/login', _payload)
    except:
        error.cannot_connect_to_cas()

    if r.status_code != 200:
        return Person()

    person_html = r.html.find("script")[0]
    person_json = json.loads(person_html.text)['user']['wsAsu']

    person = Person(username=username)
    person.id = person_json['user_id']
    person.first_name = person_json['first_name']
    person.last_name = person_json['last_name']
    person.middle_name = person_json['middle_name']
    person.group = person_json['structure'][0]['sub_dep']
    if person_json['structure'][0]['type'] == 'Студент':
        person.type = PersonType.STUDENT
    return person
