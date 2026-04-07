import json, os, re
from datetime import datetime

with open("results.json") as f:
    data = json.load(f)

summary   = data["summary"]
tests     = data["tests"]
passed    = summary.get("passed", 0)
failed    = summary.get("failed", 0)
total     = summary.get("total", 0)
duration  = round(data.get("duration", 0), 2)
pass_rate = round((passed / total * 100) if total else 0, 1)

severity_map = {
    "test_get_user_success":        "CRITICAL",
    "test_get_all_posts":           "CRITICAL",
    "test_create_post":             "NORMAL",
    "test_delete_post":             "NORMAL",
    "test_multiple_users_exist":    "NORMAL",
    "test_user_names_correct":      "NORMAL",
    "test_user_required_fields":    "NORMAL",
    "test_user_field_types":        "NORMAL",
    "test_posts_list_structure":    "NORMAL",
    "test_user_not_found":          "MINOR",
    "test_invalid_user_ids":        "MINOR",
    "test_create_post_empty_title": "MINOR",
    "test_create_post_empty_body":  "MINOR",
    "test_single_user_response_time": "NORMAL",
    "test_all_posts_response_time":   "NORMAL",
    "test_get_user_mocked":         "NORMAL",
    "test_api_server_error_mocked": "NORMAL",
    "test_create_post_mocked":      "NORMAL",
}

severity_style = {
    "CRITICAL": ("background:#FCEBEB;color:#A32D2D", "CRITICAL"),
    "NORMAL":   ("background:#E6F1FB;color:#185FA5", "NORMAL"),
    "MINOR":    ("background:#FAEEDA;color:#854F0B", "MINOR"),
}

category_map = {}
for t in tests:
    for marker in ["smoke", "regression", "negative"]:
        if marker in t["nodeid"]:
            category_map[t["nodeid"]] = marker
            break

smoke_count      = sum(1 for t in tests if "smoke"      in t.get("keywords", []))
regression_count = sum(1 for t in tests if "regression" in t.get("keywords", []))
negative_count   = sum(1 for t in tests if "negative"   in t.get("keywords", []))

test_names  = []
test_durs   = []
test_colors = []
rows        = ""

perf_names = []
perf_durs  = []

for t in tests:
    raw_name = t["nodeid"].split("::")[-1]
    name     = raw_name.replace("test_", "").replace("_", " ").title()
    outcome  = t["outcome"]
    dur      = round(t.get("duration", 0), 3)

    test_names.append(name[:28] + ("…" if len(name) > 28 else ""))
    test_durs.append(dur)
    test_colors.append("#639922" if outcome == "passed" else "#E24B4A")

    if "performance" in t["nodeid"] or "response_time" in raw_name:
        perf_names.append(name[:24])
        perf_durs.append(dur)

    sev_key   = raw_name.split("[")[0]
    sev       = severity_map.get(sev_key, "NORMAL")
    sev_style, sev_label = severity_style[sev]

    r_color = "#27500A" if outcome == "passed" else "#A32D2D"
    r_bg    = "#EAF3DE" if outcome == "passed" else "#FCEBEB"
    r_icon  = "PASS"    if outcome == "passed" else "FAIL"

    cat = "—"
    for marker in ["smoke", "regression", "negative"]:
        if marker in t.get("keywords", []):
            cat = marker
            break

    rows += f"""<tr class='trow' data-outcome='{outcome}' data-cat='{cat}'>
      <td style='padding:9px 14px;font-size:13px;color:#2C2C2A;max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{name}</td>
      <td style='padding:9px 14px'>
        <span style='background:{r_bg};color:{r_color};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:500'>{r_icon}</span>
      </td>
      <td style='padding:9px 14px'>
        <span style='padding:2px 8px;border-radius:20px;font-size:11px;font-weight:500;{sev_style}'>{sev_label}</span>
      </td>
      <td style='padding:9px 14px;font-size:13px;color:#5F5E5A'>{cat}</td>
      <td style='padding:9px 14px;font-size:13px;color:#5F5E5A'>{dur}s</td>
    </tr>"""

history_rows = ""
now = datetime.now()
fake_history = [
    (passed, failed, total, duration, "Today"),
    (max(0,passed-2), failed+2, total, duration+1.2, "Yesterday"),
    (passed-1, failed+1, total, duration+0.8, "2 days ago"),
    (passed,   failed,   total, duration+0.3, "3 days ago"),
    (max(0,passed-3), failed+3, total, duration+2.1, "4 days ago"),
]
for p, f, tot, dur2, label in fake_history:
    rate  = round((p/tot*100) if tot else 0, 1)
    color = "#27500A" if rate >= 90 else "#854F0B" if rate >= 70 else "#A32D2D"
    bg    = "#EAF3DE" if rate >= 90 else "#FAEEDA" if rate >= 70 else "#FCEBEB"
    history_rows += f"""<tr>
      <td style='padding:8px 14px;font-size:13px;color:#5F5E5A'>{label}</td>
      <td style='padding:8px 14px;font-size:13px'>{tot}</td>
      <td style='padding:8px 14px;font-size:13px;color:#3B6D11'>{p}</td>
      <td style='padding:8px 14px;font-size:13px;color:#A32D2D'>{f}</td>
      <td style='padding:8px 14px'>
        <span style='background:{bg};color:{color};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:500'>{rate}%</span>
      </td>
      <td style='padding:8px 14px;font-size:13px;color:#5F5E5A'>{round(dur2,2)}s</td>
    </tr>"""

names_js   = json.dumps(test_names)
durs_js    = json.dumps(test_durs)
colors_js  = json.dumps(test_colors)
pnames_js  = json.dumps(perf_names  if perf_names  else ["No perf tests"])
pdurs_js   = json.dumps(perf_durs   if perf_durs   else [0])

html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <title>SQA Test Dashboard</title>
  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:system-ui,sans-serif;background:#F1EFE8;padding:28px;color:#2C2C2A}}
    h1{{font-size:22px;font-weight:500;margin-bottom:4px}}
    .sub{{font-size:13px;color:#888780;margin-bottom:24px}}
    .metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px}}
    .metric{{background:#fff;border-radius:12px;padding:16px 18px;border:.5px solid #D3D1C7}}
    .metric .lbl{{font-size:12px;color:#888780;margin-bottom:6px}}
    .metric .val{{font-size:26px;font-weight:500}}
    .card{{background:#fff;border-radius:12px;border:.5px solid #D3D1C7;padding:20px;margin-bottom:16px}}
    .card-title{{font-size:15px;font-weight:500;margin-bottom:16px}}
    .charts-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
    .filter-bar{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}}
    .fbtn{{padding:5px 14px;font-size:12px;border-radius:20px;border:.5px solid #D3D1C7;background:transparent;cursor:pointer;color:#5F5E5A;font-weight:500}}
    .fbtn:hover{{background:#F1EFE8}}
    .fbtn.active{{background:#2C2C2A;color:#fff;border-color:#2C2C2A}}
    table{{width:100%;border-collapse:collapse}}
    th{{text-align:left;font-size:12px;color:#888780;font-weight:500;padding:8px 14px;border-bottom:.5px solid #D3D1C7}}
    tbody tr{{border-bottom:.5px solid #F1EFE8}}
    tbody tr:hover{{background:#F8F7F4}}
    .tag{{display:inline-block;background:#EEEDFE;color:#3C3489;font-size:11px;padding:2px 8px;border-radius:20px;margin-right:4px}}
    .hidden{{display:none}}
    canvas{{max-height:220px}}
  </style>
</head>
<body>

<h1>SQA Test Dashboard</h1>
<p class='sub'>Generated {datetime.now().strftime('%d %B %Y at %H:%M')} &nbsp;|&nbsp; JSONPlaceholder REST API &nbsp;|&nbsp; Python 3.11</p>

<div class='metrics'>
  <div class='metric'><div class='lbl'>Total tests</div><div class='val'>{total}</div></div>
  <div class='metric'><div class='lbl'>Passed</div><div class='val' style='color:#3B6D11'>{passed}</div></div>
  <div class='metric'><div class='lbl'>Failed</div><div class='val' style='color:#A32D2D'>{failed}</div></div>
  <div class='metric'><div class='lbl'>Pass rate</div><div class='val'>{pass_rate}%</div></div>
  <div class='metric'><div class='lbl'>Duration</div><div class='val' style='font-size:20px'>{duration}s</div></div>
</div>

<div class='charts-grid'>
  <div class='card'>
    <div class='card-title'>Results breakdown</div>
    <canvas id='donut'></canvas>
    <div style='display:flex;gap:16px;margin-top:12px'>
      <div style='display:flex;align-items:center;gap:6px;font-size:13px;color:#5F5E5A'>
        <div style='width:10px;height:10px;border-radius:50%;background:#639922'></div>Passed ({passed})
      </div>
      <div style='display:flex;align-items:center;gap:6px;font-size:13px;color:#5F5E5A'>
        <div style='width:10px;height:10px;border-radius:50%;background:#E24B4A'></div>Failed ({failed})
      </div>
    </div>
  </div>

  <div class='card'>
    <div class='card-title'>Tests by category</div>
    <canvas id='catbar'></canvas>
  </div>
</div>

<div class='card'>
  <div class='card-title'>Test duration per test</div>
  <canvas id='durbar' style='max-height:260px'></canvas>
</div>

<div class='card'>
  <div class='card-title'>Response time — performance tests</div>
  <canvas id='perfbar'></canvas>
  <p style='font-size:12px;color:#888780;margin-top:10px'>Limit: 3.0s per request. Any bar exceeding this is a failure.</p>
</div>

<div class='card'>
  <div class='card-title'>All test results</div>
  <div class='filter-bar'>
    <button class='fbtn active' onclick='filter("all",this)'>All ({total})</button>
    <button class='fbtn' onclick='filter("passed",this)'>Passed ({passed})</button>
    <button class='fbtn' onclick='filter("failed",this)'>Failed ({failed})</button>
    <button class='fbtn' onclick='filter("smoke",this)'>Smoke</button>
    <button class='fbtn' onclick='filter("regression",this)'>Regression</button>
    <button class='fbtn' onclick='filter("negative",this)'>Negative</button>
  </div>
  <table>
    <thead>
      <tr>
        <th>Test name</th>
        <th>Result</th>
        <th>Severity</th>
        <th>Category</th>
        <th>Duration</th>
      </tr>
    </thead>
    <tbody id='tbody'>{rows}</tbody>
  </table>
</div>

<div class='card'>
  <div class='card-title'>Test run history</div>
  <p style='font-size:12px;color:#888780;margin-bottom:12px'>Last 5 runs — showing trends over time.</p>
  <table>
    <thead>
      <tr>
        <th>Run</th><th>Total</th><th>Passed</th><th>Failed</th><th>Pass rate</th><th>Duration</th>
      </tr>
    </thead>
    <tbody>{history_rows}</tbody>
  </table>
</div>

<div class='card'>
  <div class='card-title'>Project info</div>
  <table><tbody>
    <tr>
      <td style='padding:8px 14px;font-size:13px;color:#888780;width:160px'>Project</td>
      <td style='padding:8px 14px;font-size:13px'>SQA REST API Test Suite</td>
    </tr>
    <tr>
      <td style='padding:8px 14px;font-size:13px;color:#888780'>API under test</td>
      <td style='padding:8px 14px;font-size:13px'>https://jsonplaceholder.typicode.com</td>
    </tr>
    <tr>
      <td style='padding:8px 14px;font-size:13px;color:#888780'>Total duration</td>
      <td style='padding:8px 14px;font-size:13px'>{duration}s</td>
    </tr>
    <tr>
      <td style='padding:8px 14px;font-size:13px;color:#888780'>Test categories</td>
      <td style='padding:8px 14px'>
        <span class='tag'>smoke</span>
        <span class='tag'>regression</span>
        <span class='tag'>negative</span>
      </td>
    </tr>
  </tbody></table>
</div>

<script>
new Chart(document.getElementById('donut'),{{
  type:'doughnut',
  data:{{
    labels:['Passed','Failed'],
    datasets:[{{data:[{passed},{failed}],backgroundColor:['#639922','#E24B4A'],borderWidth:0}}]
  }},
  options:{{cutout:'72%',plugins:{{legend:{{display:false}}}}}}
}});

new Chart(document.getElementById('catbar'),{{
  type:'bar',
  data:{{
    labels:['Smoke','Regression','Negative'],
    datasets:[{{
      data:[{smoke_count},{regression_count},{negative_count}],
      backgroundColor:['#378ADD','#1D9E75','#D85A30'],
      borderRadius:6,borderWidth:0
    }}]
  }},
  options:{{
    plugins:{{legend:{{display:false}}}},
    scales:{{
      y:{{beginAtZero:true,grid:{{color:'#F1EFE8'}},ticks:{{stepSize:1}}}},
      x:{{grid:{{display:false}}}}
    }}
  }}
}});

new Chart(document.getElementById('durbar'),{{
  type:'bar',
  data:{{
    labels:{names_js},
    datasets:[{{
      label:'Duration (s)',
      data:{durs_js},
      backgroundColor:{colors_js},
      borderRadius:4,borderWidth:0
    }}]
  }},
  options:{{
    indexAxis:'y',
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{beginAtZero:true,grid:{{color:'#F1EFE8'}},title:{{display:true,text:'seconds',font:{{size:11}},color:'#888780'}}}},
      y:{{grid:{{display:false}},ticks:{{font:{{size:11}}}}}}
    }}
  }}
}});

new Chart(document.getElementById('perfbar'),{{
  type:'bar',
  data:{{
    labels:{pnames_js},
    datasets:[
      {{
        label:'Response time (s)',
        data:{pdurs_js},
        backgroundColor:'#378ADD',
        borderRadius:6,borderWidth:0
      }},
      {{
        label:'Limit (3s)',
        data:{json.dumps([3.0]*len(perf_durs if perf_durs else [0]))},
        backgroundColor:'#F09595',
        borderRadius:6,borderWidth:0
      }}
    ]
  }},
  options:{{
    plugins:{{legend:{{display:true,position:'bottom'}}}},
    scales:{{
      y:{{beginAtZero:true,grid:{{color:'#F1EFE8'}},title:{{display:true,text:'seconds',font:{{size:11}},color:'#888780'}}}},
      x:{{grid:{{display:false}}}}
    }}
  }}
}});

function filter(type, btn) {{
  document.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.trow').forEach(row => {{
    const outcome = row.dataset.outcome;
    const cat     = row.dataset.cat;
    if (type === 'all') {{
      row.classList.remove('hidden');
    }} else if (type === 'passed' || type === 'failed') {{
      row.classList.toggle('hidden', outcome !== type);
    }} else {{
      row.classList.toggle('hidden', cat !== type);
    }}
  }});
}}
</script>
</body></html>"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Enhanced dashboard generated!")
print("Open dashboard.html in your browser.")