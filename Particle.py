import pygame as pg
import random as rn
import numpy as np

class Particle:
    def __init__(self, width, height) -> None:
        self.radius = rn.randint(12, 19)
        self.mass = self.radius*5
        self.pos = pg.math.Vector2(
            rn.randint(0, width-25),
            rn.randint(0, height-25)
            )
        self.velocity = pg.math.Vector2(
            rn.uniform(-1, 1),
            rn.uniform(-1, 1)
        )
        self.acceleration = pg.math.Vector2(
                            0,
                            0.8
                            )

        self.max_velocity = pg.math.Vector2((2, 2))
        self.min_velocity = pg.math.Vector2((-2, -2))
        self.max_magnitude = np.sqrt(np.power(self.max_velocity[0], 2)*2)

    
    def get_colorTarget(self):
        mag_fraction = self.velocity.magnitude()/self.max_magnitude
        target_color = 255*mag_fraction

        return target_color


    def update_color(self):
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        green = (0, 255, 0)

        updated_color = (0, 0, 0)
        
        mag_fraction = self.velocity.magnitude()/self.max_magnitude
        target_color = 255*mag_fraction
         
        if target_color/255<(1/2):
            updated_color = (255, np.clip(int(target_color), 0, 255), 0)
        elif target_color/255 == (1/2):
            updated_color = (255, 255, 0)
        else:
            updated_color = (0, np.clip(int(target_color), 0, 255), 0)

        self.color = updated_color


    def display(self, screen):
        pg.draw.circle(screen,
                       self.color,
                       self.pos,
                       self.radius,
                       )

    
    def move(self, dt, attractionPoints):
        self.velocity += self.acceleration*dt

        if self.get_Env_Vectors(attractionPoints) != False:
            ev = self.get_Env_Vectors(attractionPoints)
            for v in ev:
                self.velocity += v
            
        
        #Limit velocity & acceleration
        if self.velocity[0]+self.acceleration[0]>self.max_velocity[0]:
            self.acceleration[0] = 0
            self.velocity[0] = self.max_velocity[0]
        if self.velocity[0]+self.acceleration[0]<self.min_velocity[0]:
            self.acceleration[0] = 0
            self.velocity[0] = self.min_velocity[0]
        
        if self.velocity[1]+self.acceleration[1]>self.max_velocity[1]:
            self.acceleration[1] = 0
            self.velocity[1] = self.max_velocity[1]
        if self.velocity[1]+self.acceleration[1]<self.min_velocity[1]:
            self.acceleration[1] = 0
            self.velocity[1] = self.min_velocity[1]
        

        self.pos += self.velocity
        


    def check_boundry_collision(self, width, height):
        if self.pos[0]+self.radius>width:
            self.pos[0] = width-self.radius
            self.velocity[0] *= -1
        elif self.pos[0]-self.radius<0:
            self.pos[0] = self.radius
            self.velocity[0] *= -1
            
        if self.pos[1]+self.radius>height:
            self.pos[1] = height-self.radius
            self.velocity[1] *= -1
        elif self.pos[1]-self.radius<0:
            self.pos[1] = self.radius
            self.velocity[1] *= -1
            
    
    def check_particle_collision(self, other):
        # for other in particles:
        #     if other != self:
        min_distance = other.radius + self.radius
        distance = self.pos.distance_to(other.pos)

        #Collision
        if distance<min_distance:
            self.apply_collision(other, min_distance, distance)

            

    def apply_collision(self, other, min_distance, distance):
        unit_normal = pg.math.Vector2((self.pos[0]-other.pos[0], self.pos[1]-other.pos[1]))
        unit_normal = unit_normal.normalize()

        unit_tangent = pg.math.Vector2((unit_normal[1]*-1, unit_normal[0]))
        unit_tangent = unit_tangent.normalize()

        self_normalV = unit_normal.dot(self.velocity) #Velocity in the normal direction
        self_tangentV = unit_tangent.dot(self.velocity) #Velocity in the tangential direction
        
        other_normalV = unit_normal.dot(other.velocity)
        other_tangentV = unit_tangent.dot(other.velocity)

        new_self_normalV = (self_normalV*(self.mass-other.mass)+(2*other.mass*other_normalV))/(self.mass+other.mass)
        new_other_normalV = (other_normalV*(other.mass-self.mass)+(2*self.mass*self_normalV))/(self.mass+other.mass)
        
        #Convert scalers back to vectors
        self_normalV_vector = new_self_normalV*unit_normal
        self_tangentV_vector = self_tangentV*unit_tangent

        other_normalV_vector = new_other_normalV*unit_normal
        other_tangentV_vector = other_tangentV*unit_tangent

        self.velocity = self_normalV_vector+self_tangentV_vector
        other.velocity = other_normalV_vector+other_tangentV_vector

        repulsion = unit_normal*(min_distance-distance)

        self.pos += (repulsion/2)
        other.pos -= (repulsion/2)


    def get_Env_Vectors(self, attractionPoints):
        vectors = []
        for point in attractionPoints:
            v = pg.math.Vector2(
                point[0]-self.pos[0],
                point[1]-self.pos[1]
            )
            v = v.normalize()*self.max_velocity[0]*2
            vectors.append(v)
        
        if vectors == []:
            return False
        
        return vectors
        
        

