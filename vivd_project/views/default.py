from pyramid.view import view_config
from pyramid.response import Response
import json
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql import label

from .. import models

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:
1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.
2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='available_tickets', renderer='json', request_method='GET')
def available_tickets(request):
    """
    This view will return a JSON of all available tickets for an event
    identified as a GET query parameter
    :request params:
        - event_id: Database ID of the event
    :returns:
        - JSON with an array of tickets
    """
    try:
        print("I am inside try")
        print(request.params)
        event_id = request.GET['event_id']
        print(event_id)
        query = request.dbsession.query(models.tickets)
        one = query.filter_by(event_id=int(event_id), status=1).all()
        result = {'tickets': []} 
        columns = models.tickets.__table__.columns 
        for ticket in one:
            ticket_js = {str(key).split('.')[1]:getattr(ticket, str(key).split('.')[1]) for key in columns}
            print(ticket_js)
            result['tickets'].append(ticket_js)
        return json.dumps(result, default=myconverter)
    except KeyError:
        request.response.status = 500
        return "Invalid Request"


@view_config(route_name='new_ticket', renderer='json', request_method='POST')
def insert_ticket(request):
    """
    This view will allow the insertion of a new ticket into the
    DB
    :request params:
        - event_id: DB ID of the event
        - section: Seat section
        - rownum: Seat row
        - seat: Seat number
        - price: Price of the ticket
        - seller_id: Price
        - status: Ticket status, 0 active 1 inactive 2 on hold
    :returns:
        - JSON with Acknowledgement
    """
    required_keys = {'event_id', 'section', 'rownum', 'seat', 'price', 'seller_id', 'status'}
    param_keys = set(request.POST.keys())
    print(f"param keys - {param_keys}")
    #if len(param_keys) >= len(required_keys):
    #    return "Invalid Request"

    try:
        print(param_keys)
        new_ticket = models.tickets()
        for param in param_keys:
            if param == 'status':
                setattr(new_ticket,param, bool(request.POST[param]))
            else:
                setattr(new_ticket,param, request.POST[param])
            print(param)
        print(new_ticket)
        request.dbsession.add(new_ticket)   
        request.dbsession.flush()
    except DBAPIError:
        return "Invalid Request"
    return {'status':'success'}


@view_config(route_name='update_ticket',renderer='json', request_method='PUT')
def update_ticket(request):
    """
    Mark a ticket as sold
    :request params:
        - event_id
        - section
        - rownum
        - seat
        - status
    :returns:
        -  Aknowledgement
    """
    required_keys = {'event_id', 'section', 'rownum', 'seat', 'status'}
    param_keys = set(request.params.keys())

    if len(param_keys | required_keys) > len(required_keys):
        return "Invalid Request"
    event_id = request.POST['event_id']
    print(event_id)
    section= request.POST['section']
    rownum= request.POST['rownum']
    seat= request.POST['seat']
    status= request.POST['status']
    query = request.dbsession.query(models.tickets)
    one=query.filter_by(event_id=int(event_id), status=bool(status),section=int(section),rownum=int(rownum), seat=int(seat)).one()
    print(one.status)
    one.status=0
    request.dbsession.flush()
    
    return "success"


@view_config(route_name='best_ticket', renderer='json', request_method='GET')
def best_ticket(request):
    """
    Find the best ticket for the provided event section, row, seat an price
    :request params:
        - event_id
    :returns:
        - JSON for best ticket
    """
    event_id = request.GET['event_id']
    query = request.dbsession.query(models.tickets,label('minprice', func.min(models.tickets.price)))
    one = query.filter_by(event_id=int(event_id)).order_by('minprice').group_by('event_id','section','rownum','seat','seller_id','status').first()
    print(getattr(one[0],'event_id'))
    columns= models.tickets.__table__.columns
    result = {'tickets': []}
    ticket_js = {str(key).split('.')[1]:getattr(one[0], str(key).split('.')[1]) for key in columns}
    print(ticket_js)
    result['tickets'].append(ticket_js)
    return json.dumps(result, default=myconverter)
