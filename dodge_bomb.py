import os
import sys
import pygame as pg
import random
import math


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

def bomb_runk()->tuple[int,pg.Surface]:
    """
    引数：なし
    戻り値：速度のリストと爆弾の画像のリストのタプル
    1~10段階までのそれぞれの値のリストを作って返す関数
    """
    accs=[a for a in range(1,11)]
    bb_imgs=[]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return accs,bb_imgs

def Gameover(screen:pg.Surface):
    """
    引数：screen(pg.sruface)
    戻り値：なし
    ゲームオーバーの画面を表示
    """
    sikaku = pg.Surface((1600, 900), pg.SRCALPHA)
    sikaku.fill((0, 0, 0, 150))  # 半透明の黒
    screen.blit(sikaku, (0, 0))
    
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(800, 450))
    screen.blit(text, text_rect)

    kn_img=bg_img = pg.image.load("fig/7.png")
    kn_rect = kn_img.get_rect(center=(550, 450))
    kn_rect2 = text.get_rect(center=(1200, 450))
    screen.blit(kn_img,kn_rect)
    screen.blit(kn_img,kn_rect2) 
    
    screen.set_alpha(150)
    
    pg.display.update()
    pg.time.wait(2500)

def shearhartatack(kk_rct,bb_rct):
    yokobeku=(kk_rct[0]-bb_rct[0])**2
    tatebeku=(kk_rct[1]-bb_rct[1])**2
    norm=math.sqrt(yokobeku+tatebeku)
    targetnorm=math.sqrt(50)
    wari=norm/targetnorm
    tatebeku*=wari
    yokobeku*=wari
    if norm<300:
        tatebeku=1
        yokobeku=1
    return tatebeku,yokobeku






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
    bb_rct.center=(random.randint(0,1599),random.randint(0,899))
    vx,vy=+5,+5#横縦方向の速度ベクトル
    bb_img.set_colorkey((0, 0, 0))
    font=pg.font.Font(None,80)
    x=0
    tmr = 0
    kk_imgX=kk_img
    avx=0
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
        accs,bb_imgs=bomb_runk()
        avx=vx*accs[min(tmr//500,9)]
        bb_img=bb_imgs[min(tmr//500,9)]
        bb_rct.move_ip(avx,vy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy*=-1
        vvx,vvy=shearhartatack(kk_rct,bb_rct)
        kk_imgX=sum_check(sum_mv)
        x+=1
        txt=font.render("SCORE"+str(x),True,(0,0,0))
        screen.blit(bb_img,bb_rct)
        screen.blit(kk_imgX, kk_rct)
        screen.blit(txt,[200,100])
        if kk_rct.colliderect(bb_rct):
            Gameover(screen)
            return
        pg.display.update()
        print(bb_rct)
        tmr += 1
        clock.tick(50)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
