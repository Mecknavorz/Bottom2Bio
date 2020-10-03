# Bottom2Bio$hel
Discord bot that turns bottom key-smashing into amino acid sequences

##Bot Commands
All bot commands start with $, here are the currently implemented commands:
-$help: displays a list of the current commands
-$toggle: switches between 3-letter and 1-letter abreviations when outputting the amino acid sequence
-$auto: toggles between automatic bottom detection and manual mode, for the difference see below

##How does it work?
While on automode, Bottom2Bio works by first checking the number of spelling errors in a message, however, to avoid just accidentally detecting random typos it runs through the spell checking function twice, leaving words that the dictionary really just doesn't recongize at all, eg ideally jibberish. From there it then checks to see if that jibberish is over 25% of the string we add a 🧬 emoji as a reaction to the message because we're pretty sure that the message has or mostly is bottom spam. If one or more other uses react with 🧬 emojis to the message as well, then it is sent into our **advanced algorith** and turn it into a string of amino acids!

If automode is off then a user will have to add the 🧬 emoji to a message manually, at which point the bot will calculate the amino acid string.

##Other things
I'm currently not planning on hosting a version of this bot myself I don't particularly feel like I have the resources to do so atm, however, you're perfectly welcome to set up and run your own copy of the bot! Even further, if you wish to add bottom detection or just the amino acid maker to your own code, feel free too, just be sure to give me credit or a link to the original code! 💕

I'm not currenty planning on working on this code more I personally feel satisfied with where it is, but if I see enough of an interest in it I'll consider updating it and adding features or fixing bugs that might be there!
