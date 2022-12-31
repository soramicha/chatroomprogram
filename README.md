# Chat Room Program

#### *Video Demo:* https://youtu.be/6a9CUzjS7qw
#### *Description:* This is a chatroom program that allows two users to communicate with one another.

#### *Why I decided to make it:*
##### My dad was the one who suggested me to try and make my own chatroom program because I wasn't sure what to make at first. I wanted a challenge, and I wanted to learn more about networking, so this was the perfect goal for me.

#### *Explanations of the 3 files:*
##### There are three files in total. The two files project.py and client.py are meant to act as a server and client to allow both sides to communicate with each other. The last file, screen.py, controls the new screen created after connection is successfully created between the server and client. In the screen.py file, I used a library called curses and created an upper window for showing messages and another window at the bottom for user input, in order to make it more user friendly and organized. I gave each user a different color so when their messages pop up on the screen, it's easier to read which message is sent by whom, etc.

#### *Overall Summary/Challenges Faced:*
##### I started making this around 9 days ago. It was easy to start up a server and connect it to a client, but I struggled a lot when I started using curses. Threads were also a challenge, but I was able to get the program to work with it in around a day. Majority of my challenges occured when I worked on screen.py. I had to deal with creating a pad and a window, and knowing where to refresh the lines, etc. on the terminal window. I tested the program on different computers, and tried to make the program work on both Apple and Windows as well. At first, it didn't, but after a lot of unit testing and finding the root of the bugs + fixing it, I was able to get it to work completely.

#### *Future Improvement:*
##### In the future I want to allow more than one user to get connected onto the server and chat.

#### Personal Note:
##### Overall I really enjoyed creating this program. I went through so many difficulties but from that I was able to learn many more new things. Networking in general, is new to me, and so being able to learn more about IP addresses, ports, and how messages are sent, etc. was very fun. I also really liked learning about threads and curses. Finally, this program forced me to create a class and object, which I have never really used until now. Classes and objects were new to me and I didn't feel very comfortable using them, but after doing so for this project, I feel a lot better. Thank you for the course!
