from app.lib.money import cents_to_dollar

def format_currency(amount, convert_to_dollars=True):


    if convert_to_dollars:
        amount = cents_to_dollar(amount)

    return '{:,.2f}'.format(amount)
