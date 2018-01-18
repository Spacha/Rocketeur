import sys, math, time, pygame

from libs import Grapher
from libs import Physics

#densitySL * lPressureRelative * temperatureSL / temperature

# environment constants
ENV = {
    'airDensity': 1.225,
    'g': 9.81,
    'speed_of_light': 299792458
}

rockets = {
    'v-2':
    {
        'name':     'V-2',
        'mass':     1300,    # rocket mass, kg
        'area':     1.91,    # rocket area in respect of direction of velocity
        'thrust':   265000,   # rocket thrust, N
        'flow':     30,    # flow rate, kg/sec
        'fuel':     5600    # max amount of fuel, kg of fuel
    },
    'saturn-v':
    {
        'name':     'Saturn V',
        'mass':     177000,
        'area':     80.12,
        'thrust':   34020000,
        'flow':     5*2542,
        'fuel':     1396500
    },
}

rocket = rockets['saturn-v']

# animation framelength in seconds
frameLength = 0.02

# Initial values (variables)
t = float(0)    # time
v = 0
a = 0
h = 0
Fv = 0
fuel = rocket['fuel']
m = rocket['mass'] + fuel
G = rocket['mass'] * 9.81
thrust = rocket['thrust']
tilt = 90

graph = Grapher.Graph(10, 10)

aGraph = graph.createGraph((255,0,0))
vGraph = graph.createGraph((0,255,0))
mGraph = graph.createGraph((0,0,255), 0.01)
drGraph = graph.createGraph((255,255,255), 0.01)
thrustGraph = graph.createGraph((255,255,0), 0.001)

freeze = False
pause = False
screen = None

rollspeed = 0
prevTime = 0

# The main loop
while 1:
    startTime = time.time()

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
                thrustPercent = rocket['thrust'] / thrust
            else:
                thrustPercent = 0.0
            fuel -= thrustPercent * rocket['flow'] * frameLength

        m = rocket['mass'] + fuel*2

        # update height
        h += v * (t-prevTime)

        # update acceleration
        density = Physics.density(h)
        g = Physics.gravity(h)

        drag = 0.5 * density * (v ** 2) * rocket['area'] * 0.5 * 10
        if v < 0:
            drag = -drag
            #print(thrust-drag)
        a = ((thrust - drag) / m) - g * math.sin(math.radians(tilt))

        # update velocity by acceleration
        v += a * frameLength
        
        if v >= ENV['speed_of_light']:
            v = ENV['speed_of_light'] - 1

        # print for debug
        #print('t: {}, v: {}, a: {}, dr: {}'.format(t, v, a, drag))

    ##############################################

    xVal = t * 50
    # insert new values to Grapher
    if not freeze:
        graph.insert(xVal,v, vGraph)
        graph.insert(xVal,a, aGraph)
        graph.insert(xVal,m, mGraph)
        graph.insert(xVal,-drag, drGraph)
        graph.insert(xVal,thrust, thrustGraph)

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
                    thrust -= rocket['thrust']*0.1
                    if thrust <= 0:
                        thrust = 0

                if event.key == pygame.K_RIGHT:
                    print("Scale up")
                    thrust += rocket['thrust']*0.1
                    if thrust >= rocket['thrust']:
                        thrust = rocket['thrust']

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
        'h': h,
        'v': v,
        'a': a,
        'm': m,
        'drag': drag,
        'thrust': thrust,
        'density': density
    })

    if not screen:
        screen = graph.getScreen()
    pygame.draw.line(screen, (255,255,90), (10,30),(10+fuel/rocket['fuel']*300,30), 20)

    pygame.display.flip()

    if not freeze:
        runTime = time.time() - startTime
        rollspeed = (frameLength + runTime) * 50
        prevTime = t
        t = t + frameLength + runTime

    time.sleep(frameLength)