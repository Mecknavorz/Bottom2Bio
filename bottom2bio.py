#bottom 2 bio bot
#made by Tzarta (@Mecknavorz)

import discord #this is the library that allows us to (easily) do stuff with discord
from spellchecker import SpellChecker #spellchecker used to try and figureout keysmashing from normal text

#some global variables
client = discord.Client() #this is the instance of the client, eg how we conntect to discord
spell = SpellChecker() #the spell checker instance
fullprot = True #determines wether or not we print the 3 letter string or use the one letter abrevations
automode = True #determines wether or not the bot will automaitcally add the react to predicted bottom spawm
done = [] #list of messages we've already processed, this is to prevent spam from multiple reactions to the same message


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)) #print to the console to let us know that we've actually logged on

@client.event
async def on_message(message): #if a message is sent, do things
    #if the message is from the bot, ignore the message
    if message.author==client.user: 
        return

    #used for recongnizing commands
    #if the message isn't from the bot, do stuff
    if message.content.startswith('$'):
        if message.content == '$help':
            await message.channel.send('**__Commands:__** (all commands start with $)\n```$help\t  -\tdisplays current message\n$toggle\t-\ttoggles long mode or short mode\n$auto\t  -\ttoggles wether or not the bot will automatically predict bottom spam or not```')
        if message.content == '$toggle':
            global fullprot
            fullprot = not fullprot
            if fullprot:
                await message.channel.send('**Mode Set:** 3 letter abbreviations')
            else:
                await message.channel.send('**Mode Set:** Single letter abbreviations ')
        if message.content == '$auto':
            global automode
            automode = not automode
            if automode:
                await message.channel.send('Bio2Bottom will now automatically flag predicted bottom text')
            else:
                await message.channel.send('🧬 must be added manually to a message, the bot will no longer add it to predicted messages.')

    #if we think the text might be bottom spam, add the dna emoji to it
    if automode: #for toggling the bot's bottom detector feature
        if (calcBottom(message)):
            await message.add_reaction('🧬') #the emoji shows up as a box but it's dna

@client.event
async def on_raw_reaction_add(payload): #the paramaters here react and user are the reaction added, and the user who did it
    #if the bot is the one who added the reaction ignore
    if payload.user_id==client.user.id:
        return
    
    if payload.emoji.name=='🧬': # dna emoji again
        global done #make sure we have the global done list
        if not(payload.message_id in done): #make sure e haven't processed this message before
            channel = client.get_channel(payload.channel_id) #get the channel we need to print to by using the curchan variable
            await channel.send(fixString(await channel.fetch_message(payload.message_id))) #print the message
            done.append(payload.message_id) #add the message id to the done list to prevent spam
    

#this function is used for cleaning the input message, it isn't a client event an as such doesn't require @client.event or aysync
def fixString(message):
    #s = message.content
    cleanstr = ''.join([i for i in message.content.upper() if i.isalpha()])
    #remove letters that don't represent amino acids
    #these three can each be two seprate acids depending, but that's beooming oboslete if I undersand it since it's easier to differentiate the two
    cleanstr = cleanstr.replace('B', '')
    cleanstr = cleanstr.replace('J', '')
    cleanstr = cleanstr.replace('Z', '')
    #while these can sometimes code for Pyrrolysine and Selenocysteine it's normall stop codons and I don't wanna deal with that
    cleanstr = cleanstr.replace('O', '')
    cleanstr = cleanstr.replace('U', '')
    #turn the sequence into the three letter version if that fullprot is on
    if fullprot:
        cleanstr = fulSeq(cleanstr)
    return ('**Amino Acid Sequence:** ```' + cleanstr + '```')

#this function turns a minimal sequence (eg single letter representation and turns it into a full sequence
def fulSeq(minimal):
    tbr = '' #string to be returned at the end of the function
    #itterate through the amino acid sequence, the amino acids are in alphabetical order not the letters before u whine at me\
    for i in range(0, len(minimal)):
        if minimal[i] == 'A': #for Alanine
            tbr += ('Ala')
        if minimal[i] == 'R': #for Arginine
            tbr += ('Arg')
        if minimal[i] == 'N': #for Asparagine
            tbr += ('Asn')
        if minimal[i] == 'D': #for Aspartic acid
            tbr += ('Asp')
        if minimal[i] == 'C': #for Cysteine
            tbr += ('Cys')
        if minimal[i] == 'Q': #for for Glutamine
            tbr += ('Gln')
        if minimal[i] == 'E': #for Glutamic acid
            tbr += ('Glue')
        if minimal[i] == 'G': #for Glycine
            tbr += ('Gly')
        if minimal[i] == 'H': #for Histine
            tbr += ('His')
        if minimal[i] == 'I': #for Isoleucine
            tbr += ('Ile')
        if minimal[i] == 'L': #for Leucine
            tbr += ('Leu')
        if minimal[i] == 'K': #for Lysine
            tbr += ('Lys')
        if minimal[i] == 'M': #for Methionine
            tbr += ('Met')
        if minimal[i] == 'F': #for Phenylalannine
            tbr += ('Phe')
        if minimal[i] == 'P': #for Proline
            tbr += ('Pro')
        if minimal[i] == 'S': #for Serine
            tbr += ('Ser')
        if minimal[i] == 'T': #for threonine
            tbr += ('Thr')
        if minimal[i] == 'W': #for (wumbo) Tryptophan
            tbr += ('Trp')
        if minimal[i] == 'Y': #for Tyrosine
            tbr += ('Tyr')
        if minimal[i] == 'V': #for Valine
            tbr += ('Val')
        if minimal[i] == 'X': #for unknow amino acids
            tbr += ('Xaa')
        #add a hypen between amino acids if it's not the end of the seqeunce
        if i < (len(minimal)-1):
            tbr += ('-') 
    return tbr #return the string

#function that should return true or false based on wether or not it thinks a message is bottom spam
def calcBottom(message):
    #this part of the code calculates what ratio of a message's words are typos
    #this way it should probably ignore names and other non-real things that are just being used
    tocheck = [] #empty array we will fill with the word only parts of the input string
    for i in message.content.split():
        tocheck.append(''.join([j for j in i if j.isalpha()])) #remove non letter characters from each wordand add it to the tocheck list
    if ('' in tocheck):
        tocheck.remove('') #remove blank strings because those coutn as being missepelled
    mispelled = spell.unknown(tocheck) #used to actually find mispelled words
    i = 0 #in to keep track of mispelled words
    for word in mispelled: #this is how we actually count the number of misspellings
        i+=1
    
    #for debugging
    #print('Number of words: %s' %(len(string.split())))
    #print('num mispelled: %s' %(i))
    #print('ratio: %s' %(i/len(string.split())))
    
    #if the number of typos is greater than the desired percentage
    #decrease the percentage to make the system more sensitive
    if (i/len(message.content.split())) >= .25:
        misspelled = spell.unknown(message.content.split())
        #print('misspelled: ')
        #print(misspelled)
        typocheck = []
        for word in misspelled:
            typocheck.append(spell.correction(word))
        misspelled = spell.unknown(typocheck)
        #if there are one or more instances of keysmashing deteced
        if(len(misspelled) >= 1):
            return True
        else:
            return False
    else:
        return False

'''
-----------------------
PUT YOUR BOT TOKEN HERE
-----------------------
'''
client.run('PUT YOUR BOT KEY HERE') #use the client we made earlier using this bot
