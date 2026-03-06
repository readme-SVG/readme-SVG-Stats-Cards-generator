import math
import datetime
import hashlib
from typing import Optional

THEMES = {
    "dark": {"bg":"#0d1117","border":"#30363d","title":"#58a6ff","text":"#c9d1d9","icon":"#58a6ff","accent":"#58a6ff","subtext":"#8b949e","bar":"#238636","bar_bg":"#161b22","cell_empty":"#161b22","cell_l1":"#0e4429","cell_l2":"#006d32","cell_l3":"#26a641","cell_l4":"#39d353"},
    "radical": {"bg":"#141321","border":"#443760","title":"#fe428e","text":"#a9fef7","icon":"#f8d847","accent":"#fe428e","subtext":"#a9fef7","bar":"#fe428e","bar_bg":"#1a1830","cell_empty":"#1a1830","cell_l1":"#5a1040","cell_l2":"#9b1860","cell_l3":"#d42878","cell_l4":"#fe428e"},
    "tokyonight": {"bg":"#1a1b27","border":"#383951","title":"#70a5fd","text":"#a9b1d6","icon":"#bf91f3","accent":"#70a5fd","subtext":"#787c99","bar":"#70a5fd","bar_bg":"#20222e","cell_empty":"#20222e","cell_l1":"#1c3a5f","cell_l2":"#2d5a9e","cell_l3":"#4d7cc4","cell_l4":"#70a5fd"},
    "gruvbox": {"bg":"#282828","border":"#3c3836","title":"#fabd2f","text":"#ebdbb2","icon":"#fe8019","accent":"#fabd2f","subtext":"#a89984","bar":"#b8bb26","bar_bg":"#1d2021","cell_empty":"#1d2021","cell_l1":"#4a4520","cell_l2":"#7a7a20","cell_l3":"#98971a","cell_l4":"#b8bb26"},
    "ocean": {"bg":"#0a192f","border":"#1e3a5f","title":"#64ffda","text":"#ccd6f6","icon":"#64ffda","accent":"#64ffda","subtext":"#8892b0","bar":"#64ffda","bar_bg":"#112240","cell_empty":"#112240","cell_l1":"#0a3a3a","cell_l2":"#0d6060","cell_l3":"#20a0a0","cell_l4":"#64ffda"},
    "sunset": {"bg":"#1a1020","border":"#3d2050","title":"#ff6b6b","text":"#f0d0e0","icon":"#feca57","accent":"#ff6b6b","subtext":"#a08090","bar":"#ff9ff3","bar_bg":"#201030","cell_empty":"#201030","cell_l1":"#5a2040","cell_l2":"#a03060","cell_l3":"#d04080","cell_l4":"#ff6b6b"},
    "light": {"bg":"#ffffff","border":"#d0d7de","title":"#0969da","text":"#1f2328","icon":"#0969da","accent":"#0969da","subtext":"#656d76","bar":"#2da44e","bar_bg":"#eaeef2","cell_empty":"#ebedf0","cell_l1":"#9be9a8","cell_l2":"#40c463","cell_l3":"#30a14e","cell_l4":"#216e39"},
}

ICON_PATHS = {
    "star": "M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z",
    "commit": "M11.93 8.5a4.002 4.002 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 010 1.5zm-1.43-.25a2.5 2.5 0 10-5 0 2.5 2.5 0 005 0z",
    "pr": "M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 100 1.5.75.75 0 000-1.5zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z",
    "issue": "M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z",
    "contrib": "M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z",
    "fire": "M7.998 14.5c2.832 0 5-1.98 5-4.5 0-1.463-.68-2.19-1.879-3.383l-.036-.037c-1.013-1.008-2.3-2.29-2.834-4.434-.322.256-.63.579-.864.953-.432.696-.621 1.58-.046 2.73.473.947.67 2.284-.278 3.232-.61.61-1.545.84-2.403.588a2.06 2.06 0 01-1.162-.96C2.344 10.267 3.96 14.5 7.998 14.5z",
    "eye": "M8 2c1.981 0 3.671.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 010 1.798c-.45.678-1.367 1.932-2.637 3.023C11.67 13.008 9.981 14 8 14c-1.981 0-3.671-.992-4.933-2.078C1.797 10.831.88 9.577.43 8.9a1.619 1.619 0 010-1.798c.45-.678 1.367-1.932 2.637-3.023C4.33 2.992 6.019 2 8 2zM1.679 7.932a.12.12 0 000 .136c.411.622 1.241 1.75 2.366 2.717C5.176 11.758 6.527 12.5 8 12.5c1.473 0 2.825-.742 3.955-1.715 1.124-.967 1.954-2.096 2.366-2.717a.12.12 0 000-.136c-.412-.621-1.242-1.75-2.366-2.717C10.824 4.242 9.473 3.5 8 3.5c-1.473 0-2.824.742-3.955 1.715-1.124.967-1.954 2.096-2.366 2.717zM8 10a2 2 0 110-4 2 2 0 010 4z",
}

FONT = "Segoe UI,Ubuntu,sans-serif"


def _esc(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#39;")

def _get_theme(name):
    return THEMES.get(name, THEMES["dark"])

def _parse_color(raw, fallback):
    c = raw.strip().lstrip("#")
    if len(c) in (3,6) and all(ch in "0123456789abcdefABCDEF" for ch in c):
        return f"#{c}"
    return fallback

def _icon(name, x, y, color, size=16):
    path_d = ICON_PATHS.get(name, "")
    sc = size / 16
    return f'<g transform="translate({x},{y}) scale({sc})"><path fill-rule="evenodd" d="{path_d}" fill="{_esc(color)}"/></g>'

def _fmt(n):
    if n >= 1000000: return f"{n/1000000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k"
    return str(n)

def _calc_rank(stars,commits,prs,issues,contribs):
    s = stars*1.0 + commits*0.25 + prs*0.5 + issues*0.25 + contribs*0.1
    if s>=500: return "S+"
    if s>=200: return "S"
    if s>=100: return "A+"
    if s>=50: return "A"
    if s>=20: return "B+"
    if s>=10: return "B"
    return "C"

def _rank_progress(stars,commits,prs,issues,contribs):
    s = stars*1.0 + commits*0.25 + prs*0.5 + issues*0.25 + contribs*0.1
    th = [0,10,20,50,100,200,500,1000]
    for i in range(len(th)-1):
        if s < th[i+1]:
            return (s - th[i]) / (th[i+1] - th[i])
    return 1.0


def generate_stats_card(username="octocat",stars=0,commits=0,prs=0,issues=0,contribs=0,theme="dark",custom_title=None,hide_border=False,hide_rank=False,border_radius=10,bg_color=None,title_color=None,text_color=None,icon_color=None,border_color=None,animate=True):
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    text_c = _parse_color(text_color, t["text"]) if text_color else t["text"]
    icon_c = _parse_color(icon_color, t["icon"]) if icon_color else t["icon"]
    W, H = 495, 195
    title = _esc(custom_title or f"{username}'s GitHub Stats")
    rank = _calc_rank(stars,commits,prs,issues,contribs)
    progress = _rank_progress(stars,commits,prs,issues,contribs)
    ba = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'
    circ = 2*math.pi*40
    off = circ - circ*progress
    anim = f'''<style>
@keyframes fi{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes si{{from{{opacity:0;transform:scale(0)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes gb{{from{{stroke-dashoffset:{circ:.1f}}}to{{stroke-dashoffset:{off:.1f}}}}}
.sr{{opacity:0;animation:fi .5s ease forwards}}
.rc{{opacity:0;animation:si .6s ease .4s forwards;transform-origin:center}}
.rb{{animation:gb 1s ease .5s forwards;stroke-dashoffset:{circ:.1f}}}
</style>''' if animate else '<style>.sr{opacity:1}.rc{opacity:1}</style>'
    items = [("star","Total Stars",stars),("commit","Total Commits",commits),("pr","Total PRs",prs),("issue","Total Issues",issues),("contrib","Contributed to",contribs)]
    rows = ""
    for i,(ic,lb,vl) in enumerate(items):
        y = 50 + i*28
        rows += f'<g class="sr" style="animation-delay:{i*100}ms" transform="translate(25,{y})">{_icon(ic,0,0,icon_c,16)}<text x="26" y="12.5" fill="{_esc(text_c)}" font-size="14" font-family="{FONT}">{_esc(lb)}:</text><text x="210" y="12.5" fill="{_esc(text_c)}" font-size="14" font-weight="700" font-family="{FONT}">{_fmt(vl)}</text></g>\n'
    rk = ""
    if not hide_rank:
        rk = f'<g class="rc" transform="translate(420,105)"><circle r="40" fill="none" stroke="{_esc(t["bar_bg"])}" stroke-width="6"/><circle class="rb" r="40" fill="none" stroke="{_esc(title_c)}" stroke-width="6" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}" stroke-linecap="round" transform="rotate(-90)"/><text x="0" y="8" text-anchor="middle" fill="{_esc(title_c)}" font-size="24" font-weight="800" font-family="{FONT}">{rank}</text></g>\n'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{anim}
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{border_radius}" ry="{border_radius}" fill="{_esc(bg)}" {ba}/>
<text x="25" y="32" fill="{_esc(title_c)}" font-size="18" font-weight="700" font-family="{FONT}">{title}</text>
{rows}{rk}</svg>'''


def generate_streak_card(username="octocat",current_streak=0,longest_streak=0,total_contribs=0,streak_start="",streak_end="",longest_start="",longest_end="",theme="dark",hide_border=False,border_radius=10,bg_color=None,title_color=None,text_color=None,accent_color=None,border_color=None,animate=True):
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    text_c = _parse_color(text_color, t["text"]) if text_color else t["text"]
    accent = _parse_color(accent_color, t["accent"]) if accent_color else t["accent"]
    sub_c = t["subtext"]
    W, H = 495, 195
    ba = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'
    anim = '''<style>
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes cu{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}
.sc{opacity:0;animation:fi .5s ease forwards}
.bn{opacity:0;animation:cu .4s ease forwards;transform-origin:center}
</style>''' if animate else '<style>.sc{opacity:1}.bn{opacity:1}</style>'
    cw = W / 3
    secs = [
        ("Total Contributions", _fmt(total_contribs), "All Time", 0),
        ("Current Streak", str(current_streak), f"{streak_start} - {streak_end}" if streak_start else "", 1),
        ("Longest Streak", str(longest_streak), f"{longest_start} - {longest_end}" if longest_start else "", 2),
    ]
    cols = ""
    for lb,vl,sub,idx in secs:
        cx = cw*idx + cw/2
        dl = idx*150
        fire = _icon("fire", -12, -20, accent, 20) if idx==1 and current_streak>0 else ""
        cols += f'<g class="sc" style="animation-delay:{dl}ms" transform="translate({cx:.0f},60)">'
        cols += f'<text y="0" text-anchor="middle" fill="{_esc(sub_c)}" font-size="13" font-family="{FONT}">{_esc(lb)}</text>'
        cols += f'<g class="bn" style="animation-delay:{dl+100}ms">{fire}<text x="0" y="42" text-anchor="middle" fill="{_esc(text_c)}" font-size="38" font-weight="800" font-family="{FONT}">{_esc(vl)}</text></g>'
        cols += f'<text y="68" text-anchor="middle" fill="{_esc(sub_c)}" font-size="11" font-family="{FONT}">{_esc(sub)}</text>'
        cols += '</g>\n'
        if idx < 2:
            sx = cw*(idx+1)
            cols += f'<line x1="{sx:.0f}" y1="42" x2="{sx:.0f}" y2="168" stroke="{_esc(border)}" stroke-width="1" stroke-opacity="0.5"/>\n'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{anim}
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{border_radius}" ry="{border_radius}" fill="{_esc(bg)}" {ba}/>
<text x="{W/2}" y="30" text-anchor="middle" fill="{_esc(title_c)}" font-size="18" font-weight="700" font-family="{FONT}">{_esc(username)}&apos;s Streak Stats</text>
{cols}</svg>'''


def _gen_contribs(username, weeks=52):
    seed = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    s = seed
    data = []
    for w in range(weeks):
        wk = []
        for d in range(7):
            s = (s*1103515245+12345)&0x7FFFFFFF
            r = s%100
            if r<30: c=0
            elif r<55: c=1+(s>>4)%3
            elif r<78: c=4+(s>>8)%5
            elif r<92: c=9+(s>>12)%6
            else: c=15+(s>>16)%10
            wk.append(c)
        data.append(wk)
    return data


def generate_graph_card(username="octocat",contributions=None,theme="dark",hide_border=False,border_radius=10,bg_color=None,title_color=None,text_color=None,border_color=None,cell_size=11,cell_gap=3,weeks=52,animate=True):
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    cc = [t["cell_empty"],t["cell_l1"],t["cell_l2"],t["cell_l3"],t["cell_l4"]]
    if contributions is None:
        contributions = _gen_contribs(username, weeks)
    gw = weeks*(cell_size+cell_gap)
    gh = 7*(cell_size+cell_gap)
    px, py = 45, 55
    W = gw+px+25
    H = gh+py+30
    ba = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'
    anim = '''<style>
@keyframes cp{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.cl{opacity:0;animation:cp .15s ease forwards;transform-origin:center}
</style>''' if animate else '<style>.cl{opacity:1}</style>'
    dl = ""
    for lb,ri in [("Mon",1),("Wed",3),("Fri",5)]:
        y = py+ri*(cell_size+cell_gap)+cell_size-2
        dl += f'<text x="{px-8}" y="{y}" text-anchor="end" fill="{_esc(t["subtext"])}" font-size="10" font-family="{FONT}">{lb}</text>\n'
    ms = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    td = datetime.date.today()
    ml = ""
    for mi in range(12):
        wa = int(mi*(weeks/12))
        x = px+wa*(cell_size+cell_gap)
        ml += f'<text x="{x}" y="{py-8}" fill="{_esc(t["subtext"])}" font-size="10" font-family="{FONT}">{ms[(td.month-12+mi)%12]}</text>\n'
    cells = ""
    total = 0
    for wi,wk in enumerate(contributions[:weeks]):
        for di,cnt in enumerate(wk[:7]):
            total += cnt
            if cnt==0: lv=0
            elif cnt<=3: lv=1
            elif cnt<=8: lv=2
            elif cnt<=14: lv=3
            else: lv=4
            x = px+wi*(cell_size+cell_gap)
            y = py+di*(cell_size+cell_gap)
            d = wi*6+di
            cells += f'<rect class="cl" style="animation-delay:{d}ms" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{cc[lv]}"><title>{cnt} contributions</title></rect>\n'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{anim}
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{border_radius}" ry="{border_radius}" fill="{_esc(bg)}" {ba}/>
<text x="{px}" y="28" fill="{_esc(title_c)}" font-size="15" font-weight="700" font-family="{FONT}">{_esc(username)}&apos;s Contribution Graph</text>
<text x="{px}" y="44" fill="{_esc(t["subtext"])}" font-size="11" font-family="{FONT}">{_fmt(total)} contributions in the last year</text>
{ml}{dl}{cells}</svg>'''


def generate_views_card(username="octocat",count=0,theme="dark",label="Profile Views",style="flat",bg_color=None,label_color=None,count_color=None,icon_show=True):
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    lc = _parse_color(label_color, t["subtext"]) if label_color else t["subtext"]
    ctc = _parse_color(count_color, t["accent"]) if count_color else t["accent"]
    cs = _fmt(count)
    lw = len(label)*7+20
    cw = len(cs)*8+20
    iw = 24 if icon_show else 0
    tw = lw+cw+iw
    h = 28
    ip = _icon("eye",8,6,lc,14) if icon_show else ""
    if style=="flat":
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{h}">
<rect width="{lw+iw}" height="{h}" fill="{_esc(bg)}" rx="3"/>
<rect x="{lw+iw}" width="{cw}" height="{h}" fill="{_esc(ctc)}" rx="3"/>
<rect x="{lw+iw}" width="4" height="{h}" fill="{_esc(ctc)}"/>
{ip}
<text x="{iw+lw/2}" y="{h/2+4}" text-anchor="middle" fill="{_esc(lc)}" font-size="11" font-family="Verdana,DejaVu Sans,sans-serif">{_esc(label)}</text>
<text x="{lw+iw+cw/2}" y="{h/2+4}" text-anchor="middle" fill="#fff" font-size="11" font-weight="700" font-family="Verdana,DejaVu Sans,sans-serif">{_esc(cs)}</text>
</svg>'''
    else:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{h}">
<rect width="{tw}" height="{h}" fill="{_esc(bg)}" rx="4" stroke="{_esc(t["border"])}" stroke-width="1"/>
{ip}
<text x="{iw+8}" y="{h/2+4}" fill="{_esc(lc)}" font-size="11" font-family="Verdana,DejaVu Sans,sans-serif">{_esc(label)}</text>
<text x="{iw+lw+4}" y="{h/2+4}" fill="{_esc(ctc)}" font-size="12" font-weight="700" font-family="Verdana,DejaVu Sans,sans-serif">{_esc(cs)}</text>
</svg>'''
