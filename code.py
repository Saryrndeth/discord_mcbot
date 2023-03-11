from mcpi.minecraft import Minecraft
import time

# Minecraft 서버에 연결
mc = Minecraft.create()

while True:
    # 블록 히트 이벤트 가져오기
    blockHits = mc.events.pollBlockHits()
    for blockHit in blockHits:
        # 버튼 블록인지 확인
        block = mc.getBlockWithData(blockHit.pos)
        if block.id == 77:  # 버튼 블록 ID
            print("Button Pressed")
            time.sleep(0.2) # 디바운스 대기