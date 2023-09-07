###################
AI image generators
###################
:date: 2023-08-25 16:14
:author: wwakabobik
:tags: ai, image generation
:slug: image_generators
:category: ai
:status: published
:summary: Are there alternatives for Midjourney? Can they compete with it? I am doing my research on generative AI image tools and services.
:cover: assets/images/bg/ai.png

It's been a year since I signed up for a paid subscription to Midjourney. With the help of this amazing generative neural network, I have created thousands of different images - from desktop wallpapers and virtual background for Zoom calls, illustrations for my movie to the cover design of my Youtube channel and this site. With the advent of such powerful tools, creating unique illustrations has become as simple as possible for a non-artist, and the results, for my taste, look professional, not to say that they were prepared by an experienced graphic designer or artist.

However, in addition to the rather high monthly cost of Midjourney, it has enough disadvantages. Firstly, after the fast processing limit for a month is exhausted, Midjourney switches to the "relaxed" generation mode, which increases the time it takes to get the result. This is, in essence, a trifle. A much more sore point is the lack of at least some kind of API to use the results of work directly from the code, and, relatively speaking, substitute immediately, for example, in the responses of the OpenAI bot.

Therefore, in order not to be a rigid conservative, I decided to study what alternatives appeared during the year. Most likely, there are at least two dozen of them, but I will list only a part of them.

For testing solutions, I will use just three queries to understand how the network works with styles and portraits, as well as to understand how the network works with scenes, context and special effects.

So let's get started.

Midjourney
----------

- **Price**: $30/month
- **API**: No (only Discord bot)
- **Engine**: Midjourney
- **Site**: `Midjourney`_

Original prompt:

.. pull-quote::
   geometric shapes, bright colors, portrait of elon musk, Hyperdetailed, High Fidelity

.. image:: /assets/images/articles/ai/image_generators/elon_musk_midjourney.jpg
   :alt: Elon Musk in geometric shapes by Midjourney

Well, it's stylized, but not a best portrait of Musk, but similar person. Seems he saw some wierd stuff or had a hard night.

.. pull-quote::
   necromancers, skeletons, fog, Allods scene, magical source with flame reflection, mystical artifacts, dim lighting, scene, High angle

.. image:: /assets/images/articles/ai/image_generators/necromancers_midjourney.jpg
   :alt: Necromancers and skeletons by Midjourney

As for me it looks awesome, but still needs to be tuned or rephrased, because I see only skeletons, but not necromancers. They're probably old liches, aren't they?

.. pull-quote::
   palms of young woman, watercolor, dark background

.. image:: /assets/images/articles/ai/image_generators/palms_midjourney.jpg
   :alt: Palms by Midjourney

It's pretty accurate with delicate colors of watercolor. Yeah, it's still a bit strange because of leaves motives, because "palm" word brings a bit of fuzziness to query. But challenging is better, right?


DALL-E-2
--------

- **Price**: $0.02/image
- **API**: Yes
- **Engine**: DALL-E
- **Site**: `DALL-E-2`_

The first, most famous tool, besides Midjourney, is, of course, DALL-E2 from OpenAI. But, like a year ago, it is still an order of magnitude worse. In general, I would say that it absolutely does not fulfill the tasks assigned to it, some words, for example, mentions of famous personalities are banned in it, and the auto-translator works very badly (and if you do not use English for queries, then it is better to use third party translation service than another language to request to DALL-E2). The only plus of DALL-E2 is native integration with ChatGPT, but even then, not everything is simple here.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_dalle.jpg
   :alt: Elon Musk in geometric shapes by DALL-E-2

Due to banned person's words it's some person, but not a Musk, that's for sure.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_dalle.png
   :alt: Necromancers and skeletons by DALL-E-2

Not bad as concept. But same as for Musk image - it's only schematic, with no stylization or details. Actually, DALL-E can draw (guess) some objects, but it will be generic image with no details, and you never get any scene you want.


Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_dalle.jpg
   :alt: Palms by DALL-E-2

It's also schematic, but it's five fingers, all is correct. Colors are pastel too.


BlueWillow
----------

- **Price**: $5/month+
- **API**: No (only Discord)
- **Engine**: StableDiffusion (?)
- **Site**: `BlueWillow`_

In according to market positioning, main competitor of Midjourney. And, actually, the reason of this research. BlueWillow looks quite similar to Midjourney and supports similar keywords, like **--ar** flag. And, same as Midjourney works only via Discord chat and have no API. Seems it should generate at least Midjourney v4 level images? But not...

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_willow.jpg
   :alt: Elon Musk in geometric shapes by BlueWillow

Hm, I feel lack of stylization. Musk seems like same on photo, but it's not artistic and stylized at all.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_willow.jpg
   :alt: Necromancers and skeletons by BlueWillow

All is getting worse if scene is prompted, there are leak of details and characters. Moreover, killer-feature of Midjourney, like stylization and perspective seems totally absent. It looks like first versions of Midjourney with features (like remix/expand) of latest. Of course, it's cheaper than Midjourney, but, seriously, maybe I can find something better, especially when I'll be able to set different models by myself?

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_willow.jpg
   :alt: Palms by BlueWillow

Here it is. Extra fingers, tangled, in an unnatural position. As wierd, as it was in early models. I disappointed.


StableDiffusion
---------------

- **Price**: $0.002/image
- **API**: Yes
- **Engine**: StableDiffusion
- **Site**: `StableDiffusion`_

Most likely, most powerful and semi-open AI art generated model and service with simple and fast API. Actually, most of the services works on StableDiffusion engine, and, probably even BlueWillow also, but on homebrew tuned model. This means that next results will look quite similar, and main difference between them will be only learning curve.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_stablediffusion.jpg
   :alt: Elon Musk in geometric shapes by StableDiffusion

Hm... I hate to say it, but I like this portrait of Elon a lot more than the Midjourney version. Bravo. I am impressed.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_stablediffusion.jpg
   :alt: Necromancers and skeletons by StableDiffusion

When I saw this result I was discouraged. On the one hand, this is not what I asked for. On the other hand, apparently the dataset for training StableDiffusion is apparently familiar with the Allods universe, and its output is very similar to what could be seen in Evil Islands or, God forgive me, in Allods-online. This is a rather curious result, but after Midjourney it is unusual to see completely different weights for words in a query.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_stablediffusion.jpg
   :alt: Palms by StableDiffusion

And this art is incorrect. Unfortunately, seems there is a problems with this model, or model outdated.

Because StableDiffusion is Open-source project, you may also like to run it on your CUDA server, if you want so, or create ad tune custom model. Link_ to StableDiffusion github.

Dreamstudio.ai
--------------

- **Price**: $0.002/image
- **API**: Yes
- **Engine**: StableDiffusion
- **Site**: `Dreamstudio.ai`_

Actually it's the same engine as Stablediffusion web, but on other domain. Should I expect any difference here?

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_dreamstudio.jpg
   :alt: Elon Musk in geometric shapes by Dreamstudio.ai

I like pastel colors, seems other seed? Or dataset?

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_dreamstudio.jpg
   :alt: Necromancers and skeletons by Dreamstudio.ai

Totally different, like dark-fantasy illustration. Like it! It's not so bright and detailed as Midjourney did, but it's quite accurate.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_dreamstudio.jpg
   :alt: Palms by Dreamstudio.ai

Looks better then previous model results, but still with extra fingers. Seems, as for early midjourney it can be fixed with accurate prompt or pose, but I don't like to spend extra effort to fight against errors. Especially when it was fixed for V4 and V5 Midjourney models.


Dream.ai
--------

- **Price**: $10/month
- **API**: Yes
- **Engine**: Custom StableDiffusion
- **Site**: `Dream.ai`_

Looks like it's clone of Dreamstudio.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_dream_ai.jpg
   :alt: Elon Musk in geometric shapes by Dream.ai

No, seems I'm wrong. There's a slight difference between pure Stablediffusion. I feel leak of stylization, but creativity is plus.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_dream_ai.jpg
   :alt: Necromancers and skeletons by Dream.ai

Same here. I like creativity of scene, but it's not precise and lack of details. It might be good to say "based on", but not to "illustration of".

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_dream_ai.jpg
   :alt: Palms by Dream.ai

Seems there are five fingers! But pose is strange, and there is only one hand. It's fine, but drafty and inaccurate.

Leonardo.ai
-----------

- **Price**: $0.001/image
- **API**: Yes
- **Engine**: Custom StableDiffusion
- **Site**: `Leonardo.ai`_

This site looks like aggregator for several stablediffusion models, and still under development. Actually, before we proceed, I must say that's only one service I was impressed. Because you can choose not only "stylization" for images, but really different models, or even create and share your own model by training using your own datasets. Moreover, site offers unique features of processing and editing images.

.. image:: /assets/images/articles/ai/image_generators/models_of_leonardo.jpg
   :alt: Fine-tuned models of Leonardo.ai

.. image:: /assets/images/articles/ai/image_generators/generation_of_leonardo.jpg
   :alt: Generation tool by Leonardo.ai

.. image:: /assets/images/articles/ai/image_generators/dataset_leonardo.jpg
   :alt: Training with custom dataset of Leonardo.ai

It looks powerful, because you can create and edit your photos with AI, create textures for 3D-models, prepare and try fine-tuned models.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_leonardo.jpg
   :alt: Elon Musk in geometric shapes by Leonardo.ai

Hm, it's kind of strange. Musk here is too young, and I don't like mix of photo style with geometry background. But I used random, not photo-related model.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_leonardo.jpg
   :alt: Necromancers and skeletons by Leonardo.ai

Wow, that's my favorite. It looks like illustration of book of Nick Perumov or Chasers of the Wind by Alexey Pehov. Cool, rally cool. Because seems dataset fine-tuned for gaming and digital-art. It's not such good for general models, like Midjourney, but, who cares, if we can always switch to another model? Let's do it for rest image...

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_leonardo.jpg
   :alt: Palms by Leonardo.ai

It's quite realistic, accurate and detailed. Same as for Midjourney, there is a trick with palm tree and hands palms.


Lexica.art
----------

- **Price**: $0.008/image
- **API**: No
- **Engine**: Custom StableDiffusion
- **Site**: `Lexica.art`_

Lexica - initially reverse image search and image describe tool. But, who tell that it can't generate image by own power?

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_lexica.jpg
   :alt: Elon Musk in geometric shapes by Lexica.art

Elon here looks over stylized. Yes, I like geometry pattern, but Elon itself is too cartoon-like, sketchy, as french caricatures.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_lexica.jpg
   :alt: Necromancers and skeletons by Lexica.art

Scene of necromancers also focused on stylization, lighting and filters, not on details. Moreover, it's a bit romantic atmosphere.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_lexica.jpg
   :alt: Palms by Lexica.art

And as apogee here are palms. It's very creative, looks like popular digital art from Devianart, but it's not correct. It's only shapes of palms, and neon, but not a watercolors at all. In one word, Lexica's dataset is focused on stylization and creativeness, but not on scenes and persons.


Nightcafe.art
-------------

- **Price**: $0.015/image
- **API**: No
- **Engine**: Custom StableDiffusion, DALL-E-2
- **Site**: `Nightcafe.art`_

Nightcafe offers to use different type of models, what is rare option in my research. Here you can find mostly StableDiffusion based models, DALL-E, CLIP and VQGUN and StyleGUN models (actually it's also DALL-E related models, powered by OpenAI).

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_nightcafe.jpg
   :alt: Elon Musk in geometric shapes by Nightcafe

Musk with usage of SDXL1.0 model looks very close to Midjourney results. It's somebody looks-like Musk, or bad image of Elon. In general it's ok, but not best.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_nightcafe.jpg
   :alt: Necromancers and skeletons by Nightcafe

In other hand, necromancer's results looks close to Dreamstudio.ai, it's dark, conceptual fantasy. Not accurate, but I like it.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_nightcafe.jpg
   :alt: Palms by Nightcafe

As for other StableDiffusion models, palms have extra fingers. Palette looks fine, but model still needs to be improved. In brief, it's more expensive version of pure Stablediffusion (Dreamstudio.ai) with no API, but more user-friendly, because you can use several presets, style keywords and siting from UI.


Playground.ai
-------------

- **Price**: Free / $15/month
- **API**: No
- **Engine**: Custom StableDiffusion, DALL-E-2
- **Site**: `Playground.ai`_

Same as Nightcafe, Playground.ai offers more than one StableDiffusion model and DALL-E-2 as extra option. Moreover, it one of the model what is available for free for 1.000 usages per day! But, in other hand, limited for resolution and level of details, what can be crucial for end user.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_playground_ai.jpg
   :alt: Elon Musk in geometric shapes by Playground.ai

As for same SDXL1.0 model Elon looks stylish and correct. Maybe one of the best of his image for today.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_playground_ai.jpg
   :alt: Necromancers and skeletons by Playground.ai

Same for living bones: it's still dark fantasy, with bright fire. It's more detailed than I got previously, but as for me, I feel a bit of slight decline here.
Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_playground_ai.jpg
   :alt: Palms by Playground.ai

I regenerated palms three times actually, because of free of cost it's not a problem to set guidance and quality levels to get better results and get rid of StableDiffusion extra fingers problems. It's still not fix within model, but anyway, "relatively" free of usage give you extra possibility to spend your time to get what you want.


Dreamlike.art
-------------

- **Price**: $0.008/image
- **API**: No
- **Engine**: Custom StableDiffusion, Kandinsky
- **Site**: `Dreamlike.art`_

Dreamlike.art is first engine which uses Kandinsky model in addition to regular StableDiffusion models. It's not a best model at all, but you can try in from the box.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_dreamlike.jpg
   :alt: Elon Musk in geometric shapes by Dreamlike.art

As you can see, Kandinsky model is not precise, and primary focused to create digital art. This means model is more relaxed than StableDiffusion, have less dataset, but can operate with different styles much better than regular model.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_dreamlike.jpg
   :alt: Necromancers and skeletons by Dreamlike.art

Necromancers here looks like Gloomhaven storybook illustrations. It's fine, bright, but also isn't detailed.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_dreamlike.jpg
   :alt: Palms by Dreamlike.art

Palms are catastrophic, because model can't handle details correctly. But, if you plan to use this service, you always can switch to SDXL or StableDiffusion 1.5 or 2.1 to get photorealistic results.


Fotor
-----

- **Price**: $0.03/image
- **API**: No
- **Engine**: Fotor
- **Site**: `Fotor`_

Fotor is chinese original AI image generator. It's laconic in general, but not limited to, because you can also use separate AI-based image edit tools.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_fotor.jpg
   :alt: Elon Musk in geometric shapes by Fotor

Here is Elon. But with strange stylization. It might be good, but needs to be extra tuned.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_fotor.jpg
   :alt: Necromancers and skeletons by Fotor

I have a strange feeling, that's very close to DALL-E results with style filters. It's not very detailed, colors are dimmed, but in general it's correct.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_fotor.jpg
   :alt: Palms by Fotor

Looks semi-correct. Lef-like palm, and second image contains only five fingers, but there is only one palm, and it looks not anatomy correct.


Bing
----

- **Price**: Free
- **API**: No
- **Engine**: DALL-E
- **Site**: `Bing`_

Bing image generator now is for free for 100 images. Looks like Microsoft prepares to introduce image generation as feature for Bing engine, but, should they?

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_bing.png
   :alt: Elon Musk in geometric shapes by Bing

As for pure DALL-E, prompt restrict to use "banned" words, and here are elon in this list. Not sure why, but just prompting "engineer" or "scientist" gives similar "contemporary art" result.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_bing.jpg
   :alt: Necromancers and skeletons by Bing

Yeah, it's DALL-E style, but it looks significantly worse than in Fotor, looks like in early 3D computer games.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_bing.jpg
   :alt: Palms by Bing

Palms looks like DALL-E. But if for pure DALL-E I tried to regenerate image for couple of times to get extra finger, but with no luck; for Bing there are errors. And I must ask Microsoft: are they tried to use extra dataset? But why all get worse?


Russian DALL-E
--------------

- **Price**: Free
- **API**: No
- **Engine**: Kandinsky
- **Site**: `RuDALL-E`_

As extra research I tried to use russian image generator services. And one of them is service by Sber, based od Kandinsky models, Russian DALL-E.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_kandinsky2.jpeg
   :alt: Elon Musk in geometric shapes by Russian DALL-E

I don't know why, but Elon is banned by Sber's Kandinsky. Thus, result of generation of geometry portrait is very abstract.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_kandinsky2.jpeg
   :alt: Necromancers and skeletons by Russian DALL-E

As for Kandinsky 2.1 in Dreamlike.ai, next version of Kandinsky generates pretty same image of dark fantasy. We already saw it.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_kandinsky2.jpeg
   :alt: Palms by Russian DALL-E

Instead of 2.1 version version 2.2 of Kandinsky more accurate and can try to draw palm correctly. Almost. But, guys, what's funny here. I used native (russian) prompts to obtain images. In russian language "palm" is just part of the hand, and have no "tree" meaning. But as you can see, seems my russian prompt was translated to english and you still able to see palm tree on image. What a heck!


Fusionbrain
-----------

- **Price**: Free
- **API**: No
- **Engine**: Kandinsky
- **Site**: `Fusionbrain`_

It should be clone of Kandinsky 2.2 by Sber with only interface difference. Because, as described, service used absolutely same engine powered by Sber cloud.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_fusionbrain.jpg
   :alt: Elon Musk in geometric shapes by Fusionbrain

And here are ususual result. "Export" version of Kandinsky 2.2 have no "banned" words instead of local "Russian DALL-E", and seems have different dataset, because Musk looks like Nightcafe or mix with Midjourney results.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_fusionbrain.jpg
   :alt: Necromancers and skeletons by Fusionbrain

Sceleton art are pretty differs than previous service output. It looks like more 3D-dimensional, but as for me here are very small details, what makes image unnatural.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_fusionbrain.jpg
   :alt: Palms by Fusionbrain

Palms looks scary as for me. And, of course, there are extra fingers on them.

What should I say extra here, that Kandinsky 2.2 is available for modification and use on your devices, of course, if you have such capabilities (Github_).


Shedevrum
---------

- **Price**: Free
- **API**: No
- **Engine**: Shedevrum
- **Site**: `Shedevrum`_

It's last one service in my research. Shedevrum is AI generated developed by Yandex. There is no much information about underlying model, and I guess this based on some open model, like StableDiffusion. But main disadvantage is here that tool is available only using mobile app.

Elon Musk:

.. image:: /assets/images/articles/ai/image_generators/elon_musk_shedevrum.jpg
   :alt: Elon Musk in geometric shapes by Shedevrum

Yandex prefer to ban Elon musk, so, space enthusiast looks like any generic retro futuristic illustration. Nice, but there is no geometry here.

Necromancers:

.. image:: /assets/images/articles/ai/image_generators/necromancers_shedevrum.jpg
   :alt: Necromancers and skeletons by Shedevrum

Image looks too generic and blurry. Yes, I know, there some representation of fog, but it's too inaccurate.

Palms:

.. image:: /assets/images/articles/ai/image_generators/palms_shedevrum.jpg
   :alt: Palms by Shedevrum

Here are the scenery. Partly correct images, but focus not on palms, but on woman.

Overall it's not too bad as I ranked it, but it's completely unusable for regular way, especially here are lack of any tunes.


Summary
-------

As last, but not least I want to say that I skip several services and tools, like Getimg.ai, Easy-Peasy AI, Prompt Hunt, GLIDE, Karlo, Re.Art, ProAI, ProductAI, OmniInfer, Scum, Stormy, AlterEgoAI, Ausmium, B^ DISCOVER, etc.. It might be challengers, it might be not. Who knows, when it's time to revise them. Everything is moving too fast in AI. So, as summary I prepared following score table for tools in my article.

+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
| Service            | Engine                      | Score     | Price           | Count of models | API  | Language | Shared model? |
+====================+=============================+===========+=================+=================+======+==========+===============+
| `Midjourney`_      | Midjourney                  | 10        | \$30/month      | 6               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Leonardo.ai`_      | Custom StableDiffusion      | 9         | \$0.001/image   | Many            | Yes  | English  | Yes           |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`StableDiffusion`_  | StableDiffusion             | 8         | \$0.002/image   | 6               | Yes  | English  | Yes           |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Dreamstudio.ai`_   | StableDiffusion             | 8         | \$0.002/image   | 6               | Yes  | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Dream.ai`_         | StableDiffusion             | 7         | \$10/month      | 1               | Yes  | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Dreamlike.art`_    | Stablediffusion / Kandinsky | 7         | \$0.008/image   | 8               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`BlueWillow`_       | StableDiffusion?            | 7         | \$5+/month      | 1               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Lexica.art`_       | Custom StableDiffusion      | 7         | \$0.015/image   | 1               | Yes  | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Nightcafe`_        | Custom StableDiffusion      | 7         | Free/\$15/month | 14              | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`PlaygroundAI`_     | Custom StableDiffusion      | 6         | \$0.002/image   | 4               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Fotor`_            | Fotor (seems DALL-E based)  | 6         | \$0.030/image   | 1               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`RuDALL-E`_         | DALL-E-2, Kandinsky         | 5         | Free            | 4               | No   | Russian  | Yes           |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`FusionBrain.ai`_   | Kandinsky                   | 5         | Free            | 1               | No   | English  | Yes           |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`DALL-E-2`_         | DALL-E                      | 4         | \$0.020/image   | 2               | No   | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Bing`_             | DALL-E                      | 3         | Free            | 1               | Yes  | English  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+
|`Shedevrum`_        | ?                           | 3         | Free            | 1               | No   | Russian  | No            |
+--------------------+-----------------------------+-----------+-----------------+-----------------+------+----------+---------------+

As you can see, I still prefer to use Midjourney, because great community, variety of options and impressive results. But, in other hand, I most probably will try to use StableDiffusion via API in my products. And as for me, good starting point is to use Leonardo.ai.


.. _Midjourney: https://www.midjourney.com/
.. _DALL-E-2: https://openai.com/dall-e-2
.. _Leonardo.ai: https://leonardo.ai/
.. _StableDiffusion: https://stablediffusionweb.com/
.. _Dreamstudio.ai: https://beta.dreamstudio.ai/
.. _Dream.ai: http://dream.ai/
.. _Dreamlike.art: https://dreamlike.art/
.. _Lexica.art: https://lexica.art/
.. _BlueWillow: https://www.bluewillow.ai/
.. _Nightcafe: https://creator.nightcafe.studio/studio
.. _PlaygroundAI: https://playgroundai.com/create
.. _Fotor: https://www.fotor.com/images/create
.. _RuDALL-E: https://rudalle.ru/
.. _FusionBrain.ai: https://editor.fusionbrain.ai/
.. _Bing: https://www.bing.com/create
.. _Shedevrum: https://shedevrum.ai/
.. _Github: https://github.com/ai-forever/Kandinsky-2
.. _Link: https://github.com/Stability-AI/stablediffusion
