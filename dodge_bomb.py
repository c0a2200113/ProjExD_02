import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:  # 型ヒント
    """
    オブジェクトが画面内or画面外を判定し, 真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向, 縦方向はみ出し判定結果（画面内：True/画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向
        tate = False
    return (yoko, tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_flip = pg.transform.flip(kk_img, True, False)
    kk_img0 = pg.transform.rotozoom(kk_flip, 90, 1.0)
    kk_img1 = pg.transform.rotozoom(kk_flip, 45, 1.0)
    kk_img2 = kk_flip
    kk_img3 = pg.transform.rotozoom(kk_flip, -45, 1.0)
    kk_img4 = pg.transform.rotozoom(kk_flip, -90, 1.0)
    kk_img5 = pg.transform.rotozoom(kk_img, 45, 1.0)
    kk_img6 = kk_img
    kk_img7 = pg.transform.rotozoom(kk_img, -45, 1.0)
    kk_imgs = [kk_img0, kk_img1, kk_img2, kk_img3, kk_img4, kk_img5, kk_img6, kk_img7]  # 追加機能1
    kk_rct = kk_img.get_rect()  # 練習3:こうかとんsurface
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 練習1:surfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習2:爆弾の速度
    accs = [a * 0.05 + 1 for a in range(1, 11)]  # 追加機能2:加速度のリスト

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        if kk_rct.colliderect(bb_rct):  # 練習5:衝突判定(bbとkk逆でもいい)
            print("Game Over")
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        if sum_mv[0] == 0 and sum_mv[1] == -5:  # 追加機能1:こうかとんの向き変更
            screen.blit(kk_imgs[0], kk_rct)
        elif sum_mv[0] == +5 and sum_mv[1] == -5:
            screen.blit(kk_imgs[1], kk_rct)
        elif sum_mv[0] == +5 and sum_mv[1] == 0:
            screen.blit(kk_imgs[2], kk_rct)
        elif sum_mv[0] == +5 and sum_mv[1] == +5:
            screen.blit(kk_imgs[3], kk_rct)
        elif sum_mv[0] == 0 and sum_mv[1] == +5:
            screen.blit(kk_imgs[4], kk_rct)
        elif sum_mv[0] == -5 and sum_mv[1] == +5:
            screen.blit(kk_imgs[5], kk_rct)
        elif sum_mv[0] == -5 and sum_mv[1] == -5:
            screen.blit(kk_imgs[7], kk_rct)
        else:
            screen.blit(kk_img, kk_rct)  # 練習3:こうかとんを移動
        avx, avy = accs[min(tmr//300, 9)], accs[min(tmr//300, 9)]
        if not tmr%300 and tmr//300 <= 10:
            vx *= avx  # 追加機能2:爆弾加速
            vy *= avy
        bb_rct.move_ip(vx, vy)  # 練習2:爆弾を移動
        yoko, tate =  check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たとき
            vx *= -1
        if not tate:  # 縦方向にはみ出たとき
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()