import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Animal Hospital Roblox 2.5D", layout="centered")

st.title("Animal Hospital - Roblox 2.5D")
st.write("Phien ban nang cấp: Nhan vat thu, quay tiep tan, benh nhan va nut dieu khien tren man hinh")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Animal Hospital Deluxe</title>
    <style>
        body {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 5px;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.8);
            border: 2px solid #334155;
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: linear-gradient(135deg, #1e293b, #0f172a);
        }
        #ui-panel {
            margin-top: 6px;
            background: rgba(15, 23, 42, 0.95);
            padding: 8px 12px;
            border: 1px solid #475569;
            border-radius: 6px;
            font-size: 11px;
            width: 740px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
        #control-pad {
            margin-top: 6px;
            display: grid;
            grid-template-columns: repeat(3, 50px);
            gap: 5px;
            justify-content: center;
        }
        .ctrl-btn {
            background-color: #334155;
            color: #f8fafc;
            border: 1px solid #64748b;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            user-select: none;
        }
        .ctrl-btn:active {
            background-color: #38bdf8;
            color: #0f172a;
        }
        #dialogue-box {
            margin-top: 6px;
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #38bdf8;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            color: #e2e8f0;
            width: 740px;
            min-height: 40px;
        }
        .speaker {
            font-weight: bold;
            color: #38bdf8;
            margin-bottom: 2px;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" height="320" width="740"></canvas>
    </div>
    
    <div id="ui-panel">
        <div>CA TRUC: <span id="shift-txt">1</span></div>
        <div>SANITY: <span id="sanity-txt">100</span>%</div>
        <div>TIEN: $<span id="money-txt">200</span></div>
        <div>BENH NHAN: <span id="patient-txt">3</span></div>
    </div>

    <div id="dialogue-box">
        <div class="speaker" id="dialogue-speaker">QUAY TIEP TAN</div>
        <div id="dialogue-text">Chao mung bac si thu y den benh vien! Hay di chuyen den cac khu vuc de kham chua benh.</div>
    </div>

    <!-- Nut dieu khien tren man hinh cho dien thoại -->
    <div id="control-pad">
        <div></div>
        <button class="ctrl-btn" onclick="movePlayer(0, -0.5)">LÊN</button>
        <div></div>
        <button class="ctrl-btn" onclick="movePlayer(-0.5, 0)">TRÁI</button>
        <button class="ctrl-btn" onclick="movePlayer(0, 0.5)">XUỐNG</button>
        <button class="ctrl-btn" onclick="movePlayer(0.5, 0)">PHẢI</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const TILE_W = 56;
        const TILE_H = 28;
        const MAP_SIZE = 9;
        const ORIGIN_X = canvas.width / 2;
        const ORIGIN_Y = 35;

        let sanity = 100;
        let money = 200;
        let activePatients = 3;

        function isoToScreen(gx, gy) {
            return {
                x: ORIGIN_X + (gx - gy) * (TILE_W / 2),
                y: ORIGIN_Y + (gx + gy) * (TILE_H / 2)
            };
        }

        function drawIsoBlock(gx, gy, cTop, cLeft, cRight, height = 0) {
            const pos = isoToScreen(gx, gy);
            const topY = pos.y - height;

            ctx.beginPath();
            ctx.moveTo(pos.x, topY);
            ctx.lineTo(pos.x + TILE_W / 2, topY + TILE_H / 2);
            ctx.lineTo(pos.x, topY + TILE_H);
            ctx.lineTo(pos.x - TILE_W / 2, topY + TILE_H / 2);
            ctx.closePath();
            ctx.fillStyle = cTop;
            ctx.fill();
            ctx.strokeStyle = 'rgba(255,255,255,0.08)';
            ctx.stroke();

            if (height > 0) {
                ctx.beginPath();
                ctx.moveTo(pos.x - TILE_W / 2, topY + TILE_H / 2);
                ctx.lineTo(pos.x, topY + TILE_H);
                ctx.lineTo(pos.x, pos.y + TILE_H);
                ctx.lineTo(pos.x - TILE_W / 2, pos.y + TILE_H / 2);
                ctx.closePath();
                ctx.fillStyle = cLeft;
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(pos.x, topY + TILE_H);
                ctx.lineTo(pos.x + TILE_W / 2, topY + TILE_H / 2);
                ctx.lineTo(pos.x + TILE_W / 2, pos.y + TILE_H / 2);
                ctx.lineTo(pos.x, pos.y + TILE_H);
                ctx.closePath();
                ctx.fillStyle = cRight;
                ctx.fill();
            }
        }

        // Nhan vat chinh la Thu Y (Hinh dang thu dang yeu)
        class Player {
            constructor(gx, gy) {
                this.gx = gx;
                this.gy = gy;
            }
            draw() {
                const p = isoToScreen(this.gx, this.gy);
                // Bong
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y + 12, 8, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                // Than thu (mau cam sang)
                ctx.fillStyle = '#f97316';
                ctx.fillRect(p.x - 5, p.y - 14, 10, 12);
                // Dau thu
                ctx.fillStyle = '#fb923c';
                ctx.beginPath();
                ctx.arc(p.x, p.y - 18, 5, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        // NPC la cac dong vat trong game Roblox
        class NPC {
            constructor(name, gx, gy, color, role) {
                this.name = name;
                this.gx = gx;
                this.gy = gy;
                this.color = color;
                this.role = role;
            }
            draw() {
                const p = isoToScreen(this.gx, this.gy);
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y + 12, 8, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = this.color;
                ctx.fillRect(p.x - 5, p.y - 14, 10, 12);
                ctx.fillStyle = '#cbd5e1';
                ctx.beginPath();
                ctx.arc(p.x, p.y - 18, 4, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.font = '8px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.name, p.x, p.y - 25);
            }
        }

        const player = new Player(1, 1);

        const npcs = [
            new NPC("Dr. Harlow", 2, 1, "#a855f7", "Truong khoa: Chuc ca truc thuan loi!"),
            new NPC("Ratthew", 1, 4, "#64748b", "Benh nhan Ratthew: Toi dang tim em gai Rattina."),
            new NPC("Ron", 4, 1, "#3b82f6", "Ke toan Ron: Quan ly tai chinh benh vien tot nhe."),
            new NPC("Barney", 6, 2, "#e2e8f0", "Barney: Cho toi xin ly ca phe nong."),
            new NPC("Duckman", 7, 2, "#eab308", "Canh sat Duckman: Dang truy bat nghi pham."),
            new NPC("Liz", 2, 7, "#f59e0b", "Phong vien Liz: Dung Camera UV de soi di the."),
            new NPC("Shop Nurse", 7, 6, "#ec4899", "Y ta cua hang: Chuyen cung cấp vat pham y te.")
        ];

        function setDialogue(speaker, text) {
            document.getElementById('dialogue-speaker').innerText = speaker.toUpperCase();
            document.getElementById('dialogue-text').innerText = text;
        }

        function movePlayer(dx, dy) {
            let nextX = Math.max(0, Math.min(MAP_SIZE - 1, player.gx + dx));
            let nextY = Math.max(0, Math.min(MAP_SIZE - 1, player.gy + dy));
            player.gx = nextX;
            player.gy = nextY;
            checkInteractions();
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp' || e.key === 'w') movePlayer(0, -0.5);
            if (e.key === 'ArrowDown' || e.key === 's') movePlayer(0, 0.5);
            if (e.key === 'ArrowLeft' || e.key === 'a') movePlayer(-0.5, 0);
            if (e.key === 'ArrowRight' || e.key === 'd') movePlayer(0.5, 0);
        });

        function checkInteractions() {
            let interacted = false;
            npcs.forEach(npc => {
                const dist = Math.hypot(player.gx - npc.gx, player.gy - npc.gy);
                if (dist < 1.0) {
                    setDialogue(npc.name, npc.text);
                    interacted = true;
                }
            });

            if (!interacted) {
                // Kiem tra khu vuc quay tiep tan hoac giuong benh
                if (player.gx >= 3 && player.gx <= 5 && player.gy >= 3 && player.gy <= 5) {
                    setDialogue("KHU VUC BENH NHAN", "Dang dieu tri cho benh nhan thu cung. Nhan tien thuong!");
                    money += 10;
                    document.getElementById('money-txt').innerText = money;
                } else {
                    setDialogue("BENH VIEN", "Khu vực hanh lang va quay tiep tan chinh.");
                }
            }
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Ve ban do san nha 2.5D
            for (let gx = 0; gx < MAP_SIZE; gx++) {
                for (let gy = 0; gy < MAP_SIZE; gy++) {
                    const isEven = (gx + gy) % 2 === 0;
                    drawIsoBlock(gx, gy, isEven ? '#334155' : '#1e293b', '#0f172a', '#0f172a', 0);
                }
            }

            // Ve Quay tiep tan (Reception Desk) o trung tam
            drawIsoBlock(4, 3, '#0284c7', '#0369a1', '#075985', 10);
            drawIsoBlock(4, 4, '#38bdf8', '#0284c7', '#0369a1', 12); // Ban tiep tan chinh

            // Ve Cac giuong benh nhan thu cung xung quanh
            drawIsoBlock(2, 3, '#f43f5e', '#be123c', '#881337', 6);
            drawIsoBlock(6, 4, '#10b981', '#047857', '#065f46', 6);

            const renderList = [];

            npcs.forEach(npc => {
                renderList.push({
                    depth: npc.gx + npc.gy,
                    draw: () => npc.draw()
                });
            });

            renderList.push({
                depth: player.gx + player.gy,
                draw: () => player.draw()
            });

            renderList.sort((a, b) => a.depth - b.depth);
            renderList.forEach(item => item.draw());

            requestAnimationFrame(render);
        }

        render();
    </script>
</body>
</html>
"""

components.html(game_html, height=480)
