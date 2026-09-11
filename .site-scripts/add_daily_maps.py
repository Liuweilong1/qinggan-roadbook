from pathlib import Path
import hashlib
import sys

from PIL import Image

if len(sys.argv) != 2:
    raise SystemExit('usage: add_daily_maps.py <html>')

p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')

# Rebuild the 10/1 daily route map from the exact user-approved PNG uploaded to assets.
# Keep the published filename as day7_route_map.jpg so the existing workflow, checks,
# HTML references and browser cache behavior stay stable.
day7_source = Path('assets/ChatGPT Image 2026年9月11日 23_36_56.png')
if not day7_source.exists():
    raise SystemExit(f'10/1 approved route map source missing: {day7_source}')
source_bytes = day7_source.read_bytes()
expected_size = 2755357
expected_sha256 = '7cc519ee01f88252328447780636757a259520e6d0df290038614ffecb199554'
actual_sha256 = hashlib.sha256(source_bytes).hexdigest()
if len(source_bytes) != expected_size:
    raise SystemExit(f'10/1 route map source size mismatch: {len(source_bytes)} != {expected_size}')
if actual_sha256 != expected_sha256:
    raise SystemExit(f'10/1 route map source SHA256 mismatch: {actual_sha256} != {expected_sha256}')

day7_target = p.parent / 'assets/day7_route_map.jpg'
day7_target.parent.mkdir(parents=True, exist_ok=True)
with Image.open(day7_source) as im:
    if im.size != (1122, 1402):
        raise SystemExit(f'10/1 route map dimensions mismatch: {im.size}')
    im.convert('RGB').save(day7_target, 'JPEG', quality=98, optimize=True, subsampling=0)
with Image.open(day7_target) as check:
    if check.size != (1122, 1402):
        raise SystemExit(f'published 10/1 route map dimensions mismatch: {check.size}')
    check.verify()

style = '''
<style id="daily-route-map-style">
.day-route-panel{margin-top:18px;padding:16px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(180deg,#fffefb 0%,#f8f6ef 100%)}
.day-route-title{margin:0 0 6px;font-size:18px;font-weight:800;color:var(--ink)}
.day-route-desc{margin:0 0 12px;color:var(--muted);font-size:14px;line-height:1.7}
.day-route-link{display:block;text-decoration:none;color:inherit;cursor:zoom-in}
.day-route-img{display:block;width:100%;height:auto;border-radius:16px;border:1px solid rgba(0,0,0,.08);box-shadow:0 8px 22px rgba(42,48,46,.08);background:#edf3e7}
.day-route-tip{margin-top:10px;color:var(--muted);font-size:12px;line-height:1.6}
@media (max-width:680px){.day-route-panel{padding:12px;border-radius:16px}.day-route-img{border-radius:14px}.day-route-title{font-size:17px}}
</style>
'''
if 'id="daily-route-map-style"' not in s:
    if '</head>' not in s:
        raise SystemExit('head closing tag not found')
    s = s.replace('</head>', style + '</head>', 1)

panels = {
    'day2': (
        'D1 当日路线图｜西宁 → 青海湖 → 茶卡盐湖 → 德令哈',
        'assets/day2_route_map.jpg',
        '标出当天主要景点、段间距离、大致驾车时间，以及沿途补油和卫生间提示。',
    ),
    'day3': (
        'D2 当日路线图｜德令哈 → 察尔汗盐湖 → 翡翠湖 → 大柴旦',
        'assets/day3_route_map.jpg',
        '重点看察尔汗与翡翠湖的游览顺序，以及格尔木 / 大柴旦方向的补给节点。',
    ),
    'day4': (
        'D3 当日路线图｜大柴旦 → 黑独山 → 丝路遗产城 → 敦煌',
        'assets/day4_route_map.jpg',
        '荒漠和戈壁路段较多，图里重点标出主要路段时间、补油与卫生间条件。',
    ),
    'day5': (
        'D4 当日路线图｜敦煌 → 莫高窟 → 鸣沙山月牙泉 → 敦煌',
        'assets/day5_route_map.jpg',
        '敦煌一日景区往返图，适合快速看上午人文、下午休息、傍晚沙漠的节奏。',
    ),
    'day6': (
        'D5 当日路线图｜敦煌 → 瓜州 / 大地之子 → 嘉峪关 → 张掖',
        'assets/day6_route_map.jpg',
        '把河西走廊这一天的主要停靠点、段间距离和补给信息整合在一张图里。',
    ),
    'day7': (
        'D6 当日路线图｜张掖 / 七彩镇 → 肃南 → G213祁连9号公路 → 祁连 → 峨堡 → 门源',
        'assets/day7_route_map.jpg',
        '重点展示 10/1 绕行路线，并标出肃南、祁连、峨堡、门源等补给和休息节点。',
    ),
    'day8': (
        'D7 当日路线图｜门源 → 西宁',
        'assets/day8_route_map.jpg',
        '返程相对轻松，图里保留沿途距离、补给、卫生间与返城节奏提示。',
    ),
}

for day_id, (title, asset, desc) in panels.items():
    marker = f'<article class="day-card" id="{day_id}">'
    start = s.find(marker)
    if start < 0:
        raise SystemExit(f'day card not found: {day_id}')
    end = s.find('</article>', start)
    if end < 0:
        raise SystemExit(f'day card closing tag not found: {day_id}')
    card = s[start:end]
    if f'data-route-map="{day_id}"' in card:
        continue
    panel = f'''
      <div class="day-route-panel" data-route-map="{day_id}">
        <h4 class="day-route-title">{title}</h4>
        <p class="day-route-desc">{desc}</p>
        <a class="day-route-link" href="{asset}" target="_blank" rel="noreferrer" aria-label="点击查看{title}高清大图">
          <img class="day-route-img" src="{asset}" alt="{title}" width="1122" height="1402" loading="lazy" decoding="async">
        </a>
        <div class="day-route-tip">点击图片可在新页面查看大图。地图用于行程理解，实际驾驶仍以当天高德 / 腾讯实时导航与交管信息为准。</div>
      </div>
'''
    s = s[:end] + panel + s[end:]

p.write_text(s, encoding='utf-8')
print(f'Daily route maps inserted: day2-day8; 10/1 map rebuilt from approved PNG sha256={actual_sha256}')
