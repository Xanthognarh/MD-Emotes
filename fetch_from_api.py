import requests, os, re, json, sys, argparse
from PIL import Image

argparser = argparse.ArgumentParser(description='Download streamer emotes from Twitch.')

class TwApi:
    session = requests.Session()
    def __init__(self):
        resp = self.session.get("https://www.twitch.tv/")
        client_id = re.search('clientId="(.*?)",', resp.content.decode()).group(1)
        self.client_id = client_id
        # return client_id

    def gqlPlaybackAccessToken(self, channel: str) -> str:
        'input channel name, return channel_id'
        resp = self.session.post(
            url="https://gql.twitch.tv/gql",
            json={
                "operationName": "PlaybackAccessToken_Template",
                "query": 'query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!, $platform: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: $platform, playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isLive) {    value    signature   authorization { isForbidden forbiddenReasonCode }   __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: $platform, playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isVod) {    value    signature   __typename  }}',
                "variables": {
                    "isLive": True,
                    "login": channel,
                    "isVod": False,
                    "vodID": "",
                    "playerType": "site",
                    "platform": "web",
                },
            },
            headers={"Client-Id": self.client_id},
        )
        r_dict: dict = resp.json()
        v = json.loads(r_dict['data']['streamPlaybackAccessToken']['value'])
        r = v['channel_id']
        # print(r)
        return r.__str__()


    def gqlEmotePicker(self, channelOwnerID: str) -> dict:
        'return a dict like `{\'pewdiepieLegendBroFist\': \'emotesv2_b6e72807df1b4c78a0b70c8bb534b2fc\'}`'
        resp = self.session.post(
            url="https://gql.twitch.tv/gql",
            json=[
                {
                    "operationName": "EmotePicker_EmotePicker_UserSubscriptionProducts",
                    "variables": {"channelOwnerID": channelOwnerID},
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "71b5f829a4576d53b714c01d3176f192cbd0b14973eb1c3d0ee23d5d1b78fd7e",
                        }
                    },
                }
            ],
            headers={"Client-Id": self.client_id},
        )
        resp_dict = resp.json()
        r_dict = dict()
        if resp_dict[0]['data']['channel']['localEmoteSets'] != None:
            for emo_set in resp_dict[0]['data']['channel']['localEmoteSets']:
                for emo in emo_set['emotes']:
                    r_dict["0"+emo['token']] = emo['id']
        for index,emo_set in enumerate(resp_dict[0]['data']['user']['subscriptionProducts']):
            for emo in emo_set['emotes']:
                # if emo['assetType'] == 'ANIMATED':
                #     ext = '.gif'
                # elif emo['assetType'] == 'STATIC':
                #     ext = '.png'
                r_dict[str(index+1)+emo['token']] = emo['id']

        url="https://7tv.io/v3/users/twitch/"+channelOwnerID
        resp = requests.get(url)
        resp_dict = resp.json()
        for emo_set in resp_dict["emote_set"]["emotes"]:
            r_dict["7"+emo_set["name"]]=emo_set["id"]

        return r_dict
    
    def downloadEmote(self, filename: str, url: str):
        resp = self.session.get(url)
        if "content-type" not in resp.headers.keys():
            print("Fehler: Kein Content-Type für",filename,url)
            return
        ext = resp.headers['Content-Type'].split('/')[-1]
        # if ('.png' not in filename) and ('.gif' not in filename):
        #     from PIL import Image
        #     from io import BytesIO
        #     img = Image.open(BytesIO(resp.content))
        #     ext = img.format.lower()
        if ":" in filename:
            print(filename,"wurde nicht gespeichert, da inkompatibler Name")
            return

        fname = filename + f'.{ext}'
        with open(fname, mode='wb') as f:
            f.write(resp.content)
        print(f'download as {fname}')
        if ext=="webp":
            #Convert to gif
            with Image.open(fname) as im:
                im.info.pop('background', None)
                im.save(filename+'.gif', 'gif', save_all=True,lossless=True, quality=100, method=6, optimize=True,disposal=2)
            try:
                os.remove(fname)
            except PermissionError:
                print(fname,"konnte nicht gelöscht werden, da geöffnet")
            except FileNotFoundError:
                print(fname,"konnte nicht gelöscht werden, da nicht gefunden")
            print(f'convertet to {filename}.gif')

    def downloadEmotes(self, emote_dict: dict, max_workers: int = 20, dir: str = '', channel: str = ""):
        foldernames=[dir,os.path.join(dir, "T0_"+channel),os.path.join(dir, "T1_"+channel),os.path.join(dir, "T2_"+channel),os.path.join(dir, "T3_"+channel),os.path.join(dir, "7TV_"+channel)]
        for folder in foldernames:
            if not os.path.exists(folder):
                os.mkdir(folder)

        import concurrent.futures
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        thr_set = set()
        for filename, url in emote_dict.items():
            if filename[0]=="7":
                #7TV
                filename=os.path.join("7TV_"+channel,filename[1:])
                dlurl=f"https://cdn.7tv.app/emote/{url}/4x.webp"
            elif filename[0]=="0":
                #T0
                filename=os.path.join("T0_"+channel,filename[1:])
                dlurl=f'https://static-cdn.jtvnw.net/emoticons/v2/{url}/default/light/3.0'
            elif filename[0]=="1":
                #T1
                filename=os.path.join("T1_"+channel,filename[1:])
                dlurl=f'https://static-cdn.jtvnw.net/emoticons/v2/{url}/default/light/3.0'
            elif filename[0]=="2":
                #T2
                filename=os.path.join("T2_"+channel,filename[1:])
                dlurl=f'https://static-cdn.jtvnw.net/emoticons/v2/{url}/default/light/3.0'
            elif filename[0]=="3":
                #T3
                filename=os.path.join("T3_"+channel,filename[1:])
                dlurl=f'https://static-cdn.jtvnw.net/emoticons/v2/{url}/default/light/3.0'
            else:
                raise Exception("Unknown filename "+filename)

            thr = executor.submit(
                self.downloadEmote, 
                filename=os.path.join(dir, filename), 
                url=dlurl)
            thr_set.add(thr)
        executor.shutdown()

        for thr in thr_set:
            thr: concurrent.futures.Future
            e = thr.exception()
            if e != None:
                print(thr.result())

if __name__ == '__main__':
    argparser.add_argument('-c', '--channel', dest='channel', help='Channel name.', required=True)
    argparser.add_argument('-d', '--dir', dest='dir', help='Download files into this directory. (default: \'./emotes\', will create if not exist.)', default='./emotes')
    argparser.add_argument('-p', '--proxy', dest='proxy', help='Use specified HTTP proxy server. (e.g. \'http://localhost:10809\', or you can set https_proxy or all_proxy in the terminal)', default='')
    args = argparser.parse_args()

    if args.proxy != '':
        os.environ["all_proxy"] = args.proxy

    api = TwApi()
    channel_id = api.gqlPlaybackAccessToken(args.channel)
    emote_dict = api.gqlEmotePicker(channel_id)
    api.downloadEmotes(emote_dict=emote_dict, dir=args.dir, channel=args.channel)
    print(emote_dict)
