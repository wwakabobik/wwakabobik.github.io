################################
Generate images via API using AI
################################
:date: 2023-11-25 10:14
:author: wwakabobik
:tags: ai, image generation, api, leonardo, dalle, midjourney, python
:slug: ai_image_generators_api
:category: ai
:status: published
:summary: It's time to revisit AI image generators and use them from API. How to generate images via API using AI? Let's compare Leonardo.ai, DALL-E-3 and Midjourney.
:cover: assets/images/bg/ai.png

It's time to revisit AI image generators and use them from API. If you red my previous `article about image generators`_, you know that I am a big fan of `Midjourney`_, but I also liked `Leonardo.ai`_. I am still using them, but recently OpenAI released new version of DALL-E, DALL-E-3, and it's pretty impressive. Moreover, you most probably saw my `youtube video`_ and saw how generators works on the fly. I am going to compare them and see if there are any alternatives.

Leonardo.ai
-----------

For Leonardo.ai I wrote python wrapper, you may find it on `Leonardo API github`_ or `Leonardo API pypi`_. It's pretty simple to use, you just need to create an account and get API key. Then you can use it like this:

.. code-block:: python
    # I'll use async api, but you can use sync one
    from leonardo_api import LeonardoAsync as Leonardo

    leonardo = Leonardo(auth_token=leonardo_token)  # init API
    response = await leonardo.get_user_info()  # get user info, if you need to know your ID, etc
    prompt = "a beautiful necromancer witch resurrects skeletons against the backdrop of a burning ruined castle"
    # Then trigger generation
    response = await leonardo.post_generations(
        prompt=prompt,
        num_images=2,
        negative_prompt="bright colors, good characters, positive",  # make sure it's not too negative
        model_id="e316348f-7773-490e-adcd-46757c738eb7",
        width=1024,
        height=1024,
        guidance_scale=7,  # it's better to be 7+-2
        prompt_magic=True,  # if you want smart enhancement of your prompt
    )
    # this will create generation job, you can check it's status, or use helper method to wait for it
    response = await leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
    print(json.dumps(response[0]["url"]))  # if you generate only one image, it will be not list, use response["url"]


It's pretty simple, isn't it? You can use it to generate images in bulk or vary params of generation.


Dall-E-3
--------

It was a big surprise for me, that OpenAI released new version of DALL-E. DALL-E-2 was total disappointment and actually, complete trash to use it in real life projects, but DALL-E-3 is better. Much better.

To interact with it, you need to create an account on `OpenAI`_ and get API key. I Then you can use mine python wrapper for it (you can find it in `OpenAI API github`_ or `OpenAI API pypi`_). It's pretty simple to use, you just need to create an account on OpenAI and get API key. Then you can use it like this:

.. code-block:: python
    from openai_python_api import DALLE

    dalle = DALLE(auth_token=oai_token, organization=oai_organization)  # by default model="dall-e-3"
    resp = await dalle.create_image_url("robocop (robot policeman, from 80s movie)")

Oh, even simpler than Leonardo.ai :)

Midjourney
----------

Midjourney actually is a pain in ass. Because it's available only via discord, using Discord credentials, and you can't interact with it via API. Moreover, you shouldn't use any automation tools for it. As for Midjourney, and same for Discord. Due to this all that I wrote bellow will violate terms of service. I recommend you not to use it, or use by your own risk. I personally recommend you just wait till web interface / API of Midjourney will be implemented and use it instead of hacking the system.

Ok, at first, to generate image from code, we need at least two parts to get images from it.

Interactions bot
================

It's most crucial and dangerous part. Starting 2021 Discord prohibit to use slash commands by Discord bots and bans all of user-bots accounts. This means that this bot will violate rules of Discord. But, for sure, they exists. You may use ready-made library `discum`_, or, because we need only trigger few things, it'll be enough to trigger single request to Discord.

.. code-block:: python
    import aiohttp


    class DiscordInteractions:
        """"""
        def __init__(self, token, **kwargs):
            """
            Initialize DiscordInteractions class.

            :param token: The token to use for authorization.
            :param kwargs: The default parameters for the interaction.
            """
            self.token = token
            self.headers = {"authorization": self.token}
            self.url = "https://discord.com/api/v9/interactions"
            self.default_params = kwargs

        async def post_interaction(self, my_text_prompt, **kwargs):
            """
            Post any discord interaction.

            :param my_text_prompt: The text prompt to post.
            :type my_text_prompt: str
            :param kwargs: The parameters for the interaction.
            :return: The response from the interaction.
            """
            params = {**self.default_params, **kwargs}

            payload_data = {
                "type": 2,
                "application_id": params.get('application_id'),
                "guild_id": params.get('guild_id'),
                "channel_id": params.get('channel_id'),
                "session_id": params.get('session_id'),
                "data": {
                    "version": params.get('version'),
                    "id": params.get('interaction_id'),
                    "name": "imagine",
                    "type": 1,
                    "options": [
                        {
                            "type": 3,
                            "name": "prompt",
                            "value": my_text_prompt
                        }
                    ]
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload_data, headers=self.headers) as resp:
                    if resp.status != 200 and resp.status != 204:
                        raise ValueError(f"Request failed with status code {resp.status}")


Once again, I don't recommend you to use it, because it's against Discord rules. But, if you want to use it, you can use it like this:

* Open Chrome browser
* Open developer tools (F12)
* Go to Network tab
* Login to Discord via browser
* Find `science` request and copy `authorization` header from it - it's your token

.. image:: /assets/images/articles/ai/image_generators_api/discord_token.jpg
    :alt: Discord token

* Go to Discord channel with Midjouney bot and trigger /imagine slash command
* Find request to `interactions` and copy payload from it
* Paste values from it to `payload_data` variable in `post_interaction` method (i.e. via kwargs)

.. image:: /assets/images/articles/ai/image_generators_api/discord_payload.jpg
    :alt: Discord payload

I highly not to recommend you to use it outside of private guild and channels, so, ensure, that guild_id and channel_id are correct and it's your private channel. For usage, use following:

.. code-block:: python

    discord_interaction = DiscordInteractions(
        token=discord_midjourney_payload["auth_token"],
        application_id=discord_midjourney_payload["application_id"],
        guild_id=discord_midjourney_payload["guild_id"],
        channel_id=discord_midjourney_payload["channel_id"],
        session_id=discord_midjourney_payload["session_id"],
        version=discord_midjourney_payload["version"],
        interaction_id=discord_midjourney_payload["interaction_id"],
    )
    await discord_interaction.post_interaction(my_text_prompt=prompt)


Watcher bot
===========

Second part here is to monitor Midjourney Bot response. You may use self-bot to achieve it, or you can create official bot for such purposes. I like to use `py-cord`_, but, you can use any other framework you want.

At the beginning, you need to navigate to `Discord Developer Applications`_ and create new one. Then:

* Open this application
* Go to Bot tab
* Get the token (if you don't see it, click on `Reset Token` button))
* Scroll down and switch on all flipper switches on "Privileged Gateway Intents" section
* Ensure that all three flipper switches, especially 'MESSAGE CONTENT INTENT' is turned on
* Save changes
* Go to OAuth2 tab
* Select `bot` scope
* Select `Send Messages` and `Read Message History` and `Read Messages/View Channels` permissions
* Invite bot to your channel (where Midjourney bot is), and grant permissions for it.

.. image:: /assets/images/articles/ai/image_generators_api/discord_watcher_bot.jpg
    :alt: Discord watcher bot

Then let's code logic for watcher bot:

.. code-block:: python

    from abc import ABC

    from discord import Intents
    from discord.ext import commands

    from utils.logger_config import setup_logger


    class DiscordWatcher(commands.Bot, ABC):
        def __init__(self, watch_user_id=None, **options):
            """
            Initialize DiscordWatcher class.

            :param command_prefix: The prefix for the bot.
            :param watch_user_id: The user ID to watch.
            :param options: The options for the bot.
            """
            super().__init__(command_prefix='/', intents=Intents.all(), **options)
            self.target_user_id = watch_user_id
            self.___logger = setup_logger("discord_watcher", "discord_watcher.log")
            self.___logger.info('DiscordWatcher initialized')

        async def on_ready(self):
            """This function is called when the bot is ready."""
            self.___logger.debug('We have logged in as %s', self.user)

        async def on_message(self, message):
            """
            This function is called when a message is created and sent.

            :param message: The message that was sent.
            :type message: discord.Message
            :return: The message content.
            :rtype: str
            """
            self.___logger.debug('Got a message from %s : %s : %s', message.author, message.author.id, message.content)
            if message.author.id == self.target_user_id:
                if 'Waiting to start' not in message.content:
                    self.___logger.debug('Found a message from the target user: %s', message.content)
                    if message.attachments:
                        for attachment in message.attachments:
                            self.___logger.debug('Found an attachment: %s', attachment.url)
                            return attachment.url  # instead of return it's better to pass it to queue
                    if message.embeds:
                        for embed in message.embeds:
                            self.___logger.debug('Found an embed: %s', embed.to_dict())
                            return embed.to_dict()
                else:
                    self.___logger.debug('Found a message from the target user, but content is not ready yet...')

Ok, then you may monitor channel for any messages and content. Just execute your bot as follows:

.. code-block:: python

    watcher = DiscordWatcher(watch_user_id=discord_midjourney_payload["application_id"])  # this is Midjourney bot ID
    watcher.run(discord_watcher_token)  # use your bot token here

Now you'll get info from watcher about generated URL by Midjourney. You can use it to download image and use it in your code. Or, you may proceed further, obtain one of the action buttons and click on it via interaction.

Gathering all together and generate images
------------------------------------------

Ok, now we have all parts to compare three API generators. Let's do it.

At the beginning, we need to collect response from Midjourney Watcher bot. We can do it via queue, or via global variable. Or just parse a log. So, let's write a function to do it:

.. code-block:: python

    import time

    def find_and_clear(log_file):
        """
        Find and clear the log file.

        :param log_file: The log file to use for the function.
        :type log_file: str
        :return: The attachment found in the log file.
        :rtype: str
        """
        for _ in range(12):
            with open(log_file, "r+") as file:
                lines = file.readlines()
                for line in reversed(lines):  # read from the end of file
                    match = re.search(r"Found an attachment: (.*)", line)
                    if match:
                        file.truncate(0)  # clear file to make it ready for next iteration
                        return match.group(1)
            time.sleep(5)
        return None

Then let's wrap Midjourney and Leonardo into wrapper generation functions:

.. code-block:: python

    import json


    async def midjourney_wrapper(prompt):
        """
        Wrapper for midjourney testing.

        :param prompt: The prompt to use for the function.
        """
        discord = DiscordInteractions(
            token=discord_midjourney_payload["auth_token"],
            application_id=discord_midjourney_payload["application_id"],
            guild_id=discord_midjourney_payload["guild_id"],
            channel_id=discord_midjourney_payload["channel_id"],
            session_id=discord_midjourney_payload["session_id"],
            version=discord_midjourney_payload["version"],
            interaction_id=discord_midjourney_payload["interaction_id"],
        )
        await discord.post_interaction(my_text_prompt=prompt)
        return find_and_clear(log_file="discord_watcher.log")


    async def leonardo_wrapper(prompt):
        response = await leonardo.post_generations(
            prompt=prompt,
            num_images=1,
            model_id="1e60896f-3c26-4296-8ecc-53e2afecc132",
            width=1024,
            height=1024,
            prompt_magic=True,
        )
        response = await leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
        return json.dumps(response["url"])

Ok, one more thing to do - let's save image from URL. I'll use `aiohttp` and `aiofiles` for it:

.. code-block:: python

    import aiofiles
    import aiohttp


    async def save_image_from_url(url, file_path):
        """
        Save image from url to file.

        :param url: The url to use for the function.
        :type url: str
        :param file_path: The file path to use for the function.
        :type file_path: str
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    f = await aiofiles.open(file_path, mode="wb")
                    await f.write(await response.read())
                    await f.close()
                    print(f"Image successfully saved to {file_path}")
                    return file_path
                print(f"Unable to save image. HTTP response code: {response.status}")
                return None

Well, if DALLE API have such method, it'll be much easier to use it. But, it's not, so, let's use it as is. Last thing to do - gather all methods together and feed them with same prompts. But... you know... If you want to get good results, you need to use different prompts for different generators. Moreover, it's better to follow style guide for each generator. So, let's use different prompts for each generator. In case of Leonardo `promptmagic` and `alchemy` does a great job, but for DALLE and Midjourney it's better to use more detailed prompts. Due to that, why not to delegate it to AI? I'll use aBLT 'mAINA' bot for it. It's already trained to generate prompts for Midjourney and DALLE. So, I'll use `ablt_python_api`_ (`ablt_python_api github`_). So, let's use it:

.. code-block:: python

    import ssl

    import asyncio
    from ablt_python_api import ABLTApi_async as ABLTApi
    from leonardo_api import LeonardoAsync as Leonardo
    from openai_python_api.dalle import DALLE

    # Initialize the APIs
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    dalle = DALLE(auth_token=oai_token, organization=oai_organization)
    leonardo = Leonardo(auth_token=leonardo_token)
    ablt = ABLTApi(bearer_token=ablt_token, ssl_context=ssl_context)


    async def generate_image():  # pylint: disable=too-many-locals
        """
        Generate image.

        :return: The image list with dict (contains url and filepathes).
        :rtype: list
        """
        prompts = (
            "beautiful and scary necromancer girl riding white unicorn",
            "draw a character that is a toast-mascot in cartoon style",
            "ai robots are fighting against humans in style of Pieter Bruegel",
        )
        image_list = []
        for index, prompt in enumerate(prompts):
            midjourney_prompt = await ablt.chat(
                bot_slug="maina",
                prompt=f"Please write a midjourney prompt with aspect ratio 1:1, realistic style: '{prompt}'. "
                f"Give me the prompt only, without any comments and descriptions. "
                f"Just prompt output for midjourney.",
                stream=False,
            ).__anext__()
            dalle_prompt = await ablt.chat(
                bot_slug="maina",
                prompt=f"Please write a dalle3 prompt: '{prompt}'. "
                f"Give me the prompt only, without any comments and descriptions. Just prompt output.",
                stream=False,
            ).__anext__()
            midjourney_prompt = midjourney_prompt.replace("`", "").replace("n", "")
            leonardo_image_url_coro = leonardo_wrapper(dalle_prompt)
            dalle3_image_url_coro = dalle.create_image_url(dalle_prompt)
            midjourney_image_url_coro = midjourney_wrapper(midjourney_prompt)
            leonardo_image_url, dalle3_image_url, midjourney_image_url = await asyncio.gather(
                leonardo_image_url_coro, dalle3_image_url_coro, midjourney_image_url_coro
            )
            leonardo_image_coro = save_image_from_url(leonardo_image_url[0], f"leonardo_image_{index}.png")
            dalle3_image_coro = save_image_from_url(dalle3_image_url[0], f"dalle3_image_{index}.png")
            midjourney_image_coro = save_image_from_url(midjourney_image_url, f"midjourney_image_{index}.png")
            leonardo_image, dalle3_image, midjourney_image = await asyncio.gather(
                leonardo_image_coro, dalle3_image_coro, midjourney_image_coro
            )
            image_list.append(
                {
                    "images": {"leonardo": leonardo_image, "dalle3": dalle3_image, "midjourney": midjourney_image},
                    "url": {
                        "leonardo": leonardo_image_url.strip("'").strip('"'),
                        "dalle3": dalle3_image_url.strip("'").strip('"'),
                        "midjourney": midjourney_image_url.strip("'").strip('"'),
                    },
                    "prompts": {"leonardo": dalle_prompt, "dalle3": dalle_prompt, "midjourney": midjourney_prompt},
                }
            )
        return image_list

Ok, now we have all parts to compare three API generators. Let's do it.

.. code-block:: python

    from pprint import pprint

    async def main():
        """Main function."""
        image_list = await generate_image()
        pprint(image_list)

    asyncio.run(main())

Image generation results
------------------------

"beautiful and scary necromancer girl riding white unicorn"
===========================================================

Simple prompt will lead to simple results, like image of some girl in dark dress riding horse. It's kinda boring. Enhanced prompt version of prompt will looks like:

For DALLE:

.. pull-quote::

    beautiful yet intimidating necromancer girl with flowing dark robes and glowing eyes, riding a majestic white unicorn with a twisted horn, amidst a swirling vortex of spectral souls and arcane symbols, under a moonlit, starless sky.

For Midjourney:

.. pull-quote::

    beautiful and scary white-haired necromancer girl with flaming eyes riding a white unicorn with long spiked twisted horn, realistic, dark lighting, --ar 1:1 --q 5 --v 5.2 --s 750

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_generation_0.png
    :alt: Midjourney's necromancer girl riding white unicorn

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_generation_0.jpg
    :alt: Leonardos's necromancer girl riding white unicorn

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_generation_0.png
    :alt: DALL-E-3's necromancer girl riding white unicorn

All images looks good. To be fair, I like Midjourney's image more because of realistics, but it's just my personal opinion. DALLE's image is more related to prompt, but it looks like collage, and it's not a realistic at all. Leonardo's image is good, looks like dark fantasy or game art. In general, all images are good, just depends on your needs.

"draw a character that is a toast-mascot in cartoon style"
==========================================================

DALLE prompt:

.. pull-quote::

    A cartoon-style character designed as a whimsical toast-mascot, with butter-pat shoes, a cheerful smile, and a crusty bread texture, holding a jam jar in one hand and a butter knife in the other, set against a breakfast-themed backdrop with eggs and bacon

Midjourney prompt:

.. pull-quote::

    a character that is a toast-mascot, cartoon style, realistic textures, expressive face, standing pose, with a lice of butter, wearing a small chef hat, --ar 1:1 --q 2 --niji

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_generation_1.png
    :alt: Midjourney's toast-mascot

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_generation_1.jpg
    :alt: Leonardos's toast-mascot

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_generation_1.png
    :alt: DALL-E-3's toast-mascot

Well, cartoon style seems simpler to all models. Starting v5.2 all of Midjourney models seems to be more scenery and realistic, so, it looks like a cartoon movie, not just a drawing, and if you want to generate something like that, you need to take it into account even using niji model. Leonardo is good, looks like character from casual coop game like Overcooked. I like it. DALLE is good too, and, to be fair, much more clear, more relevant to prompt, as it was for first image. But still it have less stylization and creativity, to get more artistic results, you need to use more creative prompts.

"ai robots are fighting against humans in style of Pieter Bruegel"
===================================================================

DALLE prompt:

.. pull-quote::

    A horde of AI robots clashing with human warriors in a chaotic and detailed landscape reminiscent of Pieter Bruegel's style, with an emphasis on the tumult of the battle and the contrast between the mechanical forms of the robots and the organic figures of the humans, set against a backdrop of a 16th-century European village.

Midjourney prompt:

.. pull-quote::

    ai robots, human warriors, epic battle, Bruegel style, dynamic composition, 16th-century European landscape, dark dramatic clouds, earthy color palette, metallic textures, --ar 1:1 --v 5 --q 5

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_generation_2.png
    :alt: Midjourney's robots fighting against humans

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_generation_2.jpg
    :alt: Leonardos's robots fighting against humans

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_generation_2.png
    :alt: DALL-E-3's robots fighting against humans

I expect nothing from models, just something  like similar to topic. Something quite absourdistic, like suffering middle ages art. And I was surprised by results. Midjourney image have quite a lot of details, strange, scary robots and brave medieval humans. I looked it for a several minutes to get all details. Colors are great too. Leonardo is quite average. It's accurate, some medieval landscape, some robot-like creatures and... probably some humans defending the castle. Well, if I saw it in internet, I'll probably just scroll it through. DALLE image much more strange and atmospheric. It's like some kind of surrealistic art. I like it, but background details a bit messy, with generation errors, but, who cares - it's kind a normal for Breugel's style.

Summarizing generations I may say that all models works fine, especially with enriched prompts. In average, I still like Midjourney more, but recent DALLE-3 it's breakthrough indeed. It's much more accurate and more creative rather than Leonardo, but you need to be careful with it.

.. image:: /assets/images/articles/ai/image_generators_api/dalle_generation_0_alt.png
    :alt: DALL-E-3 vision of necromancer girl

As you can see, it contains unique details and vision, like attention to horse hair or moss on trees. It's impressive. But some details may still looks like collage, so, you need to be careful with it. And, of course regenerate, repeat and variate...

Create variations
-----------------

All of the models is able to create variations. Simplest here is Midjourney. All you need to do is to pass same (or a bit different from original) prompt and web link to any existing image (i.g. generated by Midjourney). It will be something like this:

.. code-block:: python

    async def get_midjourney_variations(image_list):
        """
        Get variations from midjourney images.

        :param image_list: The image list to use for the function.
        :type image_list: list
        :return: The variations from midjourney images.
        :rtype: list
        """
        variations = []
        for index, images in enumerate(image_list):
            midjourney_url = await midjourney_wrapper(f'{images["url"]["midjourney"]} {images["prompts"]["midjourney"]}')
            midjourney_file = await save_image_from_url(midjourney_url, f"midjourney_variation_{index}.png")
            variations.append({"url": midjourney_url.strip("'").strip('"'), "image": midjourney_file})
        return variations


For DALLE you may use any of `create_variation` methods, but I need to say that nowdays variations operated by DALL-E-2 and you may expect downgrade quality of your images. But due to that we have no choice, let's use it:

.. code-block:: python

    async def get_dalle_variations(image_list):
        """
        Get variations from dalle3 images.

        :param image_list: The image list to use for the function.
        :type image_list: list
        :return: The variations from dalle3 images.
        :rtype: list
        """
        variations = []
        dalle.default_model = None  # disable dall-e-3 because isn't supported for variations yet
        for index, images in enumerate(image_list):
            file_path = images["images"]["dalle3"]
            # you may also use dalle.create_variation_from_url_and_get_url(url), but it's won't work for dalle3 urls
            with open(file_path, "rb") as file:
                url = await dalle.create_variation_from_file_and_get_url(file)
                image = await save_image_from_url(url, f"dalle3_variation_{index}.png")
                variations.append({"url": url.strip("'").strip('"'), "image": image})
        return variations

For Leonardo you need to do same thing as for DALL-E, but the difference here that you may re-use seed (what may not be a good idea) or upload initial image to Leonardo and use it as seed. I'll use second approach:

.. code-block:: python

    async def get_leonardo_variations(image_list):
        """
        Get variations from leonardo images.

        :param image_list: The image list to use for the function.
        :type image_list: list
        :return: The variations from leonardo images.
        :rtype: list
        """
        variations = []
        for index, images in enumerate(image_list):
            image_file = images["images"]["leonardo"]
            leonardo_generation = await leonardo.upload_init_image(image_file)
            response = await leonardo.post_generations(
                prompt=images["prompts"]["leonardo"],
                num_images=1,
                model_id="1e60896f-3c26-4296-8ecc-53e2afecc132",
                width=1024,
                height=1024,
                prompt_magic=True,
                init_image_id=leonardo_generation,
            )
            response = await leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
            leonardo_url = json.dumps(response["url"])
            leonardo_file = await save_image_from_url(leonardo_url, f"leonardo_variation_{index}.png")
            variations.append({"url": leonardo_url, "image": leonardo_file})
        return variations

And, finally, let's gather all together:

.. code-block:: python

    async def generate_variations(image_list):
        """
        Generate variations.

        :return: The variations list.
        :rtype: list
        """

        dalle_variations_coro = get_dalle_variations(image_list)
        midjourney_variations_coro = get_midjourney_variations(image_list)
        leonardo_variations_coro = get_leonardo_variations(image_list)
        dalle_variations, midjourney_variations, leonardo_variations = await asyncio.gather(
            dalle_variations_coro, midjourney_variations_coro, leonardo_variations_coro
        )
        variations = []
        for leonardo_item, dalle_item, midjourney_item, image_item in zip(
            leonardo_variations, dalle_variations, midjourney_variations, image_list
        ):
            variations.append(
                {
                    "images": {
                        "leonardo": leonardo_item["image"],
                        "dalle3": dalle_item["image"],
                        "midjourney": midjourney_item["image"],
                    },
                    "url": {
                        "leonardo": leonardo_item["url"],
                        "dalle3": dalle_item["url"],
                        "midjourney": midjourney_item["url"],
                    },
                    "prompts": image_item["prompts"],
                }
            )
        return variations

    async def main():
        """Main function."""
        variation_list = await generate_variations(image_list)
        pprint(variation_list)

    asyncio.run(main())

Variations results
------------------

Brief explanation: variations usually is worse than regeneration with slight different prompt. Because during regeneration based on image model will lost some aspects of initial prompt, which may be much more significant for you. In other words, it's something like: "I want something like that you have, bot it should not be the same, surprise me". But, let's see what we have.

"beautiful and scary necromancer girl riding white unicorn"
===========================================================

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_variation_0.png
    :alt: Midjourney's necromancer girl riding white unicorn

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_variation_0.jpeg
    :alt: Leonardo's necromancer girl riding white unicorn

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_variation_0.png
    :alt: Dall-e-2's necromancer girl riding white unicorn

Midjourney lost dark side of girl, but in general still nice. Leonardo is best here - it's more accurate and more relevant to prompt, but in same time it's slightly different from original prompt. DALLE is not good at all, it looks blurry, some details lost, but, I may say that it have it's own charm.

"draw a character that is a toast-mascot in cartoon style"
==========================================================

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_variation_1.png
    :alt: Midjourney's toast-mascot

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_variation_1.jpg
    :alt: Leonardo's toast-mascot

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_variation_1.png
    :alt: Dall-e-2's toast-mascot

Same as first try, all models works fine. Midjourney is more realistic (may be even better related to initial query), Leonardo is more cartoonish, with more detailed bread, DALLE is simplified, but still a clear and nice character. All images are good, DALLE level looks like DALL-E-2 but still usable.

"ai robots are fighting against humans in style of Pieter Bruegel"
===================================================================

Midjourney:

.. image:: /assets/images/articles/ai/image_generators_api/midjourney_variation_2.png
    :alt: Midjourney's robots fighting against humans

Leonardo:

.. image:: /assets/images/articles/ai/image_generators_api/leonardo_variation_2.jpg
    :alt: Leonardo's robots fighting against humans

DALLE:

.. image:: /assets/images/articles/ai/image_generators_api/dalle_variation_2.png
    :alt: Dall-e-2's robots fighting against humans

Last try, and it most interesting. Midjourney is still good, some new details were added, like robot's helmet, but now seems there is a war between robots and reptiloids. I knew it! Leonardo is average again. It's ok, but I have nothing to say about it. DALLE iage now is complete mess and prompt ruined at all. So, fail. But I still like it, like a way of converting normal art to surrealistic, contemporary. Hm, strange thing, but as it is.

Conclusion
----------

Working with AI image generators via API is fun. It's fast, it's bulk, fast enough, it's relatively cheap than spending your time and tokens. All APIs in except of Midjourney is pretty simple to use, and you can use it in your projects. Midjourney is not, but it's still usable. I hope that Midjourney will release web interface and API soon, so, we'll be able to use it in our real-world projects. So, I hope you liked my experiments, more to come...

.. _article about image generators: https://wwakabobik.github.io/2023/08/ai_image_generators/
.. _Midjourney: https://midjourney.com/
.. _Leonardo.ai: https://leonardo.ai/
.. _Leonardo API github: https://github.com/wwakabobik/leonardo_api
.. _Leonardo API pypi: https://pypi.org/project/leonardo-api/
.. _OpenAI: https://openai.com/
.. _OpenAI API github: https://github.com/wwakabobik/openai_api
.. _OpenAI API pypi: https://pypi.org/project/openai-python-api/
.. _youtube video: https://www.youtube.com/watch?v=Ph7E`QSZPmGc
.. _discum: https://pypi.org/project/discum/
.. _py-cord: https://pypi.org/project/py-cord/
.. _Discord Developer Applications: https://discord.com/developers/applications/
.. _ablt_python_api: https://pypi.org/project/ablt-python-api/
.. _ablt_python_api github: https://github.com/ablt-ai/ablt_python_api
