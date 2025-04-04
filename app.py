from flask import Flask, request, jsonify, render_template
import requests
import browser_cookie3
import base64



app = Flask(__name__)

BASE_URL = "https://www.1024terabox.com/api"


def get_brave_cookies(domain):
    try:
        cookies = list(browser_cookie3.brave(domain_name=domain))
        if not cookies:
            return jsonify(
                {
                    "error": "No cookies"
                }
            ), 403

        # Convert cookies to a dictionary format for requests
        cookies_dict = {cookie.name: cookie.value for cookie in cookies}
        return cookies_dict
    except Exception as e:
        print("Error fetching cookies:", str(e))
        return None

def make_request(endpoint, domain, params, mode="page"):
    cookies = get_brave_cookies(domain)

    if not cookies:
        return {"error": "No cookies found"}

    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not:A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }

    if mode == "page":
        headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Cache-Control": "max-age=0",
            "Host": "www.1024terabox.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        })
    elif mode == "xhr":
        headers.update({
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.1024terabox.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.1024terabox.com/main?category=all",
            "Sec-Gpc": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
        })
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, cookies=cookies, params=params, headers=headers)
    print(response.url)
    try:
        return response.json()
    except Exception:
        return {"error": "Invalid JSON response", "raw": response.text}


def sign2(j: str, r: str) -> bytes:
    a = [ord(j[i % len(j)]) for i in range(256)]
    p = list(range(256))

    u = 0
    for q in range(256):
        u = (u + p[q] + a[q]) % 256
        p[q], p[u] = p[u], p[q]

    i = u = 0
    o = bytearray()
    for q in range(len(r)):
        i = (i + 1) % 256
        u = (u + p[i]) % 256
        p[i], p[u] = p[u], p[i]
        k = p[(p[i] + p[u]) % 256]
        o.append(ord(r[q]) ^ k)  # Use bytes instead of str

    return bytes(o)  # Ensure output is bytes



@app.route("/files", methods=["GET"])
def list_files():
    domain = "1024terabox.com"
    params = request.args.to_dict()
    response = make_request("list", domain, params).get("list", f"An error occurred!")
    keys_to_remove = ["category", "extent_int2", "extent_tinyint7", "extent_tinyint9","from_type", "local_ctime", "local_mtime", "oper_id", "owner_id", "owner_type", "pl","play_forbid", "real_category", "server_atime", "server_ctime", "server_mtime", "share", "tkbind_id", "unlist","wpfile"]
    for eachkey in keys_to_remove:
        for eachitem in response:
            eachitem.pop(eachkey)
    return jsonify(response)


@app.route("/quota", methods=["GET"])
def quota():
    domain = "1024terabox.com"
    params = request.args.to_dict()
    return jsonify(make_request("quota", domain, params))


@app.route('/download', methods=['GET'])
def start_download():

    domain = "1024terabox.com"
    params = request.args.to_dict()
    response = make_request("home/info", domain, params)
    data = response.get("data", {})

    if not data:
        return jsonify({"error": "Missing or invalid response from home/info"}), 400


    sign1 = data["sign1"]
    sign3 = data["sign3"]
    timestamp = data["timestamp"]

    raw_sign = sign2(sign3, sign1)
    base64_sign = base64.b64encode(raw_sign).decode() # Ensure correct byte encoding

    fidlist = params.get("id", "")
    downparam = {
        "fidlist": fidlist, 
        "type":"dlink",
        "vip": 2, 
        "sign": base64_sign,
        "timestamp": timestamp,
        "need_speed": 0,
    }
    downlink = make_request("download", domain, downparam, mode="xhr")
    return downlink


if __name__ == "__main__":
    app.run(debug=True)


