# Reconnect
### https://www.speech-reconnect.com
Reconnect is a website that uses speech recognition and analysis to teach people with hearing impairments to talk by giving them feedback on which words they have mispronounced, when they talked too loud/quiet, and when the breaks between the words were too long. We aspire it to be an interactive platform that assists individuals with impaired hearing to **reconnect** with communities and reintegrate into the society.

### Live demo:
Check it out at **https://www.speech-reconnect.com** 

### Our team
- Iryna Khovryak, front-end and back-end, Haverford College '22
- Samuel Tan, back-end, Haverford College '23
- Anubhav Sharma, back-end, Haverford College '23

### Description of Reconnect:
An interactive platform that assists individuals with impaired hearing to reconnect with communities and reintegrate into the society

### Inspiration
As medical treatment for impaired hearing continues to improve, there is an increase in demand for speech therapy programs. As of now, there is an existing gap in the market for innovative platforms that facilitate self-initiated learning or relearning of communication skills. Reconnect assists individuals with speech issues with the recovery process through its progressive framework. Users would relearn simple sentences that include self-introduction and request for help before moving onto complex sentences that pertain to buying groceries, etc. The entire process will be supported by real-time feedback on their pronunciation, the relative speed of their vowel enunciation, and the duration of the breaks they have between clauses and sentences.  

### What it does
Reconnect first allows the user to listen to a sound file that contains a sentence which the user should learn as part of its progressive relearning process. The user would repeat after the sound file before Reconnect begins to evaluate the user’s speech.
Reconnect uses Microsoft Azure’s Speech-to-Text function to convert the user’s speech input into text. By comparing the text against the sentence provided to the user, Reconnect is able to determine if the user’s pronunciation is adequately correct. Following which, Azure’s Text-to-Speech function is used to generate a separate speech output from the same sentence. These two .wav files will then be processed by Reconnect.
Reconnect uses the SciPy library to convert the sound files into audio data chunks. By using our self-developed algorithms to process the audio data’s amplitude, frequency, and breaks, Reconnect is able to determine the relative speed of vowel enunciation, and the presence of unnaturally long or short breaks between words and sentences.
Finally, Reconnect will compile all of these feedback before presenting them to the user. The user will then be given the opportunity to try again. The user can also type a sentence which he or she hopes to practice, and Reconnect will generate a sound file to facilitate the same learning process as mentioned above.

### Challenges we ran into
Since the team comprised of a sophomore and two freshmen having a less technical background, we ran into a lot of difficulties. This was the first time we ever played with APIs and it was difficult to get things working together. In the beginning, we did not go think about the number of channels of the input. Also, for the text comparison, it was necessary to mind the length of the expected text and the received text. While the typed text had to be preprocessed so that it did not contain any characters, the expected text had to be preprocessed so that it omitted some unintended words like “oh”, “umm” etc. Since none of us had enough experience in web development, the significant challenge was getting the input from the user in the form of audio
- Microphone input
- Two-channeled audio files and wave comparison algorithms for them

### Accomplishments that we're proud of
Despite all the challenges, we are proud that we successfully built an interactive platform Reconnect where people can practice speaking to reconnect with the world. Helping thousands of people worldwide in transitioning from impaired hearing to speaking effectively is indeed a great satisfaction to our team.

### What we learned
Being new to the hackathons, initially, we were unsure if we should go forward with this idea due to technical complexities. It was a second hackathon for all of us and our first-ever time using any sort of APIs. However, we decided to take up the challenge and finally it worked. Therefore, in addition to learning more about programming, using APIs and developing web-site, we learned to think big and apply the knowledge to have an impact on people’s life

### What's next for Reconnect
- consulting with medical professionals to get effective strategies for speech reconstruction
- expanding to different languages
- turning Reconnect into an actual learning platform with the ability to track progress and try different strategies
