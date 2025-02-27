import random
import copy

clrs=["R","G","B"]
# random.shuffle(clrs)

class card:
    def __init__(self,t,c,v):
        self.type=t
        self.color=c
        self.value=v
    def display(self):
        print(self.type,self.color,self.value)
    def realvalue(self):
        if self.type=='-':
            return -1*self.value
        return self.value

class player:
    def __init__(self,c):
        self.hand=[]
        self.color=c
        self.pos=0
    def possmoves(self,start,board):
        res=[]
        for card in self.hand:
            if card.type!='^':
                if card.color!='ANY':
                    res.append([card.color,card.realvalue(),card])
                else:
                    for c in clrs:
                        res.append([c,card.realvalue(),card])
            elif start!=[]:
                for c in start:
                    res.append([c,card.value,card])
            else:
                i=0
                while board[i]==[]:
                    i+=1
                res.append([board[i][-1],card.value,card])
        return res

class tutelgame:
    def __init__(self,colors):
        self.players=[player(c) for c in colors]

        self.start=copy.deepcopy(colors)

        self.board=[[] for _ in range(10)]

        self.pile=[card('+',c,2) for c in colors]*1+[card('+',c,1) for c in colors]*5+[card('-',c,1) for c in colors]*2
        self.pile+=[card('^','ANY',2)]*2
        self.pile+=[card('^','ANY',1)]*3
        self.pile+=[card('+','ANY',1)]*5
        self.pile+=[card('-','ANY',1)]*2
        random.shuffle(self.pile)

        self.discard=[]
        for _ in range(5):
            for p in self.players:
                    p.hand.append(self.pile[-1])
                    self.pile=self.pile[:-1]

        self.turn=0

    def print(self):
        top=len(max(self.board, key=len))-1
        while top>=0:
            for p in range(10):
                pos=self.board[p]
                if len(pos)>top:
                    print(pos[top],end='')
                else:
                    if top>0:
                        print(' ',end='')
                    else:
                        print('_',end='')
            top-=1
            print()
        print()
        if self.start!=[]:
            print(self.start)
            print()

    def move(self,c,d):
        if c in self.start:
            if d>0:
                self.players[[p.color for p in self.players].index(c)].pos=d
                self.board[d].append(c)
                self.start.remove(c)
        else:   
            i=0
            while c not in self.board[i]:
                i+=1
                if i>9:
                    return self
            im=i+d
            if im<0:
                im=0
            if im>9:
                im=9
            if im!=i:
                posc=self.board[i]
                for t in range(posc.index(c),len(posc)):
                    self.players[[p.color for p in self.players].index(posc[t])].pos=im
                    self.board[im].append(posc[t])
                self.board[i]=self.board[i][:posc.index(c)]

    def pickcard(self):
        if self.pile==[]:
            self.pile=self.discard
            random.shuffle(self.pile)
            self.discard=[]
        self.players[self.turn].hand.append(self.pile[-1])
        self.pile=self.pile[:-1]

    def playcard(self,opt):
        c,d,card=tuple(opt)
        # print(c,d)
        self.move(c,d)
        for i in self.players[self.turn].hand:
            if i.type==card.type and i.color==card.color and i.value==card.value:
                self.players[self.turn].hand.remove(i)
                break
        self.discard.append(card)
        self.pickcard()
        self.turn=(self.turn+1)%len(clrs)
    
def randagent(tg):
    tg.playcard(random.choice(tg.players[tg.turn].possmoves(tg.start,tg.board)))

def heuragent(tg):
        plr=tg.players[tg.turn]
        poss=plr.possmoves(tg.start,tg.board)
        scenarios=[]
        for i in range(len(poss)):
            g=copy.deepcopy(tg)
            g.playcard(poss[i])
            scenarios.append(g)
        heurarr=[2*sc.players[(sc.turn-1)%len(clrs)].pos-sum([posi.pos for posi in sc.players]) for sc in scenarios]
        # [print(heurarr[i],poss[i]) for i in range(len(poss))]
        thebest=[[poss[i],heurarr[i]] for i in range(len(scenarios)) if heurarr[i]==max(heurarr)]
        # print(thebest)
        if len(thebest)==1:
            tg.playcard(thebest[0][0])
            return
        # [print(o[0][2].value,min(thebest, key=lambda t: t[0][2].value)[0][2].value) for o in thebest]
        thebest=[o[0] for o in thebest if o[0][2].realvalue()==min(thebest, key=lambda t: t[0][2].realvalue())[0][2].realvalue()]
        # print(thebest)
        if len(thebest)==1:
            tg.playcard(thebest[0])
            return
        if [o for o in thebest if o[2].type!='ANY']:
            thebest=[o for o in thebest if o[2].type!='ANY']
        if [o for o in thebest if o[0]!=plr.color]!=[]:
            thebest=[o for o in thebest if o[0]!=plr.color]
            for pos in tg.board[::-1]:
                for p in pos:
                    if p in [o[0] for o in thebest]:
                        tg.playcard([o for o in thebest if o[0]==p][0])
                        return
            # print(thebest,tg.start[0])
            tg.playcard([o for o in thebest if o[0] in tg.start][0])
            return
        tg.playcard(thebest[0])

score=0
for i in range(10000):
    tg=tutelgame(clrs)
    while tg.board[-1]==[]:
        # sss=input()
        # if sss=='':
            if tg.turn==0:
                # [h.display() for h in tg.players[0].hand]
                heuragent(tg)
            else:
                randagent(tg)
            # tg.print()
    if tg.board[-1][0]=='R':
        score+=1
    print(i+1,round(100*score/(i+1),2))
# print(f"player {tg.board[-1][0]} wins")