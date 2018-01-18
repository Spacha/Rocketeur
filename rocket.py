import sys, math, time, pygame

from libs import Grapher

# environment constants
ENV = {
    'airDensity': 1.00,
    'g': 9.81,
    'speed_of_light': 299792458
}

raketti = {
    'mass':     1300,    # rocket mass, kg
    'area':     1.91,    # rocket area in respect of direction of velocity
    'thrust':  265000,   # rocket thrust, N
    'flow':     15,    # flow rate, kg/sec
    'fuel':    5600    # max amount of fuel, kg of fuel
}

# animation framelength in seconds
frameLength = 1.0

# Initial values (variables)
t = float(0)    # time
v = 0
a = 0
h = 0
Fv = 0
fuel = raketti['fuel']
m = raketti['mass'] + fuel
G = raketti['mass'] * 9.81
thrust = raketti['thrust']
tilt = 90

graph = Grapher.Graph(10, 10)

aGraph = graph.createGraph((255,0,0))
vGraph = graph.createGraph((0,255,0))
mGraph = graph.createGraph((0,0,255), 0.01)
drGraph = graph.createGraph((255,255,255), 0.01)
thrustGraph = graph.createGraph((255,255,0), 0.001)

freeze = False
pause = False
# The main loop
while 1:
    # freeze
    # if t >= 90:
        #print("Frozen.")
        # freeze = True
        # time.sleep(86400)

    if not freeze:
        if fuel <= 0:
            thrust = 0
        else:
            if thrust > 0:
                thrustPercent = raketti['thrust'] / thrust
            else:
                thrustPercent = 0.0
            fuel -= thrustPercent * raketti['flow']

        m = raketti['mass'] + fuel*2

        # update acceleration
        drag = 0.5 * ENV['airDensity'] * (v ** 2) * raketti['area'] * 0.5 * 10
        if v < 0:
            drag = -drag
            #print(thrust-drag)
        a = ((thrust - drag) / m) - ENV['g'] * math.sin(math.radians(tilt))

        # update velocity by acceleration
        v += a * frameLength
        
        if v >= ENV['speed_of_light']:
            v = ENV['speed_of_light'] - 1

        # print for debug
        #print('t: {}, v: {}, a: {}, dr: {}'.format(t, v, a, drag))

    ##############################################

    xVal = t * 10
    # insert new values to Grapher
    if not freeze:
        graph.insert(xVal,v, vGraph)
        graph.insert(xVal,a, aGraph)
        graph.insert(xVal,m, mGraph)
        graph.insert(xVal,-drag, drGraph)
        graph.insert(xVal,thrust, thrustGraph)

        rollspeed = frameLength*10
    else:
        rollspeed = 0

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:

            # cannot control rocket when frozen
            if not freeze:
                # control thrust by arrow keys
                if event.key == pygame.K_LEFT:
                    print("Scale down")
                    thrust -= raketti['thrust']*0.1
                    if thrust <= 0:
                        thrust = 0

                if event.key == pygame.K_RIGHT:
                    print("Scale up")
                    thrust += raketti['thrust']*0.1
                    if thrust >= raketti['thrust']:
                        thrust = raketti['thrust']

            if event.key == pygame.K_2:
                graph.adjustScale(0.1)
            if event.key == pygame.K_1:
                graph.adjustScale(-0.1)

            if event.key == pygame.K_SPACE:
                freeze = not freeze
                print("Switch Freeze")

    # Graphics
    graph.render(rollspeed)
    graph.simu({
        't': t,
        'v': v,
        'a': a,
        'm': m,
        'drag': drag,
        'thrust': thrust,
    })

    pygame.display.flip()
    if not freeze:
        t = t + frameLength

    time.sleep(frameLength)