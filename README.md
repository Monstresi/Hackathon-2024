# 🎭 Exposé: The Ultimate Guessing Game!

<a name="top"></a>

<h3 align="center"></h3>

<p align="center">
 
</p> 
</div>

<!---- ABOUT THE PROJECT ---->
Welcome to Exposé, where deception meets deduction! 🕵️‍♂️✨ In this game, you'll be challenged to identify the one player who doesn't have an image, all while pretending to describe an image they don't actually have! 🤫🔍 Ready to test your bluffing skills and intuition? Let's dive in!

<!---- Instructions ---->

# 🎯 Objective
In Exposé, everyone gets to see an image of a specific category (e.g., an athlete, a famous landmark, etc.), except one player. Your goal is to guess who the imposter is, while everyone else tries to describe their image with just one word, all while hiding the fact that they don’t actually have one. 🤔🕵️‍♀️
<!---- Technologies ---->
	
# How To Run
Firstly, to build the project, use: "docker build -t expose .". After that use: "docker run -p 50000:50000 expose". Then paste the generated link into your browser. When you land on our user interface, the first submission you will make is your username (we didn't have enough time to make a seperate login page). 

The current limit on server.py has been set to 3 in the cloud. Once 3 app.py client's have joined (through the docker commands above) the game will automatically start. For now, we do not have the ability to restart the game.

