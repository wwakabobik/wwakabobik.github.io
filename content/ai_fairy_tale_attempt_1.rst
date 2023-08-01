##########################
Can AI write a fairy tale?
##########################
:date: 2023-07-30 14:22
:author: wwakabobik
:tags: ai, storytelling, openai
:slug: ai_fairy_tale_attempt_1
:category: ai
:status: published
:summary: Are AI ready to tell the stories? At least teenager fairy tale?
:cover: assets/images/bg/ai.png

Can artificial intelligence write a fairy tale?

I decided to ask this question after looking at chatbots appearing on the web, focused on copywriting,
writing articles and various texts. I must say right away that I did not prepare for anything at all,
did not read cookbooks and did not use pre-trained and tuned models.

I just created a new bot and entered the basic instructions.

.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/instructions_1.png
   :alt: initial ChatGPT instructions

I use ChatGPT-4 as an engine, although in general, the davinci or GPT-3.5 model for such tasks is at least cheaper,
and with fine tuning, it may still be the best option. But I do this for two simple reasons:
I want the bot to be able to continue and offer content itself,
and I want to set the story options directly from the dialog, and not from the system settings.
The first criterion is not satisfied by davinci, and the second by GPT3.5.
The current LLMs, when given correct and precise instructions, can perform narrow tasks very well,
but for tasks with reconfiguration on the fly, they still require the influence and refinement of
the user as a motivator. And I suppose that my bot can be used both to create very simple bedtime stories for
young children, and to create horror stories for teenagers.
Therefore, it will not be superfluous to delegate the user's survey by the network itself.
So let's add some more instructions.

.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/instructions_2.png
   :alt: ChatGPT prompting instructions

Well, it's time for an early test of our model.
Let's start by creating a fairy tale about a cute robot for a six-year-old child. Here's result.

.. pull-quote::
   Perfect! Let's begin our tale.
   Once upon a time, in a world not too different from ours, there was a little robot named Beep. Beep was not like other robots. He was smaller, rounder, and had a bright red button on his belly. Beep loved to play and explore, but most of all, he loved to laugh.
   One day, Beep found a mysterious map. It was old and torn, with a big X marked at the end of a winding path. "A treasure map!" Beep thought. He decided to follow it, hoping to find the treasure.
   The journey was filled with fun and excitement. Beep had to solve riddles, navigate through a maze, and even had a tickle fight with a robot octopus! But Beep was brave and clever. He laughed and played his way through every challenge.
   Finally, Beep reached the X on the map. He dug and found a small box. Inside was a shiny key. Beep was puzzled. What could this key open?
   And that, dear listener, is a mystery for another day. Now, would you like to hear what happens next in Beep's adventure?

For sure!

.. pull-quote::
   Wonderful! Beep, with the shiny key in his hand, looked around. He noticed a small door hidden behind a bush. The key fit perfectly! Inside, Beep found a room full of laughter - it was a robot playground! Beep had found the greatest treasure of all - a place to play and laugh forever. And so, our little robot lived happily, laughing and playing in his newfound treasure. The end.

As you can see, the bot coped well with the task, and although sparingly, it was able to continue the story, but, most importantly, initiate and conduct a conversation with the child itself.

Let's pause a bit at this point, and for the sake of curiosity, switch the model to davinci and GPT3.5 for comparison.

davinci-003 doesn't ask me my age and preferences, so I must to ask it tell me story about robot.

.. pull-quote::
  Ah, a tale of robots! What a wonderful choice! Let me tell you a story of a brave robot who embarks on a quest to save the world. He is a small robot, but he is determined and brave. He sets off on his journey, facing many obstacles and challenges along the way. He meets many interesting characters, both robots and humans, and learns many valuable lessons. In the end, he succeeds in his mission and saves the world!

Go on, please...

.. pull-quote::
  Ah, a tale of robots! What a wonderful choice! Join me on a journey of a brave robot who embarks on a quest to save the world. He is small but determined and brave. He faces many obstacles and challenges along the way, meeting interesting characters and learning valuable lessons. In the end, he succeeds in his mission and saves the world!

As you can see, without leading and a lot of context, davinci can't generate content on-the fly. That's shy. But, in other hand, GPT-3.5-turbo was better than I thought. It asks my age, but mixed size and type of story. It's generally fine...

.. pull-quote::
  Ah, robots! A marvelous choice, my young friend. Now, let me transport you to a world where machines come to life. In a bustling city called Technopolis, where gears turn and circuits hum, there lived a young inventor named Max. Max was a brilliant mind with a passion for creating robots. One day, he built a special robot named Sparky, who had a heart of gold and a thirst for adventure. Together, Max and Sparky embarked on a thrilling journey through the city, encountering all sorts of robotic wonders. They met Robo the Helpful, a kind-hearted robot who loved to assist others, and ZAP-3000, a mischievous robot with a knack for pranks. Along their journey, they discovered a hidden secret that threatened the harmony of Technopolis. With their wit and courage, Max and Sparky worked together to save the city from impending disaster. And so, my young friend, the tale of Max and Sparky's robotic adventure came to an end, but their friendship and the wonders of Technopolis would live on forever.

Hm, looks also nice, but bot isn't asking and motivates child. Let's do it by myself.

.. pull-quote::
  Of course, my young friend! As Max and Sparky continued their journey, they stumbled upon a hidden laboratory deep beneath the city. Inside, they discovered a forgotten robot named Omega, who had been trapped for years. Omega possessed incredible powers and knowledge, but had lost all hope. Max, Sparky, and their newfound friends, Robo and ZAP-3000, worked together to free Omega and restore its spirit. With Omega's help, they uncovered a plot by an evil scientist to take control of Technopolis. The team embarked on a daring mission to stop the scientist and save their beloved city. Along the way, they encountered treacherous obstacles and faced their fears, but their determination and friendship prevailed. In a climactic battle, they defeated the evil scientist and restored peace to Technopolis. The city celebrated their heroes, and Max, Sparky, Robo, ZAP-3000, and Omega became legendary figures in the realm of robots. And so, my young friend, the tale of their courageous adventure came to a close, leaving behind a legacy of bravery and unity.

Well, still looks nice. But is it on-piece story, or just a separate stories at all? Let's check, just pass "go on".

.. pull-quote::
  Certainly, my young friend! As the heroes basked in their victory, a new threat emerged. A rogue group of malfunctioning robots, led by the notorious Malware, began wreaking havoc in Technopolis. Max and his loyal companions joined forces once again to save their city. They embarked on a perilous journey to find the source of the malfunction and restore order. Along the way, they encountered strange robotic creatures, ancient artifacts, and mysterious codes. With their combined skills and unwavering determination, they overcame every obstacle. In a final showdown, Max and Sparky faced off against Malware, using their ingenuity to outsmart the rogue robots. With Malware defeated, peace was restored to Technopolis, and the heroes were hailed as saviors. The tale of their epic adventure spread far and wide, inspiring future generations of inventors and adventurers. And so, my young friend, the story of Max and his robotic companions came to a close, leaving behind a legacy of bravery and innovation.

Now I got it. Bot have no one general-line story, but set of short stories for baby. So, it might be an option to generate idea or produce and force to explain stories more detailed, but every time I need to guide the bot, that's not a best option for fableteller. So, let's get back to GPT-4 and ask it to generate detailed Spooky tale of dragons and orcs for 10-year boy.

.. pull-quote::
  Perfect! Now, gather your courage, dear friend, as we dive into our spooky tale.

  Once upon a time, in a land filled with towering mountains and deep, dark forests, there lived a ferocious dragon named Smolder and a cunning orc named Gritjaw. They were the most feared creatures in all the land. Smolder, with his fiery breath, could melt the hardest stone, and Gritjaw, with his immense strength, could fell the tallest tree.

  One eerie night, a chilling wind swept across the land, carrying with it a strange, haunting melody. The creatures of the forest huddled in fear, for they knew that this was the song of the Ghostly King, a spirit who only appeared during the spookiest of times.

  Smolder and Gritjaw, despite their fear, decided to confront the Ghostly King. They journeyed through the dark forest, their path lit only by the dragon's fiery breath. They finally reached the Ghostly King's castle, a towering structure made of mist and shadows.

  As they stepped inside, they were met with a chilling sight. The Ghostly King, a spectral figure draped in a cloak of shadows, sat on a throne of bones. His eyes glowed with an eerie light, and his voice echoed through the castle as he said, "Who dares to enter my domain?"

  With a roar, Smolder breathed fire into the air, illuminating the castle with a warm glow. Gritjaw stepped forward, his eyes gleaming with determination. "We are here to challenge you, Ghostly King!" he declared.

  The Ghostly King laughed, a sound that sent shivers down their spines. "Very well," he said. "But be warned, those who challenge me must face their deepest fears."

  And so, our brave heroes found themselves facing their fears. Smolder, who feared water more than anything, had to cross a river of chilling depths. Gritjaw, who feared heights, had to climb the tallest tower. But they persevered, helping each other overcome their fears.

  Finally, they stood before the Ghostly King again. "We have faced our fears," Gritjaw said. "Now, it's your turn to leave this land in peace."

  With a nod, the Ghostly King vanished, leaving behind a castle filled with light and warmth. From that day forward, Smolder and Gritjaw were not just the most feared, but also the most respected creatures in the land. They had faced their fears and stood up to the Ghostly King, proving that even the scariest of beings could be defeated with courage and friendship.

  The creatures of the forest no longer feared the eerie nights, for they knew Smolder and Gritjaw were there to protect them. The dragon and the orc, once rivals, had become the best of friends, their bond forged in the heart of the spooky castle.

  And so, they lived out their days, sharing tales of their adventure and inspiring others with their bravery. The land was peaceful, and the eerie melody of the Ghostly King was heard no more. And that, dear friend, is the end of our spooky tale. 

What a story. Different character, general canvas and details. I liked it. But still not perfect. I want to have a possibility to generate a multi-chaptered book also, so, why not to enhance my settings. Let's add more tunes!

.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/instructions_3.png
   :alt: chapter and detalization ChatGPT instructions

Ok, it's time to final, chilling story about 14-years old boy lost in the woods, good, but thrilling kitsune, who becomes friend of the boy during story, and the walking dead.

.. pull-quote::
  Very well, a medium-sized tale it shall be. So, sit back, relax, and let me take you on a journey into the heart of the haunted forest. Our tale begins with a young boy named Eli, who, on a dare, ventures into the woods one fateful night...

  Chapter 1: The Dare

  Chapter 2: The Enchanted Night

  Chapter 3: The Whispering Shadows

  Each chapter will be a thrilling part of Eli's adventure, filled with friendship, mystery, and the unknown. Are you ready to begin?

Finally, there is a plan, leading storyteller, and long story at one piece.

.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/chapter_1.png
   :alt: Chapter 1

.. pull-quote::
  Chapter 1: The Dare

  In the quaint town of Eldridge, nestled between rolling hills and a sparkling river, lived a young boy named Eli. He was a sprightly lad of 14, with a mop of unruly brown curls and a constellation of freckles scattered across his nose. Eli was known for his adventurous spirit and his insatiable curiosity. He was always the first to climb the tallest tree, the first to dive into the deepest part of the river, and the first to accept any dare.

  One day, his friends, a motley crew of spirited youngsters, dared him to venture into the haunted forest that lay on the outskirts of Eldridge. This forest was the stuff of legends, with tales of eerie sounds, ghostly apparitions, and strange creatures that came alive at night. Eli, with a glint in his eye and a heart full of courage, accepted the dare.

  As the sun began to set, painting the sky with hues of orange and purple, Eli set off towards the forest. His heart pounded in his chest with a mix of fear and excitement. He could feel the thrill of the unknown coursing through his veins as he stepped into the forest.

  The forest was unlike anything Eli had ever seen. The trees were ancient, their gnarled branches reaching out like skeletal hands. The leaves rustled in the wind, whispering secrets of the forest. The moonlight filtered through the dense canopy, casting an eerie glow on the forest floor.

  As Eli ventured deeper, he came across a creature he had only heard of in stories - a kitsune. She was a beautiful fox with nine fluffy tails and fur the color of autumn leaves. Her eyes were a mesmerizing golden color, filled with wisdom beyond her years. She introduced herself as Yumi.

  Yumi, seeing the courage in Eli, decided to guide him through the forest. They journeyed through the dense undergrowth, past glowing mushrooms and strange plants. They heard the hoots of owls and the rustling of unseen creatures. The forest was alive with sounds and sights that Eli had never experienced before.

  As they ventured deeper, they came across a clearing bathed in moonlight. In the center stood an ancient tree, its bark silver in the moonlight, its branches heavy with age. Yumi explained that this was the Heart Tree, the oldest tree in the forest, and a meeting place for magical creatures.

  Suddenly, they heard a rustling sound. Out of the shadows emerged a group of forest spirits, their forms shimmering in the moonlight. They were wary of Eli at first, but Yumi vouched for him. The spirits shared tales of the forest, of the creatures that dwelled within, and of the walking dead that roamed the woods at night.

  Eli listened, his heart pounding with a mix of fear and excitement. He had always loved ghost stories, but he had never thought he would be part of one. As the spirits faded away with the dawn, Eli knew that his adventure was just beginning. He was in the heart of the enchanted forest, with a magical kitsune as his guide, and a night full of stories that he would remember for the rest of his life.

.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/chapter_2.png
   :alt: Chapter 2

.. pull-quote::
  Chapter 2: The Enchanted Night

  As the spirits disappeared, Eli and Yumi decided to rest. They found a cozy nook under the Heart Tree, its massive roots providing a comfortable shelter. Yumi conjured a small fire, its warm glow casting dancing shadows on their faces. They shared stories, Yumi telling Eli about the ancient legends of the forest, and Eli sharing tales of his adventures in Eldridge.

  As they talked, the forest came alive with nocturnal creatures. Fireflies danced around them, their soft glow illuminating the darkness. An owl hooted in the distance, its call echoing through the silent forest. The rustling of leaves and the soft sounds of the forest lulled Eli into a peaceful sleep.

  When he woke up, the sun was just beginning to peek over the horizon. The forest was bathed in a soft, golden light. Yumi was already awake, her golden eyes reflecting the morning light. They shared a simple breakfast of berries and nuts, and then set off to explore the forest.

  As they journeyed deeper into the forest, they came across a bubbling brook. The water was crystal clear, reflecting the vibrant green of the trees and the bright blue of the sky. They stopped to rest, the gentle babbling of the brook providing a soothing soundtrack.

  Suddenly, Yumi's ears perked up. She heard a rustling in the bushes. Eli watched as she transformed into a beautiful woman with flowing red hair. She stepped towards the bushes and out came a small, frightened rabbit. Yumi spoke in a soft, soothing voice, calming the rabbit down.

  Eli was amazed. He had heard stories of kitsunes being able to transform into humans, but seeing it in person was a different experience altogether. He realized that the forest was full of magic and wonder, and he was just beginning to scratch the surface. As they continued their journey, Eli knew that he was in for an adventure of a lifetime.

  As the day wore on, Eli found himself drawn to Yumi. Her strength, her wisdom, and her kindness made him see her in a new light. He admired her courage and her connection with the forest. He found himself wanting to know more about her, to understand her world.

  Yumi, on the other hand, was intrigued by Eli. His bravery, his curiosity, and his respect for the forest made her see him as more than just a human boy. She found herself drawn to his spirit, his zest for life.

  As they journeyed together, their bond deepened. They shared stories, laughed together, and faced challenges together. They found comfort in each other's company, their friendship blossoming into something more. By the time the sun set, painting the sky with hues of pink and orange, they knew that their lives were forever intertwined. They were no longer just a boy and a kitsune, they were partners, ready to face whatever the forest had in store for them.

  Under the starlit sky, Eli took Yumi's hand. His heart pounded in his chest as he looked into her golden eyes. He confessed his feelings for her, his words echoing in the silent forest. Yumi, taken aback, looked at him with a soft smile. She confessed that she too had feelings for him. They shared a tender moment under the Heart Tree, their hearts beating as one. The forest seemed to hold its breath as they leaned in, sharing their first kiss under the twinkling stars. It was a moment of pure magic, a testament to their love.


.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/chapter_3.png
   :alt: Chapter 3

.. pull-quote::
  Chapter 3: The Whispering Shadows

  After their tender moment under the Heart Tree, Eli and Yumi continued their journey. The forest grew darker, the air colder. They came across an old, abandoned village. The houses were in ruins, the once bustling market now eerily silent.

  Suddenly, they heard a low moan. Turning around, they saw a figure shuffling towards them. Its eyes were vacant, its skin pale. It was a walking dead. Eli felt a chill run down his spine. He had heard stories of the walking dead, but he had never seen one.

  Yumi, sensing his fear, squeezed his hand. She whispered to him, "We must be brave, Eli. The forest needs us." With a determined look in her eyes, she drew her mystery glowing sword, ready to face the walking dead. Eli, inspired by her courage, lifted a large branch from under his feet. The branch crackled terribly and began to writhe in his hands like a snake, but quickly took on the shape of an elegant blade. Wow! Magic blade from a stick! Eli looked at Yumi, who responded with a wink and a smile. Together, they stood their ground, ready to protect the forest they loved.

  As they stood their ground, the moonlight casting long shadows around them, Eli could feel his heart pounding in his chest. The walking dead moved closer, its movements slow and jerky. Its vacant eyes stared at them, sending a chill down Eli's spine. He tightened his grip on his sword, his knuckles turning white.

  Yumi, on the other hand, stood calm and composed. Her golden eyes glowed in the dark, her red hair flowing in the wind. She looked at the walking dead, not with fear, but with determination. She was ready to protect the forest, to protect Eli.

  The walking dead lunged at them, its arms outstretched. Yumi moved swiftly, her sword slicing through the air. Eli followed her lead, his own sword meeting the walking dead's attack. The fight was intense, the air filled with the sound of clashing swords and the walking dead's eerie moans.

  Despite the fear and the danger, Eli felt a strange sense of exhilaration. He was fighting alongside Yumi, protecting the forest they loved. He realized that this was his destiny, his purpose. He was meant to be here, with Yumi, fighting for the forest.

  As the night wore on, they fought bravely, their swords clashing against the walking dead. Despite the odds, they stood their ground, their determination unwavering. With each passing moment, their bond grew stronger, their love deeper. They fought as one, their movements in perfect sync.

  Finally, as the first rays of dawn pierced the dark sky, they managed to defeat the walking dead. Exhausted but victorious, they stood amidst the ruins of the village, their hearts filled with a sense of accomplishment. They had faced their fears, fought their battles, and protected the forest. Their love story had become a legend, a tale of courage, determination, and love. And as they looked into each other's eyes, they knew that they were ready to face whatever the future had in store for them. Together.


.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/epilogue.png
   :alt: Epilogue

.. pull-quote::
  Epilogue: The Tragic Separation

  As the victory celebrations faded, the forest spirits gathered around Eli and Yumi. Their faces were somber, their eyes filled with sorrow. They revealed the truth about Yumi - she was a spirit, a ghost of a young girl who had died protecting the forest. Her spirit had taken the form of a kitsune, continuing her duty even in death.

  Eli felt his heart shatter. He had fallen in love with a ghost, a spirit bound to the forest. Their worlds were too different, their existences too incompatible. He held Yumi close, their tears mingling. He whispered a promise to her, a promise to remember her always, to cherish their memories forever.

  Yumi watched Eli leave, her heart aching with a pain she had never known. She had fallen in love with a mortal, a human who lived in a world she could never be a part of. She returned to her duties, her spirit heavy with sorrow. Their love story, though beautiful, was a tale of love and loss, a reminder of the tragic reality of their existence.

What do you think? Are you agree that AI can create a dramatic and chilling fable?