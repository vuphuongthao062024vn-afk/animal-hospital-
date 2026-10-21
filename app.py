import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Animal Hospital Roblox 2.5D", layout="centered")

st.title("Animal Hospital - Roblox 2.5D")
st.write("He thong quan ly benh vien, NPC va cua hang day du")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Animal Hospital Full Game</title>
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
            padding: 10px;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 2px solid #334155;
        }
        canvas {
            display: block;
            background-color: #1e293b;
        }
        #ui-panel {
            margin-top: 8px;
            background: rgba(15, 23, 42, 0.9);
            padding: 8px 12px;
            border: 1px solid #475569;
            font-size: 12px;
            width: 760px;
            display: flex;
            justify-content: space-between;
        }
        #shop-panel {
            margin-top: 6px;
            background: rgba(30, 41, 59, 0.95);
            border: 1px solid #38bdf8;
            padding: 6px 12px;
            font-size: 12px;
            width: 760px;
            text-align: center;
        }
        #dialogue-box {
            margin-top: 6px;
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #38bdf8;
            padding: 8px;
            font-size: 12px;
            color: #e2e8f0;
            width: 760px;
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
        <canvas id="gameCanvas" height="340" width="760"></canvas>
    </div>
    <div id="ui-panel">
        <div>CA TRUC: <span id="shift-txt">1</span></div>
        <div>SANITY: <span id="sanity-txt">100</span>%</div>
        <div>TIEN: $<span id="money-txt">150</span></div>
        <div>DI THE: <span id="anomaly-txt">0</span></div>
    </div>
    <div id="shop-panel">
        CUA HANG Y TA: [1] Mua Camera UV ($50) | [2] Mua Si-ro Phong ($40) | [3] Mua Ca Phe ($30)
    </div>
    <div id="dialogue-box">
        <div class="speaker" id="dialogue-speaker">DR. HARLOW</div>
        <div id="dialogue-text">Chao mung den voi ca trực. Hay di chuyen va kiem tra cac khu vực!</div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const TILE_W = 60;
        const TILE_H = 30;
        const MAP_SIZE = 9;
        const ORIGIN_X = canvas.width / 2;
        const ORIGIN_Y = 40;

        let sanity = 100;
        let money = 150;
        let anomaliesFound = 0;

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
            ctx.strokeStyle = 'rgba(0,0,0,0.2)';
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

        class Player {
            constructor(gx, gy) {
                this.gx = gx;
                this.gy = gy;
            }
            draw() {
                const p = isoToScreen(this.gx, this.gy);
                ctx.fillStyle = 'rgba(0,0,0,0.3)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y + 14, 9, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#0284c7';
                ctx.fillRect(p.x - 5, p.y - 18, 10, 14);
                ctx.fillStyle = '#fde047';
                ctx.beginPath();
                ctx.arc(p.x, p.y - 22, 5, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        class NPC {
            constructor(name, gx, gy, color, text) {
                this.name = name;
                this.gx = gx;
                this.gy = gy;
                this.color = color;
                this.text = text;
            }
            draw() {
                const p = isoToScreen(this.gx, this.gy);
                ctx.fillStyle = 'rgba(0,0,0,0.3)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y + 14, 9, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = this.color;
                ctx.fillRect(p.x - 6, p.y - 16, 12, 12);
                ctx.fillStyle = '#ffed4a';
                ctx.beginPath();
                ctx.arc(p.x, p.y - 20, 5, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.font = '8px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.name, p.x, p.y - 28);
            }
        }

        const player = new Player(1, 1);

        const npcs = [
            new NPC("Dr. Harlow", 2, 1, "#e2e8f0", "Dr. Harlow: Hoan thanh tot nhiem vu ca truc nhe!"),
            new NPC("Ratthew", 1, 4, "#334155", "Ratthew: Toi dang tim em gai Rattina trong benh vien nay."),
            new NPC("Ron Accounting", 4, 1, "#3b82f6", "Ron Ke Toan: Dung quen kiem tra so sach tai chinh."),
            new NPC("Barney", 6, 2, "#f8fafc", "Barney: Cho xin coc ca phe va tranh canh sat Duckman."),
            new NPC("Officer Duckman", 7, 2, "#eab308", "Duckman: Toi dang truy bat con tho Barney."),
            new NPC("Liz Reporter", 2, 7, "#d97706", "Liz: Su dung Camera UV de soi di the an."),
            new NPC("Shop Nurse", 7, 6, "#ec4899", "Y Ta Cua Hang: Chao mung quy khach den voi shop vat pham!"),
            new NPC("Hazmat Staff", 5, 7, "#f97316", "Hazmat: Khu vực cach ly an toan sinh hoc.")
        ];

        let bedMonsterActive = false;

        function setDialogue(speaker, text) {
            document.getElementById('dialogue-speaker').innerText = speaker.toUpperCase();
            document.getElementById('dialogue-text').innerText = text;
        }

        window.addEventListener('keydown', (e) => {
            let nextX = player.gx;
            let nextY = player.gy;

            if (e.key === 'ArrowUp' || e.key === 'w') nextY -= 0.5;
            if (e.key === 'ArrowDown' || e.key === 's') nextY += 0.5;
            if (e.key === 'ArrowLeft' || e.key === 'a') nextX -= 0.5;
            if (e.key === 'ArrowRight' || e.key === 'd') nextX += 0.5;

            if (nextX >= 0 && nextX < MAP_SIZE && nextY >= 0 && nextY < MAP_SIZE) {
                player.gx = nextX;
                player.gy = nextY;
            }

            // Mua vat pham trong shop
            if (e.key === '1' && money >= 50) { money -= 50; alert("Da mua Camera UV!"); }
            if (e.key === '2' && money >= 40) { money -= 40; alert("Da mua Si-ro Phong!"); }
            if (e.key === '3' && money >= 30) { money -= 30; alert("Da mua Ca Phe!"); }
            document.getElementById('money-txt').innerText = money;

            checkInteractions();
        });

        function checkInteractions() {
            let nearAny = false;
            npcs.forEach(npc => {
                const dist = Math.hypot(player.gx - npc.gx, player.gy - npc.gy);
                if (dist < 1.0) {
                    setDialogue(npc.name, npc.text);
                    nearAny = true;
                }
            });

            if (!nearAny) {
                if (player.gx > 3 && player.gx < 5 && player.gy > 3 && player.gy < 5) {
                    if (bedMonsterActive) {
                        setDialogue("GHI CHU", "Phat hien di the: Quai vat duoi giuong benh!");
                        sanity = Math.max(0, sanity - 2);
                        document.getElementById('sanity-txt').innerText = sanity;
                    } else {
                        setDialogue("PHONG BENH", "Giuong benh an toan, khong co di the.");
                    }
                }
            }
        }

        setInterval(() => {
            bedMonsterActive = Math.random() < 0.4;
            if (Math.random() < 0.25) {
                anomaliesFound++;
                document.getElementById('anomaly-txt').innerText = anomaliesFound;
            }
        }, 5000);

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let gx = 0; gx < MAP_SIZE; gx++) {
                for (let gy = 0; gy < MAP_SIZE; gy++) {
                    const isEven = (gx + gy) % 2 === 0;
                    const cTop = isEven ? '#334155' : '#1e293b';
                    drawIsoBlock(gx, gy, cTop, '#0f172a', '#0f172a', 0);
                }
            }

            drawIsoBlock(4, 4, bedMonsterActive ? '#991b1b' : '#38bdf8', '#0284c7', '#0369a1', 8);

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

components.html(game_html, height=440)

