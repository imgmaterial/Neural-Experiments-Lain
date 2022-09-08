# Neural-Experiments-Lain
Neural Experiments is an anime recommendation system based on collaborative learning for neural networks. The project relies on FastAIs implementation of collaborative learning model. For the user this means that the recommendations given by the neural network rely not on the contents or attributes of the recommended title but on the interactions of users that have shown to have a similar taste in anime as the user did. A preexisting data set of MyAnimeList user ratings was used to train the model and the model is continuously being trained as information is received from new users and new shows come out.

In order to use the recommendation system the user needs to enter into the database a set of previously watched titles along with a rating on scale of 1-10.  Ability to authenticate through some of the already existing anime list sites would be implemented in the future to make the process smoother for users who already have a large collection of anime listed on a third party platform. The relevant information from the entries is then sent into our database for the model to further learn from them and the user will be able to request a list of 10 top recommendations from the neural networks perspective.

Project in early development stages.

In order to launch the project make sure Python 3.10 is installed along with the libraries used by the project. All of the required libraries can be found in requirements.txt and installed by running:

pip install -r requirements.txt


If all is installed launch web_api.py by running "python web_api.py" from directory.

Currently working HTTP methods.

/anime

GET

Takes in anime_id, returns a json with info about the anime.

![image](https://user-images.githubusercontent.com/59793640/188739125-79af59d8-20ad-4a27-93d5-2aabc7e5a6c0.png)

![image](https://user-images.githubusercontent.com/59793640/188739167-49b02de1-8339-4034-b919-7ecc8d0b252b.png)


/users

GET

Takes no input, returns entries of every user in JSON format with user name, animeid and the users score.

![image](https://user-images.githubusercontent.com/59793640/183617083-cd800902-9857-4a8f-957b-9748603a767c.png)

![image](https://user-images.githubusercontent.com/59793640/187989969-525b3562-9f5f-43e7-9117-b6433ad0051f.png)


POST

Takes in a body of form {'user': user, 'animeid': animeid, 'rating': rating} and posts a single entry into the database. If successful return code 200 and response message

![image](https://user-images.githubusercontent.com/59793640/183618894-d54bc603-9fd7-4d5f-a968-661f0639023d.png)

![image](https://user-images.githubusercontent.com/59793640/183619026-44ebc1b4-f0c0-4ca7-81c5-bb7bed8f6c70.png)

![image](https://user-images.githubusercontent.com/59793640/183619622-c53cb67f-05b8-49c6-82a2-a2d04fe48cee.png)

/rate

GET

Takes a username as an input, returns all of the ratings by this user JSON format with user name, animeid and the users score.

![image](https://user-images.githubusercontent.com/59793640/183620266-5665662f-ae13-499d-916d-b9785a52723d.png)

![image](https://user-images.githubusercontent.com/59793640/187990189-aa6291b9-f1f9-4315-9e4c-65dcec4bcb6b.png)


/rec

GET

Takes a username as an input, returns a JSON with 10 anime recomendations with the anime id, its name and predicted user rating.

![image](https://user-images.githubusercontent.com/59793640/183621169-24239c91-c52a-4eb5-90b0-ca2346f4f468.png)

![image](https://user-images.githubusercontent.com/59793640/187990309-6377bd41-21fa-42a3-9fb2-c629ffb271e8.png)





