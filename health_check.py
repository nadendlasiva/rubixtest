from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure DevOps Migration Runbook</title>
    <style>
        @keyframes slideDown { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideUp   { from { opacity: 0; transform: translateY(20px);  } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn    { from { opacity: 0; } to { opacity: 1; } }
        @keyframes growBar   { from { width: 0 !important; } to { } }
        @keyframes countUp   { from { opacity: 0; transform: scale(0.6); } to { opacity: 1; transform: scale(1); } }
        @keyframes pulse     { 0%,100% { box-shadow: 0 0 0 0 rgba(0,120,212,0.35); } 50% { box-shadow: 0 0 0 5px rgba(0,120,212,0); } }
        @keyframes pulseAmber{ 0%,100% { box-shadow: 0 0 0 0 rgba(131,91,0,0.3); }  50% { box-shadow: 0 0 0 5px rgba(131,91,0,0); } }
        @keyframes shimmer   { 0% { background-position: -400px 0; } 100% { background-position: 400px 0; } }
        @keyframes gradShift { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
        @keyframes spinRing  { to { stroke-dashoffset: 0; } }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f7; min-height: 100vh; }

        /* TOP BAR */
        .top-bar {
            background: linear-gradient(90deg, #003f8a, #0078d4, #00b4d8, #0078d4, #003f8a);
            background-size: 300% 100%;
            animation: gradShift 6s ease infinite;
            color: white; padding: 12px 24px; font-size: 14px; font-weight: 600;
            display: flex; align-items: center; gap: 10px;
            box-shadow: 0 2px 10px rgba(0,120,212,0.4);
        }
        .top-bar .live-dot {
            width: 8px; height: 8px; background: #4eff91; border-radius: 50%;
            margin-left: auto; box-shadow: 0 0 6px #4eff91;
            animation: pulse 1.5s infinite;
        }
        .top-clock { font-size: 12px; font-weight: 400; opacity: 0.85; }

        /* MONITORS */
        .monitors {
            display: flex; gap: 10px; padding: 12px 24px;
            background: linear-gradient(135deg, #f0f6ff, #e8f4ff);
            border-bottom: 1px solid #d0e4f7; flex-wrap: wrap; align-items: center;
            animation: slideDown 0.5s ease;
        }
        .monitor-chip {
            display: flex; align-items: center; gap: 8px; background: white;
            border: 1px solid #d0e4f7; border-radius: 20px; padding: 6px 14px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .monitor-chip:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,120,212,0.15); }
        .av { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; transition: transform 0.2s; }
        .av:hover { transform: scale(1.15); }
        .av-blue   { background: linear-gradient(135deg,#cce4f7,#a8d4f0); color: #004f8c; }
        .av-green  { background: linear-gradient(135deg,#c0dd97,#a8cc78); color: #27500a; }
        .av-purple { background: linear-gradient(135deg,#cecbf6,#b8b4f0); color: #26215c; }
        .av-amber  { background: linear-gradient(135deg,#fac775,#f5ae50); color: #412402; }
        .chip-name { font-size: 12px; font-weight: 600; color: #1a1a1a; }
        .chip-role { font-size: 10px; color: #666; }
        .monitor-label { font-size: 11px; color: #0078d4; font-weight: 600; margin-left: auto; }

        /* STATS BAR */
        .stats-bar {
            display: flex; gap: 14px; padding: 16px 24px; background: white;
            border-bottom: 1px solid #e0e0e0; flex-wrap: wrap;
            animation: slideDown 0.6s ease;
        }
        .stat {
            background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 10px;
            padding: 10px 22px; text-align: center; min-width: 95px;
            transition: transform 0.2s, box-shadow 0.2s;
            animation: countUp 0.6s ease both;
        }
        .stat:nth-child(1) { animation-delay: 0.1s; }
        .stat:nth-child(2) { animation-delay: 0.2s; }
        .stat:nth-child(3) { animation-delay: 0.3s; }
        .stat:nth-child(4) { animation-delay: 0.4s; }
        .stat:hover { transform: translateY(-3px); box-shadow: 0 6px 18px rgba(0,0,0,0.1); }
        .stat-num { font-size: 26px; font-weight: 700; }
        .stat-lbl { font-size: 11px; color: #666; margin-top: 2px; }
        .s-blue  { color: #0078d4; }
        .s-green { color: #107c10; }
        .s-amber { color: #835b00; }
        .s-red   { color: #c50f1f; }

        /* DONUT CHART */
        .overall-ring { display: flex; align-items: center; gap: 14px; margin-left: auto; padding-right: 4px; }
        .ring-label { font-size: 11px; color: #555; line-height: 1.5; }
        .ring-pct { font-size: 18px; font-weight: 700; color: #0078d4; }

        /* CONTENT */
        .content { padding: 20px 24px; }
        .section-card {
            background: white; border: 1px solid #e0e0e0; border-radius: 12px;
            margin-bottom: 22px; overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            animation: slideUp 0.5s ease both;
        }
        .section-card:nth-child(1) { animation-delay: 0.2s; }
        .section-card:nth-child(2) { animation-delay: 0.4s; }
        .section-header {
            padding: 14px 18px; background: linear-gradient(135deg,#f0f6ff,#e2effd);
            border-bottom: 1px solid #d0e4f7; display: flex; align-items: center; gap: 10px;
        }
        .section-header h2 { font-size: 14px; font-weight: 600; color: #004f8c; }
        .section-header span { font-size: 11px; color: #666; margin-left: auto; }
        .board { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 16px; }
        .col-header { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px; margin-bottom: 10px; }
        .col-header-l { background: linear-gradient(135deg,#EEEDFE,#e0deff); border-top: 3px solid #534AB7; border-radius: 0 0 8px 8px; }
        .col-header-s { background: linear-gradient(135deg,#FAEEDA,#f5e2c0); border-top: 3px solid #854F0B; border-radius: 0 0 8px 8px; }
        .col-name-l { font-size: 13px; font-weight: 600; color: #26215c; }
        .col-name-s { font-size: 13px; font-weight: 600; color: #412402; }
        .col-role { font-size: 10px; color: #666; margin-top: 1px; }
        .cnt { margin-left: auto; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
        .cnt-l { background: #CECBF6; color: #26215c; }
        .cnt-s { background: #FAC775; color: #412402; }

        /* TASK CARDS */
        .task {
            background: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px;
            padding: 12px; margin-bottom: 8px;
            transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
            animation: fadeIn 0.4s ease both;
        }
        .task:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,0.1); background: white; }
        .task:last-child { margin-bottom: 0; }
        .tid { font-size: 10px; color: #0078d4; font-weight: 600; margin-bottom: 3px; }
        .ttitle { font-size: 12px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; line-height: 1.4; }
        .tfields { border-top: 1px solid #f0f0f0; padding-top: 7px; display: flex; flex-direction: column; gap: 4px; }
        .trow { display: flex; justify-content: space-between; align-items: center; }
        .tkey { font-size: 10px; color: #666; }

        /* BADGES */
        .badge { font-size: 9px; font-weight: 600; padding: 3px 9px; border-radius: 20px; }
        .b-done { background: #dff6dd; color: #107c10; }
        .b-prog {
            background: #cce4f7; color: #004f8c;
            animation: pulse 2s infinite;
        }
        .b-pend {
            background: #fff4ce; color: #835b00;
            animation: pulseAmber 2.5s infinite;
        }
        .risk-l { font-size: 9px; font-weight: 600; padding: 3px 9px; border-radius: 20px; background: #dff6dd; color: #107c10; }
        .risk-m { font-size: 9px; font-weight: 600; padding: 3px 9px; border-radius: 20px; background: #fff4ce; color: #835b00; }
        .risk-h { font-size: 9px; font-weight: 600; padding: 3px 9px; border-radius: 20px; background: #fde7e9; color: #c50f1f; }
        .dval { font-size: 9px; color: #666; font-style: italic; }

        /* PROGRESS BARS */
        .prog { height: 5px; background: #e8e8e8; border-radius: 3px; margin-top: 9px; overflow: hidden; }
        .pf {
            height: 100%; border-radius: 3px;
            animation: growBar 1.2s cubic-bezier(0.4,0,0.2,1) both;
        }
        .pf-g {
            background: linear-gradient(90deg, #107c10, #4eca5a);
            width: 100%;
            box-shadow: 0 0 6px rgba(16,124,16,0.4);
        }
        .pf-b {
            background: linear-gradient(90deg, #0078d4, #00b4d8);
            box-shadow: 0 0 6px rgba(0,120,212,0.4);
        }
        .pf-p {
            background: linear-gradient(90deg, #5c2d91, #9b59b6);
            box-shadow: 0 0 6px rgba(92,45,145,0.4);
        }
        .pf-a {
            background: linear-gradient(90deg, #835b00, #d4a017);
            box-shadow: 0 0 6px rgba(131,91,0,0.4);
        }

        /* SHIMMER for completed bars */
        .pf-g::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.5) 50%, transparent 100%);
            background-size: 400px 100%;
            animation: shimmer 2s infinite;
        }
        .pf-g { position: relative; }

        footer {
            text-align: center; padding: 18px; color: #888; font-size: 11px;
            border-top: 1px solid #e0e0e0; background: white; margin-top: 8px;
            animation: fadeIn 1s ease;
        }
    </style>
</head>
<body>

<div class="top-bar">&#9651; Azure DevOps Migration Runbook &nbsp;|&nbsp; Classic Pipeline Migration <span class="top-clock" id="clock"></span><div class="live-dot"></div></div>

<div class="monitors">
    <div class="monitor-chip">
        <div class="av av-blue">VR</div>
        <div><div class="chip-name">Vivek R</div><div class="chip-role">Project Manager</div></div>
    </div>
    <div class="monitor-chip">
        <div class="av av-green">AK</div>
        <div><div class="chip-name">Akshay</div><div class="chip-role">Tech Lead</div></div>
    </div>
    <div class="monitor-label">&#128065; Monitoring all tasks</div>
</div>

<div class="stats-bar">
    <div class="stat"><div class="stat-num s-blue" data-target="18">0</div><div class="stat-lbl">Total tasks</div></div>
    <div class="stat"><div class="stat-num s-green" data-target="4">0</div><div class="stat-lbl">Completed</div></div>
    <div class="stat"><div class="stat-num s-amber" data-target="10">0</div><div class="stat-lbl">In progress</div></div>
    <div class="stat"><div class="stat-num s-red" data-target="4">0</div><div class="stat-lbl">Pending</div></div>
    <div class="overall-ring">
        <svg width="54" height="54" viewBox="0 0 54 54">
            <circle cx="27" cy="27" r="22" fill="none" stroke="#e0e0e0" stroke-width="5"/>
            <circle id="ring-arc" cx="27" cy="27" r="22" fill="none" stroke="#0078d4" stroke-width="5"
                stroke-linecap="round" stroke-dasharray="138.23" stroke-dashoffset="138.23"
                transform="rotate(-90 27 27)" style="transition: stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1);"/>
            <text x="27" y="32" text-anchor="middle" font-size="11" font-weight="700" fill="#0078d4" id="ring-txt">0%</text>
        </svg>
        <div class="ring-label">Overall<br><span class="ring-pct">Progress</span></div>
    </div>
</div>

<div class="content">

    <div class="section-card">
        <div class="section-header">
            <h2>&#127970; Runbook 1 &mdash; Full organization migration (tenant to tenant)</h2>
            <span>9 tasks</span>
        </div>
        <div class="board">
            <div>
                <div class="col-header col-header-l">
                    <div class="av av-purple">L</div>
                    <div><div class="col-name-l">Lenin</div><div class="col-role">DevOps Engineer</div></div>
                    <span class="cnt cnt-l">5</span>
                </div>
                <div class="task">
                    <div class="tid">#ORG-001</div>
                    <div class="ttitle">Inventory all projects, repos & pipelines in source org</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-done">Completed</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">None</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-g"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-002</div>
                    <div class="ttitle">Create new Azure DevOps org in target tenant</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-done">Completed</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-001</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-g"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-003</div>
                    <div class="ttitle">Migrate all Git repositories to target org</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-002</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-b" style="width:70%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-004</div>
                    <div class="ttitle">Export & recreate classic pipelines in target org</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-h">High</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-003</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-b" style="width:40%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-005</div>
                    <div class="ttitle">Validate & run all pipelines end-to-end in target</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-pend">Pending</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-h">High</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-004</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-a" style="width:10%"></div></div>
                </div>
            </div>
            <div>
                <div class="col-header col-header-s">
                    <div class="av av-amber">S</div>
                    <div><div class="col-name-s">Siva</div><div class="col-role">Cloud Engineer</div></div>
                    <span class="cnt cnt-s">4</span>
                </div>
                <div class="task">
                    <div class="tid">#ORG-006</div>
                    <div class="ttitle">Migrate service connections & variable groups</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-002</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-b" style="width:50%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-007</div>
                    <div class="ttitle">Reassign users & permissions in target org</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-006</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-b" style="width:40%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-008</div>
                    <div class="ttitle">Migrate agent pools & self-hosted agents</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-pend">Pending</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-007</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-a" style="width:15%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#ORG-009</div>
                    <div class="ttitle">Decommission source org after cutover sign-off</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-pend">Pending</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-h">High</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">ORG-005</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-a" style="width:5%"></div></div>
                </div>
            </div>
        </div>
    </div>

    <div class="section-card">
        <div class="section-header">
            <h2>&#128193; Runbook 2 &mdash; Single project migration (org to org)</h2>
            <span>9 tasks</span>
        </div>
        <div class="board">
            <div>
                <div class="col-header col-header-l">
                    <div class="av av-purple">L</div>
                    <div><div class="col-name-l">Lenin</div><div class="col-role">DevOps Engineer</div></div>
                    <span class="cnt cnt-l">5</span>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-001</div>
                    <div class="ttitle">Export project data — repos, boards, pipelines</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-done">Completed</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">None</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-g"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-002</div>
                    <div class="ttitle">Create target project in destination org</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-done">Completed</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-001</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-g"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-003</div>
                    <div class="ttitle">Migrate repos & branch policies to target project</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-002</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-p" style="width:60%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-004</div>
                    <div class="ttitle">Recreate classic build & release pipelines</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-h">High</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-003</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-p" style="width:35%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-005</div>
                    <div class="ttitle">Test all pipelines & validate deployment gates</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-pend">Pending</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-h">High</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-004</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-a" style="width:5%"></div></div>
                </div>
            </div>
            <div>
                <div class="col-header col-header-s">
                    <div class="av av-amber">S</div>
                    <div><div class="col-name-s">Siva</div><div class="col-role">Cloud Engineer</div></div>
                    <span class="cnt cnt-s">4</span>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-006</div>
                    <div class="ttitle">Migrate work items & backlogs to target project</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-002</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-p" style="width:55%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-007</div>
                    <div class="ttitle">Recreate service connections & environments</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-002</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-p" style="width:45%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-008</div>
                    <div class="ttitle">Add team members & set permissions in target</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-prog">In progress</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-l">Low</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-007</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-p" style="width:30%"></div></div>
                </div>
                <div class="task">
                    <div class="tid">#PRJ-009</div>
                    <div class="ttitle">Archive source project & notify stakeholders</div>
                    <div class="tfields">
                        <div class="trow"><span class="tkey">Status</span><span class="badge b-pend">Pending</span></div>
                        <div class="trow"><span class="tkey">Risk</span><span class="risk-m">Medium</span></div>
                        <div class="trow"><span class="tkey">Dependency</span><span class="dval">PRJ-005</span></div>
                    </div>
                    <div class="prog"><div class="pf pf-a" style="width:5%"></div></div>
                </div>
            </div>
        </div>
    </div>

</div>

<footer>
    Deployed via Azure DevOps &nbsp;|&nbsp; Migration Runbook &nbsp;|&nbsp; Version 6.0 &nbsp;|&nbsp; Monitor: Vivek R &amp; Akshay
</footer>

<script>
    // Live clock
    function updateClock() {
        const now = new Date();
        document.getElementById('clock').textContent =
            now.toLocaleTimeString('en-GB', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
    }
    updateClock(); setInterval(updateClock, 1000);

    // Counter animation
    document.querySelectorAll('.stat-num[data-target]').forEach(el => {
        const target = parseInt(el.dataset.target);
        let current = 0;
        const step = Math.ceil(target / 20);
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current;
            if (current >= target) clearInterval(timer);
        }, 40);
    });

    // Donut ring (4 completed / 18 total = 22.2%)
    window.addEventListener('load', () => {
        const completed = 4, total = 18;
        const pct = completed / total;
        const circumference = 2 * Math.PI * 22; // 138.23
        const offset = circumference * (1 - pct);
        const arc = document.getElementById('ring-arc');
        const txt = document.getElementById('ring-txt');
        setTimeout(() => {
            arc.style.strokeDashoffset = offset;
            let count = 0;
            const target = Math.round(pct * 100);
            const t = setInterval(() => {
                count++;
                txt.textContent = count + '%';
                if (count >= target) clearInterval(t);
            }, 60);
        }, 300);
    });

    // Stagger task card animations
    document.querySelectorAll('.task').forEach((card, i) => {
        card.style.animationDelay = (0.05 * i + 0.3) + 's';
    });
</script>
</body>
</html>
"""

@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "6.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)