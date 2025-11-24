**Welcome to the Writer Deck Github Repo!**

This project was built for the Sundai hackathon. Check out the project demo on our sundai card:

https://www.sundai.club/projects/5b6a7d8b-5b31-4045-8678-3e21955fad8b

This is the repo for our offline, distraction-free typing screen. Work on your novels, poems, assignments, or fanfiction on the Writer Deck without falling victim to doomscrolling!

Equipment used: Curiosity CircuitPython, Raspberry Pi 3

This works by:

- Keyboard input which is connected to the raspberry pi
- The Raspberry Pi is connected to the Arudino Ruler (not yet released device that we got to play with for the sundai hack) and streams the keyboard inputs via serial port through send_to_pykit.py. This is python program runs in a terminal which the keyboard is focused on.
- The ruler recieves the data via sysin then updates the screen via sysout
