from pathlib import Path
import re
import sys

html_path = Path(sys.argv[1])
s = html_path.read_text(encoding='utf-8')

if 'id="bj30-plan"' in s:
    raise SystemExit('BJ30 vehicle plan already exists')

# Use a deliberately conservative planning figure for the rental-car budget.
s, count = re.subn(
    r'(<input id="cons"[^>]*\bvalue=")[^"]*(")',
    r'\g<1>9\2',
    s,
    count=1,
)
if count != 1:
    raise SystemExit('Failed to update fuel-consumption default')

s = s.replace(
    '默认按4人、约3000km、普通SUV/中型车估算，可直接改。',
    '默认按4人、约3000km、神州租车 BJ30 燃油版的保守长途油耗 9L/100km 估算，可直接改。',
    1,
)

vehicle_panel = r'''
  <div id="bj30-plan" class="panel" style="margin-top:18px">
    <h3>这次租车：神州租车 BJ30 燃油版 · 满油取还</h3>
    <p>车辆信息已确认：<b>BJ30 燃油版</b>，按 <b>92号汽油</b> 规划；油箱约 <b>60L</b>，官方综合工况约 <b>8.06L/100km</b>。神州租车采用<b>满油取、满油还</b>，因此取车时先拍一张油表和里程，返程还车前再在门店附近的正规加油站补到满油即可。</p>
    <div class="grid-3" style="margin-top:14px">
      <div class="callout"><h4>⛽ 路书按 9L/100km 算</h4><p>高原、山路、满载和节假日车流都会让油耗高于理想工况，所以预算器继续按9L/100km做准备值。这样不用刻意省油，也能给绕行和堵车留余量。</p></div>
      <div class="callout"><h4>🛣️ 舒适补油间隔约 400–450km</h4><p>60L油箱按9L/100km理论上能跑更远，但路书不建议把油量用得太低。普通高速和城镇路段不用频繁加油；进入柴达木戈壁或G213祁连山路前，油量不到半箱就顺手补到接近满箱。</p></div>
      <div class="callout"><h4>↩️ 满油取还怎么做</h4><p>取车时确认油表满格并拍照留存。最后一天回西宁后，在还车门店附近的中石油 / 中石化等正规站按门店要求补至满格或加到自动跳枪，保留加油小票，再去还车最省心。</p></div>
    </div>
    <p class="map-note">按约3000km、9L/100km、油价7.3元/L粗算，全程实际消耗约270L，燃油预算约1970元。因为是满油取还，最终补回去的油基本就是旅途中实际消耗的油；若实际油耗接近官方值，总油费会低一些。</p>
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
    '<li><b>BJ30燃油版用油：</b>使用92号汽油。沿途优先中石油 / 中石化等正规站即可，不需要为了高标号汽油专门绕路。</li>',
    1,
)

s = s.replace(
    '<td><b>西宁出发前加满</b>；如果途中想补，湟源 / 倒淌河一带、茶卡镇都比较方便。茶卡离开前看一眼油量即可。</td>',
    '<td>取车时已经是<b>满油</b>，9/26出发前看一眼油表即可；如果前一晚市区用车较多，湟源 / 倒淌河一带、茶卡镇都可以顺手补。茶卡离开前再看一眼油量即可。</td>',
    1,
)

s = s.replace(
    '<td>门源县城看油量，需要就补；回到西宁再按租车公司的还车要求加油。</td>',
    '<td>门源县城按油量决定是否补；回到西宁后，在还车门店附近的正规站<b>加满再还车</b>。</td>',
    1,
)

html_path.write_text(s, encoding='utf-8')
