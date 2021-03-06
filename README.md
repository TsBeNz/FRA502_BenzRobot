# FRA502 Project
## By Thansak Pongpraket 61340500015

โปรเจ็คหุ่นยนต์ทำความสะอาดที่สั่งงานผ่านคำสั่งเสียงโดยสามารถเคลื่อนที่ได้อย่างอัตโนมัติผ่านการจำลองโดย Gazebo

## Prerequisite

* Ubuntu 20.04 system with ROS Noetic
### Python with install
* pip install SpeechRecognition
* sudo apt-get install python-pyaudio python3-pyaudio
* pip install py-espeak-ng


## Installation & Run

สร้าง catkin workspace.
```bash
mkdir -p <WORKSPACE_NAME>/src
cd <WORKSPACE_NAME>
catkin_make
cd src
```
โหลด File จาก Github นี้ (or clone) ลงไปใน /src

```bash
cd ..
catkin_make
source <PATH_TO_WORKSPACE>/devel/setup.bash
source ~/.bashrc
```
### การใช้งาน

#### เริ่ม Navigation Simulation โดยใช้คำสั่ง
* การ Run คำสั่งนี้จะทำให้สามารถควบคุมหุ่นยนต์ผ่าน GUI ของ Rvis ได้
```bash
roslaunch tsbenzbot_description benz_navigation.launch
```
* เพื่อที่จะสั่งงานผ่านคำสั่งเสียงต้อง Run คำสั่งต่อไปนี้ด้วย
```bash
rosrun tsbenzbot_description benz_navigation.launch
```
* โดยคำสั่งสียงจำต้องมีคำว่า Robot อยู่ในประโยคเเละตำเเหน่งของห้องต่างๆที่ต้องการให้หุ่นยนต์ไปทำความสะอาดหรือถามถึงสถานะโดยให้มีคำว่า Status อยู่ภายในประโยค
* ["mom bedroom","son bedroom","my bedroom","kitchen","living room"] คือห้องที่กำหนดไว้ภายในโปรเเกรม หลังทำความสะอาดเสร็จสมบูรณ์ทุกครั้งหุ่นยนค์จะกลับไปยังตำเเหน่ง Station
* เนื่องจากใช้งาน Online Speech Recognition จึงต้องเชื่อมต่อ Internet ตลอดเวลา

#### การเก็บ Map 
* Run คำสั่งนี้เพื่อเริ่ม Simulation เเละทำการควบคุมหุ่นยนต์
```bash
roslaunch tsbenzbot_description slam_map_save.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
* หลังจากที่สามารถเก็บ Map ได้ตามที่ต้องการเเล้วโดยการควบคุมหุ่นยนค์ผ่าน teleop_twist_keyboard จะใช้ map_saver ในการบันทึก
```bash
rosrun map_server map_saver -f mymap
```
## สรุปสิ่งที่ได้จากการทำโปรเจ็คนี้
### problems 
* 1. หุ่นยนต์ไม่สามารถเคลื่อนที่ได้อย่างมีประสิทธิภาพเนื่องจากการปรับค่า Parameter ต่างๆยังไม่ดีเพียงพอทำให้อาจจะมีการเดินที่ติดได้หรือหมุนเมื่อถึงเป้าหมายเเล้ว 1-2 รอบ
* 2. การสร้าง Viapoints เพื่อใช้ในการสั่งงานหุ่นยนต์ไม่มีความยืดหยุ่นต้องทำการเเก้ไขหรือปรับเปลี่ยนค่าในโปรเเกรมเพื่อกำหนดจุดหรือเส้นทางต่างๆเท่านั้น
* 3. ส่วนของเสียงยังไม่ฉลาดเท่าไหร่ จึงทำให้อาจทำงานไม่ตรงกับคำสั่งที่สั่งไปได้

### สรุปภาพรวม
* หุ่นยนต์สามารถทำงานได้เเต่ไม่ครบทุกอย่างตามที่เขียนไว้ใน proposal เช่นไม่สามารถยกเลิกการทำงานระหว่างทางได้ หรือไม่สามารถพูดคุยกับหุ่นยนค์ระหว่างการทำงานได้เป็นต้น

## Video เเสดงการทำงาน
* [Youtube Link](https://youtu.be/cDNwMhWtn8o)
* ระหว่างอัด Internet เเย่มากจึงทำให้วิเคราะห์เสียงนานมากๆ เเละไมโครโฟนมีสัญญาณรบกวนเยอะมากจากเสียงพัดลมคอมเเละอื่นๆ เนื่องจากใน Ubuntu ไม่มี Driver ของไมโครโฟน
