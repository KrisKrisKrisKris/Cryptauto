#region Imports and libraries
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import os 
import requests

#endregion

#region Variables

ScreenTextLines = None

#endregion

#region Utility Functions

# trims empty lines off a string
#inputs: original string, amount of lines you want returned (all if "None")
def trim_empty_lines(input_string, amount_of_Lines_to_return):
    lines = [line for line in input_string.splitlines() if line.strip()]
    if(amount_of_Lines_to_return != None):
        lines = lines[:amount_of_Lines_to_return]
    return '\n'.join(lines)

#endregion 

#what this prototype is doing so far: 
#1. Pull data from the webscraper's (BeautifulSoup) website
#2. Feed that to chatGPT with the instructions: ~"Summerize the website for the user" 
#3. Print the summary (with limit of size)(don't make this too big for no reason, we have a budget of $5 of tokens)

#Many improvements can be made, we'll deal with that later. 

#region WebScraper foundation

# Make a request to the website
url = 'https://www.crummy.com/software/BeautifulSoup/'
response = requests.get(url)

#if successful 
if response.status_code == 200:

    #parse gathered data with soup html parser
    #TODO: look to see if this can be done without the 'requests' library
    soup = BeautifulSoup(response.text, 'html.parser')
    ScreenText = soup.get_text()

    #Trim and get the first 7 lines scrapped
    ScreenTextLines = trim_empty_lines(ScreenText, 7)

    #trim and print
    # print (ScreenTextLines)

else:
    print("Failed to grap webpage with status code of: ", response.status_code)

#endregion

#region ChatGPT foundation

# Load environment variables from .env
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Set up ChatGPT prompt and GOOOOO
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=
        [
        {"role": "system", "content": "Summerize webpage information the user provides."},
        {"role": "user", "content": ScreenTextLines}
        ],
    stream = True,
    max_tokens = 30,
)

#print response to screen
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

#endregion
