import json
import requests

def get_name():
    global ign
    global player_data
    ign = input("Whats your minecraft name?: ")
    try:
        print("Getting player data...")
        player_data = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{ign}').json()["profiles"]
        # minion_data = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{ign}').json()["profiles"]["44b97cf8-930e-41e3-b06e-a349503b543f"]["data"]["minions"]["minions"]
        # with open('data.json', 'w') as data_file:
        #     json.dump(minion_data, data_file, indent=4)
        print("Successful!")
    except:
        print("That minecraft name doesn't exist.")
        get_name()

def get_prices(type, n):
    # print("get_prices start")
    # print(minion_data[type]["minions"][n])
    # print("id: " + minion_data[type]["minions"][n]["id"])
    if not minion_data[type]["minions"][n]["tier"] == minion_data[type]["minions"][n]["maxTier"]:
        minion_id = minion_data[type]["minions"][n]["id"]
        for x in range(minion_data[type]["minions"][n]["maxTier"]):
            if not x+1 in minion_data[type]["minions"][n]["tiers"] or minion_data[type]["minions"][n]["tiers"] == []:
                # print(f"x+1: {x+1}")
                try:
                    # print("non tier 12")
                    minion_tier_recipe = requests.get(f"https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/{minion_id}_GENERATOR_{x+1}.json").json()["recipe"]
                    price = price_recipe(minion_tier_recipe, 0)
                except KeyError: # if 12 tier does not have a recipe
                    # print("tier 12")
                    if minion_id in tony:
                        price = shop_price(tony_shop, minion_id, False, 0, 1)
                    if minion_id in bulvar:
                        price = shop_price(bulvar_shop, minion_id, True, 0, 1)
                    if minion_id in hilda:
                        if not minion_id == "REVENANT":
                            price = shop_price(hilda_shop, minion_id, True, 2, 1)
                        else:
                            price = shop_price(bartender_shop, minion_id, True, 0, 2)
                    if minion_id in einary:
                        # print("einary!")
                        price = shop_price(einary_shop, minion_id, True, 2, 3)
                # print(f"price: {price}")
                # print(f"{x+1} no")
                prices.append({"minion":minion_data[type]["minions"][n]["name"],"price":price,"tier":x+1})
        minions.append(minion_id)
        # print("get_prices end")
    try:
        get_prices(type, n+1)
    except Exception as e:
        # print(f"error in get_prices: {e}")
        try:
            # print(minion_types[minion_types.index(type)+1])
            get_prices(minion_types[minion_types.index(type)+1], 0)
        except:
            pass

def price_recipe(recipe, add): # add is meant to be for 12th tier as you also normally need to buy it with coins
        # print("price_recipe start")
        # print(f"recipe: {recipe}")
        # print(f"add: {add}")
        price = 0
        secondary_minion_price = 0
        if not recipe["A1"] == "":
            price += int(bazaar_data['products'][recipe["A1"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["A1"].split(":")[1])
        if not recipe["A2"] == "":
            price += int(bazaar_data['products'][recipe["A2"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["A2"].split(":")[1])
        if not recipe["A3"] == "":
            price += int(bazaar_data['products'][recipe["A3"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["A3"].split(":")[1])
        if not recipe["B1"] == "":
            price += int(bazaar_data['products'][recipe["B1"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["B1"].split(":")[1])
        if not recipe["B3"] == "":
            price += int(bazaar_data['products'][recipe["B3"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["B3"].split(":")[1])
        if not recipe["C1"] == "":
            price += int(bazaar_data['products'][recipe["C1"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["C1"].split(":")[1])
        if not recipe["C2"] == "":
            try:
                price += int(bazaar_data['products'][recipe["C2"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["C2"].split(":")[1])
            except Exception as e:
                # print(f"error in price_recipe: {e}")
                if "GENERATOR" in str(e): # if it utilizes a minion in the "C2" slot calculate its value
                    whole_recipe = requests.get(f'https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/{e}.json'.replace("'", "")).json()["recipe"]
                    secondary_minion_price = price_recipe(whole_recipe, 0)
        if not recipe["C3"] == "":
            price += int(bazaar_data['products'][recipe["C3"].split(":")[0].replace("-", ":")]['quick_status']['buyPrice']) * int(recipe["C3"].split(":")[1])
        price += add
        price += secondary_minion_price
        # print("price_recipe end")
        return price

def shop_price(shop, id, coins_extra, money_index, items_index):
    price = 0
    for y in shop:
        if y["result"] == f"{id}_GENERATOR_12":
            minion_tier_recipe = y["cost"][items_index].split(":")
            try:
                price += int(bazaar_data['products'][minion_tier_recipe[0]]['quick_status']['buyPrice']) * int(minion_tier_recipe[1])
            except KeyError as e: # if items don't exist in bazaar like silver fangs
                recipe = requests.get(f"https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/{e}.json".replace("'", "")).json()["recipe"]
                recipe_price = price_recipe(recipe, 0)
                price += int(recipe_price) * int(minion_tier_recipe[1])
            if coins_extra == True:
                add = y["cost"][money_index].split(":")
                price += int(add[1])
            return price
        
def sort(e):
    return e['price']

def get_profiles(data):
    profiles = []
    select = 0
    global minion_data
    profiles = [value["cute_name"] for value in data.values()]
    print("Select profile:")
    x = 0
    for i in profiles:
        print(f"[{x}] {i}")
        x += 1
    select = int(input())
    if select >= len(profiles) or select <= -1:
        print("You must select an option from the list.")
        get_profiles(data)
    else:
        key = None
        for key_, value_ in data.items():
            if value_["cute_name"] == profiles[select]:
                key = key_
                break
        # print(key)
        minion_data = data[key]["data"]["minions"]["minions"]

if __name__ == "__main__":
    get_name()
    get_profiles(player_data)
    print("Getting bazaar data...")
    bazaar_data = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar').json()
    print("Successful!")
    minion_types = ["farming","mining","combat","foraging","fishing"]
    prices = []
    minions = []
    print("Loading shops...")
    tony_shop = requests.get("https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/TONY_SHOP_NPC.json").json()["recipes"]
    bulvar_shop = requests.get("https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/BULVAR_NPC.json").json()["recipes"]
    hilda_shop = requests.get("https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/HILDA_NPC.json").json()["recipes"]
    bartender_shop = requests.get("https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/BARTENDER_NPC.json").json()["recipes"]
    einary_shop = requests.get("https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/EINARY_NPC.json").json()["recipes"]
    print("Successful!")
    print("Getting minion's tiers upgrades (might take a bit)...")
    hilda = ["GHAST","QUARTZ","GLOWSTONE","BLAZE","MAGMA_CUBE","MYCELIUM"]
    tony = ["COCOA","PUMPKIN","CHICKEN","MUSHROOM","CACTUS","PIG","WHEAT","COW","SUGAR_CANE","MELON","NETHER_WART","CARROT","POTATO","SHEEP","RABBIT"]
    bulvar = ["COBBLESTONE","OBSIDIAN","COAL","IRON","GOLD","DIAMOND","LAPIS","EMERALD","REDSTONE","MITHRIL","HARD_STONE"]
    einary = ["ICE","SNOW"]
    get_prices(minion_types[0], 0)
    print("Successful!")
    # print(prices)
    print("Sorting prices...")
    prices.sort(key=sort)
    print("Successful!")
    if prices == []:
        print("Wow, you maxed all your minions, congrats!")
    else:
        for i in prices:
            print(f"{i['minion']} minion tier {i['tier']} costs: " "{:,}".format(i['price']))
    input("Press anything to exit...")
    