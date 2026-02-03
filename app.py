from flask import Flask, request, jsonify
from netflixgc_spider import NetflixGCSpider
import os
import urllib.parse

app = Flask(__name__)
spider = NetflixGCSpider()

def load_config():
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), 'config.env')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

config = load_config()

TVBOX_HOST = config.get('TVBOX_HOST', '0.0.0.0')
TVBOX_PORT = int(config.get('TVBOX_PORT', 8000))
TVBOX_DEBUG = config.get('TVBOX_DEBUG', 'false').lower() == 'true'

def fix_garbled_keyword(keyword):
    """修复乱码关键词 - UTF-8字节被误读为latin-1"""
    if not keyword:
        return keyword
    try:
        if 'é±¿' in keyword or '鱿' not in keyword:
            return keyword.encode('latin-1').decode('utf-8', errors='ignore')
    except:
        pass
    return keyword

@app.route('/api', methods=['GET'])
@app.route('/', methods=['GET'])
def api():
    action = request.args.get('ac', request.args.get('action', ''))
    
    if action == 'list' or action == 'home':
        home_data = spider.get_home_data()
        
        result = {
            "class": [{"type_id": c["type_id"], "type_name": c["type_name"]} for c in home_data.get("categories", [])],
            "list": {}
        }
        
        banners = home_data.get("banners", [])
        if banners:
            result["banner"] = [
                {
                    "vod_id": i,
                    "vod_name": banner.get("link", ""),
                    "vod_pic": banner.get("pic", "")
                }
                for i, banner in enumerate(banners[:5])
            ]
        
        videos = home_data.get("latest_videos", [])
        result["list"]["首页"] = [
            {
                "vod_id": i,
                "vod_name": vod.get("title", ""),
                "vod_pic": vod.get("cover", ""),
                "vod_remarks": ""
            }
            for i, vod in enumerate(videos[:20])
        ]
        
        return jsonify(result)
    
    elif action == 'category':
        categories = spider.get_category_list()
        categories_data = [
            {"type_id": c["type_id"], "type_name": c["type_name"]}
            for c in categories
        ]
        return jsonify({"list": categories_data})
    
    elif action == 'videolist' or action == 'detail':
        detail_url = request.args.get('url', request.args.get('detail_url', ''))
        if detail_url:
            detail = spider.get_video_detail(detail_url)
            if detail:
                result = {
                    "vod_name": detail.get('title', ''),
                    "vod_pic": detail.get('cover', ''),
                    "vod_remarks": "",
                    "vod_actor": detail.get('actor', ''),
                    "vod_director": detail.get('director', ''),
                    "vod_year": detail.get('year', ''),
                    "vod_area": detail.get('area', ''),
                    "vod_type": detail.get('type', ''),
                    "vod_content": "",
                    "vod_play_from": "奈飞工厂",
                    "vod_play_url": "#".join([f"{play['title']}$${play['url']}" for play in detail.get('play_episodes', [])])
                }
                return jsonify(result)
        return jsonify({})
    
    elif action == 'search' or action == '':
        keyword = request.args.get('wd', request.args.get('search', ''))
        
        if not keyword:
            return jsonify({"list": []})
        
        keyword = fix_garbled_keyword(keyword)
        
        search_results = spider.search_vod(keyword)
        result = {
            "list": [
                {
                    "vod_id": i,
                    "vod_name": vod['title'],
                    "vod_pic": vod['cover'],
                    "vod_remarks": ""
                }
                for i, vod in enumerate(search_results)
            ]
        }
        return jsonify(result)
    
    else:
        return jsonify({})

@app.route('/version')
def version():
    return jsonify({
        "version": "1.0.0",
        "name": "TVBox NetflixGC API",
        "status": "running"
    })

if __name__ == '__main__':
    app.run(host=TVBOX_HOST, port=TVBOX_PORT, debug=TVBOX_DEBUG)
