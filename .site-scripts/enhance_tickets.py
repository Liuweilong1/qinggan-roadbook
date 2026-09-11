from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: enhance_tickets.py <html>")

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")

start = s.find('<section id="tickets">')
end = s.find('<section id="stay">', start)
if start < 0 or end < 0 or end <= start:
    raise SystemExit("tickets/stay section boundary not found")

section = """<section id="tickets" data-ticket-detail="v2">
<div class="wrap">
  <h2>门票 / 预约 / 景交费用明细</h2>
  <p class="section-lead">按你们 9/26–10/1 实际会去的景点逐个拆开：首道门票是否收费、景交 / 小火车等二次交通、是否必须提前预约，以及到现场怎么买。信息核验截至 2026-09-12；官方公告优先，近期公开平台票务和游客实测用于补足官方没有单列的二次消费。</p>

  <div class="grid-3" style="margin:0 0 18px">
    <div class="callout"><h4>必须优先锁票</h4><p><b>莫高窟、鸣沙山月牙泉、青海湖二郎剑</b>。前两者不要赌现场票；二郎剑你们碰上中秋假期，也建议提前线上实名购票。</p></div>
    <div class="callout"><h4>建议前一晚 / 提前1–3天</h4><p><b>茶卡、察尔汗、翡翠湖、七彩丹霞、嘉峪关</b>。多数支持当日票，但你们的日期靠近中秋和国庆，不值得把时间耗在现场排队。</p></div>
    <div class="callout"><h4>免费 / 机动点</h4><p><b>大地之子、G213祁连9号公路</b>免费；<b>岗什卡雪峰</b>首道门票目前公开口径以免费为主，但摆渡车和天气限流要当天确认。</p></div>
  </div>

  <div class="table-wrap">
  <table>
    <thead><tr><th>日期 / 景点</th><th>门票</th><th>景交 / 二次交通</th><th>预约还是现场买</th><th>你们怎么操作最稳</th></tr></thead>
    <tbody>
      <tr>
        <td><b>9/26 青海湖二郎剑</b><br><span class="pill">付费</span></td>
        <td>当前公开票务成人基础门票约 <b>90元</b>。官方最新运营通告明确高峰期建议提前预约。</td>
        <td>景区内有观光车、游船等项目，属于另购项目，价格会随线路 / 套票变化；<b>不建议提前盲买大套票</b>。</td>
        <td><b>线上实名优先</b>。近期公开票务信息显示旺季不宜依赖现场窗口；你们 9/26 正逢中秋假期。</td>
        <td><b>提前3–5天以上锁基础票</b>；到园后再决定车 / 船。你们提到的“二郎剑小路”若是私人或非正规通道不要进。</td>
      </tr>
      <tr>
        <td><b>9/26 茶卡盐湖</b><br><span class="pill">付费</span></td>
        <td>旺季成人票 <b>60元</b>。</td>
        <td>官方价：小火车 <b>50元/单程</b>；游船 <b>90元/单程</b>；观光电瓶车 <b>5元/单程</b>；观光塔 <b>20元</b>。停车场 10元/辆/次。</td>
        <td><b>线上、现场都能买</b>。官方支持公众号 / 抖音 / 携程 / 美团，也支持售票窗口、自助机。</td>
        <td>中秋客流下建议<b>前一晚买门票</b>。时间紧可“小火车单程进去 + 步行 / 电瓶车出来”，没必要往返都排小火车。</td>
      </tr>
      <tr>
        <td><b>9/27 察尔汗盐湖</b><br><span class="pill">付费</span></td>
        <td>当前主流成人票型为<b>门票 + 往返景交约102元</b>。</td>
        <td><b>景交很关键</b>。格尔木官方优惠政策明确：部分免首道门票人群仍需另购观光车票，说明景交与门票分开管理。</td>
        <td>官方近期明确<b>线上 + 线下双渠道</b>；当前平台成人套票可随买随用。</td>
        <td>你们当天还要去翡翠湖，建议<b>前一晚线上买好</b>，直接刷证 / 电子票走，少在游客中心耗时间。</td>
      </tr>
      <tr>
        <td><b>9/27 大柴旦翡翠湖</b><br><span class="pill">付费</span></td>
        <td>当前成人首道门票 <b>60元</b>，公开票务显示可订当日。</td>
        <td>2026年8月近期游客实测普遍反映穿梭小火车 / 车约 <b>50元</b>另购；观景塔约 <b>25元</b>，以现场挂牌为准。</td>
        <td><b>可当日线上买</b>，不是刚性抢票型景点。</td>
        <td>你们到达偏傍晚，建议直接买门票；若体力 / 时间不足，再加小火车，别为了“坐全程”错过柔和光线。</td>
      </tr>
      <tr>
        <td><b>9/28 黑独山</b><br><span class="pill">以景交为主</span></td>
        <td>当前公开渠道口径有差异：平台页面出现<b>40元起</b>，近期旅行产品 / 实测则常见“首道门票免费、区间车收费”。</td>
        <td>近期公开实测与旅行产品普遍出现<b>区间车约60元往返</b>。当前管理方式已不是“随便自驾开进地貌区”。</td>
        <td>普通日通常可临时处理；比抢票更重要的是<b>当天开放范围、天气和管控</b>。</td>
        <td>预算先按<b>60–100元/人</b>留弹性。只走开放游览区 / 缓冲区，不把车开进地貌、禁游区不进入。</td>
      </tr>
      <tr>
        <td><b>9/28 敦煌丝路遗产城</b><br><span class="pill">付费 · 可删</span></td>
        <td>当前公开平台基础门票约 <b>110元起</b>；夜场星空摄影等套票约 <b>398元起</b>。</td>
        <td>没有你们必须购买的刚性景交项目；不同夜场 / 星空套餐另算。</td>
        <td>当前公开平台多为<b>可当日购买</b>，不是需要提前抢的核心票。</td>
        <td>这是你们 9/28 的<b>体力机动项</b>：到敦煌早、状态好再买；晚到直接删，不要提前锁不可退套票。</td>
      </tr>
      <tr>
        <td><b>9/29 莫高窟</b><br><span class="pill">必须预约</span></td>
        <td>旺季常规全价票 <b>238元</b>：数字电影 + 8个实体洞窟；常规票每日限 <b>6000张</b>。应急票全价 100元，只看4窟。</td>
        <td>数字展示中心到窟区的官方接驳包含在常规参观流程中；不要直接自驾到窟区，核心保护区不设游客停车场 / 普通售票点。</td>
        <td><b>必须提前实名预约</b>，只走“莫高窟参观预约网”微信服务号 / 小程序或官网。官方明确未授权小红书、闲鱼等第三方代购。</td>
        <td><b>这是整趟第一优先级</b>。9/29 常规票一放就买；按预约时间至少提前30分钟到数字展示中心。</td>
      </tr>
      <tr>
        <td><b>9/29 鸣沙山月牙泉</b><br><span class="pill">必须线上</span></td>
        <td>9月旺季成人票 <b>110元</b>；近期公开票务显示首次检票后可按景区规则多日使用。</td>
        <td>骑骆驼、滑沙、鞋套、观光车均属<b>可选二消</b>，不影响只爬沙山 + 月牙泉 + 看日落。</td>
        <td>近期9月公开政策显示普通游客实行<b>线上实名预约</b>，不要把希望放在现场人工售票。</td>
        <td>建议<b>提前1–3天以上</b>；你们只去一个傍晚，优先保留日落，骆驼排队太长就直接舍弃。</td>
      </tr>
      <tr>
        <td><b>9/30 瓜州“大地之子”</b><br><span class="pill">免费</span></td>
        <td><b>免费开放</b>。</td>
        <td>无刚性景交；自驾按现场停车和道路指引即可。</td>
        <td><b>无需预约</b>。</td>
        <td>按原计划短停 <b>20–40分钟</b>即可，不要为了免费雕塑群把9/30长途节奏拖乱。</td>
      </tr>
      <tr>
        <td><b>9/30 嘉峪关关城</b><br><span class="pill">付费</span></td>
        <td>旺季全价票 <b>110元</b>；购买关城全价 / 优惠票可获当日悬壁长城、长城第一墩参观券。</td>
        <td>观光电瓶车<b>自愿</b>：当前优惠执行价往返 <b>20元</b>，单程 <b>10元</b>；也可以步行。</td>
        <td>散客不是刚性提前预约型；大型团队 / 专列需提前24小时。国庆前客流大，个人也建议提前线上买。</td>
        <td>你们只留约2小时，<b>可花20元坐往返车省脚力</b>；不要为了“赠送两景点”临时加悬壁长城 / 第一墩。</td>
      </tr>
      <tr>
        <td><b>9/30 张掖七彩丹霞</b><br><span class="pill">付费 + 景交</span></td>
        <td>2026年1月起成人门票 <b>70元</b>。</td>
        <td>官方观光车 <b>38元/人</b>，景区跨度大，实际游览按门票 + 观光车<b>约108元/人</b>准备。</td>
        <td>可线上买当日票，但你们目标是下午斜射光时段，临近国庆不建议赌临场。</td>
        <td><b>提前1–3天锁9/30下午票</b>。16点左右到最理想；游完直接住七彩镇，不回张掖市区。</td>
      </tr>
      <tr>
        <td><b>10/1 G213祁连9号公路</b><br><span class="pill">免费公路</span></td>
        <td><b>无景区首道门票</b>，它本质上是公共景观公路 / 自驾廊道。</td>
        <td>无景交车。沿线若临时进入卓尔山、阿咪东索等独立收费景区，才另外购票；你们当前不安排这些点。</td>
        <td><b>无需预约</b>。</td>
        <td>把时间留给沿线草原、峡谷、雪山视野和安全停车点。9月起G213部分地灾路段需留意落石 / 管制。</td>
      </tr>
      <tr>
        <td><b>10/1 岗什卡雪峰</b><br><span class="pill">首道免费为主</span></td>
        <td>目前公开景区信息以<b>首道门票免费</b>为主；不同入口 / 产品可能展示服务票。</td>
        <td>景区运营时存在摆渡车；近期旅行产品常见参考价约 <b>25元/人</b>，但未找到同等权威的政府定价公示，<b>以当天景区公告为准</b>。</td>
        <td>不属于抢门票型景点；重点是<b>天气、能见度、限流和摆渡车是否运营</b>。</td>
        <td>保持“天气好则正式停靠”的弹性。10/1到附近如果云层厚、堵车或太晚，远观后直接门源。</td>
      </tr>
    </tbody>
  </table>
  </div>

  <div class="panel" style="margin-top:18px">
    <h3>你们这趟的购票顺序</h3>
    <p style="margin:0;line-height:1.9"><b>① 先锁莫高窟 9/29常规票</b> → <b>② 青海湖二郎剑 + 鸣沙山</b> → ③ 茶卡 / 察尔汗 / 翡翠湖 → ④ 七彩丹霞 9/30下午 → ⑤ 嘉峪关。黑独山、丝路遗产城、岗什卡保留现场机动，不提前把自己绑死。</p>
  </div>

  <div class="panel" style="margin-top:18px">
    <h3>官方 / 近期实测核验说明</h3>
    <p style="margin:0 0 10px;line-height:1.8">价格和预约规则优先取景区官网、敦煌研究院、当地文旅 / 发改 / 政府公告；官方没有明确公示的区间车或临时二消，再用 2026 年近期公开票务平台和游客实测交叉补充。<b>小红书笔记正文目前无法稳定通过公开网页完整检索</b>，所以这里不会假装“抓到了全部最新小红书笔记”；临行前仍建议在小红书 App 用页面已有关键词复核当天排队、天气和现场照片。</p>
    <p style="margin:0;line-height:1.8">
      <a href="https://www.gonghe.gov.cn/xwdt/tzgg/content_1013653405" target="_blank" rel="noreferrer">青海湖二郎剑官方通告</a> ·
      <a href="https://www.chakasl.com/ticket.html" target="_blank" rel="noreferrer">茶卡盐湖官方票务</a> ·
      <a href="https://www.geermu.gov.cn/details?id=ff80808191c740bd019202d3eaed012b" target="_blank" rel="noreferrer">察尔汗盐湖官方信息</a> ·
      <a href="https://www.dha.ac.cn/info/1020/7498.htm" target="_blank" rel="noreferrer">莫高窟2026公告</a> ·
      <a href="https://zwfw.gansu.gov.cn/jiayuguan/tsfw/lyzq/lyzx/lyzc/art/2026/art_0076b2ad870d44ad90090478d19b45b9.html" target="_blank" rel="noreferrer">嘉峪关官方公告</a> ·
      <a href="https://www.zhangye.gov.cn/fgw/dzdt/tzgg/202507/t20250711_1426087_ghb.html" target="_blank" rel="noreferrer">七彩丹霞门票定价</a> ·
      <a href="https://www.zhangye.gov.cn/zyszfxxgk/zfwj_5652/bmwj_5656/202301/t20230118_972698_ghb.html" target="_blank" rel="noreferrer">七彩丹霞观光车定价</a>
    </p>
  </div>
</div>
</section>


"""

s = s[:start] + section + s[end:]
p.write_text(s, encoding="utf-8")
print("Detailed ticket, reservation and scenic-transport section inserted for 13 trip stops.")
