from entity.entity import *

class Units(Entity):

    def __init__(self,id_gen ,cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed = 1, _range=1):
        super().__init__(id_gen,cell_Y, cell_X, position, team, representation)
        self.hp = hp
        self.max_hp = hp
        self.training_time=training_time
        self.cost=cost

        self.distance_acc = 0
        self.attack = attack
        self.attack_speed = attack_speed
        self.range= _range
        self.attack_time_acc = 0
        self.will_attack = False
        self.attack_frame = 0
        self.entity_target_id= None
        self.entity_defend_from_id = None
        self.check_range_with_target = False
        self.first_time_pass = True
        self.locked_with_target = False
        
        self.speed=speed
    