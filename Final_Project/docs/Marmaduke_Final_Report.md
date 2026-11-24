# Marmaduke Learns Spanish and Telenovela Actor
Final Project Report | ITAI 2374

Maria Jose Viveros Riquelme | November 2026

## 1. Project Overview

Our final project used Marmaduke, a SunFounder PiDog V2 powered by a Raspberry Pi 5, to explore

natural communication between a person and a robot. We developed two connected experiences:

Marmaduke Learns Spanish and Marmaduke Telenovela Actor. The goal was to make interaction more

personal through facial recognition, spoken conversation, character performance, and simple physical

feedback. The system combined Python, a camera, a microphone, a speaker, and OpenAI language and

speech models.

## 2. Marmaduke Learns Spanish

In the first experience, Marmaduke spoke with Maria Jose in Spanish. We practiced Chilean words and

expressions, and Marmaduke was able to use remembered expressions in later conversations. We also

experimented with different ways of speaking, including a Mexican accent. Rather than repeating a fixed

list of answers, Marmaduke used a large language model (LLM) to respond to the conversation and

continue the topic. This made the exchange more flexible and natural.

The Python support program recorded spoken input, sent it for speech-to-text transcription, and requested a

response from the language model. Spoken replies were then produced with text-to-speech. The LLM

generated new answers from instructions and conversational context; this should not be confused with

retraining the underlying model.

## 3. Marmaduke Telenovela Actor

Next, we gave Marmaduke a new personality: an actor rehearsing a Mexican telenovela. The instructions

asked him to be dramatic, playful, and slightly sarcastic. He could improvise responses based on what his

conversation partner said, so the scene was not limited to a fixed script. The performance also included

both Spanish and English conversation. During the demonstration, telenovela voice playback worked,

allowing Marmaduke to speak his lines aloud.

The acting program used OpenAI to generate dialogue and synthesize a voice with expressive instructions.

The speech was saved as a WAV file and played through the Raspberry Pi speaker. In addition, the

program included a double-touch interaction: two touches on Marmaduke's head triggered a short tail wag.

This response worked during the project and provided a simple physical reaction without interrupting the

spoken dialogue.

## 4. Facial Recognition and Language Choice

The camera stream was started with Vilib, while the facial-recognition program compared live images with

a saved facial profile. We trained Maria Jose's profile using images with and without glasses. In our tests,

the software printed “Recognized: Maria Jose,” although recognition was sometimes intermittent. The

video documents that facial recognition worked.

Marmaduke also interacted with Anika in English. She introduced herself by saying her name, and

Marmaduke began speaking English. Therefore, we describe this as a successful spoken-language change

after verbal identification, not as automatic camera-based recognition of Anika.

## 5. Results and Technical Limitations

The project demonstrated several working functions: personalized facial recognition for Maria Jose,

Spanish conversation, practice with different accents, improvised telenovela dialogue, voice playback,

bilingual interaction, and double-head-touch tail feedback. These results show that the two programs could

support both educational conversation and creative role-play.

However, not every component worked. PiDog experienced recurring problems recognizing or initializing

hardware components during the project. Although ultrasonic proximity detection was written into the

acting code, it did not work successfully during execution. As a result, the planned proximity reaction was

not validated and must not be reported as a successful demonstration.

We also experienced occasional interruptions and inconsistent behavior. The system sometimes struggled

with background noise, and the LLM occasionally produced unexpected or inaccurate responses. Facial

recognition sometimes alternated between confirmed and unconfirmed results. These issues are important

because a convincing demonstration requires not only good dialogue, but also reliable hardware and

consistent sensor input.

## 6. Final Reflection

Overall, Marmaduke performed well as an interactive robot despite technical limitations. The strongest

results were its ability to communicate in Spanish and English, improvise a telenovela character, recognize

Maria Jose's face, and react to a double head touch. This project helped us understand how computer

vision, speech processing, an LLM, and robotic behavior can be combined into one experience. In future

work, we would focus on more stable hardware initialization, better noise handling, and more consistent

recognition before adding new features.
