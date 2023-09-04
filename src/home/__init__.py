from src import Game
from src.game.bg_panel import BgEnum, make_repeat_surface
from src.utils.surface import PageSurface


class HomePage(PageSurface):
    OffsetPerSec = 1
    def __init__(self, level: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level

        self.bg_pos_y = Game.geometry.y -75 
        self.bg_offset_skin = 0
        self.bg_offset_parallax = 0
        self.bg_offset_ground1 = 0
        self.bg_offset_ground2 = 0
        self.bg_offset_ground3 = 0
        self.bgs = BgEnum['level_'+str(level)].value
        self.skin_surface = make_repeat_surface(Game.geometry.x, self.bg_pos_y, self.bgs["skin"], lambda h: -h-80)
        self.parallax_surface = make_repeat_surface(Game.geometry.x, self.bg_pos_y, self.bgs["parallax"], lambda h: -h-16)
        self.ground_surface_1 = make_repeat_surface(Game.geometry.x, self.bg_pos_y, self.bgs["ground1"], lambda h: -h)
        self.ground_surface_2 = make_repeat_surface(Game.geometry.x, self.bg_pos_y, self.bgs["ground2"], lambda _: 0)
        self.ground_surface_3 = make_repeat_surface(Game.geometry.x, self.bg_pos_y, self.bgs["ground3"], lambda h: -h)

    
    def after_game_draw(self):
        bg_offset_ground3 = self.bg_offset_ground3 - self.OffsetPerSec
        self.bg_offset_ground3 = 0 if -bg_offset_ground3 == self.ground_surface_3[2].get_width() else bg_offset_ground3
        self.surface.blit(self.ground_surface_3[0], (self.bg_offset_ground3, self.ground_surface_3[1]))
    
    def draw(self):
        self.surface.fill(self.bgs['sky'], ((0, 0), (self.surface.get_width(), self.bg_pos_y)))

        skin_offset = self.bg_offset_skin - self.OffsetPerSec / 5
        self.bg_offset_skin = 0 if -skin_offset == self.skin_surface[2].get_width() else skin_offset
        self.surface.blit(self.skin_surface[0], (self.bg_offset_skin, self.skin_surface[1]))

        parallax_offset = self.bg_offset_parallax - self.OffsetPerSec / 2
        self.bg_offset_parallax = 0 if -parallax_offset == self.parallax_surface[2].get_width() else parallax_offset
        self.surface.blit(self.parallax_surface[0], (self.bg_offset_parallax, self.parallax_surface[1]))

        bg_offset_ground1 = self.bg_offset_ground1 - self.OffsetPerSec
        self.bg_offset_ground1 = 0 if -bg_offset_ground1 == self.ground_surface_1[2].get_width() else bg_offset_ground1
        self.surface.blit(self.ground_surface_1[0], (self.bg_offset_ground1, self.ground_surface_1[1]))

        self.surface.fill(self.bgs['ground'], ((0, self.bg_pos_y), (self.surface.get_width(), self.surface.get_height() - self.bg_pos_y)))

        bg_offset_ground2 = self.bg_offset_ground2 - self.OffsetPerSec
        self.bg_offset_ground2 = 0 if -bg_offset_ground2 == self.ground_surface_2[2].get_width() else bg_offset_ground2
        self.surface.blit(self.ground_surface_2[0], (self.bg_offset_ground2, self.ground_surface_2[1]))

        return super().draw(after_draw_children=self.after_game_draw)
