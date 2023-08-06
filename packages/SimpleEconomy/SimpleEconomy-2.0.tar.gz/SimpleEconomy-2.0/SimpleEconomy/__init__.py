import aiohttp
import asyncio
from aiohttp_requests import requests
from operator import itemgetter


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Seco:

    def __init__(self, client, token, project, def_bal: int = 0, def_bank: int = 0, logs=True,checkup_=False):
        self.token = token
        self.project = project
        self.queue = []
        self.cache = []
        self.info = {}
        self.def_bal = def_bal
        self.def_bank = def_bank
        self.logs = logs
        self.checkup_=checkup_
        client.loop.create_task(self.queue_loop())

    async def checkup(self):
        async def checkup(self):
            try:
                r = await requests.get(f"https://simpleco.xyz/data/{self.project}", headers={"Auth": self.token})
                data = await r.json()
                self.cache = data["data"]
                self.info = data["info"]
                print("check")
            except Exception as E:
                if self.logs:
                    print(E)
                    print("Failed to do regular checkup")
                    print(
                        "Please check at your project name spelling and api token before asking for help!")

        await checkup(self)
    async def queue_loop(self):
        await self.setup()
       
        # Needed functions

        async def insert_one(data, table):
            try:
                r = await requests.post(f"https://simpleco.xyz/database", headers={"Auth": self.token}, json={"project": self.project, "table": table, "action": "INSERT", "values": data})
                data = await r.json()
                if data.get("ERROR", False) == False:
                    if self.logs:
                        print("Inserted user")
                elif data["ERROR"] == None:
                    if self.logs:
                        print("Inserted user")
                else:

                    print(data["ERROR"])
            except Exception as E:
                print(E)

        async def update_one(data, table, update):
            try:
                r = await requests.post(f"https://simpleco.xyz/database", headers={"Auth": self.token}, json={"project": self.project, "table": table, "action": "UPDATE", "values": data, "update": update})
                data = await r.json()
                if data.get("ERROR", False) == False:
                    if self.logs:
                        print("UPDATED user")
                elif data["ERROR"] == None:
                    if self.logs:
                        print("UPDATED user")
                else:

                    print(data["ERROR"])
            except Exception as E:
                print(E)

        async def delete(data, table):
            try:
                r = await requests.post(f"https://simpleco.xyz/database", headers={"Auth": self.token}, json={"project": self.project, "table": table, "action": "DELETE", "values": data})
                data = await r.json()
                if data.get("ERROR", False) == False:
                    if self.logs:
                        print("Tried deleting all users with specificed values!")
                elif data["ERROR"] == None:
                    if self.logs:
                        print("Tried deleting all users with specificed values!")
                else:

                    print(data["ERROR"])
            except Exception as E:
                print(E)
        count=0
        while True:
            if self.checkup_:
                if count == 11:
                    await self.checkup()
                    count=0
                count+=1
            if len(self.queue) != 0:
                for item in self.queue:
                    self.queue.remove(item)
                    for i, value in item.items():
                        if i == "INSERT":
                            await insert_one(value["data"]["in"], value["data"]["table"])
                        elif i == "UPDATE":
                            await update_one(value["data"]["in"], value["data"]["table"], value["data"]["update"])
                        elif i == "DELETE":
                            await delete(value["data"]["in"], value["data"]["table"])
            await asyncio.sleep(0.1)

    async def setup(self):
        try:
            r = await requests.get(f"https://simpleco.xyz/data/{self.project}", headers={"Auth": self.token})
            data = await r.json()
            self.cache = data["data"]
            self.info = data["info"]
            if self.logs:
                print("Setup succesful.")
        except Exception as E:
            print(E)
            print("Failed to setup database!")
            print(
                "Please check at your project name spelling and api token before asking for help!")

    async def get_balance(self, userid: int):
        """
        Gets balance by users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bal)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bal)
        return int(search["balance"])

    async def get_bank(self, userid: int):
        """
        Gets bank by users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bank)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bank)
        return int(search["bank"])

    async def add_balance(self, userid: int, amount: int):
        """
        Adds balance to users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal+amount, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal + amount), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bal+amount)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal+amount, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal + amount), "bank": str(self.def_bank), "userid": str(userid)})
            return int(self.def_bal+amount)

        self.cache["users"].remove(search)
        self.cache["users"].append({"balance": str(int(
            search["balance"])+amount), "bank": str(int(search["bank"])), "userid": str(userid)})

        self.queue.append({"UPDATE": {"data": {"in": {"userid": userid}, "table": "users", "update": {
                          "balance": int(search["balance"])+amount}}}})
        return int(search["balance"])+amount

    async def add_bank(self, userid: int, amount: int):
        """
        Adds balance to users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {"balance": self.def_bal,
                                                          "bank": self.def_bank+amount, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(self.def_bal), "bank": str(
                self.def_bank + amount), "userid": str(userid)})
            print("K")
            return int(self.def_bank+amount)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {"balance": self.def_bal,
                                                          "bank": self.def_bank + amount, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(self.def_bal), "bank": str(
                self.def_bank + amount), "userid": str(userid)})
            return int(self.def_bank+amount)

        self.cache["users"].remove(search)
        self.cache["users"].append({"balance": str(int(search["balance"])), "bank": str(
            int(search["bank"]) + amount), "userid": str(userid)})

        self.queue.append({"UPDATE": {"data": {"in": {"userid": userid},
                                               "table": "users", "update": {"bank": int(search["bank"])+amount}}}})
        return int(search["bank"])+amount

    async def remove_bank(self, userid: int, amount: int):
        """
        Adds balance to users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal-amount, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(self.def_bal), "bank": str(
                self.def_bank - amount), "userid": str(userid)})
            print("K")
            return int(self.def_bank-amount)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {"balance": self.def_bal,
                                                          "bank": self.def_bank - amount, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(self.def_bal), "bank": str(
                self.def_bank - amount), "userid": str(userid)})
            return int(self.def_bank-amount)

        self.cache["users"].remove(search)
        self.cache["users"].append({"balance": str(int(search["balance"])), "bank": str(
            int(search["bank"]) - amount), "userid": str(userid)})

        self.queue.append({"UPDATE": {"data": {"in": {"userid": userid},
                                               "table": "users", "update": {"bank": int(search["bank"])-amount}}}})
        return int(search["bank"])-amount

    async def remove_balance(self, userid: int, amount: int):
        """
        Adds balance to users id
        """
        if len(self.cache["users"]) == 0:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal-amount, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal - amount), "bank": str(self.def_bank), "userid": str(userid)})
            print("K")
            return int(self.def_bal+amount)
        search=None
        for user in self.cache["users"]:
            if user["userid"]==str(userid):
                search=user
                break
        if search == None:
            self.queue.append({"INSERT": {"data": {"in": {
                              "balance": self.def_bal-amount, "bank": self.def_bank, "userid": userid}, "table": "users"}}})
            self.cache["users"].append({"balance": str(
                self.def_bal-amount), "bank": str(self.def_bank), "userid": str(userid)})
            return int(self.def_bal-amount)

        self.cache["users"].remove(search)
        self.cache["users"].append({"balance": str(int(
            search["balance"])-amount), "bank": str(int(search["bank"])), "userid": str(userid)})

        self.queue.append({"UPDATE": {"data": {"in": {"userid": userid}, "table": "users", "update": {
                          "balance": int(search["balance"])-amount}}}})
        return int(search["balance"])-amount

    async def transfer_balance(self, userid: int, to: int, amount: int):
        if await self.get_balance(userid) >= amount and amount > 0:
            await self.add_balance(to, amount)
            await self.remove_balance(userid, amount)
            return True

    async def transfer_bank(self, userid: int, to: int, amount: int):
        if await self.get_bank(userid) >= amount and amount > 0:
            await self.add_bank(to, amount)
            await self.remove_bank(userid, amount)
            return True

    async def leaderboard(self, field: str = "balance", limit: int = 10, table: str = "users", values: dict = {}):
        try:
            r = await requests.post(f"https://simpleco.xyz/database", headers={"Auth": self.token}, json={"project": self.project, "table": table, "action": "TOP", "values": values, "sort": field, "limit": limit})
            data = await r.json()
            if data.get("ERROR", False) == False:
                if self.logs:
                    print("Got leaderboard")
                return data["DATA"]
            elif data["ERROR"] == None:
                if self.logs:
                    print("Got leaderboard")
                return data["DATA"]
            else:

                print(data["ERROR"])
        except Exception as E:
            print(E)

    async def get(self, table: str, **values):

        print(self.cache)
        if not self.info.get(table, False):
            raise Exception("No such table as provided!")
        for key, value in values.items():
            if key not in self.info[table].keys():
                raise Exception(
                    f"Value: {key} does not exist in our database! Check your field names and make sure to look at spelling!")
            else:
                if self.info[table][key] == "INTEGER":
                    if not RepresentsInt(value):
                        raise Exception(
                            f"Invalid value type for the field: {key} . That field requires an integer!")
        got = None
        for item in self.cache[table]:
            didnt_pass = False
            for key, value in values.items():
                if not item[key] == str(value):
                    didnt_pass = True
                    print("DIDNT")
            if didnt_pass == False:
                got = item
                break
        if got == None:
            return None
        ngot = {}
        for key, value in got.items():
            if self.info[table][key] == "INTEGER":
                ngot.update({key: int(value)})
            else:
                ngot.update({key: str(value)})
        return ngot

    async def insert(self, table: str, **values):
        if not self.info.get(table, False):
            raise Exception("No such table as provided!")
        for key, value in values.items():
            if key not in self.info[table].keys():
                raise Exception(
                    f"Value: {key} does not exist in our database! Check your field names and make sure to look at spelling!")
            else:
                if self.info[table][key] == "INTEGER":
                    if not RepresentsInt(value):
                        raise Exception(
                            f"Invalid value type for the field: {key} . That field requires an integer!")

        if not len(self.info[table].keys()) == len(values.keys()):
            raise Exception(
                f"For inserting you need to provide all database fields!")

        self.queue.append({"INSERT": {"data": {"in": values, "table": table}}})
        f_val = {}
        for key, value in values.items():
            f_val.update({key: str(value)})
        self.cache[table].append(f_val)

        return True

    async def update(self, table, update: dict, **values):
        if not self.info.get(table, False):
            raise Exception("No such table as provided!")
        for key, value in values.items():
            if key not in self.info[table].keys():
                raise Exception(
                    f"Value: {key} does not exist in our database! Check your field names and make sure to look at spelling!")
            else:
                if self.info[table][key] == "INTEGER":
                    if not RepresentsInt(value):
                        raise Exception(
                            f"Invalid value type for the field: {key} . That field requires an integer!")

        for key, value in update.items():
            if key not in self.info[table].keys():
                raise Exception(
                    f"Value: {key} does not exist in our database! Check your field names and make sure to look at spelling!")
            else:
                if self.info[table][key] == "INTEGER":
                    if not RepresentsInt(value):
                        raise Exception(
                            f"Invalid value type for the field: {key} . That field requires an integer!")

        got = None

        for item in self.cache[table]:
            didnt_pass = False
            for key, value in values.items():
                if not item[key] == str(value):
                    didnt_pass = True
            if didnt_pass == False:
                got = item
                break
        if got == None:
            return None
        ogot = got
        for key, value in update.items():
            got[key] = value
        self.cache[table].remove(ogot)
        self.cache[table].append(got)

        self.queue.append(
            {"UPDATE": {"data": {"in": values, "table": table, "update": update}}})

        return True

    async def delete(self, table, **values):
        if not self.info.get(table, False):
            raise Exception("No such table as provided!")
        for key, value in values.items():
            if key not in self.info[table].keys():
                raise Exception(
                    f"Value: {key} does not exist in our database! Check your field names and make sure to look at spelling!")
            else:
                if self.info[table][key] == "INTEGER":
                    if not RepresentsInt(value):
                        raise Exception(
                            f"Invalid value type for the field: {key} . That field requires an integer!")
        del_count = 0
        for item in self.cache[table]:
            passes = []
            for key, value in values.items():
                if item[key] == str(value):
                    passes.append(1)
            if len(passes) == len(values.keys()):
                self.cache[table].remove(item)
                del_count += 1
        if del_count == 0:
            print("0  to delete!!!")
            return False
        self.queue.append({"DELETE": {"data": {"in": values, "table": table}}})
        return True
