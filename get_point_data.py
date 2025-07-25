import requests  # requests, module import


url = 'https://apihub.kma.go.kr/api/typ01/url/stn_inf.php?inf=AWS&stn=&tm=202211300900&help=1&authKey=Ud0jPfajTAWdIz32o5wFcg'

with open('aws_info.txt', 'wb') as f:  # open file to be saved in binary write mode
    response = requests.get(url)  # send a GET request to file's URL
    f.write(response.content)  # write contents of response to file