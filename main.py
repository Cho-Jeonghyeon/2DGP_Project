from pico2d import *
import game_framework
import start_mode

open_canvas(1200,1000)
game_framework.run(start_mode)
close_canvas()

#해야할거
#1.우주선 레벨에 따라 우주선 이미지 바꾸기
#2.드릴 레벨에 따라 드릴 이미지 바꾸기
#3.광물 체력 상태에따라 광물 이미지 바꾸기 ( 깨짐 정도 시각적 표현 )
#4.스테이지 클리어 시 stage 에서 클리어한 행성 이미지 바꾸기
#5.게임 사운드 추가
#6 2스테이지 추가 시간남으면