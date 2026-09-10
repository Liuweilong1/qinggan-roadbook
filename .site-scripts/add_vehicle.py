from pathlib import Path
import re
import sys

html_path = Path(sys.argv[1])
s = html_path.read_text(encoding='utf-8')

if 'id="bj30-plan"' in s:
    raise SystemExit('BJ30 vehicle plan already exists')

# Use a deliberately conservative planning figure for the rental-car budget.
s, count = re.subn(
    r'(<input id="cons" type="number" value=")[^"]*(" step="0\.1">)',
    r'\g<1>9\2',
    s,
    count=1,
)
if count != 1:
    raise SystemExit('Failed to update fuel-consumption default')

s = s.replace(
    '默认按4人、约3000km、普通SUV/中型车估算，可直接改。',
    '默认按4人、约3000km、神州租车 BJ30 的保守长途油耗 9L/100km 估算，可直接改。实际拿到混动版时通常会更省。',
    1,
)

vehicle_panel = r'''
  <div id="bj30-plan" class="panel" style="margin-top:18px">
    <h3>这次租车：神州租车 BJ30</h3>
    <p>神州租车的公开出行数据里已经把北京 BJ30 列为热门 SUV 车型，但公开页面没有说明你这笔订单最终交车一定是哪一个动力版本，所以取车时以现场车辆为准。北京越野目前的 BJ30 旅行家燃油版和油混版都使用 <b>92号汽油</b>：燃油版油箱约 <b>60L</b>、官方综合工况约 <b>8.06L/100km</b>；油混营运版油箱约 <b>51L</b>、官方综合工况约 <b>6.45L/100km</b>。</p>
    <div class="grid-3" style="margin-top:14px">
      <div class="callout"><h4>⛽ 路书按 9L/100km 算</h4><p>高原、山路、满载、国庆车流都会让油耗比理想工况更高一些，所以预算器不按最低油耗算。按9L做预算比较从容；如果现场拿到混动版，实际花费大概率会低于预算。</p></div>
      <div class="callout"><h4>🛣️ 舒适补油间隔约 400–450km</h4><p>不是说BJ30只能跑这么远，而是刻意留出余量。普通高速和城镇路段不用频繁加油；进入柴达木戈壁或G213祁连山路前，油量不到半箱就顺手补到接近满箱。</p></div>
      <div class="callout"><h4>📷 取车时多做 30 秒确认</h4><p>看一下仪表确认燃油/油混版本和当前油量，拍照记录油表、里程与车身；同时问清神州租车的还车油量规则。之后整趟按92号正规加油站补给即可。</p></div>
    </div>
    <p class="map-note">按约3000km、9L/100km、油价7.3元/L粗算，整趟燃油预算约1970元；这是偏保守的准备值，不是必须花到的金额。</p>
  </div>
'''

marker = '<div class="grid-3" style="margin-top:18px">'
services_pos = s.find('<section id="services">')
if services_pos < 0:
    raise SystemExit('services section not found')
marker_pos = s.find(marker, services_pos)
if marker_pos < 0:
    raise SystemExit('services grid marker not found')
s = s[:marker_pos] + vehicle_panel + '\n' + s[marker_pos:]

s = s.replace(
    '<li><b>95号汽油车型：</b>偏远乡镇不一定每个站都有高标号油，德令哈、大柴旦、敦煌、张掖等较大城镇经过时顺手补会更稳妥。</li>',
    '<li><b>BJ30用油：</b>官方燃油版和油混版都使用92号汽油。沿途优先中石油 / 中石化等正规站即可，不需要为了高标号汽油专门绕路。</li>',
    1,
)

html_path.write_text(s, encoding='utf-8')
