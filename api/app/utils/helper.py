from datetime import datetime, timedelta


def get_time():
    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return str(ist_now.time())[:8]


def format_symbol_name(symbol):
    symbol = symbol.split(":")
    return f"#{symbol[1]}:{symbol[0]}"
