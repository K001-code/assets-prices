import requests

def main():
    try:
        response = requests.get("https://api.gold-api.com/symbols")
    except requests.exceptions.HTTPError:
        print("An error has occured.")

    info = response.json()
    # print(json.dumps(info))
    assets, symbols = display_n_return(info)
    find = get_symbl("Enter(name or symbol): ", assets, symbols)

    try:
        rsp = requests.get("https://api.gold-api.com/price/" + find)
    except requests.exceptions.HTTPError:
        print("An error has occured.")

    data = rsp.json()
    price_p_unit = data["price"]
    # price per oz, per lb, per coin
    global p_oz_asset, p_lb_asset, p_coin_asset 
    p_oz_asset = ["XAG", "XAU", "XPD",]
    p_lb_asset = ["HG",]
    p_coin_asset = ["BTC", "ETH", ]

    unit = get_unit("Enter unit of measurement (name/symbol): ", find)
    qty = get_pos_int("Enter amount: ")
    total = cal(unit, qty, price_p_unit, find)
    print(f"Your total: ${total:.2f}")


def display_n_return(data):
    names, symbols = [], []
    print("\n", "Name:".center(20), "Symbol:".center(20))
    for asset in range(len(data)):
        print(data[asset]["name"].center(20), data[asset]["symbol"].center(20))
        names.append(data[asset]["name"].upper())
        symbols.append(data[asset]["symbol"])
    return names, symbols


def get_symbl(text, name, sym):
    while True:
        inp = input(f"{text}").strip().upper()
        if inp in name:
            return sym[name.index(inp)]
        elif inp in sym:
            return inp


def get_unit(text, sym):
    while True:
        if sym in p_oz_asset or sym in p_lb_asset:
            measurements = {"Ounce": "Oz", "Gram": "G", "Kilogram": "Kg", "ជី": "Ji"}
            print("\n", "Name:".center(20), "Symbol:".center(20))
            for name in measurements.keys():
                print(f"{name}".center(20), f"{measurements[name]}".center(20))
            
            unit = input(text).capitalize()
            if unit in measurements.keys():
                return measurements[unit]
            elif unit in measurements.values():
                return unit
        else:
            return "coin"


def get_pos_int(text):
    while True:
        try:
            qty = float(input(text))
        except ValueError:
            pass
        if qty > 0:
            return qty
        raise ValueError("Must be valid positive integer.")


def cal(unit, qty, price_p_unit, find):
    if unit == "oz" or unit == "lb" or unit == "coin":
        return float(price_p_unit * qty)
    elif find in p_oz_asset:
        if unit == "g":
            return float(price_p_unit * qty / 28.349523125)
        elif unit == "kg":
            return float(price_p_unit * qty / 0.028349523125)
        else:
            return float((price_p_unit * qty / 28.349523125) * 3.75)
    elif find in p_lb_asset:
        if unit == "g":
            return float(price_p_unit * qty / 453.59237)
        if unit == "kg":
            return float(price_p_unit * qty / 0.45359237)
        else:
            return float((price_p_unit * qty / 0.45359237) * 3.75)
    # 1ji = 3.75g


if __name__ == "__main__":
    main()
