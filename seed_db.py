import sys
import os
from app import create_app, get_db

def seed_fortunes(db):
    """加入假籤詩資料"""
    fortunes_data = [
        # 綜合運勢
        ('綜合運勢', '上上籤', '春雷震起蟄中蟲\n脫卻塵凡出舊墉\n忽遇風雲交際處\n自然變化得成龍', '一切進展順利，有谷底翻身、煥然一新之象。把握良機，自然能大展宏圖。', '目前正是運勢大好的時機，大膽去實踐心中的計畫吧！'),
        ('綜合運勢', '中籤', '欲求勝事可非常\n爭奈親姻暗作防\n到頭必有貴人助\n何須用盡己心腸', '事情一開始可能會遇到阻礙或他人的反對，但最終會有貴人相助而化險為夷。', '順其自然，不要固執己見，留意身邊願意幫助你的人。'),
        ('綜合運勢', '下下籤', '此事必定兩相連\n未見成時見敗前\n不是一枝好花意\n任他春色亦徒然', '目前局勢不利，強求也無法得到好結果。', '建議暫緩計畫，靜待時機，目前以守成為主。'),
        
        # 感情
        ('感情', '上籤', '天配良緣本有緣\n何須反覆問青天\n但得兩心相印處\n千里姻緣一線牽', '如果是單身，將會遇見理想對象；若有伴侶，感情將會十分融洽。', '保持開放與真誠的心，緣分自然會到來。'),
        ('感情', '下籤', '有意栽花花不發\n無心插柳柳成蔭\n若是強求難如意\n不如退步得清心', '目前的感情狀態強求無益，過度執著反而會帶來痛苦。', '退一步海闊天空，先好好愛自己，對的人會在對的時間出現。'),
        
        # 事業
        ('事業', '上上籤', '財運亨通步步高\n貴人相助樂滔滔\n若問前程何處去\n金光閃閃在今朝', '事業發展如日中天，有升職加薪或創業成功的機會。', '積極展現自己的能力，這是你發光發熱的時刻。'),
        ('事業', '中籤', '一番風雨一番晴\n半是憂疑半是明\n但得守舊方無事\n若要求新必有驚', '工作上會有一些小波折，但最終能穩定下來。', '不宜貿然轉換跑道或進行高風險的投資，穩紮穩打為上策。'),
    ]
    
    cursor = db.cursor()
    # 檢查是否已有資料
    cursor.execute("SELECT COUNT(*) as count FROM fortunes")
    if cursor.fetchone()['count'] == 0:
        cursor.executemany(
            "INSERT INTO fortunes (category, level, poem, interpretation, advice) VALUES (?, ?, ?, ?, ?)",
            fortunes_data
        )
        print("✅ 成功寫入籤詩種子資料")

def seed_tarots(db):
    """加入假塔羅牌資料"""
    tarots_data = [
        ('愚者', '/static/images/tarot/00_fool.jpg', '新的開始、冒險、天真、可能性', '魯莽、過度理想化、錯失良機、逃避責任', '這是一張代表無限可能的牌。愚者站在懸崖邊，象徵著即將踏上未知的旅程。'),
        ('魔術師', '/static/images/tarot/01_magician.jpg', '創造力、意志力、溝通、自信', '運用不當的資源、缺乏自信、欺騙、溝通不良', '魔術師擁有將想法轉化為現實的能力，代表你具備解決眼前問題的資源與能力。'),
        ('女祭司', '/static/images/tarot/02_high_priestess.jpg', '直覺、潛意識、智慧、神祕', '忽略直覺、表面化、隱藏的敵人、情緒壓抑', '女祭司象徵內在的智慧與直覺。現在是傾聽內心聲音、向內尋求指引的時候。'),
        ('戀人', '/static/images/tarot/06_lovers.jpg', '愛情、和諧、選擇、價值觀對齊', '關係不和、錯誤的選擇、誘惑、價值觀衝突', '戀人牌不僅代表愛情，也象徵著面臨重大選擇，需要你誠實面對自己的內心。'),
        ('命運之輪', '/static/images/tarot/10_wheel_of_fortune.jpg', '轉機、變化、好運、順其自然', '運氣不佳、抗拒改變、失去控制、低潮', '這張牌提醒我們世事無常，一切都在改變。順應命運的浪潮，好的轉機即將到來。'),
    ]
    
    cursor = db.cursor()
    # 檢查是否已有資料
    cursor.execute("SELECT COUNT(*) as count FROM tarots")
    if cursor.fetchone()['count'] == 0:
        cursor.executemany(
            "INSERT INTO tarots (name, image_url, upright_meaning, reversed_meaning, description) VALUES (?, ?, ?, ?, ?)",
            tarots_data
        )
        print("✅ 成功寫入塔羅牌種子資料")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db = get_db()
        seed_fortunes(db)
        seed_tarots(db)
        db.commit()
        print("🎉 資料庫初始化與種子資料寫入完成！")
