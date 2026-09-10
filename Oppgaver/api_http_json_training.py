#jsonplaceholder.typicode.com som är påhittad testdata, enkel struktur
#api.open-meteo.com som är riktig väderdata, nästlad struktur
#httpbin.org som ekar tillbaka det du skickar, perfekt för POST och felkoder

#GET = Ge mig data
#POST = ta emot data

#felkoder
    #200 OK
    #400 frågar fel
    #401 eller 403, du saknar behörighet
    #404, adressen finns inte
    #500, servern kraschade

import email
from tokenize import Comment

import requests

answer = requests.get("https://jsonplaceholder.typicode.com/users")
print(answer.status_code)

if answer.status_code == 200:
    users = answer.json()
    print(type(users))
else:
    print("Something went wrong: ",answer.status_code )

groupcounter = 0

#for user in users:
#    name:str = user["name"]
#    epost:str = user["email"]
#    city:str = user.get("address",{}).get("city")
#    company_name:str = user.get("company", {}).get("name")
#
#    if "Group" in company_name:
#        groupcounter += 1

#print(groupcounter)



#user3_post = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId":3})
#posts = user3_post.json()
#print(posts)
#print(user3_post.url)
#print(len(posts))

postId = requests.get("https://jsonplaceholder.typicode.com/comments", params={"postId":5})

comments = postId.json()

for comment in comments:
    print(comment["email"])
    print(comment["body"])
    print()
    

print(len(comments))


 


        


    




# Debug: see what you actually got