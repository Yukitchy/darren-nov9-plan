#!/usr/bin/env python3
"""コース選択ページ(エディトリアル版)。page.json と courses.json を編集して python3 build.py -> index.html
COURSES / PAGE / PH の名前は course-picker の engine/extract.py が読むので変えない。"""
import json, html, os

PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=15'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

PAGE = json.load(open('page.json'))
COURSES = json.load(open('courses.json'))
for c in COURSES:
    for k, d in (('chips', []), ('food', []), ('links', []), ('stops', []), ('steps', []), ('bars', []), ('moves', ''), ('good', ''), ('mind', ''), ('tag', ''), ('why', '')):
        c.setdefault(k, d)
    PH.setdefault(c['id'], {}).setdefault('card', {'thumb': '', 'title': '', 'lic': ''})
    PH[c['id']].setdefault('detail', []); PH[c['id']].setdefault('food', [])

# 各プランの見出し下に置く2枚(ワクワク採点の高い、人や店が写っている絵)
PICK = {'A': [('detail', 1), ('detail', 3)], 'B': [('card', None), ('detail', 3)]}
def pics(c):
    out = []
    for kind, i in PICK.get(c['id'], []):
        x = PH[c['id']][kind] if i is None else PH[c['id']][kind][i]
        out.append(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">')
    return ''.join(out)

T0 = PAGE.get('t0', 13)
SPAN = PAGE.get('span', 330)
def hm(m):
    t = T0 * 60 + m
    return f'{t // 60}:{t % 60:02d}'

def col(c):
    segs = ''
    for a, b, name, kind in c['bars']:
        two = (b - a) >= 30
        tm = f'<i>{hm(a)} to {hm(b)}</i>' if two else ''
        inner = f'<b>{html.escape(name)}</b>{tm}'
        if kind == 'w' and name == PAGE.get('ws_bar', name): inner = f'<a href="#workshop">{inner}<i class="more">{PAGE.get("ws_more", "What happens inside ↓")}</i></a>'
        segs += f'<li class="seg {kind}" style="--a:{a};--b:{b}">{inner}</li>'
    return f'<ol class="track">{segs}</ol>'

def head(c):
    cl = '' if len(COURSES) == 1 else f'<span class="cl">{c["id"]}</span>'
    return (f'<a class="chead" href="#detail-{c["id"]}">{cl}'
            f'<span class="cn">{html.escape(c["name"])}</span></a>')

def cta(c):
    one = len(COURSES) == 1
    sub = PAGE['subject'] if one else PAGE['subject'] + f' course {c["id"]} ({c["name"]})'
    label = PAGE.get('cta', 'Choose') if one else f'Choose {c["id"]}'
    return f'<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">{html.escape(label)}</a>'

def plan(c):
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    ln = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    return f'''<section class="plan" id="detail-{c['id']}"><div class="wrap pgrid">
<div class="phead"><div class="pin">
{'' if len(COURSES) == 1 else f'<span class="pl" aria-hidden="true">{c["id"]}</span>'}
<h2>{html.escape(c['name'])}</h2>
<p class="ptag">{html.escape(c['tag'])}</p>
<p class="why">{html.escape(c['why'])}</p>
{cta(c)}
</div></div>
<div class="pbody">
<div class="pics">{pics(c)}</div>
<ol class="steps">{st}</ol>
<div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p>
<dl class="notes"><div><dt>Good for</dt><dd>{html.escape(c['good'])}</dd></div><div><dt>Keep in mind</dt><dd>{html.escape(c['mind'])}</dd></div></dl>
<p class="links">{ln}</p>
</div></div></section>'''

def video(w):
    if not w.get('video'): return ''
    return f'''<div class="video"><button class="vplay" type="button" data-id="{w['video'][0]}" aria-label="Play: {html.escape(w['video'][1])}"><img src="https://i.ytimg.com/vi/{w['video'][0]}/hqdefault.jpg" alt="" loading="lazy"><span class="vico"></span></button><p class="vcap">{html.escape(w['video'][1])}</p></div>'''

def ws():
    w = PAGE['workshop']
    ph = w['photos']
    img = lambda i, cls='': f'<img class="{cls}" src="{ph[i][0]}" alt="{html.escape(ph[i][1])}" loading="lazy" referrerpolicy="no-referrer">'
    facts = ''.join(f'<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>' for k, v in w['facts'])
    steps = ''.join(f'<li><b>{i + 1}</b><div><strong>{html.escape(h)}</strong><span>{html.escape(d)}</span></div></li>' for i, (h, d) in enumerate(w['steps']))
    return f'''<section class="plan ws" id="workshop"><div class="wrap pgrid">
<div class="phead"><div class="pin">
<h2>{html.escape(w['h2'])}</h2>
<p class="why">{html.escape(w['lead'])}</p>
<dl class="wfacts">{facts}</dl>
{f'<figure class="quote"><blockquote>“{html.escape(w["quote"])}”</blockquote><figcaption>{html.escape(w["quote_by"])}</figcaption></figure>' if w.get('quote') else ''}
</div></div>
<div class="pbody">
<figure class="wmain">{img(0, 'screen-only')}{img(3, 'print-only')}</figure>
{video(w)}
<div class="pics">{img(1)}{img(2)}</div>
<ol class="steps wsteps">{steps}</ol>
{f'<div class="teacher">{img(4)}<p><strong>{html.escape(w["teacher"][0])}</strong><span>{html.escape(w["teacher"][1])}</span></p></div>' if w.get('teacher') else ''}
<p class="note">{html.escape(w['note'])}</p>
<p class="links"><a href="{w['link'][1]}" target="_blank" rel="noopener">{html.escape(w['link'][0])} ↗</a></p>
</div></div></section>'''

def sheet():
    w = PAGE['print']; A = COURSES[0]
    im = lambda u, alt, cls='': f'<img class="{cls}" src="{u}" alt="{html.escape(alt)}" referrerpolicy="no-referrer">'
    photos = ''.join(f'<figure>{im(u, cap)}<figcaption>{html.escape(cap)}</figcaption></figure>' for u, cap in w['photos'])
    route = ''.join(f'<li class="{k}"><b>{hm(a)}</b><span>{html.escape(n)}</span></li>' for a, b_, n, k in A['bars']) + f'<li class="end"><b>{w["end"][0]}</b><span>{html.escape(w["end"][1])}</span></li>'
    dirs = ''.join(f'<li><i>{i + 1}</i>{html.escape(x)}</li>' for i, x in enumerate(w['directions']))
    shops = ''.join(f'<tr><td>{html.escape(n)}</td><td>{html.escape(a)}</td><td>{html.escape(h)}</td></tr>' for n, a, h in w['shops'])
    ws = ''.join(f'<li>{html.escape(x)}</li>' for x in w['workshop'])
    contact = ' · '.join(f'{html.escape(k)} {html.escape(v)}' for k, v in w['contact'])
    facts = ' · '.join(html.escape(k) + ' ' + html.escape(v) for k, v in PAGE['facts'])
    addr = html.escape(PAGE.get('meet_addr', PAGE['meet_place']))
    return ('<section class="sheet" aria-hidden="true">'
        f'<header class="sh"><h1>{html.escape(w["title"])}</h1><p>{facts}</p></header>'
        f'<div class="sphotos">{photos}</div>'
        f'<ol class="sroute">{route}</ol>'
        + (f'<figure class="smap"><img src="img/route-{A["id"]}.png" alt="Route map"><figcaption>' + ' → '.join(f'<b>{i + 1}</b> {html.escape(x)}' + (' (optional)' if i >= A.get('opt_from', 99) else '') for i, x in enumerate(A.get('stop_names', A['stops']))) + '</figcaption></figure>' if os.path.exists(f'img/route-{A["id"]}.png') else '') +
        f'<div class="sgrid"><div class="smeet"><h2>{html.escape(w["meet_h2"])}</h2><p class="saddr">{addr}</p><ol class="sdirs">{dirs}</ol></div>'
        f'<div class="sws"><h2>{html.escape(w["ws_h2"])}</h2><div class="swsin">{im(w["ws_photo"][0], w["ws_photo"][1])}<ul>{ws}</ul></div><p class="snote">{html.escape(PAGE["workshop"]["note"])}</p></div></div>'
        f'<div class="sshops"><h2>{html.escape(w["shops_h2"])}</h2><table class="sshop">{shops}</table></div>'
        f'<footer class="sfoot">{contact} · {html.escape(PAGE["footer"])}</footer></section>')

credits = '; '.join(html.escape(x['title'].replace('File:', '')) + ' (' + x['lic'] + ')' for v in PH.values() for x in [v['card']] + v['detail'] + v['food'])
facts = ''.join(f'<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>' for k, v in PAGE['facts'])
N = len(COURSES)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(PAGE['title'])}</title><meta name="robots" content="noindex"><meta name="description" content="{html.escape(PAGE['lead'])}">
<meta name="theme-color" content="#f4f1ea">
<meta property="og:title" content="{html.escape(PAGE['title'])}"><meta property="og:description" content="{html.escape(PAGE['lead'])}">
<meta property="og:type" content="website"><meta property="og:url" content="{PAGE['url']}">
<meta property="og:image" content="{PAGE['hero_img']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet">
<style>
:root{{--paper:#f4f1ea;--ink:#111;--mute:#6a655b;--line:#d9d3c5;--seg:#e4dfd2;--red:#e60012;--s:1.9px;--gut:18px}}
*{{box-sizing:border-box;min-width:0}} html{{scroll-behavior:smooth;scroll-padding-top:56px}}
html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%;display:block}}
body{{margin:0;font-family:Archivo,-apple-system,"Hiragino Sans",sans-serif;font-stretch:100%;color:var(--ink);background:var(--paper);line-height:1.55;font-size:17px;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 var(--gut)}}
a{{color:inherit}}
h1,h2,h3{{margin:0;font-weight:800;text-wrap:balance}}
dl,dd,ol,ul{{margin:0;padding:0}} ol,ul{{list-style:none}}

.nav{{position:sticky;top:0;z-index:10;background:rgba(244,241,234,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.nav .wrap{{display:flex;gap:22px;height:48px;align-items:center;font-size:14px;font-weight:600}}
.nav a{{text-decoration:none;white-space:nowrap}} .nav a:hover{{text-decoration:underline;text-underline-offset:4px}}
.nav .sp{{margin-left:auto}} .sheet{{display:none}}
.pchoose{{position:fixed;inset:0;z-index:50;background:rgba(17,17,17,.55);display:flex;align-items:center;justify-content:center;padding:20px}} .pchoose[hidden]{{display:none}}
.pbox{{background:var(--paper);width:min(420px,100%);padding:22px 22px 16px;display:grid;gap:10px}} .pbox>p{{margin:0 0 4px;font-weight:800;font-size:22px;font-stretch:75%}}
.pbox button{{font:inherit;text-align:left;background:var(--paper);border:2px solid var(--ink);padding:12px 14px;cursor:pointer;color:inherit}} .pbox button:hover{{background:var(--ink);color:var(--paper)}}
.pbox strong{{display:block;font-size:16px}} .pbox span{{display:block;font-size:13.5px;color:var(--mute)}} .pbox button:hover span{{color:inherit}}
.pbox .pcancel{{border:0;padding:6px 0 0;font-size:13px;color:var(--mute);text-decoration:underline;text-underline-offset:3px;justify-self:start}} .pbox .pcancel:hover{{background:none;color:var(--ink)}} .pdfbtn{{font:inherit;font-size:13px;font-weight:600;background:none;border:1px solid var(--ink);padding:5px 10px;cursor:pointer;color:inherit}} .pdfbtn:hover{{background:var(--ink);color:var(--paper)}}

.facts{{margin-top:26px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 36px}}
.facts div{{display:flex;gap:10px;align-items:baseline;font-size:14px}}
.facts dt{{color:var(--mute)}} .facts dd{{font-weight:600}}
.mega{{font-size:min(22.4vw,284px);font-stretch:62%;font-weight:800;line-height:.86;letter-spacing:-.015em;text-transform:uppercase;margin:18px 0 0 -.03em;white-space:nowrap}}
.heroimg{{margin:18px 0 0;width:100vw;margin-left:calc(50% - 50vw)}}
.heroimg img{{width:100%;aspect-ratio:16/9;object-fit:cover;max-height:72vh}}
.heroimg figcaption{{font-size:12.5px;color:var(--mute);max-width:1240px;margin:0 auto;padding:8px var(--gut) 0}}
.pick{{display:grid;grid-template-columns:1fr;gap:12px;padding:42px 0 54px}}
.pick h2{{font-size:clamp(34px,6vw,76px);font-stretch:75%;line-height:.98;letter-spacing:-.02em}}
.pick p{{margin:0;font-size:19px;color:var(--mute);max-width:520px}}

.compare{{border-top:1px solid var(--ink);padding:30px 0 60px}}
.compare h2{{font-size:clamp(26px,4vw,44px);font-stretch:75%;line-height:1;letter-spacing:-.01em}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 22px;margin:16px 0 26px;font-size:14px;font-weight:600}}
.legend span{{display:inline-flex;align-items:center;gap:8px}}
.legend i{{width:14px;height:14px;display:inline-block}} .legend .w i{{background:var(--red)}} .legend .s i{{background:var(--seg)}}
.cgrid{{display:grid;grid-template-columns:1fr;gap:6px}} .cside{{position:static}}
.heads,.tracks,.ctas{{display:grid;grid-template-columns:46px repeat(var(--n,2),1fr);gap:0 8px}}
.chead{{display:flex;align-items:baseline;gap:10px;text-decoration:none;padding:0 0 12px;border-bottom:2px solid var(--ink);margin-bottom:0}}
.cl{{font-size:44px;font-weight:800;line-height:.9;font-stretch:75%;margin-right:4px}}
.cn{{font-size:14px;font-weight:700;line-height:1.2}}
.tracks{{height:calc(var(--span) * var(--s));margin:0;background-image:linear-gradient(var(--line) 1px,transparent 1px);background-size:100% calc(60 * var(--s));background-repeat:repeat-y}}
.axis{{position:relative}} .axis li{{position:absolute;left:0;transform:translateY(-.55em);font-size:12.5px;color:var(--mute);font-variant-numeric:tabular-nums;background:var(--paper);padding-right:4px;line-height:1}}
.track{{position:relative}}
.seg{{position:absolute;left:0;right:0;top:calc(var(--a) * var(--s) + 1px);height:calc((var(--b) - var(--a)) * var(--s) - 2px);background:var(--seg);padding:5px 8px;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-start;transform-origin:top;transform:scaleY(0);transition:transform .7s cubic-bezier(.2,.7,.2,1)}}
.seg.w{{background:var(--red);color:var(--paper)}}
.seg b{{font-size:13px;line-height:1.2;font-weight:700}} .seg i{{font-style:normal;font-size:12.5px;line-height:1.3;opacity:.85;font-variant-numeric:tabular-nums;margin-top:2px}}
.tt.in .seg{{transform:none}} .tt.in .track:nth-child(3) .seg{{transition-delay:.12s}}
.ctas{{margin-top:18px}}
.choose{{display:inline-block;background:var(--ink);color:var(--paper);text-decoration:none;font-weight:700;font-size:15px;padding:14px 22px;text-align:center;border:2px solid var(--ink);transition:background .15s,color .15s}}
.choose:hover{{background:var(--paper);color:var(--ink)}}

.plan{{border-top:1px solid var(--ink);padding:36px 0 64px;scroll-margin-top:48px}}
.pgrid{{display:grid;grid-template-columns:1fr;gap:28px}}
.pl{{display:block;font-size:min(34vw,200px);font-stretch:62%;font-weight:800;line-height:.8;margin-left:-.03em}}
.plan h2{{font-size:clamp(30px,4vw,48px);font-stretch:75%;line-height:1;letter-spacing:-.015em;margin-top:18px}}
.ptag{{margin:10px 0 0;font-size:15px;font-weight:600;color:var(--mute)}}
.why{{margin:18px 0 24px;font-size:17px;max-width:460px}}
.pics{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:30px}}
.pics img{{width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--seg)}}
.steps{{border-top:2px solid var(--ink)}}
.steps li{{display:grid;grid-template-columns:62px minmax(0,1fr);gap:10px;padding:14px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;font-size:17px;font-weight:700}}
.steps strong{{display:block;font-size:17px;font-weight:700;line-height:1.3}} .steps span{{display:block;color:var(--mute);font-size:15px;margin-top:3px}}
.mapbox{{margin-top:34px;background:var(--seg)}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-underline-offset:3px;white-space:nowrap}}
.notes{{display:grid;grid-template-columns:1fr;gap:18px;margin-top:30px;padding-top:20px;border-top:1px solid var(--line)}}
.notes dt{{font-size:12.5px;font-weight:700;color:var(--mute);letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}} .notes dd{{font-size:15px}}
.links{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:26px 0 0;font-size:14px}} .links a{{text-underline-offset:3px}}

.seg.w a{{display:flex;flex-direction:column;height:100%;color:inherit;text-decoration:none}}
.seg .more{{margin-top:auto;font-size:12.5px;opacity:.9;text-decoration:underline;text-underline-offset:3px}}
.ws .pin h2{{margin-top:0;font-size:clamp(34px,5vw,64px)}}
.wfacts{{display:grid;gap:14px;margin:0 0 26px;padding-top:18px;border-top:2px solid var(--ink)}}
.wfacts dt{{font-size:13px;font-weight:700;color:var(--mute);text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}} .wfacts dd{{font-size:16px}}
.quote{{margin:0;padding:18px 0 0;border-top:1px solid var(--line)}}
.quote blockquote{{margin:0;font-size:clamp(22px,2.6vw,30px);font-weight:800;font-stretch:75%;line-height:1.1;letter-spacing:-.01em;text-wrap:balance}}
.quote figcaption{{margin-top:10px;font-size:13.5px;color:var(--mute)}}
.wmain{{margin:0 0 8px}} .print-only{{display:none}} .wmain img{{width:100%;aspect-ratio:3/2;object-fit:cover;background:var(--seg)}}
.wsteps li{{grid-template-columns:40px minmax(0,1fr)}} .wsteps b{{color:var(--red);font-size:22px;line-height:1;font-stretch:75%}}
.teacher{{display:grid;grid-template-columns:96px 1fr;gap:16px;align-items:start;margin-top:30px;padding-top:20px;border-top:1px solid var(--line)}}
.teacher img{{width:96px;aspect-ratio:1;object-fit:cover;background:var(--seg)}} .teacher p{{margin:0;font-size:15px}} .teacher strong{{display:block;font-size:17px;margin-bottom:3px}} .teacher span{{color:var(--mute)}}
.note{{margin:22px 0 0;padding:14px 16px;background:var(--seg);font-size:14.5px}}

.video{{margin:8px 0 0}}
.vplay{{display:block;position:relative;width:100%;aspect-ratio:16/9;padding:0;border:0;background:var(--ink);cursor:pointer;overflow:hidden}}
.vplay img{{width:100%;height:100%;object-fit:cover;opacity:.92;transition:transform .6s,opacity .3s}} .vplay:hover img{{transform:scale(1.03);opacity:1}}
.vico{{position:absolute;left:50%;top:50%;width:76px;height:76px;margin:-38px 0 0 -38px;background:var(--red);border-radius:50%}}
.vico::after{{content:"";position:absolute;left:31px;top:24px;border-left:22px solid var(--paper);border-top:14px solid transparent;border-bottom:14px solid transparent}}
.video iframe{{display:block;width:100%;aspect-ratio:16/9;border:0;background:var(--ink)}}
.vcap{{margin:8px 0 0;font-size:13.5px;color:var(--mute)}} .vcap a{{text-underline-offset:3px}}

.meet{{border-top:1px solid var(--ink);padding:36px 0 64px}}
.meet .mgrid{{display:grid;grid-template-columns:1fr;gap:26px}}
.meet h2{{font-size:clamp(32px,5vw,60px);font-stretch:75%;line-height:1;letter-spacing:-.015em}}
.meet p{{margin:14px 0 0;font-size:17px;max-width:520px}} .meet .addr a{{font-weight:600;text-underline-offset:3px}} .meet .hint{{color:var(--mute);font-size:15px}}
.meet .mapbox{{margin:0}}
footer{{border-top:1px solid var(--ink);font-size:13px;color:var(--mute)}} footer .wrap{{padding-top:22px;padding-bottom:56px}} footer p{{margin:0 0 8px}}
.cred summary{{cursor:pointer;text-decoration:underline;text-underline-offset:3px;list-style:none;display:inline-block}} .cred summary::-webkit-details-marker{{display:none}}
.cred p{{margin:8px 0 0;font-size:12.5px;line-height:1.6}}

@media(min-width:760px){{
 :root{{--gut:32px;--s:2.1px}}
 .nav .wrap{{gap:30px}}
 .pick{{grid-template-columns:7fr 5fr;gap:40px;align-items:end;padding:56px 0 72px}}
 .heads,.tracks,.ctas{{grid-template-columns:58px repeat(var(--n,2),1fr);gap:0 14px}}
 .seg{{padding:6px 12px}} .seg b{{font-size:15px}} .seg i{{font-size:13px}}
 .cl{{font-size:64px}} .cn{{font-size:17px}}
 .pgrid,.cgrid{{grid-template-columns:5fr 7fr;gap:56px}} .cside{{position:sticky;top:76px;align-self:start}} .legend{{flex-direction:column;gap:8px}}
 .pin{{position:sticky;top:76px}}
 .pics img{{aspect-ratio:3/2}} .ws .pics img:nth-child(2){{object-position:center 20%}}
 .meet .mgrid{{grid-template-columns:5fr 7fr;gap:56px}} .mapbox iframe{{height:380px}}
}}
@media(min-width:1100px){{.wrap{{padding:0 40px}} :root{{--gut:40px}}}}
@media print{{
 @page{{size:A4;margin:9mm 10mm}}
 body:not([data-print=full])>*:not(.sheet){{display:none!important}} body:not([data-print=full]) .sheet{{display:block}}
 body{{background:#fff;color:#111;font-size:10.5pt;line-height:1.3}}
 body[data-print=full]{{font-size:14px;line-height:1.45;--gut:0}} body[data-print=full] .wrap{{padding:0;max-width:none}}
 body[data-print=full] .nav,body[data-print=full] .mapbox,body[data-print=full] .video,body[data-print=full] .choose,body[data-print=full] .cred,body[data-print=full] .pchoose,body[data-print=full] .ws .pics,body[data-print=full] .plan .pics,body[data-print=full] .notes,body[data-print=full] .quote,body[data-print=full] .pdfbtn{{display:none}}
 body[data-print=full] .screen-only{{display:none}} body[data-print=full] .print-only{{display:block}}
 body[data-print=full] main{{display:flex;flex-direction:column}} body[data-print=full] .meet{{order:-1}} body[data-print=full] .plan{{order:1}} body[data-print=full] .ws{{order:2}}
 body[data-print=full] .compare,body[data-print=full] .ws,body[data-print=full] .plan{{break-before:page;border-top:0;padding:0}} body[data-print=full] .meet{{break-before:avoid;break-inside:avoid;border-top:1px solid var(--ink);padding:16px 0 0;margin-top:14px}} body[data-print=full] footer{{break-before:avoid;border-top:1px solid var(--line);margin-top:18px}}
 body[data-print=full] h1,body[data-print=full] h2,body[data-print=full] h3{{break-after:avoid}} body[data-print=full] .tt,body[data-print=full] .steps li,body[data-print=full] .teacher,body[data-print=full] .wfacts,body[data-print=full] .note,body[data-print=full] .heads,body[data-print=full] .seg,body[data-print=full] .pics{{break-inside:avoid}}
 body[data-print=full] .mega{{font-size:20vw;margin-top:6px}} body[data-print=full] .heroimg{{width:auto;margin:10px 0 0}} body[data-print=full] .heroimg img{{max-height:30vh}} body[data-print=full] .heroimg figcaption{{padding-top:4px}} body[data-print=full] .pick{{padding:14px 0 0;gap:4px}} body[data-print=full] .pick h2{{font-size:32px}} body[data-print=full] .pick p{{font-size:15px}} body[data-print=full] .meet h2{{font-size:30px}} body[data-print=full] .meet p{{font-size:15px;margin-top:8px}}
 body[data-print=full]{{--s:1.75px}} body[data-print=full] .cgrid,body[data-print=full] .pgrid,body[data-print=full] .mgrid{{display:block}} body[data-print=full] .pin{{position:static}} body[data-print=full] .seg{{transform:none!important;transition:none}} body[data-print=full] .ctas{{display:none}} body[data-print=full] .legend{{flex-direction:row;margin:10px 0 14px}}
 body[data-print=full] .ws .pin h2,body[data-print=full] .plan h2,body[data-print=full] .meet h2{{font-size:36px}} body[data-print=full] .why{{max-width:none;margin:10px 0 14px}} body[data-print=full] .wmain img{{max-height:22vh;object-fit:cover;width:100%}} body[data-print=full] .ws .links{{display:none}}
 body[data-print=full] .steps li{{padding:6px 0}} body[data-print=full] .teacher{{margin-top:8px;padding-top:8px;gap:12px}} body[data-print=full] .teacher img{{width:60px}} body[data-print=full] .teacher p,body[data-print=full] .teacher strong{{font-size:13.5px}} body[data-print=full] .note{{margin-top:8px;padding:8px 12px;font-size:12.5px}} body[data-print=full] .pics img{{aspect-ratio:3/2}}
 body[data-print=full] .wmain img{{max-height:17vh}} body[data-print=full] .wfacts{{gap:5px;margin-bottom:10px;padding-top:8px}} body[data-print=full] .wfacts dd{{font-size:13.5px}} body[data-print=full] .ws .why{{margin-bottom:8px;font-size:14px}} body[data-print=full] .wsteps li{{padding:5px 0}}
 .sh{{display:flex;align-items:baseline;border-bottom:2pt solid #111;padding-bottom:4pt;margin-bottom:7pt}}
 .sh h1{{font-size:20pt;font-stretch:75%;font-weight:800;letter-spacing:-.01em;margin:0;white-space:nowrap}} .sh p{{margin:0 0 0 auto;padding-left:18pt;font-size:9.5pt;font-weight:600;text-align:right}}
 .sheet h2{{font-size:12pt;font-weight:800;margin:0 0 4pt;letter-spacing:0}}
 .sphotos{{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:5pt;margin-bottom:7pt}} .sphotos figure{{margin:0}} .sphotos img{{width:100%;height:86pt;object-fit:cover;display:block}} .sphotos figcaption{{font-size:7.5pt;color:#555;margin-top:1.5pt}}
 .sroute{{list-style:none;margin:0 0 9pt;padding:0;display:flex;align-items:stretch}} .sroute li{{flex:1;position:relative;background:#e4dfd2;padding:4pt 6pt 4pt 9pt;margin-right:7pt;clip-path:polygon(0 0,calc(100% - 6pt) 0,100% 50%,calc(100% - 6pt) 100%,0 100%,6pt 50%)}}
 .sroute li.w{{background:#e60012;color:#fff;flex:1.6}} .sroute li.end{{background:#111;color:#fff;margin-right:0;flex:.9}} .sroute li:first-child{{clip-path:polygon(0 0,calc(100% - 6pt) 0,100% 50%,calc(100% - 6pt) 100%,0 100%);padding-left:6pt}}
 .sroute b{{display:block;font-size:9.5pt;font-variant-numeric:tabular-nums}} .sroute span{{display:block;font-size:7.5pt;line-height:1.2;font-weight:600}}
 .smap{{margin:0 0 8pt;break-inside:avoid}} .smap img{{display:block;width:100%;height:auto}} .smap+.sgrid{{margin-top:0}} .sheet:has(.smap) .sphotos img{{height:66pt}} .smap figcaption{{font-size:7.5pt;line-height:1.25;margin-top:2pt;color:#333}} .smap b{{display:inline-block;background:#e60012;color:#fff;border-radius:50%;width:10pt;height:10pt;line-height:10pt;text-align:center;font-size:7pt}}
 .sgrid{{display:grid;grid-template-columns:1fr 1fr;gap:0 14pt;margin-bottom:8pt;break-inside:avoid}}
 .saddr{{margin:0 0 5pt;font-weight:700;font-size:10.5pt}} .sdirs{{margin:0;padding:0;list-style:none;font-size:9.5pt}} .sdirs li{{display:flex;gap:6pt;margin-bottom:3pt}} .sdirs i{{flex:none;font-style:normal;font-weight:800;color:#fff;background:#e60012;width:13pt;height:13pt;border-radius:50%;text-align:center;line-height:13pt;font-size:8.5pt}}
 .swsin{{display:grid;grid-template-columns:78pt 1fr;gap:7pt}} .swsin img{{width:78pt;height:78pt;object-fit:cover;object-position:center 30%}} .sws ul{{margin:0;padding-left:11pt;font-size:9.5pt}} .sws li{{margin-bottom:2pt}} .snote{{margin:5pt 0 0;padding:4pt 6pt;background:#eee8dc;font-size:8.5pt}}
 .sheet table{{border-collapse:collapse;width:100%;font-size:9.5pt}} .sheet td{{padding:2pt 4pt 2pt 0;border-bottom:.6pt solid #cfc9bb;vertical-align:top}}
 .sshop td:nth-child(1){{font-weight:700;width:40%}} .sshop td:nth-child(2){{width:42%}} .sshop td:nth-child(3){{white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}}
 .sfoot{{border-top:1pt solid #111;margin-top:7pt;padding-top:4pt;font-size:8.5pt;color:#444}}
}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}} .seg{{transform:none;transition:none}}}}
</style></head><body>
<nav class="nav"><div class="wrap"><a href="#compare">{"Compare" if N > 1 else "Timeline"}</a><a href="#workshop">{html.escape(PAGE.get("ws_nav", "Workshop"))}</a>{"".join(f'<a href="#detail-{c["id"]}">{"Plan " + c["id"] if N > 1 else "Plan"}</a>' for c in COURSES)}<a class="sp" href="#meet">Meeting point</a><button class="pdfbtn" type="button" onclick="window.print()">Save as PDF</button></div></nav>
<header class="wrap hero">
<dl class="facts">{facts}</dl>
<h1 class="mega">{PAGE['h1']}</h1>
<figure class="heroimg"><img src="{PAGE['hero_img']}" alt="{html.escape(PAGE['hero_alt'])}" referrerpolicy="no-referrer"><figcaption>{html.escape(PAGE['hero_cap'])}</figcaption></figure>
<div class="pick"><h2>{html.escape(PAGE['pick'])}</h2><p>{html.escape(PAGE['lead'])}</p></div>
</header>
<main>
<section class="compare" id="compare"><div class="wrap">
<div class="cgrid"><div class="cside"><h2>{html.escape(PAGE.get('compare_h2', 'The same afternoon, in two orders'))}</h2>
<div class="legend">{''.join(f'<span class="{k}"><i></i>{html.escape(t)}</span>' for k, t in PAGE['legend'])}</div></div>
<div class="tt" id="tt" style="--n:{N};--s:{PAGE.get('s', '1.9px')};--span:{SPAN}">
<div class="heads"><span></span>{"".join(head(c) for c in COURSES)}</div>
<div class="tracks"><ul class="axis">{''.join(f'<li style="top:calc({h * 60} * var(--s))">{T0 + h}:00</li>' for h in range(SPAN // 60 + 1))}</ul>{''.join(col(c) for c in COURSES)}</div>
<div class="ctas"><span></span>{"".join(cta(c) for c in COURSES)}</div>
</div></div></div></section>
{ws()}
{''.join(plan(c) for c in COURSES)}
<section class="meet" id="meet"><div class="wrap mgrid">
<div><h2>{html.escape(PAGE['meet_h2'])}</h2><p>{html.escape(PAGE['meet_text'])}</p><p class="addr"><a href="{gm(PAGE['meet_place'])}" target="_blank" rel="noopener">{html.escape(PAGE.get('meet_addr', PAGE['meet_place']))} ↗</a></p><p class="hint">{html.escape(PAGE['meet_hint'])}</p></div>
<div class="mapbox"><iframe src="{emb(PAGE['meet_place'])}" loading="lazy" title="{html.escape(PAGE['meet_place'])}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
</main>
<footer><div class="wrap"><p>{html.escape(PAGE['footer'])} <button class="pdfbtn" type="button" onclick="window.print()">Save as PDF</button></p>
<details class="cred"><summary>Photo credits</summary><p>{html.escape(PAGE.get('credits_lead', ''))} {credits}, via Wikimedia Commons.</p></details></div></footer>
<script>
(function(){{
 var t=document.getElementById('tt');
 if('IntersectionObserver' in window){{new IntersectionObserver(function(e,o){{if(e[0].isIntersecting){{t.classList.add('in');o.disconnect()}}}},{{threshold:.15}}).observe(t)}}else{{t.classList.add('in')}}
 setTimeout(function(){{t.classList.add('in')}},3500);
 var v=document.querySelector('.vplay');
 if(v)v.addEventListener('click',function(){{var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+v.dataset.id+'?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title=v.getAttribute('aria-label').replace('Play: ','');v.replaceWith(f)}});
}})();
</script>
{sheet()}
<div class="pchoose" id="pchoose" hidden><div class="pbox"><p>Save as PDF</p>
<button type="button" data-mode="sheet"><strong>One page summary</strong><span>Meeting point, times, shops. Good for printing.</span></button>
<button type="button" data-mode="full"><strong>Full guide</strong><span>Everything on this page, with photos. Several pages.</span></button>
<button type="button" class="pcancel" data-mode="">Cancel</button></div></div>
<script>
(function(){{
 var box=document.getElementById('pchoose');
 document.querySelectorAll('.pdfbtn').forEach(function(b){{b.addEventListener('click',function(){{box.hidden=false}})}});
 box.addEventListener('click',function(e){{var m=e.target.closest('button');if(!m&&e.target!==box)return;box.hidden=true;if(!m||!m.dataset.mode||box.dataset.busy)return;
   box.dataset.busy=1;document.body.dataset.print=m.dataset.mode;setTimeout(function(){{window.print();delete box.dataset.busy}},50)}});
 window.addEventListener('afterprint',function(){{delete document.body.dataset.print}});
 var q=(location.search.match(/[?&]print=(sheet|full)/)||[])[1];if(q)document.body.dataset.print=q;
}})();
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
