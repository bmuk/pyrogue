"""
    pyrogue.fov
    ~~~~~~~~~~~

    This handles field of vision for entities.
"""

VIEW_RADIUS = 5

from math import cos
from math import sin

# Essentially we are going to modify the entity class so that it
# supports FOV - we will use a decorator, which is a higher-order
# function (takes and returns a function or class).

# -ing naming convention for our decorators, looks nice:
# @viewing
# class Entity(object) ...

def viewing(entity):
    """
    This decorator adds FOV functionality to an entity.
    """
    # make new variables and assign them to entity like so:
    # foo = 5
    # entity.foo = foo
    # now our class has a foo member.
    def add_hook(old_update, new_function):
        """
        This decorator adds a function call to the end of the decorated
        function so that we can add our new functionality.
        """
        def update(self):
            """
            This method is called once per tick.
            """
            old_update()
            new_function()
        return update
    # here's where we add our functions to manipulate the variables
    # we created earlier. You can assign functions just like variables:
    # def foo(self, x):
    #     self.x = x
    #     return x
    # entity.foo = foo
    def fov(self):
        """
        This method calculates the FOV every update.
        """
        float (x,y);
        int (i);
        CLEAR_MAP_TO_NOT_VISIBLE(); #Initially set all tiles to not visible.
        for i in range(0,360,1):
            x=cos(float(i*0.0174))
            y=sin(float(i*0.0174))
            DoFov(x,y)

    def DoFov(x,y):
        int (i)
        float (ox,oy)
        ox = float(PLAYERX+0.5);
        oy = float(PLAYERY+0.5);
        while i < VIEW_RADIUS:
            MAP[int(ox)][int(oy)]=VISIBLE #Set the tile to visible.
            if(MAP[int(ox)][int(oy)]==BLOCK):
                return
            ox+=x;
            oy+=y;
            i += 1

    # alternative syntax to use decorators - can also use @decorator
    # but only when defining the function.
    entity.update = add_hook(entity.update, fov)
    return entity

