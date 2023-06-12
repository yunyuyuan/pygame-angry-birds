from src import Game


class Animation():
    '''
    特性：
    * 不可中断
    '''
    def __init__(self, speed = 150, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animation_state = -1
        # 0.01~1.00
        self.animation_progress: float = 0
        self.animation_speed = Game.fps_frame_sec/speed

    def animation_step(self, progress: float):
        raise NotImplementedError("you must define the animation step!")

    def animate(self):
        if (self.animation_progress == 0 and self.animation_state == -1) or (self.animation_progress == 1 and self.animation_state == 1):
            return
        new_progress = self.animation_progress + self.animation_speed*self.animation_state
        if new_progress < 0:
            new_progress = 0
        elif new_progress > 1:
            new_progress = 1
        self.animation_progress = new_progress
        self.animation_step(self.animation_progress)
