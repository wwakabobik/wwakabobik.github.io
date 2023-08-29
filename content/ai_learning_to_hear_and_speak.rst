###################################
Making AI chatbot to hear and speak
###################################
:date: 2023-09-01 11:08
:author: wwakabobik
:tags: ai, tts, transcribe, asyncio, threading
:slug: ai_learning_to_hear_and_speak
:category: ai
:status: published
:summary: Learning to interact with chatbots in a natural way. How to make a bot speak and listen using Python
:cover: assets/images/bg/ai.png

I really like the concept when you can expand the possibilities of perception for artificial intelligence. Today, the chat format is the most understandable and popular for interacting with AI. Of course, communication only through chat warms my introverted soul, brought up on `BBS`_ and stories about `BOFH`_. But, nevertheless, why not make communication with bots more "human", teach them to listen, hear and speak? Everything that will be discussed further in the article is not some kind of unique killer-feature, and has long been used in many services that provide access to artificial intelligence, for example, in `aBLT.ai`_ chats. In this article, I want to talk about a Python solution available to anyone.

Transcriptions
--------------

openai.Audio.transcribe
~~~~~~~~~~~~~~~~~~~~~~~

You are most likely using ChatGPT as your main LLM engine. If you turn to its API, you can find a special whisper-1 model, which is also responsible for text transcription. All you need to do to translate your voice into text is call the openai.Audio.atranscribe method. Here and below, I will use asynchronous methods where possible. This is more convenient for organizing parallel work.

.. code-block:: python

    import openai


    async def transcript(file, prompt=None, language="en", response_format="text"):
        """
        Wrapper for the transcribe function. Returns only the content of the message.

        :param file: Path with filename to transcript.
        :param prompt: Previous prompt. Default is None.
        :param language: Language on which audio is. Default is 'en'.
        :param response_format: default response format, by default is 'text'.
                               Possible values are: json, text, srt, verbose_json, or vtt.


        :return: transcription (text, json, srt, verbose_json or vtt)
        """
        kwargs = {}
        if prompt is not None:
            kwargs["prompt"] = prompt
        return await openai.Audio.atranscribe(
            model="whisper-1",
            file=file,
            language=language,
            response_format=response_format,
            temperature=1,
            **kwargs,
        )


To call this function, we pass a file to it. And let's look at the result of the work.

.. code-block:: python

    with open(file_path, "rb") as f:
        transcript = await transcript(file=f, language="en")
    response = await ask_chat(transcript)  # this method is for prompting LLM using pure string


Using a pre-made file is fine, but for the sake of completeness, is it worth assuming that you probably want to record your voice on the fly?

Recording audio: sounddevice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way is to use sounddevice. Since sounddevice records a file in wav format, it is reasonable to convert it to mp3 for transmission over the Internet, for this you can use, for example, pydab. As a result, the code will look something like this:

.. code-block:: python

    import os
    import tempfile
    import uuid

    import sounddevice as sd
    import soundfile as sf
    from pydub import AudioSegment


    def record_and_convert_audio(duration: int = 5, frequency_sample: int = 16000):
    """
    Records audio for a specified duration and converts it to MP3 format.

    This function records audio for a given duration (in seconds) with a specified frequency sample.
    The audio is then saved as a temporary .wav file, converted to .mp3 format, and the .wav file is deleted.
    The function returns the path to the .mp3 file.

    :param duration: The duration of the audio recording in seconds. Default is 5 seconds.
    :param frequency_sample: The frequency sample rate of the audio recording. Default is 16000 Hz.

    :return: The path to the saved .mp3 file.
    """
    print(f"Listening beginning for {duration}s...")
    recording = sd.rec(int(duration * frequency_sample), samplerate=frequency_sample, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    temp_dir = tempfile.gettempdir()
    wave_file = f"{temp_dir}/{str(uuid.uuid4())}.wav"
    sf.write(wave_file, recording, frequency_sample)
    print(f"Temp audiofile saved: {wave_file}")
    audio = AudioSegment.from_wav(wave_file)
    os.remove(wave_file)
    mp3_file = f"{temp_dir}/{str(uuid.uuid4())}.mp3"
    audio.export(mp3_file, format="mp3")
    print(f"Audio converted to MP3 and stored into {mp3_file}")
    return mp3_file


The resulting file can already be fed to the model. But the method looks very clumsy, because the recording continues for a fixed time, no matter how long you speak - less than the set interval and you have to wait for the end of the recording or more, which will lead to the phrase being cut off. Usually the smartest solution is to implement push-to-talk. While the user presses the button, the recording is in progress. This is how instant messengers and many online chats work.

Recording audio: AudioRecorder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

But I still don't think it's smart enough, because it doesn't fit with the concept of AI having ears. As a console user, it would be more convenient for me to do without any buttons, and, by and large, transfer this work to the code, that is, listen constantly, and if speech is noticed in the noise, then recognize it. Well, almost like how Google Assistant, Siri, and smart speakers work in your home. If you don't need to respond to any sound, you can always filter your catch phrase to be recognized first (at the start of the recording).

.. code-block:: python

    import re

    pattern = r"hellos*,?s*bunny"
    if re.match(pattern, transcript, re.IGNORECASE):
        prompt = re.sub(pattern, '', text, flags=re.IGNORECASE).lstrip()
        response = await ask_chat(prompt)

Well, for this task you can use for example my AudioRecorder based on pyaudio. He will listen to the microphone and detect noise (speech) against the background of silence using the RMS (Root Mean Square) method. Full implementation below.

.. code-block:: python

    import math
    import os
    import struct
    import tempfile
    import time
    import uuid
    import wave

    import pyaudio
    from pydub import AudioSegment


    class AudioRecorder:
        """
        The AudioRecorder class is for managing an instance of the audio recording and conversion process.

        Parameters:
        pyaudio_obj (PyAudio): Instance of PyAudio. Default is pyaudio.PyAudio().
        threshold (int): The RMS threshold for starting the recording. Default is 15.
        channels (int): The number of channels in the audio stream. Default is 1.
        chunk (int): The number of frames per buffer. Default is 1024.
        f_format (int): The format of the audio stream. Default is pyaudio.paInt16.
        rate (int): The sample rate of the audio stream. Default is 16000 Hz.
        sample_width (int): The sample width (in bytes) of the audio stream. Default is 2.
        timeout_length (int): The length of the timeout for the recording (in seconds). Default is 2 seconds.
        temp_dir (str): The directory for storing the temporary .wav and .mp3 files. Default is the system's temporary dir.
        normalize (float): The normalization factor for the audio samples. Default is 1.0 / 32768.0.
        pa_input (bool): Specifies whether the stream is an input stream. Default is True.
        pa_output (bool): Specifies whether the stream is an output stream. Default is True.
        """

        def __init__(
            self,
            pyaudio_obj=pyaudio.PyAudio(),
            threshold=15,
            channels=1,
            chunk=1024,
            f_format=pyaudio.paInt16,
            rate=16000,
            sample_width=2,
            timeout_length=2,
            temp_dir=tempfile.gettempdir(),
            normalize=(1.0 / 32768.0),
            pa_input=True,
            pa_output=True,
        ):
            """
            General init.

            This method initializes an instance of the AudioRecorder class with the specified parameters.
            The default values are used for any parameters that are not provided.

            :param pyaudio_obj: Instance of PyAudio. Default is pyaudio.PyAudio().
            :param threshold: The RMS threshold for starting the recording. Default is 15.
            :param channels: The number of channels in the audio stream. Default is 1.
            :param chunk: The number of frames per buffer. Default is 1024.
            :param f_format: The format of the audio stream. Default is pyaudio.paInt16.
            :param rate: The sample rate of the audio stream. Default is 16000 Hz.
            :param sample_width: The sample width (in bytes) of the audio stream. Default is 2.
            :param timeout_length: The length of the timeout for the recording (in seconds). Default is 2 seconds.
            :param temp_dir: The directory for storing the temporary .wav and .mp3 files. Default is temp dir.
            :param normalize: The normalization factor for the audio samples. Default is 1.0 / 32768.0.
            :param pa_input: Specifies whether the stream is an input stream. Default is True.
            :param pa_output: Specifies whether the stream is an output stream. Default is True.
            """
            self.___pyaudio = pyaudio_obj
            self.___threshold = threshold
            self.___channels = channels
            self.___chunk = chunk
            self.___format = f_format
            self.___rate = rate
            self.___sample_width = sample_width
            self.___timeout_length = timeout_length
            self.___temp_dir = temp_dir
            self.___normalize = normalize
            self.___input = pa_input
            self.___output = pa_output
            self.stream = self.init_stream(
                f_format=self.___format,
                channels=self.___channels,
                rate=self.___rate,
                pa_input=self.___input,
                pa_output=self.___output,
                frames_per_buffer=self.___chunk,
            )

        def init_stream(self, f_format, channels, rate, pa_input, pa_output, frames_per_buffer):
            """
            Initializes an audio stream with the specified parameters.

            This function uses PyAudio to open an audio stream with the given format, channels, rate, input, output,
            and frames per buffer.

            :param f_format: The format of the audio stream.
            :param channels: The number of channels in the audio stream.
            :param rate: The sample rate of the audio stream.
            :param pa_input: Specifies whether the stream is an input stream. A true value indicates an input stream.
            :param pa_output: Specifies whether the stream is an output stream. A true value indicates an output stream.
            :param frames_per_buffer: The number of frames per buffer.
            :type frames_per_buffer: int

            :return: The initialized audio stream.
            """
            return self.___pyaudio.open(
                format=f_format,
                channels=channels,
                rate=rate,
                input=pa_input,
                output=pa_output,
                frames_per_buffer=frames_per_buffer,
            )

        def record(self):
            """
            Starts recording audio when noise is detected.

            This function starts recording audio when noise above a certain threshold is detected.
            The recording continues for a specified timeout length.
            The recorded audio is then saved as a .wav file, converted to .mp3 format, and the .wav file is deleted.
            The function returns the path to the .mp3 file.

            :return: The path to the saved .mp3 file.
            """
            print("Noise detected, recording beginning")
            rec = []
            current = time.time()
            end = time.time() + self.___timeout_length

            while current <= end:
                data = self.stream.read(self.___chunk)
                if self.rms(data) >= self.___threshold:
                    end = time.time() + self.___timeout_length

                current = time.time()
                rec.append(data)
            filename = self.write(b"".join(rec))
            return self.convert_to_mp3(filename)

        def write(self, recording):
            """
            Saves the recorded audio to a .wav file.

            This function saves the recorded audio to a .wav file with a unique filename.
            The .wav file is saved in the specified temporary directory.

            :param recording: The recorded audio data.

            :return: The path to the saved .wav file.
            """
            filename = os.path.join(self.___temp_dir, f"{str(uuid.uuid4())}.wav")

            wave_form = wave.open(filename, "wb")
            wave_form.setnchannels(self.___channels)
            wave_form.setsampwidth(self.___pyaudio.get_sample_size(self.___format))
            wave_form.setframerate(self.___rate)
            wave_form.writeframes(recording)
            wave_form.close()
            return filename

        def convert_to_mp3(self, filename):
            """
            Converts a .wav file to .mp3 format.

            This function converts a .wav file to .mp3 format. The .wav file is deleted after the conversion.
            The .mp3 file is saved with a unique filename in the specified temporary directory.

            :param filename: The path to the .wav file to be converted.

            :return: The path to the saved .mp3 file.
            """
            audio = AudioSegment.from_wav(filename)
            mp3_file_path = os.path.join(self.___temp_dir, f"{str(uuid.uuid4())}.mp3")
            audio.export(mp3_file_path, format="mp3")
            os.remove(filename)
            return mp3_file_path

        def listen(self):
            """
            Starts listening for audio.

            This function continuously listens for audio and starts recording when the
            RMS value of the audio exceeds a certain threshold.

            :return: The path to the saved .mp3 file if recording was triggered.
            """
            print("Listening beginning...")
            while True:
                mic_input = self.stream.read(self.___chunk)
                rms_val = self.rms(mic_input)
                if rms_val > self.___threshold:
                    return self.record()

        def rms(self, frame):
            """
            Calculates the Root Mean Square (RMS) value of the audio frame.

            This function calculates the RMS value of the audio frame, which is a measure of the power in the audio signal.

            :param frame: The audio frame for which to calculate the RMS value.

            :return: The RMS value of the audio frame.
            """
            count = len(frame) / self.___sample_width
            f_format = "%dh" % count
            shorts = struct.unpack(f_format, frame)

            sum_squares = 0.0
            for sample in shorts:
                normal_sample = sample * self.___normalize
                sum_squares += normal_sample * normal_sample
            rms = math.pow(sum_squares / count, 0.5)

            return rms * 1000

You may need to experiment with the threshold, timeout, channels, sample_length, chunk, and rate parameters depending on your microphone. And finally, the code to get the entry for the model.

.. code-block:: python

    from utils.audio_recorder import AudioRecorder

    file_path = AudioRecorder().listen()


speech_recognition
~~~~~~~~~~~~~~~~~~

Using OpenAI's ready-made methods is fine, but the tokens are not free, and you might want to use an alternative approach. Or this method does not suit you at all, because you use, for example, llama2 or Bard instead of ChatGPT. Then an alternative solution may be to use the speech_recognition library.
I use google recognition, but you can use other engines if you want, like wit, azure, sphinx. The library has everything we need so that we can recognize both an audio file and record directly using the Microphone() class. Just like my AudioRecorder, it's convenient to use voice activation. The only thing you need to specify is the language of the audio file. Yes, this is not as flexible and convenient as in the method from OpenAI, where you can omit the language parameter and hope that the system itself will select the correct language, but I personally would not recommend not specifying the language in order to avoid errors. An example method might look like this:

.. code-block:: python

    import speech_recognition as sr


    class CustomTranscriptor:
        """
        This is wrapper class for Google Transcriptor which uses microphone to get audio sample.
        """

        def __init__(self, language="en-EN"):
            """
            General init.

            :param language: Language, what needs to be transcripted.
            """
            self.___recognizer = sr.Recognizer()
            self.___source = sr.Microphone()
            self.language = language

            def transcript(self):
        """
        This function transcripts audio (from microphone recording) to text using Google transcriptor.

        :return: transcripted text (string).
        """
        print("Listening beginning...")
        with self.___source as source:
            audio = self.___recognizer.listen(source, timeout=5)

        user_input = None
        try:
            user_input = self.___recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            print("Google Speech Recognition can't transcript audio")
        except sr.RequestError as error:
            print(f"Unable to fetch from resource Google Speech Recognition: {error}")
        except sr.WaitTimeoutError as error:
            print(f"Input timeout, only silence is get: {error}")
        return user_input


Finally, the code for working with chat via voice might look like this.

.. code-block:: python

    import asyncio

    from utils.audio_recorder import AudioRecorder
    from utils.transcriptors import CustomTranscriptor

    async def main():
        method = "google"
        while True:
            try:
                if "google" not in method:
                    file_path = AudioRecorder().listen()
                    with open(file_path, "rb") as f:
                        transcript = await gpt.transcript(file=f, language="en")
                else:
                    transcript = CustomTranscriptor(language="en-US").transcript()
                    pass
                if transcript:
                    print(transcript)
                    response = await ask_chat(transcript)
            except KeyboardInterrupt:
                break

    asyncio.run(main())


Text-to-Speach
--------------

It's time to teach our artificial intelligence to speak. Unfortunately, there is no out-of-the-box solution here if you work directly with LLM. To convert text to voice, one of the TTS implementations must be used.

gtts
~~~~

The first option is to use the gtts library from Google. In this case, gtts will create a file with voice acting, which will need to be played in some player, and then deleted. In order not to produce entities, I use pydub.playback.

.. code-block:: python

    import os
    import tempfile
    from uuid import uuid4

    from gtts import gTTS
    from pydub import AudioSegment, playback


    def process_via_gtts(text):
        temp_dir = tempfile.gettempdir()
        tts = gTTS(text, lang="en")
        raw_file = f"{temp_dir}/{str(uuid4())}.mp3"
        tts.save(raw_file)
        audio = AudioSegment.from_file(raw_file, format="mp3").speedup(1.3)  # haste a bit
        os.remove(raw_file)
        playback.play(audio)

pyttsx
~~~~~~

The second option is to use the pyttsx library. Unlike gtts, speech synthesis occurs on the fly in a loop, which is more convenient and faster when streaming text.

.. code-block:: python

    from time import sleep

    from pyttsx4 import init as pyttsx_init


    def process_via_pytts(text):
        """
        Converts text to speach using python-tts text-to-speach method

        :param text: Text needs to be converted to speach.
        """
        engine = pyttsx_init()
        engine.setProperty("voice", 'com.apple.voice.enhanced.ru-RU.Katya')
        engine.say(text)
        engine.startLoop(False)

        while engine.isBusy():
            engine.iterate()
            sleep(0.1)

        engine.endLoop()

To check which voices do you have, you may get more system voices using following code:

.. code-block:: python

    engine = pyttsx_init()
    engine.getProperty("voices")


Actually, to put it together, we get a response from the chat and play it through some kind of tts engine.

.. code-block:: python

    import asyncio

    from utils.audio_recorder import AudioRecorder
    from utils.transcriptors import CustomTranscriptor
    from utils.tts import process_via_gtts, process_via_pytts

    async def tts_process(text, method):
        """
        Converts text to speach using pre-defined model

        :param text: Text needs to be converted to speach.
        :param method: method of tts
        """
        if "google" in method:
            process_via_gtts(text)
        else:
            process_via_pytts(text)

    async def main():
        method = "google"
        while True:
            try:
                if "google" not in method:
                    file_path = AudioRecorder().listen()
                    with open(file_path, "rb") as f:
                        transcript = await gpt.transcript(file=f, language="en")
                else:
                    transcript = CustomTranscriptor(language="en-US").transcript()
                    pass
                if transcript:
                    print(transcript)
                    response = await ask_chat(transcript)  # this method returns string of whole chatbot response
                    await tts_process(response, "not google")
            except KeyboardInterrupt:
                break

    asyncio.run(main())


Reality and usage challenges
----------------------------

As in a wonderful anecdote about Chapaev: but there is one caveat. Receiving a response from the chatbot takes some time, depending on the model, it can be quite long. When using tts, we have to wait for a full response and start playing the voice, which further increases the final response time. When I first started my experiments, it ruined all the magic of live communication and caused only irritation and a desire to return to satrom-kind text communication. But it is not all that bad. To be honest, I'm in love with ChatGPT's stream method, which returns a response on the fly from ChatCompletion. So my idea is to call tts as soon as something is received in response from the bot. But probably those who used this feature probably know that anything can be returned - both words and sentences or individual letters. And that's a problem if you try to run tts on every chunk you get.

.. code-block:: json

    {
      "id": "chatcmpl-ABCABC",
      "object": "chat.completion.chunk",
      "created": 1234567890,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 0,
          "delta": {
            "content": "Hel"
          },
          "finish_reason": null
        }
      ]
    }

    {
      "id": "chatcmpl-ABCABC",
      "object": "chat.completion.chunk",
      "created": 1234567890,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 1,
          "delta": {
            "content": "lo, "
          },
          "finish_reason": null
        }
      ]
    }
    <...>

    {
      "id": "chatcmpl-ABCABC",
      "object": "chat.completion.chunk",
      "created": 1234567890,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 12,
          "delta": {
            "content": "ay?"
          },
          "finish_reason": null
        }
      ]
    }

First iteration: let's wait for the whole word to be received, and only then start voice acting.

.. code-block:: python

    import string
    import sys

    from utils.tts import tts_process


    async def ask_chat(user_input):
        full_response = ""
        word = ""
        async for response in gpt.str_chat(user_input):
            for char in response:
                word += char
                if char in string.whitespace or char in string.punctuation:
                    if word:
                        tts_process(word)
                        word = ""
                sys.stdout.write(char)  # I use direct stdout output to make output be printed on-the-fly.
                sys.stdout.flush()      # To get typewriter effect I forcefully flush output each time.
                full_response += char
        print("\n")
        return full_response   # if we'll need whole prompt for some reasons later

The result, to be honest, will be so-so - torn. It's probably a good idea to wait for a few words, like 2-3, and speak them out. Words will be added to an asynchronous queue and checked in a parallel running task.

.. code-block:: python

    import string
    import sys

    import asyncio

    from utils.tts import tts_process


    prompt_queue = asyncio.Queue()


    async def ask_chat(user_input):
        full_response = ""
        word = ""
        async for response in gpt.str_chat(user_input):
            for char in response:
                word += char
                if char in string.whitespace or char in string.punctuation:
                    if word:
                        await prompt_queue.put(word)
                        word = ""
                sys.stdout.write(char)  # I use direct stdout output to make output be printed on-the-fly.
                sys.stdout.flush()      # To get typewriter effect I forcefully flush output each time.
                full_response += char
        print("\n")
        return full_response   # if we'll need whole prompt for some reasons later


    async def tts_task():
        limit = 3
        empty_counter = 0
        while True:
            if prompt_queue.empty():
                empty_counter += 1
            if empty_counter >= 3:
                limit = 3
                empty_counter = 0
            words = []
            # Get all available words
            limit_counter = 0
            while len(words) < limit:
                print(len(words))
                try:
                    word = await asyncio.wait_for(prompt_queue.get(), timeout=1)
                    words.extend(word.split())
                    if len(words) >= limit:
                        break
                except asyncio.TimeoutError:
                    limit_counter += 1
                    if limit_counter >= 10:
                        limit = 1

            # If we have at least limit words or queue was empty 3 times, process them
            if len(words) >= limit:
                text = " ".join(words)
                await tts.process(text)
                limit = 1

    async def main():
            asyncio.create_task(tts_task())
            # and rest of the code

This already sounds better, but intonation and punctuation are lost in the process of processing. Finally, let's make the assumption that only sentences should be processed, well, or parts of them, that is, pieces that will end with the characters ".?!,;:".

.. code-block:: python

    import string
    import sys

    import asyncio

    from utils.tts import tts_process


    prompt_queue = asyncio.Queue()


    async def ask_chat(user_input):
        full_response = ""
        word = ""
        async for response in gpt.str_chat(user_input):
            for char in response:
                word += char
                if char in string.whitespace or char in string.punctuation:
                    if word:
                        await prompt_queue.put(word)
                        word = ""
                sys.stdout.write(char)  # I use direct stdout output to make output be printed on-the-fly.
                sys.stdout.flush()      # To get typewriter effect I forcefully flush output each time.
                full_response += char
        print("\n")
        return full_response   # if we'll need whole prompt for some reasons later

    async def tts_sentence_task():
        punctuation_marks = ".?!,;:"
        sentence = ""
        while True:
            try:
                word = await asyncio.wait_for(prompt_queue.get(), timeout=0.5)
                sentence += " " + word
                # If the last character is a punctuation mark, process the sentence
                if sentence[-1] in punctuation_marks:
                    await tts_process(sentence)
                    sentence = ""
            except Exception as error:
                pass

    async def main():
        asyncio.create_task(tts_sentence_task())
        # and rest of the code

If you tried my examples, you will notice that the chat output is interrupted during the voiceover. To fix this, we need to run tts on a separate thread. To do this, we will need to form a second queue for tts. And start another parallel task for the handler.

.. code-block:: python

    import string
    import sys

    import asyncio

    from utils.tts import tts_process


    prompt_queue = asyncio.Queue()
    tts_queue = asyncio.Queue()


    async def ask_chat(user_input):
        # same

    async def tts_sentence_task():
    punctuation_marks = ".?!,;:"
    sentence = ""
    while True:
        try:
            word = await asyncio.wait_for(prompt_queue.get(), timeout=0.5)
            sentence += " " + word
            # If the last character is a punctuation mark, process the sentence
            if sentence[-1] in punctuation_marks:
                await tts_queue.put(sentence)
                sentence = ""
        except Exception as error:
            pass


    async def tts_worker():
        while True:
            sentence = await tts_queue.get()
            if sentence:
                await tts_process(sentence)
                tts_queue.task_done()

    async def main():
        asyncio.create_task(tts_sentence_task())
        asyncio.create_task(tts_worker())
        # and rest of the code

And yet the task is not solved, because, alas, the methods of tts (what is gtts, what is pyttsx) are synchronous. This means that for the duration of voice acting, the execution of the main loop is blocked, and awaits the execution of a synchronous task. To solve this problem, you should, for example, run the players in separate threads. The easiest way to do this is using the threading library.

.. code-block:: python

        import threading


        async def process_via_gtts(text):
        """
        Converts text to speach using gtts text-to-speach method

        :param text: Text needs to be converted to speach.
        """
            temp_dir = tempfile.gettempdir()
            tts = gTTS(text, lang="en")
            raw_file = f"{temp_dir}/{str(uuid4())}.mp3"
            tts.save(raw_file)
            audio = AudioSegment.from_file(raw_file, format="mp3").speedup(1.3)
            os.remove(raw_file)
            player_thread = threading.Thread(target=playback.play(audio), args=(audio,))
            player_thread.start()

        async def tts_process(text):
        """
        Converts text to speach using pre-defined model

        :param text: Text needs to be converted to speach.
        """
        if "google" in self.___method:
            await self.__process_via_gtts(text)
        else:
            player_thread = threading.Thread(target=process_via_pytts, args=(text,))
            player_thread.start()

In this case, we get a new problem - now tts will be played as soon as a new offer appears in the queue. If, by the time the first sentence is spoken, the second sentence is received, then it will be played, then the third, and a cacophony will result. To avoid this, finally, you need to use the semaphore mechanism. Before the work, we check and wait for the release of the semaphore, and upon its completion, we release the semaphore.

.. code-block:: python

    import threading


    semaphore = threading.Semaphore(1)


    def play_audio(self, audio):
        """ Service method to play audio in monopoly mode using pydub

        :param audio: AudioSegment needs to be played.
        """
        playback.play(audio)
        semaphore.release()

    async def process_via_gtts(text):
        """
        Converts text to speach using gtts text-to-speach method

        :param text: Text needs to be converted to speach.
        """
        temp_dir = tempfile.gettempdir()
        tts = gTTS(text, lang=self.___lang)
        raw_file = f"{temp_dir}/{str(uuid4())}.mp3"
        tts.save(raw_file)
        audio = AudioSegment.from_file(raw_file, format="mp3").speedup(self.___speedup)
        os.remove(raw_file)
        semaphore.acquire()
        player_thread = threading.Thread(target=self.play_audio, args=(audio,))
        player_thread.start()

    def process_via_pytts(text):
        """
        Converts text to speach using python-tts text-to-speach method

        :param text: Text needs to be converted to speach.
        """
        engine = self.___pytts
        engine.setProperty("voice", self.___voice)
        engine.say(text)
        engine.startLoop(False)

        while engine.isBusy():
            engine.iterate()
            sleep(self.___frame)

        engine.endLoop()
        semaphore.release()

    async def process(text):
        """
        Converts text to speach using pre-defined model

        :param text: Text needs to be converted to speach.
        """
        if "google" in self.___method:
            await self.__process_via_gtts(text)
        else:
            semaphore.acquire()
            player_thread = threading.Thread(target=self.__process_via_pytts, args=(text,))
            player_thread.start()


As a conclusion
---------------

Why is it needed? Here everyone can answer depending on their tasks and needs. I was curious to explore possible ways to implement "natural communication" with chatbots. For example, my bot can be a personal assistant, available at hand at any time, and behaving the way I expect it to. Well, let's say, ask on the fly to find out the current weather or draw a beautiful necromancer girl riding a white horse.


.. image:: /assets/images/articles/ai/learning_to_hear_and_speak/necromancer.jpg
   :alt: Necromancer girl riding white horse



.. _BBS: https://en.wikipedia.org/wiki/FidoNet
.. _aBLT.ai: https://ablt.ai/
.. _BOFH: http://www.bofharchive.com/