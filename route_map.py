#!/usr/bin/env python3
"""1枚PDF用のルート図。courses.json の stops を順に線で結んだ PNG を img/route-<id>.png に書く。
Googleの埋め込みiframeはPDFに写らないので静止画にする。座標は courses.json の "ll" に保存（無ければ Nominatim で引いて保存）。
使い方: python3 route_map.py && python3 build.py"""
import json, math, io, time, urllib.request, urllib.parse, os
from PIL import Image, ImageDraw, ImageFont

W, HMIN, HMAX = 1200, 400, 500   # 出力px。高さは地点の広がりに合わせて HMIN〜HMAX
TILE = 256                # OSM標準タイル
UA = {'User-Agent': 'yukitchy-course-map/1.0'}
RED = (230, 0, 18)

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read()

def geocode(q):
    r = json.loads(get('https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=jp&q=' + urllib.parse.quote(q)))
    time.sleep(1.1)  # Nominatim の利用規約: 1秒1件
    if not r: raise SystemExit(f'座標が引けない: {q} → courses.json の "ll" に [lat, lon] を手で入れる')
    return [round(float(r[0]['lat']), 5), round(float(r[0]['lon']), 5)]

def px(lat, lon, z):
    n = 2 ** z * TILE
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n

def font(size):
    for f in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/System/Library/Fonts/Helvetica.ttc'):
        if os.path.exists(f): return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def draw(c):
    ll = c['ll']
    pad = 45
    z = 17
    while z > 10:  # 全地点が余白込みで収まる最大ズーム
        xs, ys = zip(*(px(a, b, z) for a, b in ll))
        if max(xs) - min(xs) <= W - 2 * pad and max(ys) - min(ys) <= HMAX - 2 * pad: break
        z -= 1
    xs, ys = zip(*(px(a, b, z) for a, b in ll))
    H = int(max(HMIN, max(ys) - min(ys) + 2 * pad))
    ox, oy = (max(xs) + min(xs)) / 2 - W / 2, (max(ys) + min(ys)) / 2 - H / 2
    img = Image.new('RGB', (W, H), (240, 238, 232))
    for tx in range(int(ox // TILE), int((ox + W) // TILE) + 1):
        for ty in range(int(oy // TILE), int((oy + H) // TILE) + 1):
            t = Image.open(io.BytesIO(get(f'https://tile.openstreetmap.org/{z}/{tx}/{ty}.png'))).convert('RGB')
            img.paste(t, (int(tx * TILE - ox), int(ty * TILE - oy)))
    d = ImageDraw.Draw(img)
    P = [(x - ox, y - oy) for x, y in zip(xs, ys)]
    d.line(P, fill=RED, width=6, joint='curve')
    f, fs = font(24), font(18)
    r = 19
    groups = []  # 近すぎて重なる連続地点は1つのピン「4–7」にまとめる
    for i, p in enumerate(P):
        if groups and math.dist(p, P[groups[-1][0]]) < 2.2 * r: groups[-1].append(i)
        else: groups.append([i])
    for g in groups:
        x, y = P[g[0]]
        t = str(g[0] + 1) if len(g) == 1 else f'{g[0] + 1}–{g[-1] + 1}'
        w = max(r, d.textlength(t, font=f) / 2 + 10)
        d.rounded_rectangle((x - w, y - r, x + w, y + r), radius=r, fill=RED, outline='white', width=4)
        d.text((x, y), t, font=f, fill='white', anchor='mm')
    note = '© OpenStreetMap contributors'
    d.rectangle((W - 260, H - 28, W, H), fill=(255, 255, 255))
    d.text((W - 8, H - 14), note, font=fs, fill=(90, 90, 90), anchor='rm')
    os.makedirs('img', exist_ok=True)
    img.save(f'img/route-{c["id"]}.png', optimize=True)
    print(f'img/route-{c["id"]}.png  z={z}  stops={len(P)}')

if __name__ == '__main__':
    C = json.load(open('courses.json'))
    changed = False
    for c in C:
        if not c.get('stops'): continue
        if len(c.get('ll', [])) != len(c['stops']):
            c['ll'] = [geocode(s) for s in c['stops']]; changed = True
        draw(c)
    if changed: json.dump(C, open('courses.json', 'w'), ensure_ascii=False, indent=1)
