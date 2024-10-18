# ChadGPT
### What am I
I let friends organize and compete in online capture the flag challenges through a discord channel. :triangular_flag_on_post: 

I also have a feature that prevents your friends from polluting specific discord channels with bot commands while there's a channel meant for it. :rage:

### Commands
`!set_ctf_channel <channel>`  
`!set_ctf_mention <mention>`   
`!new <challenge_name> <challenge_url> <challenge_value>` (private command only)   
`!submit <challenge_name> <flag>` (private command only)  
`!leaderboard <leaderboard_length>`

`!restrict_command <restricted_command> <restricted_channel_1> ...`

### Usage notes
- The bot must have a fresh account on the ctf plateform.
- Note that the bot can't verify picoCTF since some/all flags have a random bit.
- Note that the bot has been tested on https://ctf.hackin.ca/. Any other plateform might produce buggy behaviour. Help would be appreciated here for testing.

### Problem encountered
The bot was meant to be run on a Raspberry Pi which has the ARM processor architecture. Since no undetected chrome driver exist for ARM architecture, I'm archiving the project.
