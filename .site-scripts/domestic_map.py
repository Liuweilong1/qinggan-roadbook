from pathlib import Path
import sys

html_path = Path(sys.argv[1])
s = html_path.read_text(encoding='utf-8')

# Use a mainland-friendly CDN for Leaflet assets instead of unpkg.
s = s.replace(
    '<link rel="preconnect" href="https://unpkg.com">\n<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">',
    '<link rel="preconnect" href="https://cdn.bootcdn.net">\n<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/leaflet/1.9.4/leaflet.css">',
    1,
)
s = s.replace(
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
    '<script src="https://cdn.bootcdn.net/ajax/libs/leaflet/1.9.4/leaflet.js"></script>',
    1,
)

# Prefer Tencent tiles in mainland/WeChat. If no tiles arrive, automatically
# fall back to Gaode's current official-style wprd endpoint.
old_tile = """  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom:18, attribution:'© OpenStreetMap contributors'
  }).addTo(map);"""
new_tile = """  let baseLayer;
  let primaryLoads=0;
  let fallbackLoads=0;
  let usingFallback=false;

  function useGaodeFallback(){
    if(usingFallback) return;
    usingFallback=true;
    if(baseLayer) map.removeLayer(baseLayer);
    baseLayer=L.tileLayer('https://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8&ltype=11',{
      subdomains:['1','2','3','4'], maxZoom:18, attribution:'© 高德地图（备用底图）'
    }).addTo(map);
    baseLayer.on('tileload',()=>{ fallbackLoads++; });
    setTimeout(()=>{
      if(fallbackLoads===0){
        const fb=document.getElementById('mapFallback');
        if(fb){
          fb.style.display='block';
          fb.innerHTML='地图底图暂未加载出来，但路线点位和连线仍可查看。可稍后重试，或直接用高德/百度导航查看沿线区域。';
        }
      }
    },5000);
  }

  baseLayer=L.tileLayer('https://rt{s}.map.gtimg.com/realtimerender?z={z}&x={x}&y={y}&type=vector&style=0',{
    subdomains:['0','1','2'], tms:true, minZoom:3, maxZoom:18, attribution:'© 腾讯地图'
  }).addTo(map);
  let tileErrors=0;
  baseLayer.on('tileload',()=>{ primaryLoads++; });
  baseLayer.on('tileerror',()=>{
    tileErrors++;
    if(primaryLoads===0 && tileErrors>=4) useGaodeFallback();
  });
  setTimeout(()=>{ if(primaryLoads===0) useGaodeFallback(); },3500);"""
if old_tile not in s:
    raise SystemExit('OpenStreetMap tile block not found')
s = s.replace(old_tile, new_tile, 1)

# Domestic basemaps use GCJ-02 while the roadbook points are stored as WGS-84.
# Convert only for rendering so markers/polyline line up with the basemap.
converter = r'''
function outOfChina(lat, lon) {
  return lon < 72.004 || lon > 137.8347 || lat < 0.8293 || lat > 55.8271;
}
function transformLat(x, y) {
  let ret = -100 + 2*x + 3*y + .2*y*y + .1*x*y + .2*Math.sqrt(Math.abs(x));
  ret += (20*Math.sin(6*x*Math.PI) + 20*Math.sin(2*x*Math.PI))*2/3;
  ret += (20*Math.sin(y*Math.PI) + 40*Math.sin(y/3*Math.PI))*2/3;
  ret += (160*Math.sin(y/12*Math.PI) + 320*Math.sin(y*Math.PI/30))*2/3;
  return ret;
}
function transformLon(x, y) {
  let ret = 300 + x + 2*y + .1*x*x + .1*x*y + .1*Math.sqrt(Math.abs(x));
  ret += (20*Math.sin(6*x*Math.PI) + 20*Math.sin(2*x*Math.PI))*2/3;
  ret += (20*Math.sin(x*Math.PI) + 40*Math.sin(x/3*Math.PI))*2/3;
  ret += (150*Math.sin(x/12*Math.PI) + 300*Math.sin(x/30*Math.PI))*2/3;
  return ret;
}
function wgs84ToGcj02(lat, lon) {
  if (outOfChina(lat, lon)) return [lat, lon];
  const a = 6378245.0;
  const ee = 0.00669342162296594323;
  let dLat = transformLat(lon - 105.0, lat - 35.0);
  let dLon = transformLon(lon - 105.0, lat - 35.0);
  const radLat = lat / 180.0 * Math.PI;
  let magic = Math.sin(radLat);
  magic = 1 - ee * magic * magic;
  const sqrtMagic = Math.sqrt(magic);
  dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * Math.PI);
  dLon = (dLon * 180.0) / (a / sqrtMagic * Math.cos(radLat) * Math.PI);
  return [lat + dLat, lon + dLon];
}

'''
marker = 'try {\n  if (!window.L) throw new Error(\'Leaflet unavailable\');'
if marker not in s:
    raise SystemExit('Leaflet init marker not found')
s = s.replace(marker, converter + marker, 1)

old_loop = """  points.forEach((p,i)=>{
    latlngs.push([p.lat,p.lon]);
    L.marker([p.lat,p.lon]).addTo(map).bindPopup(`<b>${i+1}. ${p.name}</b><br>${p.date} · ${p.note}`);
  });"""
new_loop = """  points.forEach((p,i)=>{
    const [lat,lon]=wgs84ToGcj02(p.lat,p.lon);
    latlngs.push([lat,lon]);
    L.marker([lat,lon]).addTo(map).bindPopup(`<b>${i+1}. ${p.name}</b><br>${p.date} · ${p.note}`);
  });"""
if old_loop not in s:
    raise SystemExit('Map point loop not found')
s = s.replace(old_loop, new_loop, 1)

s = s.replace(
    '地图用于理解环线结构与停靠点，不替代高德/百度的实时导航。10/1以当天导航与交管公告为准即可。',
    '地图用于理解环线结构与停靠点，优先使用腾讯地图国内底图，若加载失败会自动切换高德备用底图；实际驾车仍以高德/百度当天实时导航和交管公告为准。',
    1,
)

html_path.write_text(s, encoding='utf-8')
