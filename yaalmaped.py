import pygame
import os, math, copy, struct, io

class MapTile():
    def __init__(self):
        self.type = 0
        self.g_id = 0
        self.g_id_2 = 0
        self.g_l_t = 0
        self.g_t = 0
        self.d = 0
    def serialize(self):
        return struct.pack('BBBBBB', self.type, self.g_id, self.g_id_2, self.g_t, self.g_l_t, self.d)
    def deserialize(self, data):
        rd = struct.unpack('BBBBBB', data)
        self.type = rd[0]
        self.g_id = rd[1]
        self.g_id_2 = rd[2]
        self.g_t = rd[3]
        self.g_l_t = rd[4]
        self.d = rd[5]

w, h = 32, 16
game_map = [[0 for y in range(h)] for x in range(w)] 
sel_tile = MapTile()
sel_tile.type = 1
sel_tile.g_id = 1
map_name = "Test Map"
song_id = 0
level_id = 0

def save(file):
    f = io.open(file, "wb")
    hdr = struct.pack("64sii", bytes(map_name, "utf-8"), song_id, level_id)
    f.write(hdr)
    for x in range(0, w):
        for y in range(0, h):
            f.write(game_map[x][y].serialize())
    f.close()

def load(file):
    f = io.open(file, "rb")
    struct.unpack("64sii",f.read(struct.calcsize("64sii")))
    for x in range(0, w):
        for y in range(0, h):
            t = MapTile()
            t.deserialize(f.read(struct.calcsize("BBBBBB")))
            game_map[x][y] = t

def load_icon_set(dir, font):
    tile_icons = []
    tile_icon_count = 5
    for i in range(0,tile_icon_count):
        n = "%s/%i.png" % (dir,i)
        if os.path.exists(n):
            tile_icons.append(pygame.image.load(n))
        else:
            tile_icons.append(font.render("?%i" % i, True, (255,255,255), (0,0,0)))
    return tile_icons 

def draw_icon(screen, m, x, y, i):
    if m:
        if m.type != 0:
            if len(i[0]) > m.g_id:
                screen.blit(i[0][m.g_id], (x*16,y*16))
            if m.g_l_t != 0:
                if len(i[1]) > m.g_l_t:
                    screen.blit(i[1][m.g_l_t], (x*16,y*16))
            if m.g_id_2 != 0:
                if len(i[2]) > m.g_id_2:
                    screen.blit(i[2][m.g_id_2], (x*16+8,y*16))
        else:
            screen.blit(i[0][0], (x*16,y*16))

def main():
    for x in range(0, w):
        for y in range(0, h):
            game_map[x][y] = MapTile()

    pygame.init()
    pygame.display.set_icon(pygame.image.load("yaalicon.png"))
    pygame.display.set_caption("YaalMapEd")
    screen = pygame.display.set_mode((640,480))

    font = pygame.font.Font('freesansbold.ttf', 16)

    tile_icons = load_icon_set("tiles", font)
    light_icons = load_icon_set("lights", font)
    ext_icons = load_icon_set("icons", font)
    sets = (tile_icons, light_icons, ext_icons)

    stattxt = font.render("welcome to YaalMapEd", True, (255,255,255), (0,0,0))
    hlptxt = font.render("s saves the map to ./tmp.map, = loads from ./tmp.map",  True, (255,255,255), (0,0,0))
    hlptxt2 = font.render("u/j increases/decreases type, i/k increases/decreases graphics id", True, (255,255,255), (0,0,0))
    hlptxt3 = font.render("o/l increases/decreases graphics ext id, y/h increases/decreases light type", True, (255,255,255), (0,0,0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                k = pygame.mouse.get_pressed()
                p = pygame.mouse.get_pos()
                p_tx = math.floor(p[0] / 16)
                p_ty = math.floor(p[1] / 16)
                if k[0] and not k[1]:
                    game_map[p_tx][p_ty] = copy.copy(sel_tile)
                elif not k[0] and k[0]:
                    pass
                elif k[0] and k[0]:
                    pass
            elif event.type == pygame.KEYDOWN:
                k = pygame.key.get_pressed()
                if k[pygame.K_s]:
                    save("tmp.map")
                elif k[pygame.K_EQUALS]:
                    load("tmp.map")
                elif k[pygame.K_u]:
                    sel_tile.type += 1
                elif k[pygame.K_j]:
                    sel_tile.type -= 1
                elif k[pygame.K_i]:
                    sel_tile.g_id += 1
                elif k[pygame.K_k]:
                    sel_tile.g_id -= 1
                elif k[pygame.K_o]:
                    sel_tile.g_id_2 += 1
                elif k[pygame.K_l]:
                    sel_tile.g_id_2 -= 1
                elif k[pygame.K_y]:
                    sel_tile.g_l_t += 1
                elif k[pygame.K_h]:
                    sel_tile.g_l_t -= 1
                elif k[pygame.K_u]:
                    sel_tile.g_t += 1
                elif k[pygame.K_j]:
                    sel_tile.g_t -= 1
                stattxt = font.render("T: %i, G: %i, G2: %i, t: %i, L: %i" % (sel_tile.type, sel_tile.g_id, sel_tile.g_id_2, sel_tile.g_t, sel_tile.g_l_t), True, (255,255,255), (0,0,0))
                
        screen.fill((64, 64, 64))

        screen.blit(stattxt, (0,480-16))    
        screen.blit(hlptxt, (0,(h)*16))        
        screen.blit(hlptxt2, (0,(h+1)*16))  
        screen.blit(hlptxt3, (0,(h+2)*16))
        
        for x in range(0,w):
            for y in range(0,h):    
                m = game_map[x][y]
                draw_icon(screen, m, x, y, sets)

        draw_icon(screen, sel_tile, 0, h+5, sets)

        pygame.display.flip()

if __name__=="__main__":
    main()