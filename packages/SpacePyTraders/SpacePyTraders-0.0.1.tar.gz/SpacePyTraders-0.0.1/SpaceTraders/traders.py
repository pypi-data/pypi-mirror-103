from SpaceTraders import core, trackers, db_handler
import time
import datetime
import math
import pandas as pd
import logging
from .config.secrets import get_token

URL = "https://api.spacetraders.io/"
TOKEN = get_token()
GAME = core.Game(TOKEN)
username = "JimHawkins"

user = core.get_user(TOKEN, username)

# Colours
R  = '\033[31m' # red
G  = '\033[32m' # green
W  = '\033[0m'  # white (normal)

def trading_run(ship, destination):
    print(R+"Making a trading run with {}. Flying to {}".format(ship.id, destination)+W)
    # Fill up
    if ship.get_fuel_level() < 20:
      print(G+"Filling up Fuel"+W)
      user.new_order(ship.id, "FUEL", 20 - ship.get_fuel_level())
      ship = user.get_ship(ship.id)
    
    # Buy Best Good
    what_to_buy = core.Market(GAME).what_should_I_buy(ship, destination)
    print(G+"Buying {} units of {} for {} with an expected profit of {}".\
      format(what_to_buy['units'], what_to_buy['symbol'], what_to_buy['total_cost'], what_to_buy['expected_profit'])+W)
    user.new_order(ship.id, what_to_buy['symbol'], what_to_buy['units'])
    ship = user.get_ship(ship.id)
    
    # Fly to destination
    user.fly(ship.id, destination, track=False)
    ship = user.get_ship(ship.id)

    # Sell goods
    order = user.sell_order(ship.id, what_to_buy['symbol'], what_to_buy['units'])
    print(G+"Sold {} units of {} at {} with a profit of {}".\
      format(what_to_buy['units'], what_to_buy['symbol'], order['order']['total'], order['order']['total']-what_to_buy['total_cost'])+W)
    ship = user.get_ship(ship.id)
    
    # Return the profit of the run
    return order['order']['total'] - what_to_buy['total_cost']

def find_optimum_trade_route(ship):
    # Get tracked markets and remove the current market
    all_tracker_locs = [ship.location for ship in user.get_ships(filter_by=[('manufacturer', 'Jackshaw')])]
    # remove current market of ship
    all_tracker_locs.remove(ship.location)

    # Get marketplace of ships current location - lessons calls to API
    ship_marketplace = GAME.locations[ship.location].marketplace()

    # Work out the best trade
    potential_trades = [core.Market(GAME).what_should_I_buy(ship, loc, ship_marketplace) for loc in all_tracker_locs]
    # Pair up loc with best trade
    pt_loc = list(zip(all_tracker_locs, potential_trades))
    # Return trade with Max expected profit
    return max(pt_loc, key=lambda d: d[1]['expected_profit']) 

def find_optimum_trade_routes(ship):
    # Get tracked markets and remove the current market
    all_tracker_locs = [ship.location for ship in user.get_ships(filter_by=[('manufacturer', 'Jackshaw')])]
    # remove current market of ship & the warp locations as they have no markets
    all_tracker_locs.remove(ship.location)
    if 'XV-OE-2-91' in all_tracker_locs:
      all_tracker_locs.remove('XV-OE-2-91')
    if 'OE-XV-91-2' in all_tracker_locs:
      all_tracker_locs.remove('OE-XV-91-2')

    # Get marketplace of ships current location - lessons calls to API
    ship_marketplace = GAME.locations[ship.location].marketplace()

    # Work out the best trades
    return [core.Market(GAME).what_should_I_buy(ship, loc, ship_marketplace) for loc in all_tracker_locs]

def any_dest_trading_run(ship):
  print(ship.location)
  # First sell any existing cargo
  if len(ship.cargo) > 0:
    if any(x['good'] != "FUEL" for x in ship.cargo):
      print(f"{R}Goods still left on ship that require selling{W}")
      cargo_to_sell = next(good for good in ship.cargo if good['good'] != "FUEL")
      if cargo_to_sell['quantity'] > 300:
        # Rounding up - how many order to make
        count = math.ceil(cargo_to_sell['quantity'] / 300)
        temp_units = cargo_to_sell['quantity']
        # Do buy order as many times as requried
        for i in range(count):
            if temp_units / 300 > 1:
                sell_order = user.sell_order(ship.id, cargo_to_sell['good'], 300)
                temp_units = temp_units - 300
            else:
                sell_order = user.sell_order(ship.id, cargo_to_sell['good'], temp_units)
      else:
        sell_order = user.sell_order(ship.id, cargo_to_sell['good'], cargo_to_sell['quantity'])
      print(f"{G}Sold {cargo_to_sell['quantity']} units of {cargo_to_sell['good']} for {sell_order['order']['total']}{W}")
      ship.update_cargo(sell_order['ship']['cargo'], sell_order['ship']['spaceAvailable'])

  did_buy_goods = False
  # Get the optimum trade routes - USES 9 API Calls
  trade_routes = find_optimum_trade_routes(ship)
  # Drop non-profitable trades
  trade_routes_profit = list(filter(lambda x: x['profit'] > 0, trade_routes))
  
  # Handle not profitable trades
  if len(trade_routes_profit) == 0:
    print("No Profitable Trades")
    # Calculate distance to closest location
    closet_location = ship.get_closest_location()
    flight_path = {"to": closet_location[0].symbol, "fuel_required": ship.calculate_fuel_usage(GAME.locations[ship.location], distance=closet_location[1])}
    logging.info(f"No profitable trade info: {flight_path}")
  else:
    flight_path = max(trade_routes_profit, key=lambda tr: tr['expected_profit'])
    if flight_path['total_cost'] > user.credits:
      print("Not enough money to do trade")
      # Calculate distance to closest location
      closet_location = ship.get_closest_location()
      flight_path = {"to": closet_location[0].symbol, "fuel_required": ship.calculate_fuel_usage(GAME.locations[ship.location], distance=closet_location[1])}
    else: 
      # Buy Good
      print(G+"Buying {} units of {} for {} with an expected profit of {}".\
          format(flight_path['units'], 
                flight_path['symbol'], 
                flight_path['total_cost'], 
                flight_path['expected_profit'])+W)
      
      # Handle cases where Grav III is buying more than 300 units - throws a server error otherwise
      if flight_path['units'] > 300:
        # Rounding up - how many order to make
        count = math.ceil(flight_path['units'] / 300)
        temp_units = flight_path['units']
        # Do buy order as many times as requried
        for i in range(count):
            if temp_units / 300 > 1:
                buy_order = user.new_order(ship.id, flight_path['symbol'], 300)
                temp_units = temp_units - 300
            else:
                buy_order = user.new_order(ship.id, flight_path['symbol'], temp_units)
      else:
        buy_order = user.new_order(ship.id, flight_path['symbol'], flight_path['units'])

      # Collate Data to Upload to Datebase
      data = [[datetime.datetime.now(), ship.location, flight_path['symbol'],
              flight_path['units'], flight_path['cost'], flight_path['total_cost'], 
              flight_path['profit'], flight_path['profit_per_volume'], flight_path['expected_profit'], 
              flight_path['to']]]
      columns = ['time', 'location', 'symbol', 'units', 'cost', 'total_cost', 'profit',
                'profit_per_volume', 'expected_profit', 'sell_location']
      db_handler.write_buy_order_to_db(pd.DataFrame(data, columns=columns))
      # Update Ship
      ship.update_cargo(buy_order['ship']['cargo'], buy_order['ship']['spaceAvailable'])
      did_buy_goods = True
  
  # Buy Fuel
  # Check if fuel order is required
  print(f"Current Fuel Level: {ship.get_fuel_level()}", ship.cargo)
  if flight_path['fuel_required'] - ship.get_fuel_level() > 0:
    fuel_order = user.new_order(ship.id, "FUEL", flight_path['fuel_required'] - ship.get_fuel_level())
    # Update Ship
    ship.update_cargo(fuel_order['ship']['cargo'], fuel_order['ship']['spaceAvailable'])

  # Fly
  flight = user.fly(ship.id, flight_path['to'], track=False)
  # Collate Data to Upload to Datebase
  to = GAME.locations[flight_path['to']]
  flightReason = "Trade" if did_buy_goods else "Relocating"
  try:
    data = [[datetime.datetime.now(), ship.location, flight_path['to'],
          flight['distance'], flight_path['fuel_required'], flight['fuelConsumed'], 
          flight['timeRemainingInSeconds'], ship.manufacturer, ship.type, ship.speed, 
          ship.maxCargo - ship.spaceAvailable, ship.plating, ship.weapons, flightReason]]
  except Exception:
    logging.exception(f"Something went wrong flight: {str(flight)}, to: {to}, flight_path: {str(flight_path)}, ship: {ship}")
  columns = ['time', 'from_loc', 'to_loc', 'distance', 'estimated_fuel_required', 'actual_fuel_required',
              'time_taken', 'ship_manufactorer', 'ship_type', 'speed', 'totalVolume', 'plating', 'weapons', 
              'flight_reason']
  db_handler.write_flight_path_to_db(pd.DataFrame(data, columns=columns))
  # Update Ship
  ship.update_location(GAME.location(flight_path['to']).x, GAME.location(flight_path['to']).y, flight_path['to'])

  if did_buy_goods:
    # Sell Order
    # Handle cases where Grav III is buying more than 300 units - throws a server error otherwise
    if flight_path['units'] > 300:
      # Rounding up - how many order to make
      count = math.ceil(flight_path['units'] / 300)
      temp_units = flight_path['units']
      # Do buy order as many times as requried
      for i in range(count):
          if temp_units / 300 > 1:
              sell_order = user.sell_order(ship.id, flight_path['symbol'], 300)
              temp_units = temp_units - 300
          else:
              sell_order = user.sell_order(ship.id, flight_path['symbol'], temp_units)
    else:
      sell_order = user.sell_order(ship.id, flight_path['symbol'], flight_path['units'])
    print(G+"Sold {} units of {} for {} with a profit of {}".\
        format(flight_path['units'], 
               flight_path['symbol'], 
               sell_order['order']['total'], 
               sell_order['order']['total'] - buy_order['order']['total'])+W)
    # Collate Data to Upload to Datebase
    data = [[datetime.datetime.now(), ship.location, flight_path['symbol'],
            flight_path['units'], flight_path['cost'], flight_path['total_cost'], 
            flight_path['expected_profit'], flight_path['from']]]
    columns = ['time', 'location', 'symbol', 'units', 'sell_price', 'total_sell_amount',
               'expected_profit', 'buy_location']
    db_handler.write_sell_order_to_db(pd.DataFrame(data, columns=columns))
    # Update Ship
    ship.update_cargo(sell_order['ship']['cargo'], sell_order['ship']['spaceAvailable'])
    return sell_order['order']['total'] - buy_order['order']['total']
  else:
    return 0

def do_trading_run(shipId, times):
  ship = user.get_ship(shipId)
  start = datetime.datetime.now()
  profit = []

  # Perform the trading runs
  for x in range(times):
    profit.append(any_dest_trading_run(ship))
    print(R+"Total money made so far: " + str(sum(profit))+W)
    now = datetime.datetime.now() - start
    print(R+"Time taken so far: " + str(now)+W)
    profit_per_hour = round( sum(profit) / (now.total_seconds() / 3600), 2)
    print(R+"Current profit per Hour: " + str(profit_per_hour)+W)

  # Display Results
  print("Total money made: " + str(sum(profit)))
  now = datetime.datetime.now() - start
  print("Time taken: " + str(now))
  profit_per_hour = round( sum(profit) / (now.total_seconds() / 3600), 2)
  print("Profit per Hour: " + str(profit_per_hour))

if __name__ == "__main__":
  do_trading_run('cknxw0jyz10305031bs6rdlv226q', 1)

  