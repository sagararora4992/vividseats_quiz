def includeme(config):
    config.add_route('available_tickets', '/available_tickets')
    config.add_route('new_ticket', '/new_ticket')
    config.add_route('update_ticket', '/update_ticket')
    config.add_route('best_ticket', '/best_ticket')
