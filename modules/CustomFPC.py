from ursina import *

class CustomFirstPersonController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.height = 1
        self.camera_pivot = Entity(parent=self, y=self.height)
        self.base = application.base
        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = False
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.can_rotate = True
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y

    def center_pointer(self):
        self.base.win.movePointer(0, int(self.base.win.getXSize() / 2), int(self.base.win.getYSize() / 2))

    def update(self):
        if self.can_rotate :
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        #self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        #self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)
        self.direction = Vec3(
                self.forward * 0
                + self.right * 0
                ).normalized()
        
        self.rotation_y = min(45,self.rotation_y)
        self.rotation_y = max(-45,self.rotation_y)

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount





    def input(self, key):
        if key == 'space':
            pass


    def on_enable(self):
        mouse.locked = False
        if hasattr(self, 'camera_pivot') and hasattr(self, '_original_camera_transform'):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform


    def on_disable(self):
        mouse.locked = False
        self._original_camera_transform = camera.transform  
        camera.world_parent = scene

    def block_rotation(self):
        self.can_rotate = False
        self.center_pointer()
        self.rotation_y = 0

