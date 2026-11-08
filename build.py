#!/usr/bin/env python3
"""Darren, Mon Nov 9: one-route map-led scroll story (same type as patrick-tokyo-day).
python3 build.py -> index.html   (CSS in style.css, map code in map.js)"""
import json

gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
def links(*ls): return '<ul class="links">' + ''.join('<li>' + A(u, t) + '</li>' for t, u in ls) + '</ul>'
def pts(*ps): return '<ul class="pts">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in ps) + '</ul>'
def nums(*ns): return '<dl class="nums">' + ''.join(f'<div><dt>{a}</dt><dd class="n">{b}</dd><dd class="s">{c}</dd></div>' for a, b, c in ns) + '</dl>'
def ph(src, alt): return f'<div class="ph"><img src="{src}" alt="{alt}"></div>'
def ph2(*ims): return '<div class="ph2">' + ''.join(f'<img src="{s}" alt="{a}">' for s, a in ims) + '</div>'

LINE = dict(J=('JR Sobu Rapid Line', '#0067c0'), Y=('Yurakucho Line', '#d7c447'))
def ln(k): return f'<span class="ln" style="--c:{LINE[k][1]}">{k}</span>{LINE[k][0]}'
def nxt(*rows): return '<div class="next"><p class="nl">Next</p>' + ''.join(f'<p>{r}</p>' for r in rows) + '</div>'

# lat, lon, full name, short label, label side, time
P = [None,
     (35.6969, 139.8143, 'Excelsior Caffé, Kinshicho Station', 'Excelsior', 'r', '9:00'),
     (35.6767, 139.7634, 'MAPPA EXPO, Tokyo International Forum', 'MAPPA EXPO', 'r', '10:00'),
     (35.6752, 139.7631, 'Lunch near Yurakucho', 'Lunch', 'l', '12:00'),
     (35.7303, 139.7149, 'Animate and the shops, Ikebukuro', 'Animate', 'l', '14:00'),
     (35.7312, 139.7157, 'Signing, Animate 8F Space Galleria', 'Signing', 'r', '15:45')]
LI = -1
LUNCH_JS = []

TT = [('9:00', 'Excelsior Caffé, Kinshicho'), ('9:15', 'JR Sobu Rapid Line to Tokyo'), ('10:00', 'MAPPA EXPO'),
      ('12:00', 'Lunch near Yurakucho'), ('13:15', 'Yurakucho Line to Ikebukuro'), ('14:00', 'Animate and the shops'),
      ('15:45', 'Signing, Space Galleria 8F'), ('17:30', 'Done, in Ikebukuro')]
tt = ''.join(f'<tr class="st-plain"><td class="v">{t}</td><td><span class="k">{k}</span></td></tr>' for t, k in TT)

def step(i, h, body):
    t = P[i][5]
    return f'<article class="step" data-i="{i}"><p class="no"><i>{i}</i>{t}</p><h2>{h}</h2>{body}</article>'

S = []
S.append('<article class="step" data-i="0"><p class="no"><i>0</i>The whole day</p><h2>Monday, <span class="l2">9:00 to <em>17:30</em></span></h2>'
         '<p class="lead">MAPPA EXPO in the morning at Yurakucho, lunch, then Ikebukuro for the Kaoruhana Rin to Saku 5th anniversary exhibition and the Mikami Saka signing. Entry to the signing is at 16:00.</p>'
         f'<div class="tt"><p class="cap">The day</p><table>{tt}</table></div>'
         + pts(('Keep in mind', 'Times are approximate. The exhibition closes at 17:00 on its last day and the last entry is 16:30, so we are at Space Galleria before 16:00.'))
         + links(('Open the whole route in Google Maps', 'https://www.google.com/maps/dir/?api=1&origin=Excelsior+Caffe+Kinshicho+Station&destination=Animate+Ikebukuro+Main+Store&waypoints=Tokyo+International+Forum&travelmode=transit'))
         + '</article>')
S.append(step(1, 'We meet at <em>Excelsior Caffé</em>',
              '<p class="lead">Excelsior Caffé is right in front of Kinshicho Station, near your Airbnb. I am there from 9:00. A coffee first, then we go.</p>'
              + nums(('Time', '9:00', 'Monday, November 9'), ('Finish', '17:30', 'Ikebukuro'))
              + links(('Excelsior Caffé on Google Maps', gm('Excelsior Caffe Kinshicho Station')))
              + nxt(f'{ln("J")} to Tokyo, about 10 min, then 10 min on foot')))
S.append(step(2, '<em>MAPPA EXPO</em> 15th Anniversary',
              ph('img/mappa-kv.jpg', 'MAPPA EXPO 15th Anniversary key visual') + ph2(('img/mappa-aot.jpg', 'Attack on Titan exhibit'), ('img/mappa-entrance.jpg', 'The 15th sign at the entrance'))
              + '<p class="lead">Fifteen years of MAPPA work: Chainsaw Man, Attack on Titan, Jujutsu Kaisen and more. It is in YURAKUCHO MUSEUM on B1F of Tokyo International Forum. Entry is from 10:00 and we give it about two hours.</p>'
              + nums(('Open', '10:00 to 18:00', 'Last entry 17:00'))
              + '<p class="note" style="font-size:13px;color:var(--mute)">The goods-set ticket does not include goods at the venue. They are picked up later, so there is nothing to carry out.</p>'
              + links(('MAPPA EXPO official site', 'https://expo.mappa.co.jp/en'), ('Tokyo International Forum on Google Maps', gm('Tokyo International Forum')))
              + nxt('Walk to lunch')))
S.append(step(3, '<em>Lunch</em> near Yurakucho',
              '<p class="lead">There are many places under the tracks and in the station buildings. We pick one together on the day.</p>'
              + nxt(ln('Y') + ' from Yurakucho Station to Ikebukuro, about 20 min, no change')))
S.append(step(4, '<em>Animate</em> Ikebukuro',
              ph('img/animate.jpg', 'The Animate Ikebukuro main store building')
              + '<p class="lead">Animate is Japan\'s biggest anime shop chain. The main store is a short walk from Ikebukuro Station, with more anime shops on the streets around it. We look around before the signing.</p>'
              + links(('Animate on Google Maps', gm('Animate Ikebukuro Main Store')), ('Official site', 'https://www.animate.co.jp/shop/ikebukuro/'))
              + nxt('Gather at Space Galleria on 8F by 15:45')))
S.append(step(5, 'The <em>Kaoruhana</em> signing',
              ph2(('img/kaoruhana-ex.jpg', 'Kaoruhana 5th anniversary exhibition key visual'), ('img/kaoruhana.jpg', 'Kaoruhana anime key visual'))
              + '<p class="lead">The Kaoruhana Rin to Saku 5th anniversary exhibition is in Space Galleria on the 8th floor of the Animate main store. The signing is by the author, Mikami Saka. Entry is at 16:00.</p>'
              + nums(('Entry', '16:00', 'Signing ticket'), ('Closes', '17:00', 'Last entry 16:30'))
              + '<p class="note" style="font-size:13px;color:var(--mute)">I carry the tickets for both places. Please bring your passport in case staff ask for ID.</p>'
              + links(('Exhibition information (e+)', 'https://eplus.jp/kaoruhana-ex/'), ('Animate on Google Maps', gm('Animate Ikebukuro Main Store')))
              + nxt('Done around 17:30. Dinner in Ikebukuro if you like, or the train back to Kinshicho.')))
credit_items = ['Tokyo-International-Forum Glass-Building Outside.jpg, CC BY-SA', 'Animate Ikebukuro.jpg, CC BY-SA',
                'MAPPA EXPO visuals: official site and press images. Attack on Titan exhibit © Isayama Hajime / Kodansha / Attack on Titan The Final Season Production Committee',
                'Kaoruhana visuals: © Mikami Saka / Kodansha / Kaoruhana Rin to Saku Production Committee']
credit = ('<footer class="credit"><p class="note" style="margin:0 0 10px">Times are approximate and can move on the day. Message Yuuki if you want to change anything.</p><details><summary>Credits</summary><ul>'
          + ''.join(f'<li>{c}</li>' for c in credit_items)
          + '</ul><p>Map: Tiles © Esri / © ' + A('https://www.openstreetmap.org/copyright', 'OpenStreetMap') + '</p></details></footer>')
dn = ''.join(f'<button type="button" class="dn" data-i="{i}" aria-label="{"The whole day" if i == 0 else P[i][5]}">{i}</button>' for i in range(len(P)))
OG = 'https://yukitchy.github.io/darren-nov9-plan/img/hero.jpg'
head = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="robots" content="noindex,nofollow"><title>Monday, November 9</title>'
        f'<meta property="og:title" content="Monday, November 9"><meta property="og:description" content="MAPPA EXPO, then the Kaoruhana signing in Ikebukuro."><meta property="og:image" content="{OG}"><meta name="twitter:card" content="summary_large_image">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;900&display=swap">'
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><style>' + open('style.css').read()
        + '.ph2{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:6px;margin:0 0 14px}.ph2 img{display:block;width:100%;height:150px;object-fit:cover;background:#e4e0d2}</style></head><body>')
intro = ('<div class="wrap"><div class="mapbox"><div id="map" aria-label="Map of the day"></div><p class="where"><small>Mon, November 9</small><b>The whole day</b></p>'
         '<nav class="dial" aria-label="Switch stop"><button type="button" class="ar" data-d="-1" aria-label="Previous stop">&lsaquo;</button><div class="nums-r">' + dn + '</div><button type="button" class="ar" data-d="1" aria-label="Next stop">&rsaquo;</button></nav></div>'
         '<main class="story"><header class="intro"><p class="date">Monday, November 9 · 9:00 to 17:30</p><h1>Monday, November 9</h1><p class="who">Darren, with Yuuki. MAPPA EXPO, then the Kaoruhana signing in Ikebukuro.</p>'
         '<dl class="cn"><div><dt>Meet</dt><dd class="n">9:00</dd><dd class="s">Excelsior Caffé, Kinshicho</dd></div><div><dt>Finish</dt><dd class="n">17:30</dd><dd class="s">Ikebukuro</dd></div></dl>'
         '<div class="tools"><a class="tool" href="Darren-Nov9-plan.pdf" target="_blank" rel="noopener">Open the PDF (A4, 1 page)</a></div></header>')
js = ('<script>const LI=%d,LUNCH=%s,DAYS=%s,P=%s,GEO=[[35.7345,139.7158,"Ikebukuro"]];'
      % (LI, json.dumps(LUNCH_JS), json.dumps(['The whole day'] + [p[5] for p in P[1:]]), json.dumps([None] + [[p[0], p[1], p[2], p[3], p[4], 0] for p in P[1:]])))
js += open('map.js').read() + '</script>'
dev = '<script src="devbar.js"></script>'
open('index.html', 'w').write(head + intro + ''.join(S) + credit + '</main></div>' + js + dev + '</body></html>')
print('index.html written')
