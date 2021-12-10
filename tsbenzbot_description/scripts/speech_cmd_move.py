#!/usr/bin/env python3

import speech_recognition as sr
from subprocess import call
import tf
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import random


path_Master_bedroom = [[-5.13,-3.85,0],[-7.85,-5.65,90],[]]
In_Station = True


s = '-s 140'
g = '-g 0.7'
f = '-vf3'
a = '-a 70'

list_room = ["mom bedroom","son bedroom","my bedroom","kitchen","living room"] 

def PrintAndSpeek(input = "test"):
    print(input)
    call(['espeak', s, g, f, a, input])  

def Path_Create(y_top,y_bot,x_r,x_l,count = 4):
    buffer = []
    diff = (x_l-x_r)/count
    for i in range(count+1):
        if (i%2 == 0):
            buffer.append([x_r+(i*diff),y_top,3.14592/2])
            buffer.append([x_r+(i*diff),y_bot,0])
        else:
            buffer.append([x_r+(i*diff),y_bot,-3.14592/2])
            buffer.append([x_r+(i*diff),y_top,0])         
    return buffer

def p2p_move2pos(x_in=0, y_in=0, theta_in = 0):
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )
    goal = MoveBaseGoal()
    goal.target_pose.pose.position.x = x_in
    goal.target_pose.pose.position.y = y_in
    x , y, z, w = tf.transformations.quaternion_from_euler(0, 0, theta_in)
    goal.target_pose.pose.orientation.x = x
    goal.target_pose.pose.orientation.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w    
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    sac.wait_for_server()
    sac.send_goal(goal)                     #send goal
    # rospy.loginfo("Move to" + str(x_in) + "," + str(y_in) + "," + str(theta_in))
    sac.wait_for_result()                   #finish
    # rospy.loginfo("Finish Move")            #print result

def voice_cmd():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_listen = r.listen(source, timeout=3.0)

        sound_cmd_in = r.recognize_google(audio_listen)
        sound_cmd_in = sound_cmd_in.lower()
        print(sound_cmd_in)
        if "robot" in sound_cmd_in:
            for i in range(len(list_room)):  
                if list_room[i] in sound_cmd_in:
                    PrintAndSpeek("OK, Cleaning " + list_room[i])
                    return [True , list_room[i]] 
            else:
                if "status" in sound_cmd_in:
                    if In_Station:
                        PrintAndSpeek("Charging Battery"+ str(random.randint(50,90))+ "% Battery Remaining.")
                        return [False , "0"]
                    else:
                        PrintAndSpeek("I'm Working ")
                        return [False , "0"]
                else:
                    PrintAndSpeek("I don't understand try again.")
                    return [False , "0"]
        else:
            PrintAndSpeek("Did you call me?")
            return [False , "0"]

    except sr.WaitTimeoutError:
        rospy.loginfo("WaitTimeoutError")
        return [False , "0"]
    except sr.UnknownValueError:
        rospy.loginfo("UnknownValueError")
        return [False , "0"]

if __name__ == '__main__':
    try:
        rospy.init_node('auto_move_base')
        rospy.Rate(1)  #setup Rate
        r = sr.Recognizer()
        mic = sr.Microphone()
        Bedroom_my_Path = Path_Create(-5.7,-2.15,-8,-3.2,6)
        Bedroom_mom_Path = Path_Create(3.4,6.4,-7.97,-4.3,3)
        Bedroom_son_Path = Path_Create(2,6.1,-0.2,2.9)
        kitchen_Path = Path_Create(-0.55,6.69,4.52,7.82,3)
        living_Path = Path_Create(-5.8,0.41,-1.05,2.85)
        station_pos = [2.59,-1.7,3.14592]
        PrintAndSpeek("I'm going to station.")
        p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])    
        while not rospy.is_shutdown():
            [Go , Room] = voice_cmd()
            if Go:
                if Room == "mom bedroom":
                    for goal in Bedroom_mom_Path:
                        p2p_move2pos(goal[0],goal[1],goal[2])
                    PrintAndSpeek("Work Done")
                    PrintAndSpeek("I'm going to station.")
                    p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
                elif Room == "son bedroom":
                    p2p_move2pos(-2.25,0.59,90)
                    p2p_move2pos(0.575,6.1,90)
                    p2p_move2pos(0.575,6.1,90)
                    for goal in Bedroom_son_Path:
                        p2p_move2pos(goal[0],goal[1],goal[2])
                    PrintAndSpeek("Work Done")
                    PrintAndSpeek("I'm going to station.")
                    p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
                elif Room == "my bedroom":
                    p2p_move2pos(-2.53,-0.31,-3.143592/2)
                    for goal in Bedroom_my_Path:
                        p2p_move2pos(goal[0],goal[1],goal[2])
                    PrintAndSpeek("Work Done")
                    PrintAndSpeek("I'm going to station.")
                    p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
                elif Room == "kitchen":
                    for goal in kitchen_Path:
                        p2p_move2pos(goal[0],goal[1],goal[2])
                    p2p_move2pos(7.58432674407959,4.393033027648926,-3.14592/2)
                    PrintAndSpeek("Work Done")
                    PrintAndSpeek("I'm going to station.")
                    p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
                elif Room == "living room":
                    for goal in living_Path:
                        p2p_move2pos(goal[0],goal[1],goal[2])
                    PrintAndSpeek("Work Done")
                    PrintAndSpeek("I'm going to station.")
                    p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
                elif Room == "station":
                        p2p_move2pos(station_pos[0],station_pos[1],station_pos[2])
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")