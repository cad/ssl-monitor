import sys
import socket
import struct
import threading
import pickle
import math
import time

from time import sleep

from proto import messages_robocup_ssl_wrapper_pb2 as pb_wrapper
from proto import messages_robocup_ssl_detection_pb2 as pb_detection
from proto import messages_robocup_ssl_geometry_pb2 as pb_geometry
from proto import messages_robocup_ssl_refbox_log_pb2 as pb_refbox

balls = None
yellow = None
blue = None

def __get_ball():
    global balls
    # FIXME: use an appropriate codition here.
    if balls and len(balls)> 0:
        return balls[0]
    else:
        return None

def sanitize_packet(msg):
    global balls
    global yellow
    global blue

    packet = pb_wrapper.SSL_WrapperPacket()
    packet.ParseFromString(msg)
        
    if packet.HasField('detection'):

        def sanitize_robot(robot):
            t = time.time()
            return {'x':robot.x,
                    'y':robot.y,
                    'pixel_x':robot.pixel_x,
                    'pixel_y':robot.pixel_y,
                    'orientation':robot.orientation,
                    'height':robot.height,
                    'confidence':robot.confidence,
                    'time': t
            }
            
        def sanitize_ball(ball):
            t = time.time()
            
            def get_speed():
                oldball = __get_ball()
                if not oldball:
                    oldball = {'x':0.0, 'y':0.0, 'time':0.0, 'speed':0.0}
                    
                    oldx, oldy, oldt = oldball['x'], oldball['y'], oldball['time']
                    # print "DELTAt:       %s" %  (t - oldt)
                    # print "OLDX, OLDY: (%s, %s)" % (oldx, oldy)
                    # print "X, Y:       (%s, %s)" % (ball.x, ball.y)
                    # print "SPEED:      %s" % (((float((ball.x - oldx))**2) + (float((ball.y - oldy)) **2)) / float((t - oldt)),)
                    speed = abs(math.sqrt((ball.x - oldx) **2 + (ball.y - oldy) **2)) / (t - oldt)
                    

            speed = get_speed()
                    
            # except:
            #     speed = 0.0
                    

            return {'confidence':ball.confidence,
                    'area':ball.area,
                    'x':ball.x,
                    'y':ball.y,
                    'z':ball.z,
                    'pixel_x':ball.pixel_x,
                    'pixel_y':ball.pixel_y,
                    'time':t,
                    'speed':speed,
            }
            

        blue, yellow, balls = {}, {}, {}
        for robot in packet.detection.robots_blue:
            blue[int(robot.robot_id)] = sanitize_robot(robot)
            
        for robot in packet.detection.robots_yellow:
            yellow[int(robot.robot_id)] = sanitize_robot(robot)
            
        for id, ball in enumerate(packet.detection.balls):
            balls[int(id)] = sanitize_ball(ball)
        return {'blue':blue, 'yellow':yellow, 'balls':balls}
