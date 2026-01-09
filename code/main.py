from flask import Flask, request, jsonify , abort
from threading import Thread, Lock
import time, os, json
import random

# Độ Dài Cuỗi Random 10 => 20 ký tự (*2)
lenght_random = 10

app = Flask(__name__)


class Save:
    def __init__(self, file_path: str, time_save: int = 20):
        "time_save : default 60s"

        if not os.path.exists(file_path):
            pointer = open(file_path, "w")
            pointer.close()

        self.file_path = file_path
        self.time_save = time_save

        self.data = self.read_json()

        self.update = {}
        self.tokens = []

        self.Lock_Update = Lock()
        self.Lock_Remove = Lock()
        Thread(target=self._update, daemon=True).start()

    def upload(self, data: dict):
        with self.Lock_Update:
            for key , value in data.items():
                if key not in self.data:
                    self.data[key] = value
                    self.write_json()
                else:
                    self.update.update(data)

    def remove_token(self, token: str):
        with self.Lock_Remove:
            self.tokens.append(token)

    def _update(self):
        while True:
            self.data = self.read_json()
            with self.Lock_Update:
                if self.update:
                    if isinstance(self.data , dict):
                        self.data.update(self.update)
                    elif isinstance(self.data , list):
                        self.data.append(self.update)

                    self.write_json()

            with self.Lock_Remove:
                if self.tokens:
                    for token in self.tokens:
                        try:
                            del self.data[token]
                        except:
                            pass
                    self.write_json()

            self.update = {}
            self.tokens = []

            time.sleep(self.time_save)

    def read_json(self) -> dict:
        try:
            return json.loads(open(self.file_path, "r").read())
        except:
            return {}

    def write_json(self) -> dict:
        try:
            open(self.file_path, "w").write(json.dumps(self.data, indent=4))
        except:
            ...


def get_value(data: dict):
    while True:
        value = random.randbytes(lenght_random)
        if value not in data:
            return value.hex()


Cdata_user = Save("data_user.json")  # Class Data User
Cdata_mod = Save("data_mod.json")  # Class Data Mod


# ========== LOG API ==========


def isBan():
    return jsonify({"message": "You have been banned"}), 403


# ========== ACCOUNT API ==========


@app.route("/<token>/login", methods=["GET"])
def login(token):

    if token not in Cdata_user.data:
        data_user_default = {
            "username": token,
            "uid": token,
            "avatar": "",
            "name": f"User {token}",
            "coin": 0,
            "isMe": True,
            "isBan": False,
        }

        Cdata_user.upload({token: data_user_default})
        return jsonify(data_user_default)

    else:
        print(Cdata_user.data[token])
        return jsonify(Cdata_user.data[token])


@app.route("/<token>/remove", methods=["GET"])
def remove_account(token):
    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

        Cdata_user.remove_token(token)
        return jsonify({"message": "Delete Account Done !"})

    return jsonify({"error": "Account not found"}), 404


@app.route("/<token>/getInfosFromUid", methods=["GET"])
def getInfosFromUid(token):
    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()


        setting = Cdata_user.data[token]

        return jsonify(
            {"data": {"username": setting["username"], "avatar": setting["avatar"]}}
        )

    return jsonify({"error": "Account Not Found"}), 404


@app.route("/<token>/settings", methods=["POST"])
def settings(token):
    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()


        setting = Cdata_user.data[token]
        setting["avatar"] = request.args.get("avatar", type=str)
        setting["name"] = request.args.get("name", type=str)
        Cdata_user.upload({token: setting})
        return jsonify({"message": "Upload Done !"})

    return jsonify({"error": "Account Not Found"}), 404


# ========== MOD API ==========


@app.route("/<token>/mod/upmod", methods=["POST"])
def upmod(token):
    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

    try:
        uid = get_value(Cdata_mod.data)
        data = {
            "uid": uid,
            "uidUser": token,
            "name": request.args.get("name", type=str),
            "avatar": request.args.get("avatar", type=str),
            "linkjotpkg": request.args.get("linkjotpkg", type=str),
            "description": request.args.get("description", type=str),
            "shortenedlink": request.args.get("shortenedlink", type=str),
            "cointPassLink": request.args.get("cointPassLink", type=str),
            "disabled": False,
        }

        Cdata_mod.upload({uid : data})

        return jsonify({"message": "Mod uploaded", "uid": f"{uid}"}), 201

    except Exception as e:
        return jsonify({"error": f"{e}"}), 415


@app.route(f"/<token>/mod/remove", methods=["POST"])
def remove_mod(token):

    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

    uid = request.args.get("uid")
    if uid in Cdata_mod.data:
        del Cdata_mod.data[uid]
        return jsonify({"message": f"Mod {uid} removed"})

    return jsonify({"error": "Mod not found"}), 404


@app.route(f"/<token>/mod/disable", methods=["POST"])
def disable_mod(token):

    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

    uid = request.args.get("uid")
    if uid in Cdata_mod.data:
        block_data = Cdata_mod.data[uid]
        block_data["disabled"] = True

        Cdata_mod.upload({uid : block_data})

        return jsonify({"message": f"Mod {uid} disabled"})

    return jsonify({"error": "Mod not found"}), 404


@app.route(f"/<token>/mod/enable", methods=["POST"])
def enable_mod(token):

    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

    uid = request.args.get("uid")
    if uid in Cdata_mod.data:
        block_data = Cdata_mod.data[uid]
        block_data["disabled"] = False

        Cdata_mod.upload({uid : block_data})

        return jsonify({"message": f"Mod {uid} enabled"})

    return jsonify({"error": "Mod not found"}), 404


@app.route(f"/<token>/mod/update", methods=["POST"])
def update_mod(token):

    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()

    uid = request.args.get("uid")
    data = request.json
    if uid in Cdata_mod.data:
        Cdata_mod.data[uid].update(data)
        return jsonify({"message": f"Mod {uid} updated", "data": Cdata_mod.data[uid]})

    return jsonify({"error": "Mod not found"}), 404


@app.route("/<token>/mod/get", methods=["GET"])
def get_mods(token):

    if token in Cdata_user.data:
        if Cdata_user.data[token]["isBan"]:
            return isBan()
    
    data_mod = []
    for uid , block_data in Cdata_mod.data.items():
        data_mod.append(block_data)

    return jsonify({"data": data_mod})


# ========== MAIN ==========

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in {"127.0.0.1", "192.168.1.11"}:
        abort(403)

app.run(debug = True)