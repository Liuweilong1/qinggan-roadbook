from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: add_gangshika.py <html>')

p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'Gangshika update target not found: {label}')
    s = s.replace(old, new, 1)

# Main recommended-route chips: make Gangshika the visible travel stop.
replace_once(
    '<span class="new">祁连</span><span class="new">峨堡</span><span class="new">G0611</span><span class="new">门源</span>',
    '<span class="new">祁连</span><span class="new">岗什卡雪峰</span><span class="new">门源</span>',
    'recommended route chips',
)

# The relaxed copy produced earlier in the pipeline.
replace_once(
    '把10/1留给风景公路和沿途休息，顺着路况前往门源，整体会更从容。',
    '把10/1留给G213风景公路和沿途休息；天气、能见度和时间合适时顺路游览岗什卡雪峰，再前往门源。峨堡仅作为经S302上G0611的交通节点，不安排专门停留。',
    'recommended route explanation',
)

# Fallback text used when the interactive map tiles cannot load.
replace_once(
    '肃南 → 祁连 → 峨堡 → 门源 → 西宁。',
    '肃南 → 祁连 → 岗什卡雪峰 → 门源 → 西宁。',
    'map fallback route',
)

# Day 7 main card.
replace_once(
    '<h3>七彩镇 → 肃南 → G213“9号公路” → 祁连 → 峨堡 → 门源</h3>',
    '<h3>七彩镇 → 肃南 → G213“9号公路” → 祁连 → 岗什卡雪峰 → 门源</h3>',
    'day7 title',
)
replace_once(
    '<span class="pill">官方绕行</span>',
    '<span class="pill">官方绕行</span><span class="pill">岗什卡机动</span>',
    'day7 tags',
)
replace_once(
    '<div><b>约430–500 km</b><span>预计里程</span></div>\n        <div><b>约7–9 h（节假日可能更久）</b><span>纯驾驶</span></div>',
    '<div><b>约430–540 km</b><span>预计里程 · 视岗什卡停留</span></div>\n        <div><b>约7–9.5 h（不含游览）</b><span>纯驾驶</span></div>',
    'day7 metrics',
)
replace_once(
    '<div class="time">下午</div><div class="what">祁连县 → S302 → 峨堡镇；再上G0611向门源方向。</div>',
    '<div class="time">下午</div><div class="what">祁连县 → S302，经峨堡收费站上G0611 → 岗什卡雪峰。天气、能见度和时间合适就停留游览；若云层较厚或路上较慢，远观后直接前往门源。</div>',
    'day7 afternoon step',
)
replace_once(
    '经典“张掖—扁都口—峨堡—祁连山草原—门源”的G227走法在你们出行时不可用：2026/9/1起相关路段全封闭施工。官方给小型车的绕行就是“张掖—肃南—G213—祁连—S302—峨堡—G0611”。这条路景色很好，但山路多、节假日车流会集中。',
    '经典“张掖—扁都口—峨堡—祁连山草原—门源”的G227走法在你们出行时不可用：2026/9/1起相关路段全封闭施工。交通上仍按“张掖—肃南—G213—祁连—S302—峨堡收费站—G0611”绕行；旅行主线则把峨堡降级为交通节点，把岗什卡雪峰作为天气好时的正式停靠点。',
    'day7 strategy',
)

# The daily route-map card is rebuilt from the new 10/1 image uploaded by the user.
replace_once(
    'D6 当日路线图｜张掖 / 七彩镇 → 肃南 → G213祁连9号公路 → 祁连 → 峨堡 → 门源',
    'D6 当日路线图｜张掖 / 七彩镇 → 肃南 → G213祁连9号公路 → 祁连 → 岗什卡雪峰 → 门源',
    'day7 route-map title',
)
replace_once(
    '重点展示 10/1 绕行路线，并标出肃南、祁连、峨堡、门源等补给和休息节点。',
    '10/1 新版路线图已将岗什卡雪峰作为正式观景点；峨堡仅保留为经S302上G0611的交通节点。',
    'day7 route-map description',
)

# Services section: route display follows the travel itinerary; Ebao stays in the practical traffic note.
replace_once(
    '<td><b>10/1</b><br>七彩镇 → 肃南 → G213祁连9号公路 → 祁连 → 峨堡 → 门源</td>',
    '<td><b>10/1</b><br>七彩镇 → 肃南 → G213祁连9号公路 → 祁连 → 岗什卡雪峰 → 门源</td>',
    'services day7 route',
)
replace_once(
    '七彩镇酒店 → 肃南县城 → 祁连县城 → 峨堡镇 → 门源。G213中间如果遇到开放的观景 / 公共服务点可以休息，但不预设一定有厕所。',
    '七彩镇酒店 → 肃南县城 → 祁连县城 → 经峨堡收费站上G0611 → 岗什卡雪峰景区 / 游客服务点（以当天开放为准）→ 门源。G213中间如果遇到开放的观景 / 公共服务点可以休息，但不预设一定有厕所。',
    'services day7 rest stops',
)

# Interactive route map: replace the visible Ebao marker with Gangshika.
replace_once(
    '{"name": "峨堡镇", "lat": 37.96, "lon": 100.92, "date": "10/1", "note": "转G0611"}',
    '{"name": "岗什卡雪峰", "lat": 37.69, "lon": 101.46, "date": "10/1", "note": "天气和时间合适则游览；交通仍经峨堡收费站上G0611"}',
    'interactive map point',
)

# Share/copy text follows the visible itinerary while preserving the traffic instruction.
replace_once(
    '青甘大环线自驾：西宁→青海湖→茶卡→德令哈→察尔汗→大柴旦→黑独山→敦煌→嘉峪关→七彩丹霞→祁连→门源→西宁。关键提醒：G227封闭，10/1需按官方路线绕行。',
    '青甘大环线自驾：西宁→青海湖→茶卡→德令哈→察尔汗→大柴旦→黑独山→敦煌→嘉峪关→七彩丹霞→祁连→岗什卡雪峰→门源→西宁。关键提醒：G227封闭，10/1交通仍需经S302、峨堡收费站上G0611绕行。',
    'share text',
)
replace_once(
    '10/1 七彩镇-肃南-G213-祁连-S302-峨堡-G0611-门源',
    '10/1 七彩镇-肃南-G213-祁连-S302-经峨堡收费站上G0611-岗什卡雪峰-门源',
    'copy plan',
)

# Add a note beside the route map to distinguish attraction vs. traffic node.
replace_once(
    '注：黑独山、丝路遗产城等点位为行程导览近似点位，具体入口与停车点以景区/导航为准。',
    '注：黑独山、丝路遗产城、岗什卡雪峰等点位为行程导览近似点位，具体入口与停车点以景区/导航为准。10/1交通仍经峨堡收费站上G0611，峨堡不作为专门游玩点。',
    'map note',
)

p.write_text(s, encoding='utf-8')
print('Gangshika promoted to the 10/1 travel stop; Ebao retained as traffic-only node.')
