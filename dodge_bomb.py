import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
key_dict={#移動量の辞書
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0)
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect，または，爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img2=pg.transform.flip(kk_img,True,False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct=bb_img.get_rect()
    bb_rct.center=(random.randint(0,1600),random.randint(0,900))
    vx,vy=+5,+5#横縦方向の速度ベクトル
    bb_img.set_colorkey((0, 0, 0))
    font=pg.font.Font(None,80)
    tmr = 0
    kk_imgX=kk_img
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in key_dict.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct.move_ip(vx,vy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy*=-1
        kk_imgX=sum_check(sum_mv)
        screen.blit(bb_img,bb_rct)
        screen.blit(kk_imgX, kk_rct)
        if kk_rct.colliderect(bb_rct):
            return
        pg.display.update()
        tmr += 1
        clock.tick(50)
def sum_check(sum_mv:list)->pg.Surface:
    """
    引数：sum_mv(移動ベクトルの合計)
    戻り値：こうかとんの画像
    sum_mvによって戻り値のこうかとんの画像が変化する。
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img2=pg.transform.flip(kk_img,True,False)
    kk_dict={ #移動方向の辞書
        (0,-5):pg.transform.rotozoom(kk_img2,90,1.0),
        (5,-5): pg.transform.rotozoom(kk_img2,45,1.0),
        (5,0):pg.transform.rotozoom(kk_img2,0,1.0),
        (5,5):pg.transform.rotozoom(kk_img2,-45,1.0),
        (0,5):pg.transform.rotozoom(kk_img2,-90,1.0),
        (-5,5):pg.transform.rotozoom(kk_img,45,1.0),
        (-5,0):pg.transform.rotozoom(kk_img,0,1.0),
        (-5,-5):pg.transform.rotozoom(kk_img,-45,1.0)
    }
    if sum_mv == [0,0]:
        kk_imgX=pg.image.load("fig/pg_bg.jpg")
        kk_imgX=pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    else:
        kk_imgX = kk_dict[tuple(sum_mv)]
    return kk_imgX




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
