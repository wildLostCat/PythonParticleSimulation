import pygame as pg
import numpy as np
import os
from Particle import Particle


class ParticleSimulator:
    def __init__(self) -> None:
        #Constants
        self.WIDTH, self.HEIGHT = 1400, 900
        self.FPS = 60
        self.dt = 1/self.FPS
        self.PARTICLE_N = 10


        icon = pg.image.load('atomIcon.png')
        
        #Pygame initialization  
        pg.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('FiraCode Nerd Font', 50)
        pg.display.set_caption('Particle pool')
        pg.display.set_icon(icon)
        
        
        os.system('cls')
        print(f'⚛️\n PARTICLE SIMULATOR')

        #Particle init
        self.particles = [Particle(self.WIDTH, self.HEIGHT) for _ in range(self.PARTICLE_N)]

        self.mainloop()


    def mainloop(self) -> None:
        self.attractionPoints = []
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                
            # Clear frame
            self.screen.fill((3, 3, 3))

            self.sweep_intervals()

            for particle in self.particles:
                particle.check_boundry_collision(self.WIDTH, self.HEIGHT)
                
                particle.move(self.dt, self.attractionPoints)
                particle.update_color()
                particle.display(self.screen)
                

            #Display particle count
            text = self.font.render(str(self.PARTICLE_N), 1, (0, 0, 160))
            self.screen.blit(text, (0, 0))
            
            

            #Draw frame
            pg.display.flip()
            self.clock.tick(self.FPS)


        print("Exited with 0 errors 🎩")
        pg.quit()


    def get_ranges(self) -> list:
        ranges = []
        for i, particle in enumerate(self.particles):
            range = (particle.pos[0]-particle.radius, particle.pos[0]+particle.radius)
            ranges.append((i, range))   

        ranges = sorted(ranges, key=lambda item: item[1][0])


        return ranges

            
    def create_intervals(self) -> list:
        ranges = self.get_ranges()
        intervals = []

        for i, current in enumerate(ranges):
            interval = []
            interval.append(current)

            for other in ranges:
                if current is not other:
                    if other[1][0] <= current[1][1] and other[1][1] >= current[1][0]:
                        interval.append(other)
            
            if len(interval) != 1:
                intervals.append(interval)
        
        return intervals


    def sweep_intervals(self) -> None:
        intervals = self.create_intervals()

        for active_interval in intervals:
            for current in active_interval:
                for other in active_interval:
                    if current is not other:
                        self.particles[current[0]].check_particle_collision(self.particles[other[0]])



if __name__ == '__main__':
    app = ParticleSimulator()